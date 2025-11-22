# backend/models/admin.py - Admin model for authentication

import hashlib
import re

class Admin:
    """Admin model for managing admin data and authentication"""
    
    def __init__(self, admin_id, email, password_hash, first_name, last_name, created_at):
        self.id = admin_id
        self.email = email
        self.password_hash = password_hash
        self.first_name = first_name
        self.last_name = last_name
        self.created_at = created_at
    
    def to_dict(self):
        """Convert admin to dictionary"""
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'created_at': str(self.created_at)
        }
    
    @staticmethod
    def hash_password(password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def validate_email(email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_password(password):
        """Validate password strength"""
        # At least 6 characters
        if len(password) < 6:
            return False, "Password must be at least 6 characters"
        
        # Check for at least one number
        if not any(char.isdigit() for char in password):
            return False, "Password must contain at least one number"
        
        return True, "Password is valid"
    
    def get_full_name(self):
        """Get admin's full name"""
        return f"{self.first_name} {self.last_name}".strip()