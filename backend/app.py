# backend/app.py - Simple Flask app for menu API

from flask import Flask, jsonify
from flask_cors import CORS
from flask import request
import mysql.connector

app = Flask(__name__)
CORS(app)  # Allow frontend to connect

# Database configuration (same as your setup)
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Charl0tt3-22',  # Change to your MySQL password
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

@app.route('/api/checkout', methods=['POST'])
def checkout():
    data = request.get_json()
    cart_items = data.get('cart', [])

    if not cart_items:
        return jsonify({'error': 'Cart is empty'}), 400

    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO orders (total_price) VALUES (0)")
        order_id = cursor.lastrowid
        total = 0

        for item in cart_items:
            cursor.execute(
                "INSERT INTO order_items (order_id, item_id, quantity, price) VALUES (%s, %s, %s, %s)",
                (order_id, item['id'], item['quantity'], item['price'])
            )
            total += item['price'] * item['quantity']

        cursor.execute("UPDATE orders SET total_price = %s WHERE id = %s", (total, order_id))
        connection.commit()

        return jsonify({'message': 'Order placed successfully', 'order_id': order_id}), 200

    except Exception as e:
        connection.rollback()
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        connection.close()

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
     