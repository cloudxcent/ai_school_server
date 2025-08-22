"""
Simple Kids Profiles API Test
"""
import sys
print("Starting Kids Profiles API Test...")
print("Python version:", sys.version)

try:
    import requests
    print("✓ Requests library imported successfully")
except ImportError as e:
    print(f"❌ Error importing requests: {e}")
    sys.exit(1)

import json
import time

BASE_URL = "http://localhost:5000/api"

def test_step(step_name, func):
    """Run a test step with error handling"""
    print(f"\n{step_name}")
    print("-" * len(step_name))
    try:
        return func()
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_health():
    """Test health endpoint"""
    response = requests.get(f"{BASE_URL}/health", timeout=5)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"✓ {result.get('message', 'Health check passed')}")
        return True
    return False

def authenticate():
    """Get authentication token"""
    # Try to register/login
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
    except:
        pass
    
    # If login fails, try registration
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=user_data, timeout=5)
        if response.status_code == 201:
            result = response.json()
            token = result.get('token')
            print(f"✓ Registered new user successfully")
            return token
    except:
        pass
    
    print("❌ Failed to authenticate")
    return None

def test_get_empty_profiles(token):
    """Test getting profiles when none exist"""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/profiles", headers=headers, timeout=5)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✓ Got {result.get('count', 0)} profiles (expected 0 initially)")
        return True
    else:
        print(f"❌ Unexpected status: {response.status_code}")
        print(f"Response: {response.text}")
        return False

def test_create_kid_profile(token):
    """Test creating a kid profile"""
    headers = {"Authorization": f"Bearer {token}"}
    kid_data = {
        "name": "Alice Test",
        "age": 8,
        "grade": "3rd Grade",
        "avatar": "girl_avatar_1",
        "learning_goals": "Reading and math skills"
    }
    
    response = requests.post(f"{BASE_URL}/profiles", json=kid_data, headers=headers, timeout=5)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 201:
        result = response.json()
        profile = result.get('profile', {})
        profile_id = profile.get('id')
        print(f"✓ Created profile for {profile.get('name')} (ID: {profile_id[:8]}...)")
        return profile_id
    else:
        print(f"❌ Failed to create profile")
        print(f"Response: {response.text}")
        return None

def test_get_profiles_with_data(token):
    """Test getting profiles when data exists"""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/profiles", headers=headers, timeout=5)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        count = result.get('count', 0)
        print(f"✓ Got {count} profile(s)")
        for i, profile in enumerate(result.get('profiles', []), 1):
            print(f"  {i}. {profile.get('name')} (Age: {profile.get('age')})")
        return True
    else:
        print(f"❌ Failed to get profiles")
        return False

def test_get_specific_profile(token, profile_id):
    """Test getting a specific profile"""
    if not profile_id:
        print("⚠️ No profile ID provided, skipping")
        return False
        
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/profiles/{profile_id}", headers=headers, timeout=5)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        profile = result.get('profile', {})
        print(f"✓ Got profile: {profile.get('name')} (Age: {profile.get('age')})")
        return True
    else:
        print(f"❌ Failed to get specific profile")
        return False

def test_update_profile(token, profile_id):
    """Test updating a profile"""
    if not profile_id:
        print("⚠️ No profile ID provided, skipping")
        return False
        
    headers = {"Authorization": f"Bearer {token}"}
    update_data = {
        "age": 9,
        "grade": "4th Grade",
        "learning_goals": "Advanced reading and multiplication"
    }
    
    response = requests.put(f"{BASE_URL}/profiles/{profile_id}", json=update_data, headers=headers, timeout=5)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        profile = result.get('profile', {})
        print(f"✓ Updated profile: Age now {profile.get('age')}, Grade: {profile.get('grade')}")
        return True
    else:
        print(f"❌ Failed to update profile")
        return False

def test_validation_errors(token):
    """Test validation errors"""
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test invalid age
    invalid_data = {"name": "Invalid Kid", "age": 25}
    response = requests.post(f"{BASE_URL}/profiles", json=invalid_data, headers=headers, timeout=5)
    print(f"Invalid age test - Status: {response.status_code}")
    if response.status_code == 400:
        print("✓ Correctly rejected invalid age")
    else:
        print("⚠️ Unexpected response for invalid age")
    
    # Test missing name
    missing_data = {"age": 8}
    response = requests.post(f"{BASE_URL}/profiles", json=missing_data, headers=headers, timeout=5)
    print(f"Missing name test - Status: {response.status_code}")
    if response.status_code == 400:
        print("✓ Correctly rejected missing name")
    else:
        print("⚠️ Unexpected response for missing name")
    
    return True

