"""
LEGACY USER AUTHENTICATION
Intentionally vulnerable for demo purposes

NOTE: This file needs security review and modernization.
"""

import hashlib
import sqlite3

class UserAuth:
    def __init__(self):
        self.conn = sqlite3.connect('users.db')
    
    # SECURITY: Weak password hashing (MD5)
    def hash_password(self, password):
        return hashlib.md5(password.encode()).hexdigest()
    
    # SECURITY: SQL Injection + weak hashing
    def login(self, username, password):
        cursor = self.conn.cursor()
        hashed = self.hash_password(password)
        # SQL Injection vulnerability
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{hashed}'"
        cursor.execute(query)
        user = cursor.fetchone()
        return user
    
    # SECURITY: No password strength validation
    def register(self, username, password, email):
        cursor = self.conn.cursor()
        hashed = self.hash_password(password)
        # No validation of inputs
        query = f"INSERT INTO users (username, password, email) VALUES ('{username}', '{hashed}', '{email}')"
        cursor.execute(query)
        self.conn.commit()
        return True
    
    # SECURITY: Information disclosure
    def get_user_details(self, user_id):
        cursor = self.conn.cursor()
        query = f"SELECT id, username, password, email, ssn, credit_card FROM users WHERE id = {user_id}"
        cursor.execute(query)
        user = cursor.fetchone()
        # Returns sensitive data including password hash, SSN, credit card
        return {
            "id": user[0],
            "username": user[1],
            "password": user[2],  # NEVER return password hash!
            "email": user[3],
            "ssn": user[4],       # PII exposure
            "credit_card": user[5] # PCI violation
        
        }
