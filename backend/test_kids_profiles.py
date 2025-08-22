"""
Test script for Kids Profiles API
Tests all the kids profile management endpoints
"""

import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_kids_profiles_api():
    """Test the complete kids profiles API flow"""
    print("🧪 Testing AI School Kids Profiles API")
    print("=" * 60)
    
    # Step 1: Health check
    print("\n1. Testing Health Endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"   ✓ Status: {response.status_code}")
        print(f"   ✓ Response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Step 2: Get authentication token
    print("\n2. Getting Authentication Token...")
    user_data = {
        "email": "parent@aischool.com",
        "password": "password123",
        "full_name": "Parent User",
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
    headers = {"Authorization": f"Bearer {token}"}
    
    # Step 3: Test getting empty profiles list
    print("\n3. 📋 Testing GET /api/profiles (empty list)...")
    try:
        response = requests.get(f"{BASE_URL}/profiles", headers=headers)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ SUCCESS! Got profiles list:")
            print(f"   📄 Response: {json.dumps(result, indent=6)}")
        else:
            print(f"   ❌ FAILED - Status: {response.status_code}")
            print(f"   Response: {response.json()}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Step 4: Create first kid profile
    print("\n4. 👶 Testing POST /api/profiles (Create first kid)...")
    kid1_data = {
        "name": "Alice Johnson",
        "age": 7,
        "grade": "2nd Grade",
        "avatar": "girl_avatar_1",
        "learning_goals": "Improve reading and basic math"
    }
    
    kid1_id = None
    try:
        response = requests.post(f"{BASE_URL}/profiles", json=kid1_data, headers=headers)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            kid1_id = result['profile']['id']
            print(f"   ✅ SUCCESS! First kid profile created:")
            print(f"   👧 Name: {result['profile']['name']}")
            print(f"   🎂 Age: {result['profile']['age']}")
            print(f"   📚 Grade: {result['profile']['grade']}")
            print(f"   🎯 Goals: {result['profile']['learning_goals']}")
            print(f"   🆔 ID: {kid1_id}")
        else:
            print(f"   ❌ FAILED - Status: {response.status_code}")
            print(f"   Response: {response.json()}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Step 5: Create second kid profile
    print("\n5. 👦 Testing POST /api/profiles (Create second kid)...")
    kid2_data = {
        "name": "Bob Johnson",
        "age": 10,
        "grade": "5th Grade",
        "avatar": "boy_avatar_1",
        "learning_goals": "Advanced mathematics and science"
    }
    
    kid2_id = None
    try:
        response = requests.post(f"{BASE_URL}/profiles", json=kid2_data, headers=headers)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            kid2_id = result['profile']['id']
            print(f"   ✅ SUCCESS! Second kid profile created:")
            print(f"   👦 Name: {result['profile']['name']}")
            print(f"   🎂 Age: {result['profile']['age']}")
            print(f"   📚 Grade: {result['profile']['grade']}")
            print(f"   🎯 Goals: {result['profile']['learning_goals']}")
            print(f"   🆔 ID: {kid2_id}")
        else:
            print(f"   ❌ FAILED - Status: {response.status_code}")
            print(f"   Response: {response.json()}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Step 6: Get all profiles (should have 2 now)
    print("\n6. 📋 Testing GET /api/profiles (with profiles)...")
    try:
        response = requests.get(f"{BASE_URL}/profiles", headers=headers)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ SUCCESS! Got {result['count']} profiles:")
            for i, profile in enumerate(result['profiles'], 1):
                print(f"   Profile {i}:")
                print(f"     👤 Name: {profile['name']}")
                print(f"     🎂 Age: {profile['age']}")
                print(f"     📚 Grade: {profile['grade']}")
                print(f"     🆔 ID: {profile['id']}")
        else:
            print(f"   ❌ FAILED - Status: {response.status_code}")
            print(f"   Response: {response.json()}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Step 7: Get specific kid profile
    if kid1_id:
        print(f"\n7. 👧 Testing GET /api/profiles/{kid1_id} (Get specific profile)...")
        try:
            response = requests.get(f"{BASE_URL}/profiles/{kid1_id}", headers=headers)
            print(f"   Status Code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                profile = result['profile']
                print(f"   ✅ SUCCESS! Got specific profile:")
                print(f"   👧 Name: {profile['name']}")
                print(f"   🎂 Age: {profile['age']}")
                print(f"   📚 Grade: {profile['grade']}")
                print(f"   🎯 Goals: {profile['learning_goals']}")
                print(f"   📅 Created: {profile['created_at']}")
            else:
                print(f"   ❌ FAILED - Status: {response.status_code}")
                print(f"   Response: {response.json()}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # Step 8: Update kid profile
    if kid1_id:
        print(f"\n8. ✏️ Testing PUT /api/profiles/{kid1_id} (Update profile)...")
        update_data = {
            "age": 8,
            "grade": "3rd Grade",
            "learning_goals": "Reading comprehension and multiplication tables"
        }
        
        try:
            response = requests.put(f"{BASE_URL}/profiles/{kid1_id}", json=update_data, headers=headers)
            print(f"   Status Code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                profile = result['profile']
                print(f"   ✅ SUCCESS! Profile updated:")
                print(f"   👧 Name: {profile['name']}")
                print(f"   🎂 Age: {profile['age']} (updated)")
                print(f"   📚 Grade: {profile['grade']} (updated)")
                print(f"   🎯 Goals: {profile['learning_goals']} (updated)")
            else:
                print(f"   ❌ FAILED - Status: {response.status_code}")
                print(f"   Response: {response.json()}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # Step 9: Test validation errors
    print("\n9. ⚠️ Testing Validation Errors...")
    
    # Test invalid age
    invalid_data = {"name": "Invalid Kid", "age": 25}
    try:
        response = requests.post(f"{BASE_URL}/profiles", json=invalid_data, headers=headers)
        print(f"   Invalid age test - Status: {response.status_code}")
        if response.status_code == 400:
            print(f"   ✅ Correctly rejected invalid age")
        else:
            print(f"   ⚠️ Unexpected response for invalid age")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test missing required fields
    missing_data = {"age": 8}
    try:
        response = requests.post(f"{BASE_URL}/profiles", json=missing_data, headers=headers)
        print(f"   Missing name test - Status: {response.status_code}")
        if response.status_code == 400:
            print(f"   ✅ Correctly rejected missing name")
        else:
            print(f"   ⚠️ Unexpected response for missing name")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Step 10: Test unauthorized access
    print("\n10. 🔒 Testing Security...")
    try:
        response = requests.get(f"{BASE_URL}/profiles")
        print(f"   No token test - Status: {response.status_code}")
        if response.status_code == 401:
            print(f"   ✅ Correctly rejected request without token")
        
        invalid_headers = {"Authorization": "Bearer invalid_token"}
        response = requests.get(f"{BASE_URL}/profiles", headers=invalid_headers)
        print(f"   Invalid token test - Status: {response.status_code}")
        if response.status_code == 401:
            print(f"   ✅ Correctly rejected invalid token")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Step 11: Delete a profile (optional - uncomment to test)
    # if kid2_id:
    #     print(f"\n11. 🗑️ Testing DELETE /api/profiles/{kid2_id} (Delete profile)...")
    #     try:
    #         response = requests.delete(f"{BASE_URL}/profiles/{kid2_id}", headers=headers)
    #         print(f"   Status Code: {response.status_code}")
    #         
    #         if response.status_code == 200:
    #             print(f"   ✅ SUCCESS! Profile deleted")
    #             
    #             # Verify it's gone
    #             response = requests.get(f"{BASE_URL}/profiles", headers=headers)
    #             if response.status_code == 200:
    #                 result = response.json()
    #                 print(f"   Remaining profiles: {result['count']}")
    #         else:
    #             print(f"   ❌ FAILED - Status: {response.status_code}")
    #             print(f"   Response: {response.json()}")
    #             
    #     except Exception as e:
    #         print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Kids Profiles API Testing Complete!")
    print("\n📋 Summary of Endpoints Tested:")
    print("   ✓ GET  /api/profiles - List all kids profiles")
    print("   ✓ POST /api/profiles - Create new kid profile")
    print("   ✓ GET  /api/profiles/<id> - Get specific profile")
    print("   ✓ PUT  /api/profiles/<id> - Update profile")
    print("   ✓ Security and validation testing")
    print("\n🗃️ Database Tables:")
    print("   📊 users - Parent/user accounts")
    print("   👶 kidsprofiles - Children profiles")
    print("\n🔗 Features Available:")
    print("   • Multiple kids per parent account")
    print("   • Age validation (3-18 years)")
    print("   • Grade levels and learning goals")
    print("   • Avatar selection")
    print("   • Profile management (CRUD operations)")
    print("   • JWT authentication for all operations")
    print("\n📱 Ready for Android integration!")

if __name__ == "__main__":
    test_kids_profiles_api()
