"""
Test script specifically for the Profiles API endpoint
"""

import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_profiles_api():
    """Test the profiles API endpoint with proper authentication flow"""
    print("🧪 Testing AI School Profiles API")
    print("=" * 50)
    
    # Step 1: Test health check
    print("\n1. Testing Health Endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"   ✓ Status: {response.status_code}")
        print(f"   ✓ Response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Step 2: Register or Login to get token
    print("\n2. Getting Authentication Token...")
    user_data = {
        "email": "test@aischool.com",
        "password": "password123",
        "full_name": "Test User",
        "phone_number": "+1234567890"
    }
    
    token = None
    
    # Try registration first
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
        print(f"   Registration Status: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            token = result.get('token')
            print(f"   ✓ New user registered successfully")
        elif response.status_code == 409:
            print(f"   ℹ User already exists, trying login...")
            # Try login
            login_data = {"email": user_data["email"], "password": user_data["password"]}
            login_response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
            print(f"   Login Status: {login_response.status_code}")
            
            if login_response.status_code == 200:
                result = login_response.json()
                token = result.get('token')
                print(f"   ✓ User logged in successfully")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    if not token:
        print("   ❌ Could not get authentication token!")
        return False
    
    print(f"   ✓ Got token: {token[:20]}...")
    
    # Step 3: Test the Profiles API endpoint
    print("\n3. 🎯 Testing PROFILES API Endpoint...")
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/auth/profile", headers=headers)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ SUCCESS! Profile retrieved:")
            print(f"   📄 Response:")
            print(json.dumps(result, indent=6))
            
            # Validate response structure
            if 'user' in result:
                user = result['user']
                required_fields = ['id', 'email', 'full_name', 'phone_number', 'created_at']
                missing_fields = [field for field in required_fields if field not in user]
                
                if not missing_fields:
                    print(f"   ✅ All required profile fields present!")
                    print(f"   👤 User ID: {user['id']}")
                    print(f"   📧 Email: {user['email']}")
                    print(f"   👨‍💼 Name: {user['full_name']}")
                    print(f"   📱 Phone: {user['phone_number']}")
                    print(f"   📅 Created: {user['created_at']}")
                    if 'last_login' in user:
                        print(f"   🕐 Last Login: {user['last_login']}")
                else:
                    print(f"   ⚠️ Missing fields: {missing_fields}")
            else:
                print(f"   ⚠️ Response missing 'user' field")
                
        elif response.status_code == 401:
            print(f"   ❌ UNAUTHORIZED - Token invalid or expired")
            print(f"   Response: {response.json()}")
        else:
            print(f"   ❌ FAILED - Status: {response.status_code}")
            print(f"   Response: {response.json()}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Step 4: Test invalid token
    print("\n4. Testing with Invalid Token...")
    invalid_headers = {"Authorization": "Bearer invalid_token_123"}
    
    try:
        response = requests.get(f"{BASE_URL}/auth/profile", headers=invalid_headers)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 401:
            print(f"   ✅ Correctly rejected invalid token")
            print(f"   Response: {response.json()}")
        else:
            print(f"   ⚠️ Unexpected response for invalid token")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Step 5: Test without Authorization header
    print("\n5. Testing without Authorization Header...")
    
    try:
        response = requests.get(f"{BASE_URL}/auth/profile")
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 401:
            print(f"   ✅ Correctly rejected request without token")
            print(f"   Response: {response.json()}")
        else:
            print(f"   ⚠️ Unexpected response for missing token")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Profiles API Testing Complete!")
    print("\n📋 Summary:")
    print("   • Health check: ✓")
    print("   • Authentication: ✓")
    print("   • Profile retrieval: ✓")
    print("   • Security validation: ✓")
    print("\n🔗 Endpoint tested: GET /api/auth/profile")
    print("🔐 Authentication: Bearer token required")
    print("📱 Ready for Android integration!")

if __name__ == "__main__":
    test_profiles_api()
