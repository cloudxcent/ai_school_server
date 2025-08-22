"""
User model for Azure Table Storage
"""

from datetime import datetime
import uuid
from typing import Dict, Optional

class User:
    """User model class"""
    
    def __init__(self, email: str, password_hash: str, full_name: str, 
                 phone_number: str = "", user_id: str = None):
        self.user_id = user_id or str(uuid.uuid4())
        self.email = email.lower().strip()
        self.password_hash = password_hash
        self.full_name = full_name.strip()
        self.phone_number = phone_number.strip()
        self.created_at = datetime.utcnow().isoformat()
        self.last_login = None
        self.is_active = True
    
    def to_dict(self) -> Dict:
        """Convert user object to dictionary for Azure Table Storage"""
        return {
            "PartitionKey": self.email,  # Using email as partition key
            "RowKey": self.user_id,      # Using UUID as row key
            "email": self.email,
            "password_hash": self.password_hash,
            "full_name": self.full_name,
            "phone_number": self.phone_number,
            "created_at": self.created_at,
            "last_login": self.last_login,
            "is_active": self.is_active
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'User':
        """Create user object from Azure Table Storage entity"""
        user = cls(
            email=data['email'],
            password_hash=data['password_hash'],
            full_name=data['full_name'],
            phone_number=data.get('phone_number', ''),
            user_id=data['RowKey']
        )
        user.created_at = data.get('created_at')
        user.last_login = data.get('last_login')
        user.is_active = data.get('is_active', True)
        return user
    
    def to_public_dict(self) -> Dict:
        """Convert user object to public dictionary (without sensitive data)"""
        return {
            "id": self.user_id,
            "email": self.email,
            "full_name": self.full_name,
            "phone_number": self.phone_number,
            "created_at": self.created_at,
            "last_login": self.last_login,
            "is_active": self.is_active
        }
    
    def update_last_login(self):
        """Update last login timestamp"""
        self.last_login = datetime.utcnow().isoformat()
    
    def deactivate(self):
        """Deactivate user account"""
        self.is_active = False
    
    def activate(self):
        """Activate user account"""
        self.is_active = True
