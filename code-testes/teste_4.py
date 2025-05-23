import shutil
import sqlite3
import logging
import os
import random
import string
import time

logging.basicConfig(level=logging.INFO, filename="database.log")
logger = logging.getLogger("database_manager")

class DatabaseManager:
    def __init__(self, db_path="app.db"):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.connected = False
        self.last_query_time = None
        self.query_count = 0
        self.transaction_active = False
        self.cached_results = {}
        self.init_connection()
    
    def init_connection(self):
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            self.connected = True
            self.create_tables()
            logger.info(f"Database connection established: {self.db_path}")
        except Exception as e:
            logger.error(f"Failed to connect to database: {str(e)}")
            self.connected = False
    
    def create_tables(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT,
            email TEXT,
            created_at TEXT,
            last_login TEXT
        )
        ''')
        
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT,
            price REAL,
            description TEXT,
            stock INTEGER
        )
        ''')
        
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            total REAL,
            status TEXT,
            created_at TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        ''')
        
        self.conn.commit()
    
    def query(self, sql, params=None):
        if not self.connected:
            self.init_connection()
        
        start_time = time.time()
        
        try:
            if params:
                self.cursor.execute(sql, params)
            else:
                self.cursor.execute(sql)
            
            result = self.cursor.fetchall()
            self.query_count += 1
            self.last_query_time = time.time() - start_time
            
            logger.info(f"Query executed: {sql}")
            logger.info(f"Parameters: {params}")
            logger.info(f"Query time: {self.last_query_time:.4f}s")
            
            return result
        except Exception as e:
            logger.error(f"Query failed: {sql}")
            logger.error(f"Error: {str(e)}")
            return None
    
    def insert_user(self, username, password, email):
        created_at = time.strftime('%Y-%m-%d %H:%M:%S')
        
        sql = f"INSERT INTO users (username, password, email, created_at) VALUES ('{username}', '{password}', '{email}', '{created_at}')"
        
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            user_id = self.cursor.lastrowid
            logger.info(f"User created: {username} (ID: {user_id})")
            return user_id
        except Exception as e:
            logger.error(f"Failed to create user {username}: {str(e)}")
            return None
    
    def authenticate_user(self, username, password):
        sql = f"SELECT id, username FROM users WHERE username = '{username}' AND password = '{password}'"
        
        result = self.query(sql)
        if result and len(result) > 0:
            user_id = result[0][0]
            now = time.strftime('%Y-%m-%d %H:%M:%S')
            update_sql = f"UPDATE users SET last_login = '{now}' WHERE id = {user_id}"
            self.cursor.execute(update_sql)
            self.conn.commit()
            return result[0]
        return None
    
    def search_products(self, keyword):
        sql = f"SELECT * FROM products WHERE name LIKE '%{keyword}%' OR description LIKE '%{keyword}%'"
        return self.query(sql)
    
    def backup_database(self, backup_path):
        if not self.connected:
            logger.error("Cannot backup: database not connected")
            return False
        
        try:
            self.conn.commit()  
            shutil.copy2(self.db_path, backup_path)
            logger.info(f"Database backed up to {backup_path}")
            return True
        except Exception as e:
            logger.error(f"Backup failed: {str(e)}")
            return False
    
    def close(self):
        if self.connected:
            self.conn.close()
            self.connected = False
            logger.info("Database connection closed")
