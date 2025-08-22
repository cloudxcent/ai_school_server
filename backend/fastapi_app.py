"""
AI School FastAPI Backend Server
User authentication with Azure Table Storage using FastAPI
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from azure.data.tables import TableServiceClient, TableEntity
from pydantic import BaseModel, EmailStr, field_validator
import bcrypt
import jwt
import datetime
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
AZURE_CONN_STR = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
if not AZURE_CONN_STR:
    raise ValueError("AZURE_STORAGE_CONNECTION_STRING environment variable is required")

TABLE_NAME = "users"
SECRET_KEY = os.getenv('SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable is required")

# Azure Table Storage setup
table_service = TableServiceClient.from_connection_string(conn_str=AZURE_CONN_STR)

# Create table if it doesn't exist
try:
    table_service.create_table(TABLE_NAME)
    print(f"✓ Table '{TABLE_NAME}' created or already exists")
except Exception as e:
    if "already exists" not in str(e).lower():
        print(f"Error creating table: {e}")

table_client = table_service.get_table_client(table_name=TABLE_NAME)

# FastAPI app initialization
app = FastAPI(
    title="AI School Backend API",
    description="Authentication server for AI School mobile app",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your Android app's domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Pydantic models
class UserRegister(BaseModel):
    username: str
    password: str
    email: EmailStr
    fullName: str
    dob: str  # Date of birth in YYYY-MM-DD format
    location: str
    
    @field_validator('username')
    @classmethod
    def validate_username(cls, v):
        if len(v) < 3:
            raise ValueError('Username must be at least 3 characters long')
        if len(v) > 30:
            raise ValueError('Username must be less than 30 characters')
        return v.strip()
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters long')
        return v
    
    @field_validator('fullName')
    @classmethod
    def validate_full_name(cls, v):
        if len(v.strip()) < 2:
            raise ValueError('Full name must be at least 2 characters long')
        return v.strip()
    
    @field_validator('dob')
    @classmethod
    def validate_dob(cls, v):
        try:
            datetime.datetime.strptime(v, '%Y-%m-%d')
        except ValueError:
            raise ValueError('Date of birth must be in YYYY-MM-DD format')
        return v

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    username: str
    email: str
    fullName: str
    dob: str
    location: str
    created_at: Optional[str] = None
    last_login: Optional[str] = None

class LoginResponse(BaseModel):
    success: bool
    message: str
    token: str
    user: UserResponse

class RegisterResponse(BaseModel):
    success: bool
    message: str
    token: str
    user: UserResponse

class MessageResponse(BaseModel):
    success: bool
    message: str

# Utility functions
def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash"""
    return bcrypt.checkpw(password.encode(), hashed.encode())

def generate_jwt_token(username: str, email: str) -> str:
    """Generate JWT token"""
    payload = {
        'username': username,
        'email': email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24),
        'iat': datetime.datetime.utcnow()
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def verify_jwt_token(token: str) -> dict:
    """Verify JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current user from JWT token"""
    token = credentials.credentials
    payload = verify_jwt_token(token)
    
    # Get user from database
    try:
        entities = table_client.query_entities(f"RowKey eq '{payload['username']}'")
        entity = next(entities, None)
        if not entity:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        return entity
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

def update_last_login(username: str):
    """Update user's last login timestamp"""
    try:
        entities = table_client.query_entities(f"RowKey eq '{username}'")
        entity = next(entities, None)
        if entity:
            entity["last_login"] = datetime.datetime.utcnow().isoformat()
            table_client.update_entity(entity, mode='merge')
    except Exception as e:
        print(f"Error updating last login: {e}")

# API Routes
@app.get("/", response_model=MessageResponse)
def root():
    """Root endpoint"""
    return {
        "success": True,
        "message": "AI School Backend API is running"
    }

@app.get("/health", response_model=MessageResponse)
def health_check():
    """Health check endpoint"""
    return {
        "success": True,
        "message": "AI School Backend Server is healthy"
    }

@app.post("/register", response_model=RegisterResponse)
def register(user: UserRegister):
    """User registration endpoint"""
    try:
        # Check if user already exists
        entities = table_client.query_entities(f"RowKey eq '{user.username}'")
        if list(entities):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already exists"
            )
        
        # Check if email already exists
        email_entities = table_client.query_entities(f"email eq '{user.email}'")
        if list(email_entities):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create new user entity
        entity = TableEntity()
        entity["PartitionKey"] = "User"
        entity["RowKey"] = user.username
        entity["email"] = user.email
        entity["password_hash"] = hash_password(user.password)
        entity["fullName"] = user.fullName
        entity["dob"] = user.dob
        entity["location"] = user.location
        entity["created_at"] = datetime.datetime.utcnow().isoformat()
        entity["last_login"] = None
        entity["is_active"] = True
        
        # Save to database
        table_client.create_entity(entity)
        
        # Generate JWT token
        token = generate_jwt_token(user.username, user.email)
        
        # Prepare response
        user_response = UserResponse(
            username=user.username,
            email=user.email,
            fullName=user.fullName,
            dob=user.dob,
            location=user.location,
            created_at=entity["created_at"]
        )
        
        return RegisterResponse(
            success=True,
            message="User registered successfully",
            token=token,
            user=user_response
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Registration error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@app.post("/login", response_model=LoginResponse)
def login(user: UserLogin):
    """User login endpoint"""
    try:
        # Find user by username
        entities = table_client.query_entities(f"RowKey eq '{user.username}'")
        entity = next(entities, None)
        
        if not entity:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )
        
        # Verify password
        if not verify_password(user.password, entity["password_hash"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )
        
        # Check if user is active
        if not entity.get("is_active", True):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Account is deactivated"
            )
        
        # Update last login
        update_last_login(user.username)
        
        # Generate JWT token
        token = generate_jwt_token(user.username, entity["email"])
        
        # Prepare response
        user_response = UserResponse(
            username=entity["RowKey"],
            email=entity["email"],
            fullName=entity["fullName"],
            dob=entity["dob"],
            location=entity["location"],
            created_at=entity.get("created_at"),
            last_login=datetime.datetime.utcnow().isoformat()
        )
        
        return LoginResponse(
            success=True,
            message="Login successful",
            token=token,
            user=user_response
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@app.get("/profile", response_model=UserResponse)
def get_profile(current_user = Depends(get_current_user)):
    """Get user profile (protected endpoint)"""
    try:
        return UserResponse(
            username=current_user["RowKey"],
            email=current_user["email"],
            fullName=current_user["fullName"],
            dob=current_user["dob"],
            location=current_user["location"],
            created_at=current_user.get("created_at"),
            last_login=current_user.get("last_login")
        )
    except Exception as e:
        print(f"Profile error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@app.post("/logout", response_model=MessageResponse)
def logout():
    """User logout endpoint"""
    # Since we're using stateless JWT tokens, logout is handled client-side
    return MessageResponse(
        success=True,
        message="Logged out successfully"
    )

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return {"success": False, "message": "Endpoint not found"}

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return {"success": False, "message": "Internal server error"}

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting AI School FastAPI Backend Server...")
    print("📚 Endpoints available:")
    print("   GET  /")
    print("   GET  /health")
    print("   POST /register")
    print("   POST /login")
    print("   GET  /profile")
    print("   POST /logout")
    print("   GET  /docs (Swagger UI)")
    print("   GET  /redoc (ReDoc)")
    print()
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
