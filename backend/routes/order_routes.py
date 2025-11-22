# backend/routes/order_routes.py - Order management endpoints

from flask import Blueprint, jsonify, request
import mysql.connector

order_bp = Blueprint('orders', __name__)

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

@order_bp.route('/api/orders/all', methods=['GET'])
def get_all_orders():
    """Get all orders"""
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, customer_name, customer_phone, customer_address, total_amount, order_status, created_at FROM orders ORDER BY created_at DESC"
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

@order_bp.route('/api/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """Get a specific order by ID"""
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, customer_name, customer_phone, customer_address, total_amount, order_status, created_at FROM orders WHERE id = %s",
            (order_id,)
        )
        order = cursor.fetchone()
        
        if not order:
            cursor.close()
            connection.close()
            return jsonify({'error': 'Order not found'}), 404
        
        # Get items for order
        cursor.execute(
            "SELECT item_name, item_price, quantity, subtotal FROM order_items WHERE order_id = %s",
            (order_id,)
        )
        order['items'] = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        return jsonify(order), 200
    
    except mysql.connector.Error as e:
        return jsonify({'error': str(e)}), 500

@order_bp.route('/api/orders/<int:order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    """Update order status"""
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        data = request.get_json()
        
        if not data or not data.get('status'):
            return jsonify({'error': 'Status is required'}), 400
        
        new_status = data.get('status').lower()
        
        # Validate status
        valid_statuses = ['pending', 'preparing', 'ready', 'completed']
        if new_status not in valid_statuses:
            return jsonify({'error': f'Invalid status. Must be one of: {", ".join(valid_statuses)}'}), 400
        
        # Update order status
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE orders SET order_status = %s WHERE id = %s",
            (new_status, order_id)
        )
        connection.commit()
        
        if cursor.rowcount == 0:
            cursor.close()
            connection.close()
            return jsonify({'error': 'Order not found'}), 404
        
        cursor.close()
        connection.close()
        
        return jsonify({
            'success': True,
            'message': f'Order status updated to {new_status}',
            'order_id': order_id,
            'status': new_status
        }), 200
    
    except mysql.connector.Error as e:
        connection.rollback()
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@order_bp.route('/api/orders/user/<int:user_id>', methods=['GET'])
def get_user_orders(user_id):
    """Get all orders for a specific user"""
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, customer_name, customer_phone, customer_address, total_amount, order_status, created_at FROM orders WHERE user_id = %s ORDER BY created_at DESC",
            (user_id,)
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