"""
Run single test: test_create_kid_profile
"""
import requests
import sys

print("🧪 Testing Create Kid Profile Function")
print("=" * 50)

BASE_URL = "http://localhost:5000/api"

def authenticate():
    """Get authentication token"""
    user_data = {
        "email": "testparent@aischool.com",
        "password": "password123",
        "full_name": "Test Parent",
        "phone_number": "+1234567890"
    }
    
    # Try login first
    login_data = {"email": user_data["email"], "password": user_data["password"]}
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data, timeout=5)
        if response.status_code == 200:
            result = response.json()
            token = result.get('token')
            print(f"✓ Logged in successfully")
            return token
    except Exception as e:
        print(f"Login error: {e}")
    
    # If login fails, try registration
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=user_data, timeout=5)
        if response.status_code == 201:
            result = response.json()
            token = result.get('token')
            print(f"✓ Registered new user successfully")
            return token
    except Exception as e:
        print(f"Registration error: {e}")
    
    print("❌ Failed to authenticate")
    return None

def test_create_kid_profile(token):
    """Test creating a kid profile"""
    print("\nTesting Create Kid Profile...")
    print("-" * 30)
    
    headers = {"Authorization": f"Bearer {token}"}
    kid_data = {
        "name": "Alice Test",
        "age": 8,
        "grade": "3rd Grade",
        "avatar": "girl_avatar_1",
        "learning_goals": "Reading and math skills"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/profiles", json=kid_data, headers=headers, timeout=5)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            profile = result.get('profile', {})
            profile_id = profile.get('id')
            print(f"✓ Created profile for {profile.get('name')} (ID: {profile_id[:8] if profile_id else 'None'}...)")
            print(f"Profile details: Age {profile.get('age')}, Grade: {profile.get('grade')}")
            return profile_id
        else:
            print(f"❌ Failed to create profile")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def main():
    print("1. Health Check...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"Status: {response.status_code}")
        if response.status_code != 200:
            print("❌ Server is not responding properly")
            return
        print("✓ Server is running")
    except Exception as e:
        print(f"❌ Server connection error: {e}")
        return
    
    print("\n2. Authentication...")
    token = authenticate()
    if not token:
        print("❌ Could not authenticate. Stopping test.")
        return
    
    print("\n3. Creating Kid Profile...")
    profile_id = test_create_kid_profile(token)
    
    print("\n" + "=" * 50)
    if profile_id:
        print("🎉 Create Kid Profile Test PASSED!")
        print(f"✅ Successfully created profile with ID: {profile_id}")
    else:
        print("❌ Create Kid Profile Test FAILED!")

if __name__ == "__main__":
    main()
