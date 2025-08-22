"""
AI School Backend Server
Main Flask application for user authentication with Azure Table Storage
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import bcrypt
import jwt
import datetime
import os
from dotenv import load_dotenv
from azure.data.tables import TableServiceClient, TableClient
from azure.core.exceptions import ResourceExistsError, ResourceNotFoundError
import uuid

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-change-this')
AZURE_STORAGE_CONNECTION_STRING = os.getenv('AZURE_STORAGE_CONNECTION_STRING')

if not AZURE_STORAGE_CONNECTION_STRING:
    raise ValueError("AZURE_STORAGE_CONNECTION_STRING environment variable is required")

# Azure Table Storage setup
table_service_client = TableServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
users_table_name = "users"
kids_profiles_table_name = "kidsprofiles"

# Create users table if it doesn't exist
try:
    table_service_client.create_table(users_table_name)
    print(f"✓ Table '{users_table_name}' created or already exists")
except ResourceExistsError:
    print(f"✓ Table '{users_table_name}' already exists")

# Create kids profiles table if it doesn't exist
try:
    table_service_client.create_table(kids_profiles_table_name)
    print(f"✓ Table '{kids_profiles_table_name}' created or already exists")
except ResourceExistsError:
    print(f"✓ Table '{kids_profiles_table_name}' already exists")

users_table_client = TableClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING, users_table_name)
kids_profiles_table_client = TableClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING, kids_profiles_table_name)

# Helper functions
def hash_password(password):
    """Hash a password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password, hashed_password):
    """Verify a password against its hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def generate_jwt_token(user_id, email):
    """Generate JWT token for authenticated user"""
    payload = {
        'user_id': user_id,
        'email': email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24),
        'iat': datetime.datetime.utcnow()
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

def verify_jwt_token(token):
    """Verify and decode JWT token"""
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def get_user_by_email(email):
    """Get user from Azure Table Storage by email"""
    try:
        # Use email as partition key for efficient querying
        entities = users_table_client.query_entities(f"PartitionKey eq '{email}'")
        for entity in entities:
            return entity
        return None
    except Exception as e:
        print(f"Error querying user: {e}")
        return None

def create_user(email, password, full_name, phone_number=None):
    """Create a new user in Azure Table Storage"""
    try:
        user_id = str(uuid.uuid4())
        user_entity = {
            "PartitionKey": email,  # Using email as partition key
            "RowKey": user_id,      # Using UUID as row key
            "email": email,
            "password_hash": hash_password(password),
            "full_name": full_name,
            "phone_number": phone_number or "",
            "created_at": datetime.datetime.utcnow().isoformat(),
            "is_active": True,
            "last_login": None
        }
        
        users_table_client.create_entity(user_entity)
        return user_entity
    except Exception as e:
        print(f"Error creating user: {e}")
        return None

def update_last_login(email):
    """Update user's last login timestamp"""
    try:
        user = get_user_by_email(email)
        if user:
            user['last_login'] = datetime.datetime.utcnow().isoformat()
            users_table_client.update_entity(user, mode='merge')
    except Exception as e:
        print(f"Error updating last login: {e}")

# Kids Profile Functions

def create_kid_profile(user_id, name, age, grade=None, avatar=None, learning_goals=None):
    """Create a new kid profile for a user"""
    try:
        profile_id = str(uuid.uuid4())
        kid_profile = {
            "PartitionKey": user_id,  # Using user_id as partition key
            "RowKey": profile_id,     # Using UUID as row key
            "user_id": user_id,
            "name": name,
            "age": age,
            "grade": grade or "",
            "avatar": avatar or "default",
            "learning_goals": learning_goals or "",
            "created_at": datetime.datetime.utcnow().isoformat(),
            "last_activity": None,
            "progress": "{}",  # JSON string to store progress data
            "is_active": True
        }
        
        kids_profiles_table_client.create_entity(kid_profile)
        return kid_profile
    except Exception as e:
        print(f"Error creating kid profile: {e}")
        return None

def get_kids_profiles_by_user(user_id):
    """Get all kids profiles for a specific user"""
    try:
        entities = kids_profiles_table_client.query_entities(f"PartitionKey eq '{user_id}' and is_active eq true")
        profiles = []
        for entity in entities:
            profiles.append({
                'id': entity['RowKey'],
                'name': entity['name'],
                'age': entity['age'],
                'grade': entity['grade'],
                'avatar': entity['avatar'],
                'learning_goals': entity['learning_goals'],
                'created_at': entity['created_at'],
                'last_activity': entity.get('last_activity'),
                'progress': entity.get('progress', '{}')
            })
        return profiles
    except Exception as e:
        print(f"Error getting kids profiles: {e}")
        return []

