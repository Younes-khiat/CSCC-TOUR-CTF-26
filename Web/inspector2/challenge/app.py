from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for
import sqlite3
import time
import threading
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db_connection
from playwright.sync_api import sync_playwright

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/', methods=['GET'])
def index():
    """Check if user has a valid session, if yes go to app, if no go to register"""
    if 'user_id' in session:
        # Session exists, validate it
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id FROM users WHERE id = ?", (session['user_id'],))
            user = cursor.fetchone()
            conn.close()
            
            if user:
                # Valid session, redirect to app
                return redirect(url_for('auth.app_route'))
        except:
            conn.close()
        
        # Invalid session, clear it
        session.clear()
    
    # No valid session, redirect to register
    return redirect(url_for('auth.register'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        # Return register HTML form
        return render_template('register.html')
    
    # Handle POST request
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')    
    if not username or not password:
        return jsonify({'message': 'Username and password required'}), 400

    # Hash the password before storing
    hashed_password = generate_password_hash(password)

    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("INSERT INTO users (username, password, admin) VALUES (?, ?, ?)", 
                       (username, hashed_password, 0))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'message': 'User already exists'}), 400
    finally:
        conn.close()

    return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        # Return login HTML form
        return render_template('login.html')
    
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = username
            session['admin'] = user['admin']
            return jsonify({'message': 'Login successful'}), 200
        
        return jsonify({'message': 'Invalid credentials'}), 401
    
    finally:
        conn.close()

@auth_bp.route('/logout', methods=['GET'])
def logout():
    session.clear()  # Clear entire session
    return redirect(url_for('auth.register'))

@auth_bp.route('/app', methods=['GET', 'POST'])
def app_route():
    # Check if user is authenticated
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    if request.method == 'GET':
        # Get all comments from database
        conn = get_db_connection()
        cursor = conn.cursor()
         
        try:
            cursor.execute("""
                SELECT c.id, c.user_id, u.username, c.comment, c.created_at 
                FROM comments c 
                JOIN users u ON c.user_id = u.id 
                ORDER BY c.created_at DESC
            """)
            comments = cursor.fetchall()
            
            cursor.execute("SELECT username FROM users WHERE id = ?", (session['user_id'],))
            user = cursor.fetchone()
            username = user['username'] if user else 'Unknown'
            
            # Check if there's a target_user parameter (for bot viewing specific user's XSS)
            target_user = request.args.get('target_user', type=int)
            
            return render_template('app.html', comments=comments, username=username, user_id=session['user_id'], is_admin=session.get('admin', 0), target_user=target_user)
        finally:
            conn.close()
    
    elif request.method == 'POST':
        # Handle adding a new comment
        user_id = session.get('user_id')

        if not user_id:
            return jsonify({"message": "Unauthorized"}), 401
        
        comment_text = request.form.get('comment', '').strip()
        
        # Check for blocked patterns
        blocked_patterns = ['script', 'cookie', 'document', 'http', 'fetch', 'https', 'script']
        if any(pattern in comment_text.lower() for pattern in blocked_patterns):
            return jsonify({"message": " blocked"}), 400
        
        if not comment_text:
            return jsonify({"message": "Comment cannot be empty"}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "INSERT INTO comments (user_id, comment) VALUES (?, ?)",
                (user_id, comment_text)
            )
            conn.commit()
            
            # Fetch all comments again to return updated page
            cursor.execute("""
                SELECT c.id, c.user_id, u.username, c.comment, c.created_at 
                FROM comments c 
                JOIN users u ON c.user_id = u.id 
                ORDER BY c.created_at DESC
            """)
            comments = cursor.fetchall()

        finally:
            conn.close()
        
        # Start bot in background thread so it doesn't block the response
        bot_thread = threading.Thread(target=admin_bot_visit, args=(user_id,))
        bot_thread.daemon = True
        bot_thread.start()

        return render_template('app.html', username=session['username'], comments=comments, user_id=session.get('user_id'), is_admin=session.get('admin', 0))

