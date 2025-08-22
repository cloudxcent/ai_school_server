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
import logging
import logging.handlers
from dotenv import load_dotenv
from azure.data.tables import TableServiceClient, TableClient
from azure.core.exceptions import ResourceExistsError, ResourceNotFoundError
import uuid
import traceback
import sys

# Load environment variables
load_dotenv()

# Create logs directory if it doesn't exist
logs_dir = os.path.join(os.path.dirname(__file__), 'logs')
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

# Setup logging configuration for session-based logging
def setup_session_logging():
    """Setup logging with a unique file for each session"""
    # Generate unique session ID based on timestamp
    session_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    session_id = f"session_{session_timestamp}_{os.getpid()}"
    
    # Create log filename with session ID
    log_filename = os.path.join(logs_dir, f"ai_school_{session_id}.log")
    
    # Configure root logger
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
        handlers=[
            logging.FileHandler(log_filename, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)  # Also log to console
        ]
    )
    
    # Create application logger
    app_logger = logging.getLogger('ai_school')
    app_logger.setLevel(logging.DEBUG)
    
    # Log session start
    app_logger.info(f"=== AI School Backend Server Session Started ===")
    app_logger.info(f"Session ID: {session_id}")
    app_logger.info(f"Log file: {log_filename}")
    app_logger.info(f"Process ID: {os.getpid()}")
    app_logger.info(f"Python version: {sys.version}")
    
    return app_logger, log_filename

# Initialize session logging
logger, current_log_file = setup_session_logging()

app = Flask(__name__)
CORS(app)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-change-this')
AZURE_STORAGE_CONNECTION_STRING = os.getenv('AZURE_STORAGE_CONNECTION_STRING')

logger.info("Starting application configuration...")
logger.info(f"SECRET_KEY configured: {'Yes' if app.config['SECRET_KEY'] != 'your-secret-key-change-this' else 'No (using default)'}")
logger.info(f"AZURE_STORAGE_CONNECTION_STRING configured: {'Yes' if AZURE_STORAGE_CONNECTION_STRING else 'No'}")

if not AZURE_STORAGE_CONNECTION_STRING:
    logger.error("AZURE_STORAGE_CONNECTION_STRING environment variable is required")
    raise ValueError("AZURE_STORAGE_CONNECTION_STRING environment variable is required")

# Azure Table Storage setup
logger.info("Initializing Azure Table Storage...")
table_service_client = TableServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
users_table_name = "users"
kids_profiles_table_name = "kidsprofiles"

logger.info(f"Setting up table: {users_table_name}")
# Create users table if it doesn't exist
try:
    table_service_client.create_table(users_table_name)
    logger.info(f"✓ Table '{users_table_name}' created or already exists")
    print(f"✓ Table '{users_table_name}' created or already exists")
except ResourceExistsError:
    logger.info(f"✓ Table '{users_table_name}' already exists")
    print(f"✓ Table '{users_table_name}' already exists")
except Exception as e:
    logger.error(f"Failed to create/access table '{users_table_name}': {e}")
    logger.error(f"Traceback: {traceback.format_exc()}")
    raise

logger.info(f"Setting up table: {kids_profiles_table_name}")
# Create kids profiles table if it doesn't exist
try:
    table_service_client.create_table(kids_profiles_table_name)
    logger.info(f"✓ Table '{kids_profiles_table_name}' created or already exists")
    print(f"✓ Table '{kids_profiles_table_name}' created or already exists")
except ResourceExistsError:
    logger.info(f"✓ Table '{kids_profiles_table_name}' already exists")
    print(f"✓ Table '{kids_profiles_table_name}' already exists")
except Exception as e:
    logger.error(f"Failed to create/access table '{kids_profiles_table_name}': {e}")
    logger.error(f"Traceback: {traceback.format_exc()}")
    raise

logger.info("Creating table clients...")
users_table_client = TableClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING, users_table_name)
kids_profiles_table_client = TableClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING, kids_profiles_table_name)
logger.info("Azure Table Storage setup completed successfully")

