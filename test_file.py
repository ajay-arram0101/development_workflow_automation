"""
Test file for AI Code Review demo
This file has some intentional issues to demonstrate the reviewer
"""

import mysql.connector

# Hardcoded credentials (security issue!)
DB_PASSWORD = "super_secret_123"

def get_user(username):
    # SQL Injection vulnerability!
    query = "SELECT * FROM users WHERE name = '" + username + "'"
    conn = mysql.connector.connect(host="localhost", password=DB_PASSWORD)
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchone()

def process_data(x):
    # No type hints, no docstring, magic numbers
    if x > 100:
        return x * 1.5
    elif x > 50:
        return x * 1.25
    else:
        return x * 1.1
