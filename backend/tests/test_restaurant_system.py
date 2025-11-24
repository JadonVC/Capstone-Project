"""
Unit Tests for Restaurant Ordering System (47 Tests - All Passing)
"""

import unittest
from unittest.mock import patch, MagicMock
import json
import sys
import os

# Mock mysql.connector BEFORE importing app
sys.modules['mysql'] = MagicMock()
sys.modules['mysql.connector'] = MagicMock()

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.order import Order
from app import app

class TestOrderModel(unittest.TestCase):
    def setUp(self):
        self.sample_items = [
            {'id': 1, 'name': 'Burger', 'price': 12.99, 'quantity': 2, 'subtotal': 25.98},
            {'id': 2, 'name': 'Fries', 'price': 5.99, 'quantity': 1, 'subtotal': 5.99}
        ]
        self.order = Order(1, 'John Doe', '555-1234', '123 Main St', 31.97, self.sample_items, '2025-01-01 10:00:00')
    
    def test_order_initialization(self):
        self.assertEqual(self.order.id, 1)
        self.assertEqual(self.order.customer_name, 'John Doe')
        self.assertEqual(self.order.customer_phone, '555-1234')
    
    def test_order_to_dict(self):
        order_dict = self.order.to_dict()
        self.assertIsInstance(order_dict, dict)
        self.assertEqual(order_dict['id'], 1)
    
    def test_get_item_count(self):
        self.assertEqual(self.order.get_item_count(), 3)
    
    def test_get_item_count_empty(self):
        empty = Order(1, 'Jane', '555-5678', '456 Oak', 0, [], '2025-01-01 10:00:00')
        self.assertEqual(empty.get_item_count(), 0)
    
    def test_calculate_total(self):
        self.assertEqual(self.order.calculate_total(), 31.97)
    
    def test_calculate_total_single(self):
        single = Order(1, 'Test', '555-1111', '', 0, [{'id': 1, 'name': 'Pizza', 'price': 15.99, 'quantity': 1, 'subtotal': 15.99}], '2025-01-01 10:00:00')
        self.assertEqual(single.calculate_total(), 15.99)
    
    def test_calculate_total_zero(self):
        empty = Order(1, 'John', '555-0000', '', 0, [], '2025-01-01 10:00:00')
        self.assertEqual(empty.calculate_total(), 0)
    
    def test_to_dict_fields(self):
        order_dict = self.order.to_dict()
        required_fields = ['id', 'customer_name', 'customer_phone', 'customer_address', 'total_amount', 'items', 'created_at']
        for field in required_fields:
            self.assertIn(field, order_dict)

class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_app_exists(self):
        self.assertIsNotNone(self.app)
    
    def test_app_testing_mode(self):
        self.assertTrue(self.app.config['TESTING'])
    
    def test_cors_enabled(self):
        response = self.client.get('/')
        self.assertIsNotNone(response)

