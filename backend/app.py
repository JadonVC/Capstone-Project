# backend/app.py - Simple Flask app for menu API

from flask import Flask, jsonify, request, send_from_directory, session
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
        
        if not customer.get('name') or not customer.get('phone'):
            return jsonify({'error': 'Customer name and phone are required'}), 400
        
        if not items or len(items) == 0:
            return jsonify({'error': 'Order must contain at least one item'}), 400
        
        cursor = connection.cursor()
        
        cursor.execute(
            "INSERT INTO orders (customer_name, customer_phone, customer_address, total_amount) VALUES (%s, %s, %s, %s)",
            (customer['name'], customer['phone'], customer.get('address', ''), total)
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
@app.route('/payment', methods=['GET', 'POST'])
def payment_page():
    if request.method == 'GET':
        # Serve the payment page
        return send_from_directory('frontend/html', 'payment.html')

    # Handle POST (payment submission)
    data = request.get_json()
    order_id = data.get('order_id')
    card_number = data.get('card_number')
    amount = data.get('amount')

    if not all([order_id, card_number, amount]):
        return jsonify({'status': 'error', 'message': 'Missing payment info'}), 400

    if str(card_number).startswith('4'):
        return jsonify({
            'status': 'success',
            'message': 'Payment processed successfully!',
            'transaction_id': f'TXN-{order_id[-4:] if order_id else "0000"}',
            'amount': amount
        })
    else:
        return jsonify({
            'status': 'error',
            'message': 'Payment failed. Invalid card number.'
        }), 400



if __name__ == '__main__':
    print("Starting Restaurant Menu API...")
    print("Available at: http://localhost:5000")
    print("Menu endpoint: http://localhost:5000/api/menu")
    app.run(debug=True, host='localhost', port=5000)


def login_required(f):
    def decorated_function(*args, **kwargs):
        if 'customer_id' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function
@app.route('/api/loyalty/balance', methods=['GET'])
@login_required
def get_loyalty_balance():
    """Get customer's loyalty points balance"""
    try:
        customer_id = session['customer_id']
        balance = LoyaltyManager.get_balance(customer_id)
        return jsonify(balance)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/loyalty/rewards', methods=['GET'])
@login_required
def get_rewards():
    """Get available rewards"""
    try:
        customer_id = session['customer_id']
        rewards = LoyaltyManager.get_available_rewards(customer_id)
        return jsonify(rewards)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/loyalty/redeem', methods=['POST'])
@login_required
def redeem_reward():
    """Redeem a reward"""
    try:
        customer_id = session['customer_id']
        data = request.get_json()
        reward_id = data.get('reward_id')
        
        if not reward_id:
            return jsonify({'error': 'reward_id required'}), 400
        
        discount = LoyaltyManager.redeem_reward(customer_id, reward_id)
        
        # Store discount in session for checkout
        session['pending_discount'] = discount
        
        return jsonify({
            'success': True,
            'discount': discount
        })
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/loyalty/history', methods=['GET'])
@login_required
def get_loyalty_history():
    """Get transaction history"""
    try:
        customer_id = session['customer_id']
        limit = request.args.get('limit', 20, type=int)
        history = LoyaltyManager.get_transaction_history(customer_id, limit)
        return jsonify(history)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
     