import requests
import json
import time

# Test server connectivity first
try:
    response = requests.get("http://localhost:5000/api/health", timeout=5)
    print(f"Health check: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test user registration
    user_data = {
        "email": "azuretest@aischool.com",
        "password": "password123", 
        "full_name": "Azure Test User",
        "phone_number": "+1234567890"
    }
    
    print("\nTesting user registration...")
    response = requests.post("http://localhost:5000/api/auth/register", json=user_data, timeout=5)
    print(f"Registration: {response.status_code}")
    
    if response.status_code in [200, 201]:
        result = response.json()
        token = result.get('token')
        print("✓ Got authentication token")
        
        # Test creating kid profile
        print("\nTesting kid profile creation...")
        headers = {"Authorization": f"Bearer {token}"}
        kid_data = {
            "name": "Azure Test Kid",
            "age": 8,
            "grade": "3rd Grade",
            "avatar": "test_avatar",
            "learning_goals": "Azure database testing"
        }
        
        response = requests.post("http://localhost:5000/api/profiles", json=kid_data, headers=headers, timeout=5)
        print(f"Profile creation: {response.status_code}")
        print(f"Response: {response.text[:200]}...")
        
        if response.status_code == 201:
            print("✓ Successfully created kid profile in Azure!")
            
        # Test getting profiles
        print("\nTesting profile retrieval...")
        response = requests.get("http://localhost:5000/api/profiles", headers=headers, timeout=5)
        print(f"Get profiles: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Found {result.get('count', 0)} profiles")
            
    elif response.status_code == 409:
        print("User already exists, trying login...")
        login_data = {"email": user_data["email"], "password": user_data["password"]}
        response = requests.post("http://localhost:5000/api/auth/login", json=login_data, timeout=5)
        print(f"Login: {response.status_code}")
        
except Exception as e:
    print(f"Error: {e}")

print("\nTest completed!")
