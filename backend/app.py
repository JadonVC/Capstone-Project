# backend/app.py - Simple Flask app for menu API

from flask import Flask, jsonify, request
from flask_cors import CORS
from routes.auth_routes import auth_bp
from routes.admin_routes import admin_bp
from routes.order_routes import order_bp
import mysql.connector

app = Flask(__name__)
CORS(app)  # Allow frontend to connect

app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(order_bp)

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

@app.route('/api/orders', methods=['POST'])
def create_order():
    """Create a new order with items"""
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        data = request.get_json()
        
        if not data or 'customer' not in data or 'items' not in data:
            return jsonify({'error': 'Missing required fields: customer and items'}), 400
        
        customer = data['customer']
        items = data['items']
        total = data.get('total', 0)
        user_id = data.get('user_id')  # Get user_id from frontend
        
        if not customer.get('name') or not customer.get('phone'):
            return jsonify({'error': 'Customer name and phone are required'}), 400
        
        if not items or len(items) == 0:
            return jsonify({'error': 'Order must contain at least one item'}), 400
        
        cursor = connection.cursor()
        
        cursor.execute(
            "INSERT INTO orders (customer_name, customer_phone, customer_address, total_amount, user_id) VALUES (%s, %s, %s, %s, %s)",
            (customer['name'], customer['phone'], customer.get('address', ''), total, user_id)
        )
        
        order_id = cursor.lastrowid
        
        for item in items:
            cursor.execute(
                "INSERT INTO order_items (order_id, menu_item_id, item_name, item_price, quantity, subtotal) VALUES (%s, %s, %s, %s, %s, %s)",
                (order_id, item['id'], item['name'], item['price'], item['quantity'], item['price'] * item['quantity'])
            )
        
        connection.commit()
        cursor.close()
        connection.close()
        
        return jsonify({
            'success': True,
            'order_id': order_id,
            'message': 'Order placed successfully'
        }), 201
    
    except mysql.connector.Error as e:
        connection.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """Get a specific order by ID with all items"""
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM orders WHERE id = %s", (order_id,))
        order = cursor.fetchone()
        
        if not order:
            cursor.close()
            connection.close()
            return jsonify({'error': 'Order not found'}), 404
        
        cursor.execute("SELECT * FROM order_items WHERE order_id = %s", (order_id,))
        items = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        order['items'] = items
        
        return jsonify(order), 200
    
    except mysql.connector.Error as e:
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    """Simple home route"""
    return jsonify({
        'message': 'Restaurant Menu API',
        'endpoints': [
            '/api/menu - Get all menu items',
            '/api/menu/<category> - Get items by category',
            '/api/orders - Create new order (POST)',
            '/api/orders/<order_id> - Get order by ID'
        ]
    })

@app.route('/api/orders/all', methods=['GET'])
def get_all_orders():
    """Get all orders"""
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, customer_name, customer_phone, customer_address, total_amount, created_at FROM orders ORDER BY created_at DESC"
        )
        orders = cursor.fetchall()
        
        # Get items for each order
        for order in orders:
            cursor.execute(
                "SELECT item_name, item_price, quantity, subtotal FROM order_items WHERE order_id = %s",
                (order['id'],)
            )
            order['items'] = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        return jsonify(orders), 200
    
    except mysql.connector.Error as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/menu/add', methods=['POST'])
def add_menu_item():
    """Add a new menu item"""
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        data = request.get_json()
        
        if not data or not data.get('name') or not data.get('price') or not data.get('category'):
            return jsonify({'error': 'Name, price, and category are required'}), 400
        
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO menu_items (name, description, price, category) VALUES (%s, %s, %s, %s)",
            (data['name'], data.get('description', ''), data['price'], data['category'])
        )
        connection.commit()
        item_id = cursor.lastrowid
        cursor.close()
        connection.close()
        
        return jsonify({
            'success': True,
            'item_id': item_id,
            'message': 'Menu item added successfully'
        }), 201
    
    except mysql.connector.Error as e:
        connection.rollback()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting Restaurant Menu API...")
    print("Available at: http://localhost:5000")
    print("Menu endpoint: http://localhost:5000/api/menu")
    app.run(debug=True, host='localhost', port=5000)
     