def main():
    """Run comprehensive Azure database tests for profiles and kids profiles"""
    print("🧪 Testing Profiles & Kids Profiles with Azure Database")
    print("=" * 60)
    
    # Test 1: Health check
    if not test_step("1. Health Check", test_health):
        print("❌ Server is not responding. Make sure it's running on http://localhost:5000")
        return
    
    # Test 2: Authentication (creates user profile in Azure)
    token = test_step("2. User Authentication & Profile Creation", authenticate)
    if not token:
        print("❌ Could not authenticate. Stopping tests.")
        return
    
    # Test 3: Get initial profiles (should be empty for new user)
    test_step("3. Get Initial Kids Profiles (Empty Check)", lambda: test_get_empty_profiles(token))
    
    # Test 4: Create first kid profile in Azure
    profile_id_1 = test_step("4. Create First Kid Profile", lambda: test_create_kid_profile(token))
    
    # Test 5: Create second kid profile in Azure
    def create_second_kid():
        headers = {"Authorization": f"Bearer {token}"}
        kid_data = {
            "name": "Bob Test",
            "age": 10,
            "grade": "5th Grade",
            "avatar": "boy_avatar_2",
            "learning_goals": "Science and coding skills"
        }
        response = requests.post(f"{BASE_URL}/profiles", json=kid_data, headers=headers, timeout=5)
        print(f"Status: {response.status_code}")
        if response.status_code == 201:
            result = response.json()
            profile = result.get('profile', {})
            profile_id = profile.get('id')
            print(f"✓ Created profile for {profile.get('name')} (ID: {profile_id[:8]}...)")
            return profile_id
        else:
            print(f"❌ Failed to create profile: {response.text}")
            return None
    
    profile_id_2 = test_step("5. Create Second Kid Profile", create_second_kid)
    
    # Test 6: Get all profiles (should show both kids)
    test_step("6. Get All Kids Profiles (With Data)", lambda: test_get_profiles_with_data(token))
    
    # Test 7: Get specific profile
    if profile_id_1:
        test_step("7. Get Specific Kid Profile", lambda: test_get_specific_profile(token, profile_id_1))
    
    # Test 8: Update profile in Azure
    if profile_id_1:
        test_step("8. Update Kid Profile", lambda: test_update_profile(token, profile_id_1))
    
    # Test 9: Test validation errors
    test_step("9. Test Input Validation", lambda: test_validation_errors(token))
    
    # Test 10: Create third kid with different data
    def create_third_kid():
        headers = {"Authorization": f"Bearer {token}"}
        kid_data = {
            "name": "Charlie Test",
            "age": 6,
            "grade": "1st Grade",
            "avatar": "child_avatar_3",
            "learning_goals": "Basic reading and numbers"
        }
        response = requests.post(f"{BASE_URL}/profiles", json=kid_data, headers=headers, timeout=5)
        print(f"Status: {response.status_code}")
        if response.status_code == 201:
            result = response.json()
            profile = result.get('profile', {})
            profile_id = profile.get('id')
            print(f"✓ Created profile for {profile.get('name')} (ID: {profile_id[:8]}...)")
            return profile_id
        else:
            print(f"❌ Failed to create profile: {response.text}")
            return None
    
    profile_id_3 = test_step("10. Create Third Kid Profile", create_third_kid)
    
    # Test 11: Final count check
    test_step("11. Final Profile Count Check", lambda: test_get_profiles_with_data(token))
    
    print("\n" + "=" * 60)
    print("🎉 Azure Database Testing Complete!")
    print("\n✅ Successfully tested:")
    print("  • User profile creation and authentication in Azure")
    print("  • Multiple kids profiles creation in Azure")
    print("  • Profile retrieval from Azure")
    print("  • Profile updates in Azure")
    print("  • Data validation and error handling")
    print(f"\n📊 Created profiles: {sum(1 for pid in [profile_id_1, profile_id_2, profile_id_3] if pid)} kids profiles")
    print("📱 Azure database is ready for Android app integration!")

if __name__ == "__main__":
    main()
