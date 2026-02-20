from flask import Flask
from flask_cors import CORS
from database import init_db
from app import auth_bp
import os
import secrets

app = Flask(__name__)

# Configure secret key for session management
app.secret_key = os.environ.get('SECRET_KEY') or '9c7c59e8c4c446e2b79e3d6b7b0c3f9c5b8f25d8c1a7d4f3a2b1c9d8e7f6a5b4'

# Configure session cookies to be accessible via JavaScript (for CTF XSS challenge)
app.config['SESSION_COOKIE_HTTPONLY'] = False
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Enable CORS for all routes
CORS(app, supports_credentials=True)

# Register blueprints
app.register_blueprint(auth_bp)

# Initialize database
init_db()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
