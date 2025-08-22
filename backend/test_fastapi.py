"""
FastAPI Test Script for AI School Backend
Tests all the authentication endpoints with FastAPI
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("1. Testing Health Endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"   Error: {e}")
        return False

def test_register():
    """Test user registration with all required fields"""
    print("\n2. Testing User Registration...")
    user_data = {
        "username": "testuser123",
        "password": "password123",
        "email": "testuser@aischool.com",
        "fullName": "Test User",
        "dob": "1995-05-15",
        "location": "New York, USA"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/register", json=user_data)
        print(f"   Status: {response.status_code}")
        result = response.json()
        print(f"   Response: {json.dumps(result, indent=2)}")
        
        if response.status_code == 200:
            return result.get('token')
        elif response.status_code == 400:
            print("   User already exists, trying login...")
            return None
        else:
            return None
    except Exception as e:
        print(f"   Error: {e}")
        return None

def test_login():
    """Test user login"""
    print("\n3. Testing User Login...")
    login_data = {
        "username": "testuser123",
        "password": "password123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/login", json=login_data)
        print(f"   Status: {response.status_code}")
        result = response.json()
        print(f"   Response: {json.dumps(result, indent=2)}")
        
        if response.status_code == 200:
            return result.get('token')
        return None
    except Exception as e:
        print(f"   Error: {e}")
        return None

def test_profile(token):
    """Test protected profile endpoint"""
    print("\n4. Testing Protected Profile Endpoint...")
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/profile", headers=headers)
        print(f"   Status: {response.status_code}")
        result = response.json()
        print(f"   Response: {json.dumps(result, indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"   Error: {e}")
        return False

def test_logout():
    """Test logout endpoint"""
    print("\n5. Testing Logout Endpoint...")
    try:
        response = requests.post(f"{BASE_URL}/logout")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"   Error: {e}")
        return False

def test_docs():
    """Test if API documentation is available"""
    print("\n6. Testing API Documentation...")
    try:
        response = requests.get(f"{BASE_URL}/docs")
        print(f"   Swagger UI Status: {response.status_code}")
        
        response = requests.get(f"{BASE_URL}/redoc")
        print(f"   ReDoc Status: {response.status_code}")
        
        return True
    except Exception as e:
        print(f"   Error: {e}")
        return False

def main():
    print("AI School FastAPI Backend Test")
    print("=" * 50)
    
    # Test if server is running
    if not test_health():
        print("\n❌ Server is not running or health check failed!")
        print("Please start the FastAPI server: python fastapi_app.py")
        return
    
    # Test registration
    token = test_register()
    
    # If registration failed (user exists), try login
    if not token:
        token = test_login()
    
    if not token:
        print("\n❌ Could not get authentication token!")
        return
    
    print(f"\n✓ Got authentication token: {token[:20]}...")
    
    # Test protected endpoint
    test_profile(token)
    
    # Test logout
    test_logout()
    
    # Test documentation
    test_docs()
    
    print("\n" + "=" * 50)
    print("🎉 FastAPI Testing Complete!")
    print("\nYour AI School FastAPI backend is working correctly!")
    print("📖 Visit http://localhost:8000/docs for interactive API documentation")
    print("📖 Visit http://localhost:8000/redoc for alternative documentation")

if __name__ == "__main__":
    main()
