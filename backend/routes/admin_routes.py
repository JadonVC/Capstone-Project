# backend/routes/admin_routes.py - Admin authentication endpoints

from flask import Blueprint, jsonify, request
import mysql.connector
from models.admin import Admin

admin_bp = Blueprint('admin', __name__)

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

@admin_bp.route('/api/admin/signup', methods=['POST'])
def admin_signup():
    """Register a new admin"""
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
        
        # Validate email format
        if not Admin.validate_email(email):
            return jsonify({'error': 'Invalid email format'}), 400
        
        # Validate password strength
        is_valid, message = Admin.validate_password(password)
        if not is_valid:
            return jsonify({'error': message}), 400
        
        # Hash password
        password_hash = Admin.hash_password(password)
        
        # Check if email already exists
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM admins WHERE email = %s", (email,))
        if cursor.fetchone():
            cursor.close()
            connection.close()
            return jsonify({'error': 'Email already registered'}), 409
        
        # Insert new admin
        cursor.execute(
            "INSERT INTO admins (email, password_hash, first_name, last_name) VALUES (%s, %s, %s, %s)",
            (email, password_hash, first_name, last_name)
        )
        connection.commit()
        admin_id = cursor.lastrowid
        cursor.close()
        connection.close()
        
        return jsonify({
            'success': True,
            'message': 'Admin account created successfully',
            'admin_id': admin_id,
            'email': email
        }), 201
    
    except mysql.connector.Error as e:
        connection.rollback()
        return jsonify({'error': f'Database error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/api/admin/login', methods=['POST'])
def admin_login():
    """Login admin"""
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
        password_hash = Admin.hash_password(password)
        
        # DEBUG: Print the hash to terminal
        print(f"DEBUG: Email: {email}")
        print(f"DEBUG: Generated hash: {password_hash}")
        
        # Query admin by email - first get the stored hash
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT password_hash FROM admins WHERE email = %s", (email,))
        admin_record = cursor.fetchone()
        if admin_record:
            print(f"DEBUG: Stored hash: {admin_record['password_hash']}")
            print(f"DEBUG: Hashes match: {password_hash == admin_record['password_hash']}")
        
        # Now do the actual login check
        cursor.execute(
            "SELECT id, email, first_name, last_name, created_at FROM admins WHERE email = %s AND password_hash = %s",
            (email, password_hash)
        )
        
        admin = cursor.fetchone()
        cursor.close()
        connection.close()
        
        if not admin:
            return jsonify({'error': 'Invalid email or password'}), 401
        
        return jsonify({
            'success': True,
            'message': 'Admin login successful',
            'admin': {
                'id': admin['id'],
                'email': admin['email'],
                'first_name': admin['first_name'],
                'last_name': admin['last_name']
            }
        }), 200
    
    except mysql.connector.Error as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/api/admin/<int:admin_id>', methods=['GET'])
def get_admin(admin_id):
    """Get admin by ID"""
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, email, first_name, last_name, created_at FROM admins WHERE id = %s",
            (admin_id,)
        )
        admin = cursor.fetchone()
        cursor.close()
        connection.close()
        
        if not admin:
            return jsonify({'error': 'Admin not found'}), 404
        
        return jsonify(admin), 200
    
    except mysql.connector.Error as e:
        return jsonify({'error': str(e)}), 500
    
@admin_bp.route('/api/admin/all', methods=['GET'])
def get_all_admins():
    """Get all admins"""
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, email, first_name, last_name, created_at FROM admins ORDER BY created_at DESC"
        )
        admins = cursor.fetchall()
        cursor.close()
        connection.close()
        
        return jsonify(admins), 200
    
    except mysql.connector.Error as e:
        return jsonify({'error': str(e)}), 500