def get_kid_profile_by_id(user_id, profile_id):
    """Get a specific kid profile by ID"""
    try:
        entity = kids_profiles_table_client.get_entity(partition_key=user_id, row_key=profile_id)
        if entity and entity.get('is_active', True):
            return {
                'id': entity['RowKey'],
                'name': entity['name'],
                'age': entity['age'],
                'grade': entity['grade'],
                'avatar': entity['avatar'],
                'learning_goals': entity['learning_goals'],
                'created_at': entity['created_at'],
                'last_activity': entity.get('last_activity'),
                'progress': entity.get('progress', '{}')
            }
        return None
    except ResourceNotFoundError:
        return None
    except Exception as e:
        print(f"Error getting kid profile: {e}")
        return None

def update_kid_profile(user_id, profile_id, update_data):
    """Update a kid profile"""
    try:
        entity = kids_profiles_table_client.get_entity(partition_key=user_id, row_key=profile_id)
        if entity and entity.get('is_active', True):
            # Update allowed fields
            allowed_fields = ['name', 'age', 'grade', 'avatar', 'learning_goals', 'progress']
            for field in allowed_fields:
                if field in update_data:
                    entity[field] = update_data[field]
            
            kids_profiles_table_client.update_entity(entity, mode='merge')
            return True
        return False
    except Exception as e:
        print(f"Error updating kid profile: {e}")
        return False

def delete_kid_profile(user_id, profile_id):
    """Soft delete a kid profile (mark as inactive)"""
    try:
        entity = kids_profiles_table_client.get_entity(partition_key=user_id, row_key=profile_id)
        if entity:
            entity['is_active'] = False
            kids_profiles_table_client.update_entity(entity, mode='merge')
            return True
        return False
    except Exception as e:
        print(f"Error deleting kid profile: {e}")
        return False

# API Routes

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'AI School Backend Server is running',
        'timestamp': datetime.datetime.utcnow().isoformat()
    }), 200

