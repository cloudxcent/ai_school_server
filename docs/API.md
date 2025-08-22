# API Documentation - AI School Backend

## Base URL
```
http://localhost:5000/api
```

## Authentication
The API uses JWT (JSON Web Tokens) for authentication. Include the token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

## Endpoints

### Health Check
**GET** `/health`

Check if the server is running.

**Response:**
```json
{
    "status": "healthy",
    "message": "AI School Backend Server is running",
    "timestamp": "2025-08-22T10:30:00.000Z"
}
```

### User Registration
**POST** `/auth/register`

Register a new user account.

**Request Body:**
```json
{
    "email": "student@example.com",
    "password": "securepassword123",
    "full_name": "John Doe",
    "phone_number": "+1234567890"
}
```

**Response (Success - 201):**
```json
{
    "message": "User registered successfully",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
        "id": "uuid-here",
        "email": "student@example.com",
        "full_name": "John Doe",
        "phone_number": "+1234567890",
        "created_at": "2025-08-22T10:30:00.000Z"
    }
}
```

**Response (Error - 400/409):**
```json
{
    "error": "User with this email already exists"
}
```

### User Login
**POST** `/auth/login`

Authenticate user and get access token.

**Request Body:**
```json
{
    "email": "student@example.com",
    "password": "securepassword123"
}
```

**Response (Success - 200):**
```json
{
    "message": "Login successful",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
        "id": "uuid-here",
        "email": "student@example.com",
        "full_name": "John Doe",
        "phone_number": "+1234567890",
        "last_login": "2025-08-22T10:30:00.000Z"
    }
}
```

**Response (Error - 401):**
```json
{
    "error": "Invalid email or password"
}
```

### Get User Profile
**GET** `/auth/profile`

Get current user's profile information. Requires authentication.

**Headers:**
```
Authorization: Bearer <your_jwt_token>
```

**Response (Success - 200):**
```json
{
    "user": {
        "id": "uuid-here",
        "email": "student@example.com",
        "full_name": "John Doe",
        "phone_number": "+1234567890",
        "created_at": "2025-08-22T10:30:00.000Z",
        "last_login": "2025-08-22T10:30:00.000Z"
    }
}
```

**Response (Error - 401):**
```json
{
    "error": "Authorization token required"
}
```

### User Logout
**POST** `/auth/logout`

Logout user (client-side token removal).

**Response (Success - 200):**
```json
{
    "message": "Logged out successfully"
}
```

## Error Codes

- **400** - Bad Request (validation errors)
- **401** - Unauthorized (authentication required)
- **404** - Not Found (endpoint doesn't exist)
- **409** - Conflict (resource already exists)
- **500** - Internal Server Error

## Data Models

### User
```json
{
    "id": "string (UUID)",
    "email": "string (unique)",
    "full_name": "string",
    "phone_number": "string (optional)",
    "created_at": "string (ISO datetime)",
    "last_login": "string (ISO datetime, nullable)",
    "is_active": "boolean"
}
```

## Security Features

- Password hashing using bcrypt
- JWT token authentication with 24-hour expiration
- Email validation
- Input sanitization
- CORS enabled for cross-origin requests

## Rate Limiting
Currently not implemented. Consider adding rate limiting for production use.

## CORS
Cross-Origin Resource Sharing is enabled to allow requests from web and mobile applications.
