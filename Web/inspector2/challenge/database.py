import sqlite3
import os
from datetime import datetime
from werkzeug.security import generate_password_hash

DATABASE = 'ctf.db'

def get_db_connection():
    """Get a connection to the SQLite database"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with required tables"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            admin INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create comments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            comment TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')

    # Create or update admin user
    hashed_password = generate_password_hash('houddini_is_admin_of_this_app!')
    
    # Check if admin exists
    cursor.execute('SELECT id FROM users WHERE username = ?', ('admin',))
    admin_exists = cursor.fetchone()
    
    if admin_exists:
        # Update admin password
        cursor.execute('UPDATE users SET password = ? WHERE username = ?', (hashed_password, 'admin'))
    else:
        # Create admin user
        cursor.execute('''
            INSERT INTO users (username, password, admin) 
            VALUES (?, ?, 1)
        ''', ('admin', hashed_password))
    
    conn.commit()
    conn.close()