@auth_bp.route('/admin', methods=['GET'])
def admin():
    # Check if user is authenticated
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    # Check if user is admin
    if not session.get('admin'):
        return jsonify({'message': 'Access denied. Admin only.'}), 403
    
    return render_template('admin.html', username=session.get('username'))

@auth_bp.route('/api/comments', methods=['GET'])
def get_comments():
    # Check if user is authenticated
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT c.id, c.user_id, u.username, c.comment, c.created_at 
            FROM comments c 
            JOIN users u ON c.user_id = u.id 
            ORDER BY c.created_at DESC
        """)
        comments = cursor.fetchall()
        
        # Convert to list of dictionaries
        current_user_id = session.get('user_id')
        is_admin = session.get('admin', 0)
        target_user = request.args.get('target_user', type=int)
        
        comments_list = []
        for comment in comments:
            # Determine if content should be escaped (backend-level decision)
            # Render raw (unsafe) if: user's own comment OR admin viewing target_user
            should_render_unsafe = (comment[1] == current_user_id) or (is_admin and target_user and comment[1] == target_user)
            
            # Escape HTML if not rendering unsafe (safe mode)
            comment_content = comment[3]
            if not should_render_unsafe:
                # Escape HTML special characters
                import html
                comment_content = html.escape(comment_content)
            
            comments_list.append({
                'id': comment[0],
                'user_id': comment[1],
                'username': comment[2],
                'comment': comment_content,
                'created_at': comment[4]
            })
        
        return jsonify({
            'comments': comments_list,
            'current_user_id': current_user_id,
            'is_admin': is_admin,
            'target_user': target_user
        })
    finally:
        conn.close()

@auth_bp.route('/addpost', methods=['GET'])
def addpost():
    # Check if user is authenticated
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    return render_template('ad_post.html', username=session.get('username'))


def admin_bot_visit(target_user_id):
    print(f"[BOT] Admin is visiting to view user {target_user_id}'s comments with Playwright...", flush=True)
    
    # Sleep for 5 seconds before starting
    time.sleep(5)

    print("[BOT] Starting bot visit...", flush=True)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()
            
            # Go to login page
            page.goto("http://localhost:5000/login", timeout=5000)
            print("[BOT] Navigated to login page", flush=True)
            
            # Fill in admin credentials
            page.fill('#username', 'admin')
            page.fill('#password', 'houddini_is_admin_of_this_app!')
            print("[BOT] Filled in admin credentials", flush=True)
            
            # Submit login form and wait for response
            page.click('button[type="submit"]')
            page.wait_for_load_state('networkidle')
            print("[BOT] Login submitted", flush=True)
            
            # Check if login was successful by trying to navigate to /app
            page.goto("http://localhost:5000/app", timeout=5000)
            print("[BOT] Successfully navigated to /app", flush=True)
            
            # Now visit with target_user parameter to reload and trigger XSS
            page.goto(f"http://localhost:5000/app?target_user={target_user_id}", timeout=5000)
            print(f"[BOT] Visiting /app to view user {target_user_id}'s comments", flush=True)
            
            # Wait for page to fully load
            page.wait_for_load_state('networkidle')
            print("[BOT] Page loaded, viewing comments", flush=True)
            
            # Wait for XSS to execute
            page.wait_for_timeout(3000)
            
            # Get cookies (in case XSS stole them)
            cookies = context.cookies()
            print(f"[BOT] Admin cookies: {cookies}", flush=True)
            print(f"[BOT] Successfully viewed user {target_user_id}'s comments", flush=True)
            
            browser.close()
    except Exception as e:
        print(f"[BOT] Error during visit: {e}", flush=True)
        import traceback
        print(f"[BOT] Traceback: {traceback.format_exc()}", flush=True)
    finally:
        print("[BOT] Done.", flush=True)