# backend/models/user.py - User model for authentication

import hashlib
import re

class User:
    """User model for managing user data and authentication"""
    
    def __init__(self, user_id, email, phone, password_hash, first_name, last_name, created_at):
        self.id = user_id
        self.email = email
        self.phone = phone
        self.password_hash = password_hash
        self.first_name = first_name
        self.last_name = last_name
        self.created_at = created_at
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'email': self.email,
            'phone': self.phone,
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
    
    @staticmethod
    def validate_phone(phone):
        """Validate phone number format"""
        # Remove common separators
        cleaned = re.sub(r'[\s\-().]', '', phone)
        
        # Check if it's 10+ digits
        if not cleaned.isdigit() or len(cleaned) < 10:
            return False
        
        return True
    
    def get_full_name(self):
        """Get user's full name"""
        return f"{self.first_name} {self.last_name}".strip()