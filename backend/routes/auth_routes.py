# backend/routes/auth_routes.py - Authentication endpoints

from flask import Blueprint, jsonify, request
import mysql.connector
from models.user import User

auth_bp = Blueprint('auth', __name__)

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'restaurant_ordering',
    'port': 3306
}

def get_db_connection():
    """Get database connection"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return None

@auth_bp.route('/api/auth/signup', methods=['POST'])
def signup():
    """Register a new user"""
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password are required'}), 400
        
        email = data.get('email').lower().strip()
        password = data.get('password')
        first_name = data.get('first_name', '').strip()
        last_name = data.get('last_name', '').strip()
        phone = data.get('phone', '').strip()
        
        # Validate email format
        if not User.validate_email(email):
            return jsonify({'error': 'Invalid email format'}), 400
        
        # Validate password strength
        is_valid, message = User.validate_password(password)
        if not is_valid:
            return jsonify({'error': message}), 400
        
        # Validate phone if provided
        if phone and not User.validate_phone(phone):
            return jsonify({'error': 'Invalid phone number format'}), 400
        
        # Hash password
        password_hash = User.hash_password(password)
        
        # Check if email already exists
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            cursor.close()
            connection.close()
            return jsonify({'error': 'Email already registered'}), 409
        
        # Insert new user
        cursor.execute(
            "INSERT INTO users (email, phone, password_hash, first_name, last_name) VALUES (%s, %s, %s, %s, %s)",
            (email, phone if phone else None, password_hash, first_name, last_name)
        )
        connection.commit()
        user_id = cursor.lastrowid
        cursor.close()
        connection.close()
        
        return jsonify({
            'success': True,
            'message': 'Account created successfully',
            'user_id': user_id,
            'email': email
        }), 201
    
    except mysql.connector.Error as e:
        connection.rollback()
        return jsonify({'error': f'Database error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/api/auth/login', methods=['POST'])
def login():
    """Login user"""
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        data = request.get_json()
        
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password are required'}), 400
        
        email = data.get('email').lower().strip()
        password = data.get('password')
        
        # Hash the provided password
        password_hash = User.hash_password(password)
        
        # Query user by email
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, email, phone, first_name, last_name, created_at FROM users WHERE email = %s AND password_hash = %s",
            (email, password_hash)
        )
        
        user = cursor.fetchone()
        cursor.close()
        connection.close()
        
        if not user:
            return jsonify({'error': 'Invalid email or password'}), 401
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'user': {
                'id': user['id'],
                'email': user['email'],
                'phone': user['phone'],
                'first_name': user['first_name'],
                'last_name': user['last_name']
            }
        }), 200
    
    except mysql.connector.Error as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/api/auth/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get user by ID"""
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, email, phone, first_name, last_name, created_at FROM users WHERE id = %s",
            (user_id,)
        )
        user = cursor.fetchone()
        cursor.close()
        connection.close()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify(user), 200
    
    except mysql.connector.Error as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/api/auth/user/<int:user_id>/orders', methods=['GET'])
def get_user_orders(user_id):
    """Get all orders for a user"""
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        # Get orders
        cursor.execute(
            "SELECT id, customer_name, customer_phone, total_amount, created_at FROM orders WHERE user_id = %s ORDER BY created_at DESC",
            (user_id,)
        )
        orders = cursor.fetchall()
        
        # For each order, get items
        for order in orders:
            cursor.execute(
                "SELECT item_name, item_price, quantity, subtotal FROM order_items WHERE order_id = %s",
                (order['id'],)
            )
            order['items'] = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        return jsonify({
            'user_id': user_id,
            'orders': orders,
            'total_orders': len(orders)
        }), 200
    
    except mysql.connector.Error as e:
        return jsonify({'error': str(e)}), 500