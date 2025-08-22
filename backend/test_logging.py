"""
Test script to verify the logging functionality of the AI School Backend Server
"""

import requests
import json
import time

def test_logging():
    """Test the logging functionality by making API requests"""
    base_url = "http://localhost:5000"
    
    print("🧪 Testing AI School Backend Logging Functionality")
    print("=" * 60)
    
    # Test 1: Health Check
    print("1. Testing Health Check endpoint...")
    try:
        response = requests.get(f"{base_url}/api/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    time.sleep(1)
    
    # Test 2: Register a test user
    print("\n2. Testing User Registration...")
    register_data = {
        "email": "test@example.com",
        "password": "testpass123",
        "full_name": "Test User",
        "phone_number": "1234567890"
    }
    try:
        response = requests.post(
            f"{base_url}/api/auth/register",
            json=register_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 201:
            user_data = response.json()
            token = user_data.get('token')
            print(f"   User registered successfully")
            print(f"   User ID: {user_data['user']['id']}")
        else:
            print(f"   Response: {response.json()}")
            return
    except Exception as e:
        print(f"   Error: {e}")
        return
    
    time.sleep(1)
    
    # Test 3: Login
    print("\n3. Testing User Login...")
    login_data = {
        "email": "test@example.com",
        "password": "testpass123"
    }
    try:
        response = requests.post(
            f"{base_url}/api/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            login_response = response.json()
            token = login_response.get('token')
            print(f"   Login successful")
        else:
            print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    time.sleep(1)
    
    # Test 4: Get User Profile
    print("\n4. Testing Get User Profile...")
    try:
        response = requests.get(
            f"{base_url}/api/auth/user",
            headers={"Authorization": f"Bearer {token}"}
        )
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    time.sleep(1)
    
    # Test 5: Create Kid Profile
    print("\n5. Testing Create Kid Profile...")
    kid_data = {
        "name": "Test Kid",
        "age": 8,
        "grade": "3rd Grade",
        "avatar": "robot",
        "learning_goals": "Learn math and science"
    }
    try:
        response = requests.post(
            f"{base_url}/api/profiles",
            json=kid_data,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 201:
            profile_data = response.json()
            profile_id = profile_data['profile']['id']
            print(f"   Kid profile created successfully")
            print(f"   Profile ID: {profile_id}")
        else:
            print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    time.sleep(1)
    
    # Test 6: Get Kids Profiles
    print("\n6. Testing Get Kids Profiles...")
    try:
        response = requests.get(
            f"{base_url}/api/profiles",
            headers={"Authorization": f"Bearer {token}"}
        )
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    time.sleep(1)
    
    # Test 7: Test Invalid Endpoint (404)
    print("\n7. Testing Invalid Endpoint (404)...")
    try:
        response = requests.get(f"{base_url}/api/invalid-endpoint")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 Logging test completed!")
    print("📁 Check the 'logs' directory for the session log file.")
    print("📊 The log file should contain detailed traces of all operations.")

if __name__ == "__main__":
    test_logging()
