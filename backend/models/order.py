# backend/models/order.py - Order model

class Order:
    """Order model for managing order data"""
    
    def __init__(self, order_id, customer_name, customer_phone, customer_address, total_amount, items, created_at):
        self.id = order_id
        self.customer_name = customer_name
        self.customer_phone = customer_phone
        self.customer_address = customer_address
        self.total_amount = total_amount
        self.items = items
        self.created_at = created_at
    
    def to_dict(self):
        """Convert order to dictionary"""
        return {
            'id': self.id,
            'customer_name': self.customer_name,
            'customer_phone': self.customer_phone,
            'customer_address': self.customer_address,
            'total_amount': float(self.total_amount),
            'items': self.items,
            'created_at': str(self.created_at)
        }
    
    def get_item_count(self):
        """Get total number of items in order"""
        total = 0
        for item in self.items:
            total += item.get('quantity', 0)
        return total
    
    def calculate_total(self):
        """Calculate total from items"""
        total = 0
        for item in self.items:
            total += item.get('subtotal', 0)
        return total