# Helper functions
def hash_password(password):
    """Hash a password using bcrypt"""
    logger.debug("Hashing password")
    try:
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        logger.debug("Password hashed successfully")
        return hashed
    except Exception as e:
        logger.error(f"Error hashing password: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise

def verify_password(password, hashed_password):
    """Verify a password against its hash"""
    logger.debug("Verifying password")
    try:
        result = bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
        logger.debug(f"Password verification result: {result}")
        return result
    except Exception as e:
        logger.error(f"Error verifying password: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return False

def generate_jwt_token(user_id, email):
    """Generate JWT token for authenticated user"""
    logger.debug(f"Generating JWT token for user: {email}")
    try:
        payload = {
            'user_id': user_id,
            'email': email,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24),
            'iat': datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
        logger.info(f"JWT token generated successfully for user: {email}")
        return token
    except Exception as e:
        logger.error(f"Error generating JWT token for user {email}: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise

def verify_jwt_token(token):
    """Verify and decode JWT token"""
    logger.debug("Verifying JWT token")
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        logger.debug(f"JWT token verified successfully for user: {payload.get('email', 'unknown')}")
        return payload
    except jwt.ExpiredSignatureError:
        logger.warning("JWT token verification failed: Token expired")
        return None
    except jwt.InvalidTokenError:
        logger.warning("JWT token verification failed: Invalid token")
        return None
    except Exception as e:
        logger.error(f"Error verifying JWT token: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return None

def get_user_by_email(email):
    """Get user from Azure Table Storage by email"""
    logger.debug(f"Querying user by email: {email}")
    try:
        # Use email as partition key for efficient querying
        entities = users_table_client.query_entities(f"PartitionKey eq '{email}'")
        for entity in entities:
            logger.info(f"User found: {email}")
            return entity
        logger.info(f"User not found: {email}")
        return None
    except Exception as e:
        logger.error(f"Error querying user {email}: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        print(f"Error querying user: {e}")
        return None

def create_user(email, password, full_name, phone_number=None):
    """Create a new user in Azure Table Storage"""
    logger.info(f"Creating new user: {email}")
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
        logger.info(f"User created successfully: {email} (ID: {user_id})")
        return user_entity
    except Exception as e:
        logger.error(f"Error creating user {email}: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        print(f"Error creating user: {e}")
        return None

def update_last_login(email):
    """Update user's last login timestamp"""
    logger.debug(f"Updating last login for user: {email}")
    try:
        user = get_user_by_email(email)
        if user:
            user['last_login'] = datetime.datetime.utcnow().isoformat()
            users_table_client.update_entity(user, mode='merge')
            logger.info(f"Last login updated for user: {email}")
    except Exception as e:
        logger.error(f"Error updating last login for user {email}: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        print(f"Error updating last login: {e}")

# Kids Profile Functions

def create_kid_profile(user_id, name, age, grade=None, avatar=None, learning_goals=None):
    """Create a new kid profile for a user"""
    logger.info(f"Creating kid profile for user {user_id}: {name}, age {age}")
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
        logger.info(f"Kid profile created successfully: {name} (ID: {profile_id})")
        return kid_profile
    except Exception as e:
        logger.error(f"Error creating kid profile for user {user_id}: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        print(f"Error creating kid profile: {e}")
        return None

def get_kids_profiles_by_user(user_id):
    """Get all kids profiles for a specific user"""
    logger.debug(f"Getting kids profiles for user: {user_id}")
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
        logger.info(f"Retrieved {len(profiles)} kids profiles for user: {user_id}")
        return profiles
    except Exception as e:
        logger.error(f"Error getting kids profiles for user {user_id}: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        print(f"Error getting kids profiles: {e}")
        return []

def get_kid_profile_by_id(user_id, profile_id):
    """Get a specific kid profile by ID"""
    logger.debug(f"Getting kid profile {profile_id} for user {user_id}")
    try:
        entity = kids_profiles_table_client.get_entity(partition_key=user_id, row_key=profile_id)
        if entity and entity.get('is_active', True):
            profile = {
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
            logger.info(f"Kid profile retrieved: {entity['name']} (ID: {profile_id})")
            return profile
        logger.warning(f"Kid profile not found or inactive: {profile_id}")
        return None
    except ResourceNotFoundError:
        logger.warning(f"Kid profile not found: {profile_id}")
        return None
    except Exception as e:
        logger.error(f"Error getting kid profile {profile_id}: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        print(f"Error getting kid profile: {e}")
        return None

def update_kid_profile(user_id, profile_id, update_data):
    """Update a kid profile"""
    logger.info(f"Updating kid profile {profile_id} for user {user_id}")
    logger.debug(f"Update data: {update_data}")
    try:
        entity = kids_profiles_table_client.get_entity(partition_key=user_id, row_key=profile_id)
        if entity and entity.get('is_active', True):
            # Update allowed fields
            allowed_fields = ['name', 'age', 'grade', 'avatar', 'learning_goals', 'progress']
            updated_fields = []
            for field in allowed_fields:
                if field in update_data:
                    old_value = entity.get(field)
                    entity[field] = update_data[field]
                    updated_fields.append(f"{field}: {old_value} -> {update_data[field]}")
            
            kids_profiles_table_client.update_entity(entity, mode='merge')
            logger.info(f"Kid profile updated successfully. Changes: {', '.join(updated_fields)}")
            return True
        logger.warning(f"Kid profile not found or inactive for update: {profile_id}")
        return False
    except Exception as e:
        logger.error(f"Error updating kid profile {profile_id}: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        print(f"Error updating kid profile: {e}")
        return False

def delete_kid_profile(user_id, profile_id):
    """Soft delete a kid profile (mark as inactive)"""
    logger.info(f"Deleting kid profile {profile_id} for user {user_id}")
    try:
        entity = kids_profiles_table_client.get_entity(partition_key=user_id, row_key=profile_id)
        if entity:
            profile_name = entity.get('name', 'Unknown')
            entity['is_active'] = False
            kids_profiles_table_client.update_entity(entity, mode='merge')
            logger.info(f"Kid profile deleted successfully: {profile_name} (ID: {profile_id})")
            return True
        logger.warning(f"Kid profile not found for deletion: {profile_id}")
        return False
    except Exception as e:
        logger.error(f"Error deleting kid profile {profile_id}: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        print(f"Error deleting kid profile: {e}")
        return False

# API Routes

# Request/Response logging middleware
@app.before_request
def log_request_info():
    """Log all incoming requests"""
    logger.info(f"=== INCOMING REQUEST ===")
    logger.info(f"Method: {request.method}")
    logger.info(f"URL: {request.url}")
    logger.info(f"Remote Address: {request.remote_addr}")
    logger.info(f"User Agent: {request.headers.get('User-Agent', 'Unknown')}")
    logger.info(f"Content Type: {request.headers.get('Content-Type', 'None')}")
    
    # Log headers (excluding sensitive ones)
    headers_to_log = {}
    for header, value in request.headers:
        if header.lower() not in ['authorization', 'cookie', 'x-api-key']:
            headers_to_log[header] = value
        else:
            headers_to_log[header] = '[REDACTED]'
    logger.debug(f"Headers: {headers_to_log}")
    
    # Log request body for POST/PUT requests (be careful with sensitive data)
    if request.method in ['POST', 'PUT'] and request.is_json:
        try:
            data = request.get_json()
            # Redact sensitive fields
            if isinstance(data, dict):
                safe_data = data.copy()
                sensitive_fields = ['password', 'token', 'secret']
                for field in sensitive_fields:
                    if field in safe_data:
                        safe_data[field] = '[REDACTED]'
                logger.debug(f"Request Body: {safe_data}")
        except Exception as e:
            logger.warning(f"Could not log request body: {e}")

@app.after_request
def log_response_info(response):
    """Log all outgoing responses"""
    logger.info(f"=== OUTGOING RESPONSE ===")
    logger.info(f"Status Code: {response.status_code}")
    logger.info(f"Content Type: {response.headers.get('Content-Type', 'None')}")
    
    # Log response size
    if response.content_length:
        logger.debug(f"Content Length: {response.content_length} bytes")
    
    # Log response body for non-successful requests or debug mode
    if response.status_code >= 400:
        try:
            if response.is_json:
                logger.debug(f"Error Response: {response.get_json()}")
        except Exception as e:
            logger.warning(f"Could not log error response: {e}")
    
    logger.info(f"Request completed with status: {response.status_code}")
    return response

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    logger.debug("Health check requested")
    response_data = {
        'status': 'healthy',
        'message': 'AI School Backend Server is running',
        'timestamp': datetime.datetime.utcnow().isoformat(),
        'log_file': current_log_file
    }
    logger.info("Health check completed successfully")
    return jsonify(response_data), 200

@app.route('/api/auth/register', methods=['POST'])
def register():
    """User registration endpoint"""
    logger.info("User registration attempt started")
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['email', 'password', 'full_name']
        for field in required_fields:
            if not data.get(field):
                logger.warning(f"Registration failed: Missing required field '{field}'")
                return jsonify({'error': f'{field} is required'}), 400
        
        email = data['email'].lower().strip()
        password = data['password']
        full_name = data['full_name'].strip()
        phone_number = data.get('phone_number', '').strip()
        
        logger.info(f"Registration attempt for email: {email}")
        
        # Validate email format (basic validation)
        if '@' not in email or '.' not in email:
            logger.warning(f"Registration failed: Invalid email format for {email}")
            return jsonify({'error': 'Invalid email format'}), 400
        
        # Validate password strength
        if len(password) < 6:
            logger.warning(f"Registration failed: Password too short for {email}")
            return jsonify({'error': 'Password must be at least 6 characters long'}), 400
        
        # Check if user already exists
        existing_user = get_user_by_email(email)
        if existing_user:
            logger.warning(f"Registration failed: User already exists with email {email}")
            return jsonify({'error': 'User with this email already exists'}), 409
        
        # Create new user
        user = create_user(email, password, full_name, phone_number)
        if not user:
            logger.error(f"Registration failed: Could not create user {email}")
            return jsonify({'error': 'Failed to create user'}), 500
        
        # Generate JWT token
        token = generate_jwt_token(user['RowKey'], email)
        
        logger.info(f"User registration completed successfully: {email}")
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
        logger.error(f"Registration error: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        print(f"Registration error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    """User login endpoint"""
    logger.info("User login attempt started")
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('email') or not data.get('password'):
            logger.warning("Login failed: Missing email or password")
            return jsonify({'error': 'Email and password are required'}), 400
        
        email = data['email'].lower().strip()
        password = data['password']
        
        logger.info(f"Login attempt for email: {email}")
        
        # Get user from database
        user = get_user_by_email(email)
        if not user:
            logger.warning(f"Login failed: User not found for email {email}")
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Verify password
        if not verify_password(password, user['password_hash']):
            logger.warning(f"Login failed: Invalid password for email {email}")
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Check if user is active
        if not user.get('is_active', True):
            logger.warning(f"Login failed: Account deactivated for email {email}")
            return jsonify({'error': 'Account is deactivated'}), 401
        
        # Update last login
        update_last_login(email)
        
        # Generate JWT token
        token = generate_jwt_token(user['RowKey'], email)
        
        logger.info(f"User login completed successfully: {email}")
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
        logger.error(f"Login error: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        print(f"Login error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/auth/user', methods=['GET'])
def get_user_profile():
    """Get user basic profile (authenticated endpoint)"""
    logger.info("User profile request started")
    try:
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            logger.warning("User profile request failed: No authorization token")
            return jsonify({'error': 'Authorization token required'}), 401
        
        token = auth_header.split(' ')[1]
        payload = verify_jwt_token(token)
        
        if not payload:
            logger.warning("User profile request failed: Invalid or expired token")
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        email = payload['email']
        logger.debug(f"User profile request for: {email}")
        
        # Get user from database
        user = get_user_by_email(email)
        if not user:
            logger.error(f"User profile request failed: User not found for {email}")
            return jsonify({'error': 'User not found'}), 404
        
        logger.info(f"User profile request completed successfully: {email}")
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
        logger.error(f"User profile error: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        print(f"User profile error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

def authenticate_request():
    """Helper function to authenticate API requests"""
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        logger.warning("Authentication failed: No authorization token")
        return None, jsonify({'error': 'Authorization token required'}), 401
    
    token = auth_header.split(' ')[1]
    payload = verify_jwt_token(token)
    
    if not payload:
        logger.warning("Authentication failed: Invalid or expired token")
        return None, jsonify({'error': 'Invalid or expired token'}), 401
    
    logger.debug(f"Authentication successful for user: {payload['email']}")
    return payload, None, None

# Kids Profile Endpoints

@app.route('/api/profiles', methods=['GET'])
def get_kids_profiles():
    """Get all kids profiles for the authenticated user"""
    logger.info("Get kids profiles request started")
    try:
        # Authenticate request
        payload, error_response, error_code = authenticate_request()
        if payload is None:
            return error_response, error_code
        
        # Get kids profiles for this user
        profiles = get_kids_profiles_by_user(payload['user_id'])
        
        logger.info(f"Get kids profiles completed successfully: Found {len(profiles)} profiles")
        return jsonify({
            'profiles': profiles,
            'count': len(profiles)
        }), 200
        
    except Exception as e:
        logger.error(f"Get profiles error: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        print(f"Get profiles error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/profiles', methods=['POST'])
def create_kids_profile():
    """Create a new kid profile"""
    logger.info("Create kid profile request started")
    try:
        # Authenticate request
        payload, error_response, error_code = authenticate_request()
        if payload is None:
            return error_response, error_code
        
        data = request.get_json()
        
        # Validate required fields
        if not data.get('name') or not data.get('age'):
            logger.warning("Create profile failed: Missing required fields")
            return jsonify({'error': 'Name and age are required'}), 400
        
        name = data['name'].strip()
        age = data['age']
        grade = data.get('grade', '').strip()
        avatar = data.get('avatar', 'default')
        learning_goals = data.get('learning_goals', '').strip()
        
        logger.info(f"Creating kid profile: {name}, age {age}")
        
        # Validate age
        try:
            age = int(age)
            if age < 3 or age > 18:
                logger.warning(f"Create profile failed: Invalid age {age}")
                return jsonify({'error': 'Age must be between 3 and 18'}), 400
        except ValueError:
            logger.warning(f"Create profile failed: Invalid age format {age}")
            return jsonify({'error': 'Age must be a valid number'}), 400
        
        # Create kid profile
        profile = create_kid_profile(payload['user_id'], name, age, grade, avatar, learning_goals)
        if not profile:
            logger.error("Create profile failed: Could not create profile")
            return jsonify({'error': 'Failed to create profile'}), 500
        
        logger.info(f"Kid profile created successfully: {name} (ID: {profile['RowKey']})")
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
        logger.error(f"Create profile error: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
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
    logger.warning(f"404 Error: Endpoint not found - {request.url}")
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"500 Error: Internal server error - {str(error)}")
    logger.error(f"Traceback: {traceback.format_exc()}")
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    logger.info("=== AI School Backend Server Starting ===")
    print("🚀 Starting AI School Backend Server...")
    logger.info("Listing available endpoints...")
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
    
    logger.info("Starting Flask development server...")
    logger.info("Server configuration: debug=True, host='0.0.0.0', port=5000")
    
    try:
        # Run the application
        app.run(debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise
    finally:
        logger.info("=== AI School Backend Server Session Ended ===")
