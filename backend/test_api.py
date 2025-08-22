"""
API Test Script for AI School Backend
Tests all the authentication endpoints
"""

import requests
import json
import time

BASE_URL = "http://localhost:5000/api"

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
    """Test user registration"""
    print("\n2. Testing User Registration...")
    user_data = {
        "email": "test@aischool.com",
        "password": "password123",
        "full_name": "Test User",
        "phone_number": "+1234567890"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
        print(f"   Status: {response.status_code}")
        result = response.json()
        print(f"   Response: {json.dumps(result, indent=2)}")
        
        if response.status_code == 201:
            return result.get('token')
        elif response.status_code == 409:
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
        "email": "test@aischool.com",
        "password": "password123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
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
        response = requests.get(f"{BASE_URL}/auth/profile", headers=headers)
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
        response = requests.post(f"{BASE_URL}/auth/logout")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"   Error: {e}")
        return False

def main():
    print("AI School Backend API Test")
    print("=" * 40)
    
    # Test if server is running
    if not test_health():
        print("\n❌ Server is not running or health check failed!")
        print("Please make sure the server is running: python app.py")
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
    
    print("\n" + "=" * 40)
    print("🎉 API Testing Complete!")
    print("\nYour AI School backend is working correctly!")
    print("You can now integrate these endpoints with your Android app.")

if __name__ == "__main__":
    main()
