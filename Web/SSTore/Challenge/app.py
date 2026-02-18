import os
import sqlite3
import time
import logging
from flask import Flask, render_template, render_template_string, request, redirect, url_for, session, g, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.logger.setLevel(logging.INFO)
DATABASE = 'store.db'

# Rate limiting for SSTI endpoint
_visits = {}
RATE_WINDOW = 60  # seconds
RATE_MAX = 30     # max requests per window per IP

def rate_check(ip):
    """Simple rate limiting"""
    now = time.time()
    q = _visits.get(ip, [])
    q = [t for t in q if t > now - RATE_WINDOW]
    q.append(now)
    _visits[ip] = q
    if len(q) > RATE_MAX:
        return False, len(q)
    return True, len(q)

def get_db():
    """Get database connection"""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    """Close database connection"""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    """Initialize database with tables and sample data"""
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    
    # Create users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Create products table
    c.execute('''CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        description TEXT NOT NULL
    )''')
    
    # Check if products table is empty
    c.execute('SELECT COUNT(*) FROM products')
    if c.fetchone()[0] == 0:
        # Insert sample products
        sample_products = [
            ('Laptop', 999.99, 'High-performance laptop with 16GB RAM and SSD storage'),
            ('Wireless Mouse', 29.99, 'Ergonomic wireless mouse with 2.4GHz connection'),
            ('Mechanical Keyboard', 89.99, 'RGB mechanical keyboard with Cherry MX switches'),
            ('USB-C Hub', 49.99, '7-in-1 USB-C hub with HDMI and power delivery'),
            ('Monitor 27"', 299.99, '4K UHD monitor with HDR support and USB-C'),
            ('Webcam 1080p', 79.99, 'Full HD webcam with built-in microphone')
        ]
        c.executemany('INSERT INTO products (name, price, description) VALUES (?, ?, ?)', sample_products)
    
    db.commit()
    db.close()

def login_required(f):
    """Decorator to require login for a route"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def get_current_user():
    """Get current logged-in user"""
    if 'user_id' in session:
        db = get_db()
        c = db.cursor()
        c.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],))
        user = c.fetchone()
        return user
    return None

@app.route('/')
def index():
    """Main store page displaying all products"""
    db = get_db()
    c = db.cursor()
    c.execute('SELECT * FROM products')
    products = c.fetchall()
    user = get_current_user()
    return render_template('index.html', products=products, user=user)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration route"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        error = None
        
        if not username:
            error = 'Username is required.'
        elif not email:
            error = 'Email is required.'
        elif not password:
            error = 'Password is required.'
        elif password != confirm_password:
            error = 'Passwords do not match.'
        elif len(password) < 6:
            error = 'Password must be at least 6 characters long.'
        
        if error is None:
            db = get_db()
            c = db.cursor()
            try:
                password_hash = generate_password_hash(password)
                c.execute(
                    'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
                    (username, email, password_hash)
                )
                db.commit()
                return redirect(url_for('login'))
            except sqlite3.IntegrityError:
                error = 'Username already exists.'
        
        return render_template('register.html', error=error)
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login route"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        error = None
        
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        
        if error is None:
            db = get_db()
            c = db.cursor()
            c.execute('SELECT * FROM users WHERE username = ?', (username,))
            user = c.fetchone()
            
            if user is None:
                error = 'Incorrect username.'
            elif not check_password_hash(user['password_hash'], password):
                error = 'Incorrect password.'
        
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        
        return render_template('login.html', error=error)
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """User logout route"""
    session.clear()
    return redirect(url_for('index'))

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """User profile page (requires login) - VULNERABLE TO SSTI/RCE"""
    if request.method == 'POST':
        new_username = request.form.get('username', '').strip()
        
        if new_username:
            db = get_db()
            c = db.cursor()
            try:
                c.execute('UPDATE users SET username = ? WHERE id = ?', (new_username, session['user_id']))
                db.commit()
            except sqlite3.IntegrityError:
                pass
        
        return redirect(url_for('profile'))
    
    user = get_current_user()
    
    # VULNERABILITY: render_template_string with user-controlled data allows SSTI -> RCE
    ip = request.remote_addr or "unknown"
    ok, cnt = rate_check(ip)
    
    if not ok:
        return "Rate limit exceeded", 429
    
    try:
        # Render the username as a Jinja2 template - allows SSTI/RCE
        rendered_username = render_template_string(user[1])
    except Exception as e:
        rendered_username = f"Template error: {str(e)}"
    
    return render_template('profile.html', 
                         user=user, 
                         rendered_username=rendered_username,
                         ts=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify(status="ok", now=int(time.time()))

if __name__ == '__main__':
    if not os.path.exists(DATABASE):
        init_db()
    app.run(debug=True)
