"""
Authentication utilities for AI School backend
"""

import bcrypt
import jwt
import datetime
from functools import wraps
from flask import request, jsonify, current_app
from typing import Optional, Dict, Any

def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt
    
    Args:
        password (str): Plain text password
        
    Returns:
        str: Hashed password
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash
    
    Args:
        password (str): Plain text password
        hashed_password (str): Hashed password
        
    Returns:
        bool: True if password matches, False otherwise
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def generate_jwt_token(user_id: str, email: str, 
                      secret_key: str, expiration_hours: int = 24) -> str:
    """
    Generate JWT token for authenticated user
    
    Args:
        user_id (str): User ID
        email (str): User email
        secret_key (str): JWT secret key
        expiration_hours (int): Token expiration time in hours
        
    Returns:
        str: JWT token
    """
    payload = {
        'user_id': user_id,
        'email': email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=expiration_hours),
        'iat': datetime.datetime.utcnow()
    }
    return jwt.encode(payload, secret_key, algorithm='HS256')

def verify_jwt_token(token: str, secret_key: str) -> Optional[Dict[str, Any]]:
    """
    Verify and decode JWT token
    
    Args:
        token (str): JWT token
        secret_key (str): JWT secret key
        
    Returns:
        Optional[Dict]: Decoded payload if valid, None otherwise
    """
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def validate_email(email: str) -> bool:
    """
    Basic email validation
    
    Args:
        email (str): Email address to validate
        
    Returns:
        bool: True if email format is valid, False otherwise
    """
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password_strength(password: str) -> Dict[str, Any]:
    """
    Validate password strength
    
    Args:
        password (str): Password to validate
        
    Returns:
        Dict: Validation result with is_valid and messages
    """
    result = {
        'is_valid': True,
        'messages': []
    }
    
    if len(password) < 6:
        result['is_valid'] = False
        result['messages'].append('Password must be at least 6 characters long')
    
    if len(password) > 128:
        result['is_valid'] = False
        result['messages'].append('Password must be less than 128 characters')
    
    # Check for at least one letter
    if not any(c.isalpha() for c in password):
        result['messages'].append('Password should contain at least one letter')
    
    # Check for at least one digit
    if not any(c.isdigit() for c in password):
        result['messages'].append('Password should contain at least one digit')
    
    return result

def token_required(f):
    """
    Decorator to require JWT token for protected routes
    
    Args:
        f: Function to decorate
        
    Returns:
        Decorated function
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({'error': 'Authorization token required'}), 401
        
        try:
            payload = verify_jwt_token(token, current_app.config['SECRET_KEY'])
            if not payload:
                return jsonify({'error': 'Invalid or expired token'}), 401
            
            # Add user info to request context
            request.current_user = payload
            
        except Exception as e:
            return jsonify({'error': 'Token verification failed'}), 401
        
        return f(*args, **kwargs)
    
    return decorated

def sanitize_input(data: str) -> str:
    """
    Basic input sanitization
    
    Args:
        data (str): Input data to sanitize
        
    Returns:
        str: Sanitized data
    """
    if not isinstance(data, str):
        return str(data)
    
    # Remove leading/trailing whitespace
    data = data.strip()
    
    # Basic HTML tag removal (simple approach)
    import re
    data = re.sub(r'<[^>]+>', '', data)
    
    return data
