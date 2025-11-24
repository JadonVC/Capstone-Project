# backend/routes/menu_routes.py - Menu management endpoints

from flask import Blueprint, jsonify, request
import mysql.connector

menu_bp = Blueprint('menu', __name__)

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'restaurant_ordering',
    'port': 3306
}

def get_db_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return None

# Add new menu item
@menu_bp.route('/api/menu/add', methods=['POST'])
def add_menu_item():
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

# Edit menu item
@menu_bp.route('/api/menu/edit/<int:item_id>', methods=['PUT'])
def edit_menu_item(item_id):
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        cursor = connection.cursor()
        
        # Check if item exists
        cursor.execute("SELECT id FROM menu_items WHERE id = %s", (item_id,))
        if not cursor.fetchone():
            cursor.close()
            connection.close()
            return jsonify({'error': 'Menu item not found'}), 404
        
        # Update only provided fields
        update_fields = []
        update_values = []
        
        if 'name' in data:
            update_fields.append("name = %s")
            update_values.append(data['name'])
        if 'description' in data:
            update_fields.append("description = %s")
            update_values.append(data['description'])
        if 'price' in data:
            update_fields.append("price = %s")
            update_values.append(data['price'])
        if 'category' in data:
            update_fields.append("category = %s")
            update_values.append(data['category'])
        
        if not update_fields:
            cursor.close()
            connection.close()
            return jsonify({'error': 'No fields to update'}), 400
        
        update_values.append(item_id)
        query = f"UPDATE menu_items SET {', '.join(update_fields)} WHERE id = %s"
        
        cursor.execute(query, update_values)
        connection.commit()
        cursor.close()
        connection.close()
        
        return jsonify({
            'success': True,
            'message': 'Menu item updated successfully',
            'item_id': item_id
        }), 200
    
    except mysql.connector.Error as e:
        connection.rollback()
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Delete menu item
@menu_bp.route('/api/menu/delete/<int:item_id>', methods=['DELETE'])
def delete_menu_item(item_id):
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = connection.cursor()
        
        # Check if item exists
        cursor.execute("SELECT id FROM menu_items WHERE id = %s", (item_id,))
        if not cursor.fetchone():
            cursor.close()
            connection.close()
            return jsonify({'error': 'Menu item not found'}), 404
        
        # Delete the item
        cursor.execute("DELETE FROM menu_items WHERE id = %s", (item_id,))
        connection.commit()
        cursor.close()
        connection.close()
        
        return jsonify({
            'success': True,
            'message': 'Menu item deleted successfully',
            'item_id': item_id
        }), 200
    
    except mysql.connector.Error as e:
        connection.rollback()
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500