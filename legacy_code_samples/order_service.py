"""
LEGACY ORDER SERVICE
This is intentionally bad code with common legacy issues:
- SQL injection vulnerabilities
- No input validation
- Hardcoded credentials
- Poor error handling
- No type hints
- Outdated patterns
"""

import mysql.connector
import json

# SECURITY ISSUE: Hardcoded credentials
DB_HOST = "localhost"
DB_USER = "admin"
DB_PASSWORD = "admin123"  # TODO: move to env
API_KEY = "sk-1234567890abcdef"  # Exposed API key

class OrderService:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database="ecommerce"
        )
    
    # SECURITY ISSUE: SQL Injection vulnerability
    def get_order(self, order_id):
        cursor = self.conn.cursor()
        # BAD: String concatenation in SQL
        query = "SELECT * FROM orders WHERE id = '" + order_id + "'"
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        return result
    
    # SECURITY ISSUE: Another SQL injection
    def search_orders(self, customer_name):
        cursor = self.conn.cursor()
        # BAD: f-string in SQL query
        query = f"SELECT * FROM orders WHERE customer_name LIKE '%{customer_name}%'"
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        return results
    
    # CODE QUALITY: No validation, poor error handling
    def create_order(self, data):
        cursor = self.conn.cursor()
        # No input validation
        # No try/except
        query = "INSERT INTO orders (customer_id, product_id, quantity, total) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (data['customer_id'], data['product_id'], data['quantity'], data['total']))
        self.conn.commit()
        cursor.close()
        return cursor.lastrowid
    
    # CODE QUALITY: Callback hell, outdated pattern
    def process_order(self, order_id, callback):
        order = self.get_order(order_id)
        if order:
            # Nested callbacks (outdated pattern)
            self.validate_inventory(order, lambda valid: 
                self.charge_payment(order, lambda charged:
                    self.ship_order(order, lambda shipped:
                        callback(shipped)
                    )
                ) if valid else callback(None)
            )
        else:
            callback(None)
    
    def validate_inventory(self, order, callback):
        # Simulated async with callback
        callback(True)
    
    def charge_payment(self, order, callback):
        callback(True)
    
    def ship_order(self, order, callback):
        callback(True)
    
    # CODE QUALITY: God method - does too many things
    def generate_report(self, start_date, end_date, format, include_returns, include_refunds, send_email, email_to):
        cursor = self.conn.cursor()
        query = f"SELECT * FROM orders WHERE created_at BETWEEN '{start_date}' AND '{end_date}'"
        cursor.execute(query)
        orders = cursor.fetchall()
        
        if include_returns:
            query2 = f"SELECT * FROM returns WHERE created_at BETWEEN '{start_date}' AND '{end_date}'"
            cursor.execute(query2)
            returns = cursor.fetchall()
        
        if include_refunds:
            query3 = f"SELECT * FROM refunds WHERE created_at BETWEEN '{start_date}' AND '{end_date}'"
            cursor.execute(query3)
            refunds = cursor.fetchall()
        
        # Build report
        report = {"orders": orders}
        if include_returns:
            report["returns"] = returns
        if include_refunds:
            report["refunds"] = refunds
        
        # Format report
        if format == "json":
            output = json.dumps(report)
        elif format == "csv":
            output = "id,customer,total\n"
            for o in orders:
                output += f"{o[0]},{o[1]},{o[2]}\n"
        else:
            output = str(report)
        
        # Send email if requested
        if send_email:
            import smtplib
            server = smtplib.SMTP('smtp.company.com', 587)
            server.login("reports@company.com", "reportpass123")  # SECURITY: Hardcoded password
            server.sendmail("reports@company.com", email_to, output)
            server.quit()
        
        cursor.close()
        return output


# OUTDATED: Using old-style string formatting
def format_price(amount):
    return "$%.2f" % amount


# CODE SMELL: Magic numbers
def calculate_shipping(weight):
    if weight < 1:
        return 5.99
    elif weight < 5:
        return 9.99
    elif weight < 10:
        return 14.99
    else:
        return 19.99 + (weight - 10) * 0.50