@app.route('/api/auth/register', methods=['POST'])
def register():
    """User registration endpoint"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['email', 'password', 'full_name']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        email = data['email'].lower().strip()
        password = data['password']
        full_name = data['full_name'].strip()
        phone_number = data.get('phone_number', '').strip()
        
        # Validate email format (basic validation)
        if '@' not in email or '.' not in email:
            return jsonify({'error': 'Invalid email format'}), 400
        
        # Validate password strength
        if len(password) < 6:
            return jsonify({'error': 'Password must be at least 6 characters long'}), 400
        
        # Check if user already exists
        existing_user = get_user_by_email(email)
        if existing_user:
            return jsonify({'error': 'User with this email already exists'}), 409
        
        # Create new user
        user = create_user(email, password, full_name, phone_number)
        if not user:
            return jsonify({'error': 'Failed to create user'}), 500
        
        # Generate JWT token
        token = generate_jwt_token(user['RowKey'], email)
        
        return jsonify({
            'message': 'User registered successfully',
            'token': token,
            'user': {
                'id': user['RowKey'],
                'email': user['email'],
                'full_name': user['full_name'],
                'phone_number': user['phone_number'],
                'created_at': user['created_at']
            }
        }), 201
        
    except Exception as e:
        print(f"Registration error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    """User login endpoint"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password are required'}), 400
        
        email = data['email'].lower().strip()
        password = data['password']
        
        # Get user from database
        user = get_user_by_email(email)
        if not user:
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Verify password
        if not verify_password(password, user['password_hash']):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Check if user is active
        if not user.get('is_active', True):
            return jsonify({'error': 'Account is deactivated'}), 401
        
        # Update last login
        update_last_login(email)
        
        # Generate JWT token
        token = generate_jwt_token(user['RowKey'], email)
        
        return jsonify({
            'message': 'Login successful',
            'token': token,
            'user': {
                'id': user['RowKey'],
                'email': user['email'],
                'full_name': user['full_name'],
                'phone_number': user['phone_number'],
                'last_login': user.get('last_login')
            }
        }), 200
        
    except Exception as e:
        print(f"Login error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/auth/user', methods=['GET'])
def get_user_profile():
    """Get user basic profile (authenticated endpoint)"""
    try:
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Authorization token required'}), 401
        
        token = auth_header.split(' ')[1]
        payload = verify_jwt_token(token)
        
        if not payload:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        # Get user from database
        user = get_user_by_email(payload['email'])
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'user': {
                'id': user['RowKey'],
                'email': user['email'],
                'full_name': user['full_name'],
                'phone_number': user['phone_number'],
                'created_at': user['created_at'],
                'last_login': user.get('last_login')
            }
        }), 200
        
    except Exception as e:
        print(f"User profile error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

# Kids Profile Endpoints

@app.route('/api/profiles', methods=['GET'])
def get_kids_profiles():
    """Get all kids profiles for the authenticated user"""
    try:
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Authorization token required'}), 401
        
        token = auth_header.split(' ')[1]
        payload = verify_jwt_token(token)
        
        if not payload:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        # Get kids profiles for this user
        profiles = get_kids_profiles_by_user(payload['user_id'])
        
        return jsonify({
            'profiles': profiles,
            'count': len(profiles)
        }), 200
        
    except Exception as e:
        print(f"Get profiles error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/profiles', methods=['POST'])
def create_kids_profile():
    """Create a new kid profile"""
    try:
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Authorization token required'}), 401
        
        token = auth_header.split(' ')[1]
        payload = verify_jwt_token(token)
        
        if not payload:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        data = request.get_json()
        
        # Validate required fields
        if not data.get('name') or not data.get('age'):
            return jsonify({'error': 'Name and age are required'}), 400
        
        name = data['name'].strip()
        age = data['age']
        grade = data.get('grade', '').strip()
        avatar = data.get('avatar', 'default')
        learning_goals = data.get('learning_goals', '').strip()
        
        # Validate age
        try:
            age = int(age)
            if age < 3 or age > 18:
                return jsonify({'error': 'Age must be between 3 and 18'}), 400
        except ValueError:
            return jsonify({'error': 'Age must be a valid number'}), 400
        
        # Create kid profile
        profile = create_kid_profile(payload['user_id'], name, age, grade, avatar, learning_goals)
        if not profile:
            return jsonify({'error': 'Failed to create profile'}), 500
        
        return jsonify({
            'message': 'Kid profile created successfully',
            'profile': {
                'id': profile['RowKey'],
                'name': profile['name'],
                'age': profile['age'],
                'grade': profile['grade'],
                'avatar': profile['avatar'],
                'learning_goals': profile['learning_goals'],
                'created_at': profile['created_at']
            }
        }), 201
        
    except Exception as e:
        print(f"Create profile error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/profiles/<profile_id>', methods=['GET'])
def get_kid_profile(profile_id):
    """Get a specific kid profile"""
    try:
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Authorization token required'}), 401
        
        token = auth_header.split(' ')[1]
        payload = verify_jwt_token(token)
        
        if not payload:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        # Get specific kid profile
        profile = get_kid_profile_by_id(payload['user_id'], profile_id)
        if not profile:
            return jsonify({'error': 'Profile not found'}), 404
        
        return jsonify({'profile': profile}), 200
        
    except Exception as e:
        print(f"Get profile error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/profiles/<profile_id>', methods=['PUT'])
def update_kids_profile(profile_id):
    """Update a kid profile"""
    try:
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Authorization token required'}), 401
        
        token = auth_header.split(' ')[1]
        payload = verify_jwt_token(token)
        
        if not payload:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        data = request.get_json()
        
        # Validate age if provided
        if 'age' in data:
            try:
                age = int(data['age'])
                if age < 3 or age > 18:
                    return jsonify({'error': 'Age must be between 3 and 18'}), 400
                data['age'] = age
            except ValueError:
                return jsonify({'error': 'Age must be a valid number'}), 400
        
        # Update profile
        success = update_kid_profile(payload['user_id'], profile_id, data)
        if not success:
            return jsonify({'error': 'Profile not found or update failed'}), 404
        
        # Get updated profile
        updated_profile = get_kid_profile_by_id(payload['user_id'], profile_id)
        
        return jsonify({
            'message': 'Profile updated successfully',
            'profile': updated_profile
        }), 200
        
    except Exception as e:
        print(f"Update profile error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/profiles/<profile_id>', methods=['DELETE'])
def delete_kids_profile(profile_id):
    """Delete a kid profile"""
    try:
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Authorization token required'}), 401
        
        token = auth_header.split(' ')[1]
        payload = verify_jwt_token(token)
        
        if not payload:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        # Delete profile
        success = delete_kid_profile(payload['user_id'], profile_id)
        if not success:
            return jsonify({'error': 'Profile not found'}), 404
        
        return jsonify({'message': 'Profile deleted successfully'}), 200
        
    except Exception as e:
        print(f"Delete profile error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    """User logout endpoint"""
    # Since we're using stateless JWT tokens, logout is handled client-side
    # The client should delete the token from storage
    return jsonify({'message': 'Logged out successfully'}), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("🚀 Starting AI School Backend Server...")
    print("📚 Endpoints available:")
    print("   GET  /api/health")
    print("   POST /api/auth/register")
    print("   POST /api/auth/login")
    print("   GET  /api/auth/user")
    print("   POST /api/auth/logout")
    print("   📋 Kids Profiles:")
    print("   GET  /api/profiles")
    print("   POST /api/profiles")
    print("   GET  /api/profiles/<id>")
    print("   PUT  /api/profiles/<id>")
    print("   DELETE /api/profiles/<id>")
    print()
    
    # Run the application
    app.run(debug=True, host='0.0.0.0', port=5000)
