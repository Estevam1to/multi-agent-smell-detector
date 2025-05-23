import html
import re
import json
import base64
import hashlib
import os
import sqlite3
import subprocess

class WebApp:
    def __init__(self, db_path="app.db"):
        # God class with too many responsibilities
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.session_store = {}
        self.csrf_tokens = {}
        self.xss_patterns = ["<script>", "javascript:", "onerror=", "onload="]
        self.blocked_ips = []
        self.setup_database()
    
    def setup_database(self):
        # Create necessary tables
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT,
            email TEXT,
            role TEXT
        )
        ''')
        
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            title TEXT,
            content TEXT,
            created_at TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        ''')
        
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY,
            post_id INTEGER,
            user_id INTEGER,
            content TEXT,
            created_at TEXT,
            FOREIGN KEY (post_id) REFERENCES posts (id),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        ''')
        
        self.conn.commit()
    
    def create_user(self, username, password, email, role="user"):
        # Weak password hashing (security smell)
        hashed_password = hashlib.md5(password.encode()).hexdigest()
        
        try:
            # SQL Injection vulnerability
            query = f"INSERT INTO users (username, password, email, role) VALUES ('{username}', '{hashed_password}', '{email}', '{role}')"
            self.cursor.execute(query)
            self.conn.commit()
            return self.cursor.lastrowid
        except Exception as e:
            print(f"Error creating user: {str(e)}")
            return None
    
    def login(self, username, password):
        # Weak authentication (security smell)
        hashed_password = hashlib.md5(password.encode()).hexdigest()
        
        # SQL Injection vulnerability
        query = f"SELECT id, username, role FROM users WHERE username = '{username}' AND password = '{hashed_password}'"
        
        self.cursor.execute(query)
        user = self.cursor.fetchone()
        
        if user:
            # Generate session ID
            session_id = base64.b64encode(os.urandom(24)).decode()
            self.session_store[session_id] = {
                "user_id": user[0],
                "username": user[1],
                "role": user[2],
                "authenticated": True
            }
            return {"session_id": session_id, "user_id": user[0]}
        
        return None
    
    def create_post(self, session_id, title, content):
        # Check authentication
        session = self.session_store.get(session_id)
        if not session or not session.get("authenticated"):
            return {"error": "Not authenticated"}
        
        user_id = session["user_id"]
        
        # XSS vulnerability - no proper sanitization
        # Just a basic check that can be bypassed
        for pattern in self.xss_patterns:
            if pattern in content.lower():
                content = content.replace(pattern, "")
        
        try:
            # SQL Injection vulnerability
            query = f"INSERT INTO posts (user_id, title, content, created_at) VALUES ({user_id}, '{title}', '{content}', datetime('now'))"
            self.cursor.execute(query)
            self.conn.commit()
            return {"post_id": self.cursor.lastrowid}
        except Exception as e:
            print(f"Error creating post: {str(e)}")
            return {"error": str(e)}
    
    def get_post(self, post_id):
        # SQL Injection vulnerability
        query = f"SELECT p.id, p.title, p.content, p.created_at, u.username FROM posts p JOIN users u ON p.user_id = u.id WHERE p.id = {post_id}"
        
        try:
            self.cursor.execute(query)
            post = self.cursor.fetchone()
            
            if not post:
                return {"error": "Post not found"}
            
            return {
                "id": post[0],
                "title": post[1],
                "content": post[2],  # Stored XSS vulnerability - content not sanitized on output
                "created_at": post[3],
                "author": post[4]
            }
        except Exception as e:
            print(f"Error getting post: {str(e)}")
            return {"error": str(e)}
    
    def add_comment(self, session_id, post_id, content):
        # Check authentication
        session = self.session_store.get(session_id)
        if not session or not session.get("authenticated"):
            return {"error": "Not authenticated"}
        
        user_id = session["user_id"]
        
        # XSS vulnerability - no proper sanitization
        # Just a basic check that can be bypassed
        for pattern in self.xss_patterns:
            if pattern in content.lower():
                content = content.replace(pattern, "")
        
        try:
            # SQL Injection vulnerability
            query = f"INSERT INTO comments (post_id, user_id, content, created_at) VALUES ({post_id}, {user_id}, '{content}', datetime('now'))"
            self.cursor.execute(query)
            self.conn.commit()
            return {"comment_id": self.cursor.lastrowid}
        except Exception as e:
            print(f"Error adding comment: {str(e)}")
            return {"error": str(e)}
    
    def search_posts(self, keyword):
        # SQL Injection vulnerability
        query = f"SELECT id, title, substr(content, 1, 100) || '...' FROM posts WHERE title LIKE '%{keyword}%' OR content LIKE '%{keyword}%'"
        
        try:
            self.cursor.execute(query)
            posts = self.cursor.fetchall()
            
            results = []
            for post in posts:
                results.append({
                    "id": post[0],
                    "title": post[1],
                    "preview": post[2]
                })
            
            return results
        except Exception as e:
            print(f"Error searching posts: {str(e)}")
            return {"error": str(e)}
    
    def execute_admin_action(self, session_id, action, params):
        # Check authentication and admin role
        session = self.session_store.get(session_id)
        if not session or not session.get("authenticated"):
            return {"error": "Not authenticated"}
        
        if session.get("role") != "admin":
            return {"error": "Unauthorized"}
        
        # Command injection vulnerability
        if action == "run_system_command":
            command = params.get("command", "")
            try:
                # Command injection vulnerability
                output = subprocess.check_output(command, shell=True)
                return {"output": output.decode()}
            except subprocess.CalledProcessError as e:
                return {"error": str(e), "output": e.output.decode() if e.output else ""}
        
        # More vulnerable actions could be added here
        
        return {"error": "Unknown action"}
    
    def update_user_profile(self, session_id, email=None, new_password=None):
        # Check authentication
        session = self.session_store.get(session_id)
        if not session or not session.get("authenticated"):
            return {"error": "Not authenticated"}
        
        user_id = session["user_id"]
        updates = []
        
        if email:
            # SQL Injection vulnerability
            updates.append(f"email = '{email}'")
        
        if new_password:
            # Weak password hashing
            hashed_password = hashlib.md5(new_password.encode()).hexdigest()
            updates.append(f"password = '{hashed_password}'")
        
        if not updates:
            return {"error": "No updates provided"}
        
        try:
            # SQL Injection vulnerability
            query = f"UPDATE users SET {', '.join(updates)} WHERE id = {user_id}"
            self.cursor.execute(query)
            self.conn.commit()
            return {"success": True}
        except Exception as e:
            print(f"Error updating profile: {str(e)}")
            return {"error": str(e)}
    
    def generate_report(self, session_id, report_type, output_file):
        # Check authentication and admin role
        session = self.session_store.get(session_id)
        if not session or not session.get("authenticated"):
            return {"error": "Not authenticated"}
        
        if session.get("role") != "admin":
            return {"error": "Unauthorized"}
        
        # Path traversal vulnerability
        try:
            if report_type == "users":
                self.cursor.execute("SELECT id, username, email, role FROM users")
                users = self.cursor.fetchall()
                
                report = "User Report\n\n"
                for user in users:
                    report += f"ID: {user[0]}, Username: {user[1]}, Email: {user[2]}, Role: {user[3]}\n"
                
                # Path traversal vulnerability - no validation of output_file
                with open(output_file, 'w') as f:
                    f.write(report)
                
                return {"success": True, "file": output_file}
            
            return {"error": "Unknown report type"}
        except Exception as e:
            print(f"Error generating report: {str(e)}")
            return {"error": str(e)}