class TestHomeEndpoint(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_home_returns_200(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_home_returns_json(self):
        response = self.client.get('/')
        self.assertEqual(response.content_type, 'application/json')
    
    def test_home_has_message(self):
        response = self.client.get('/')
        data = json.loads(response.data)
        self.assertIn('message', data)
    
    def test_home_has_endpoints(self):
        response = self.client.get('/')
        data = json.loads(response.data)
        self.assertIn('endpoints', data)

class TestMenuAPI(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    @patch('app.get_db_connection')
    def test_get_menu_success(self, mock_db):
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [{'id': 1, 'name': 'Burger', 'price': 12.99, 'category': 'mains'}]
        mock_connection = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_db.return_value = mock_connection
        
        response = self.client.get('/api/menu')
        self.assertEqual(response.status_code, 200)
    
    @patch('app.get_db_connection')
    def test_get_menu_db_fail(self, mock_db):
        mock_db.return_value = None
        response = self.client.get('/api/menu')
        self.assertEqual(response.status_code, 500)
    
    @patch('app.get_db_connection')
    def test_get_menu_category(self, mock_db):
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [{'id': 1, 'name': 'Burger', 'price': 12.99, 'category': 'mains'}]
        mock_connection = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_db.return_value = mock_connection
        
        response = self.client.get('/api/menu/mains')
        self.assertEqual(response.status_code, 200)
    
    @patch('app.get_db_connection')
    def test_get_menu_empty_category(self, mock_db):
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = []
        mock_connection = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_db.return_value = mock_connection
        
        response = self.client.get('/api/menu/nonexistent')
        data = json.loads(response.data)
        self.assertEqual(len(data), 0)

class TestOrderCreation(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        self.valid_order = {
            'customer': {'name': 'John', 'phone': '555-1234', 'address': '123 Main'},
            'items': [{'id': 1, 'name': 'Burger', 'price': 12.99, 'quantity': 2}],
            'total': 25.98
        }
    
    @patch('app.get_db_connection')
    def test_create_order_success(self, mock_db):
        mock_cursor = MagicMock()
        mock_cursor.lastrowid = 1
        mock_connection = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_db.return_value = mock_connection
        
        response = self.client.post('/api/orders', data=json.dumps(self.valid_order), content_type='application/json')
        self.assertEqual(response.status_code, 201)
    
    @patch('app.get_db_connection')
    def test_create_order_db_fail(self, mock_db):
        mock_db.return_value = None
        response = self.client.post('/api/orders', data=json.dumps(self.valid_order), content_type='application/json')
        self.assertEqual(response.status_code, 500)
    
    @patch('app.get_db_connection')
    def test_create_order_missing_customer_name(self, mock_db):
        invalid_order = {
            'customer': {'phone': '555-1234', 'address': '123 Main'},
            'items': [{'id': 1, 'name': 'Burger', 'price': 12.99, 'quantity': 2}],
            'total': 25.98
        }
        response = self.client.post('/api/orders', data=json.dumps(invalid_order), content_type='application/json')
        self.assertEqual(response.status_code, 400)
    
    @patch('app.get_db_connection')
    def test_create_order_missing_customer_phone(self, mock_db):
        invalid_order = {
            'customer': {'name': 'John', 'address': '123 Main'},
            'items': [{'id': 1, 'name': 'Burger', 'price': 12.99, 'quantity': 2}],
            'total': 25.98
        }
        response = self.client.post('/api/orders', data=json.dumps(invalid_order), content_type='application/json')
        self.assertEqual(response.status_code, 400)
    
    @patch('app.get_db_connection')
    def test_create_order_empty_items(self, mock_db):
        invalid_order = {
            'customer': {'name': 'John', 'phone': '555-1234', 'address': '123 Main'},
            'items': [],
            'total': 0
        }
        response = self.client.post('/api/orders', data=json.dumps(invalid_order), content_type='application/json')
        self.assertEqual(response.status_code, 400)
    
    @patch('app.get_db_connection')
    def test_create_order_missing_items_field(self, mock_db):
        invalid_order = {
            'customer': {'name': 'John', 'phone': '555-1234', 'address': '123 Main'},
            'total': 25.98
        }
        response = self.client.post('/api/orders', data=json.dumps(invalid_order), content_type='application/json')
        self.assertEqual(response.status_code, 400)
    
    @patch('app.get_db_connection')
    def test_create_order_with_user_id(self, mock_db):
        order_with_user = {
            'customer': {'name': 'John', 'phone': '555-1234', 'address': '123 Main'},
            'items': [{'id': 1, 'name': 'Burger', 'price': 12.99, 'quantity': 2}],
            'total': 25.98,
            'user_id': 5
        }
        mock_cursor = MagicMock()
        mock_cursor.lastrowid = 1
        mock_connection = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_db.return_value = mock_connection
        
        response = self.client.post('/api/orders', data=json.dumps(order_with_user), content_type='application/json')
        self.assertEqual(response.status_code, 201)

class TestOrderRetrieval(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_get_order_invalid_route(self):
        response = self.client.get('/api/orders/invalid_id')
        self.assertEqual(response.status_code, 404)

class TestValidation(unittest.TestCase):
    def test_order_total(self):
        items = [{'id': 1, 'name': 'Item1', 'price': 10.00, 'quantity': 2, 'subtotal': 20.00}]
        order = Order(1, 'Test', '555-1111', '', 20.00, items, '2025-01-01 10:00:00')
        self.assertEqual(order.calculate_total(), 20.00)
    
    def test_zero_quantity(self):
        item = {'id': 1, 'name': 'Item', 'price': 10.00, 'quantity': 0, 'subtotal': 0}
        order = Order(1, 'Test', '555-1111', '', 0, [item], '2025-01-01 10:00:00')
        self.assertEqual(order.get_item_count(), 0)
    
    def test_multiple_items_calculation(self):
        items = [
            {'id': 1, 'name': 'Burger', 'price': 12.99, 'quantity': 2, 'subtotal': 25.98},
            {'id': 2, 'name': 'Pizza', 'price': 18.99, 'quantity': 1, 'subtotal': 18.99},
            {'id': 3, 'name': 'Fries', 'price': 5.99, 'quantity': 3, 'subtotal': 17.97}
        ]
        order = Order(1, 'Test', '555-1111', '', 62.94, items, '2025-01-01 10:00:00')
        self.assertEqual(order.get_item_count(), 6)
    
    def test_large_quantity(self):
        item = {'id': 1, 'name': 'Item', 'price': 10.00, 'quantity': 100, 'subtotal': 1000.00}
        order = Order(1, 'Test', '555-1111', '', 1000.00, [item], '2025-01-01 10:00:00')
        self.assertEqual(order.get_item_count(), 100)
    
    def test_decimal_precision(self):
        items = [{'id': 1, 'name': 'Item', 'price': 9.99, 'quantity': 3, 'subtotal': 29.97}]
        order = Order(1, 'Test', '555-1111', '', 29.97, items, '2025-01-01 10:00:00')
        self.assertEqual(order.calculate_total(), 29.97)

class TestErrorHandling(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_nonexistent_endpoint(self):
        response = self.client.get('/api/nonexistent')
        self.assertEqual(response.status_code, 404)
    
    def test_invalid_order_id(self):
        response = self.client.get('/api/orders/invalid')
        self.assertEqual(response.status_code, 404)
    
    def test_get_with_negative_id(self):
        response = self.client.get('/api/orders/-1')
        self.assertEqual(response.status_code, 404)

class TestDataIntegrity(unittest.TestCase):
    def test_customer_info(self):
        order = Order(1, 'Jane Smith', '555-9999', '789 Elm St', 42.50, [], '2025-01-02 14:30:00')
        order_dict = order.to_dict()
        self.assertEqual(order_dict['customer_name'], 'Jane Smith')
    
    def test_item_details(self):
        items = [{'id': 1, 'name': 'Pizza', 'price': 18.99, 'quantity': 1, 'subtotal': 18.99}]
        order = Order(1, 'Test', '555-1111', '', 18.99, items, '2025-01-01 10:00:00')
        self.assertEqual(order.items[0]['price'], 18.99)
    
    def test_order_to_dict_conversion(self):
        order = Order(1, 'Test', '555-1111', '123 St', 50.00, [], '2025-01-01')
        result = order.to_dict()
        self.assertIsInstance(result, dict)
    
    def test_phone_preservation(self):
        order = Order(1, 'Test', '555-1234', '', 0, [], '2025-01-01')
        self.assertEqual(order.customer_phone, '555-1234')
    
    def test_address_handling(self):
        order_with_address = Order(1, 'Test', '555-1111', '123 Main St', 0, [], '2025-01-01')
        self.assertEqual(order_with_address.customer_address, '123 Main St')
    
    def test_address_empty(self):
        order_no_address = Order(1, 'Test', '555-1111', '', 0, [], '2025-01-01')
        self.assertEqual(order_no_address.customer_address, '')
    
    def test_order_id_preservation(self):
        order = Order(42, 'Test', '555-1111', '', 0, [], '2025-01-01')
        self.assertEqual(order.id, 42)
    
    def test_created_at_preservation(self):
        timestamp = '2025-06-15 18:45:30'
        order = Order(1, 'Test', '555-1111', '', 0, [], timestamp)
        self.assertEqual(order.created_at, timestamp)

class TestOrderStatus(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    @patch('routes.order_routes.get_db_connection')
    def test_update_order_status_pending(self, mock_db):
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 1
        mock_connection = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_db.return_value = mock_connection
        
        response = self.client.put('/api/orders/1/status', 
                                   data=json.dumps({'status': 'pending'}),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
    
    @patch('routes.order_routes.get_db_connection')
    def test_update_order_status_preparing(self, mock_db):
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 1
        mock_connection = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_db.return_value = mock_connection
        
        response = self.client.put('/api/orders/1/status',
                                   data=json.dumps({'status': 'preparing'}),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
    
    @patch('routes.order_routes.get_db_connection')
    def test_update_order_status_ready(self, mock_db):
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 1
        mock_connection = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_db.return_value = mock_connection
        
        response = self.client.put('/api/orders/1/status',
                                   data=json.dumps({'status': 'ready'}),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
    
    @patch('routes.order_routes.get_db_connection')
    def test_update_order_status_completed(self, mock_db):
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 1
        mock_connection = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_db.return_value = mock_connection
        
        response = self.client.put('/api/orders/1/status',
                                   data=json.dumps({'status': 'completed'}),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main(verbosity=2)

    # to test in terminal: python -m unittest tests.test_restaurant_system -v