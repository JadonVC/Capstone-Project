# backend/app.py - Simple Flask app for menu API

from flask import Flask, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)  # Allow frontend to connect

# Database configuration (same as your setup)
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',  # Change to your MySQL password
    'database': 'restaurant_ordering',
    'port': 3306
}

def get_db_connection():
    """Simple database connection"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return None

@app.route('/api/menu', methods=['GET'])
def get_menu():
    """Get all menu items"""
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM menu_items ORDER BY category, name")
        menu_items = cursor.fetchall()
        cursor.close()
        connection.close()
        
        return jsonify(menu_items)
    
    except mysql.connector.Error as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/menu/<category>', methods=['GET'])
def get_menu_by_category(category):
    """Get menu items by category"""
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM menu_items WHERE category = %s ORDER BY name", (category,))
        menu_items = cursor.fetchall()
        cursor.close()
        connection.close()
        
        return jsonify(menu_items)
    
    except mysql.connector.Error as e:
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    """Simple home route"""
    return jsonify({
        'message': 'Restaurant Menu API',
        'endpoints': [
            '/api/menu - Get all menu items',
            '/api/menu/<category> - Get items by category'
        ]
    })

if __name__ == '__main__':
    print("Starting Restaurant Menu API...")
    print("Available at: http://localhost:5000")
    print("Menu endpoint: http://localhost:5000/api/menu")
    app.run(debug=True, host='localhost', port=5000)
     