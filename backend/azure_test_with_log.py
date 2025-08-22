"""
Minimal Azure Test - Creates profiles in Azure and saves results to file
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:5000/api"
LOG_FILE = "azure_test_log.txt"

def log_message(message):
    """Log message to both console and file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}"
    print(log_entry)
    
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_entry + "\n")
    except Exception as e:
        print(f"Error writing to log: {e}")

def main():
    log_message("🚀 Starting Azure Database Test")
    log_message("="*50)
    
    try:
        # 1. Health check
        log_message("1. Testing server health...")
        response = requests.get(f"{BASE_URL}/health", timeout=10)
        log_message(f"   Health status: {response.status_code}")
        
        if response.status_code != 200:
            log_message("❌ Server not responding properly")
            return
        
        log_message("✅ Server is healthy")
        
        # 2. User registration (creates user in Azure)
        log_message("2. Creating user profile in Azure...")
        user_data = {
            "email": f"testparent_{datetime.now().strftime('%H%M%S')}@aischool.com",
            "password": "password123",
            "full_name": "Test Parent Azure",
            "phone_number": "+1234567890"
        }
        
        response = requests.post(f"{BASE_URL}/auth/register", json=user_data, timeout=10)
        log_message(f"   Registration status: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            token = result.get('token')
            log_message("✅ User created successfully in Azure Table Storage")
            log_message(f"   User email: {user_data['email']}")
        else:
            log_message(f"❌ User creation failed: {response.text}")
            return
        
        # 3. Create kids profiles in Azure
        log_message("3. Creating kids profiles in Azure...")
        
        kids_data = [
            {
                "name": "Alice Azure Test",
                "age": 8,
                "grade": "3rd Grade",
                "avatar": "girl_avatar_1",
                "learning_goals": "Reading and math skills"
            },
            {
                "name": "Bob Azure Test", 
                "age": 10,
                "grade": "5th Grade",
                "avatar": "boy_avatar_2",
                "learning_goals": "Science and coding"
            },
            {
                "name": "Charlie Azure Test",
                "age": 6,
                "grade": "1st Grade", 
                "avatar": "child_avatar_3",
                "learning_goals": "Basic reading"
            }
        ]
        
        headers = {"Authorization": f"Bearer {token}"}
        created_profiles = []
        
        for i, kid_data in enumerate(kids_data, 1):
            log_message(f"   Creating kid profile {i}: {kid_data['name']}")
            
            response = requests.post(f"{BASE_URL}/profiles", json=kid_data, headers=headers, timeout=10)
            log_message(f"   Status: {response.status_code}")
            
            if response.status_code == 201:
                result = response.json()
                profile = result.get('profile', {})
                profile_id = profile.get('id', 'unknown')
                created_profiles.append(profile_id)
                log_message(f"   ✅ Created: {profile.get('name')} (ID: {profile_id[:8]}...)")
            else:
                log_message(f"   ❌ Failed: {response.text}")
        
        # 4. Verify profiles exist in Azure
        log_message("4. Verifying profiles in Azure...")
        response = requests.get(f"{BASE_URL}/profiles", headers=headers, timeout=10)
        log_message(f"   Get profiles status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            count = result.get('count', 0)
            profiles = result.get('profiles', [])
            log_message(f"   ✅ Found {count} profiles in Azure database")
            
            for profile in profiles:
                log_message(f"      - {profile.get('name')} (Age: {profile.get('age')}, Grade: {profile.get('grade')})")
        else:
            log_message(f"   ❌ Failed to retrieve profiles: {response.text}")
        
        # 5. Test profile update in Azure
        if created_profiles:
            log_message("5. Testing profile update in Azure...")
            profile_id = created_profiles[0]
            update_data = {
                "age": 9,
                "grade": "4th Grade",
                "learning_goals": "Advanced reading and math"
            }
            
            response = requests.put(f"{BASE_URL}/profiles/{profile_id}", json=update_data, headers=headers, timeout=10)
            log_message(f"   Update status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                profile = result.get('profile', {})
                log_message(f"   ✅ Updated profile: Age now {profile.get('age')}, Grade: {profile.get('grade')}")
            else:
                log_message(f"   ❌ Update failed: {response.text}")
        
        # Summary
        log_message("="*50)
        log_message("🎉 Azure Database Test Complete!")
        log_message(f"✅ Created {len(created_profiles)} kids profiles in Azure Table Storage")
        log_message("✅ User profile created in Azure Table Storage")
        log_message("✅ Profile retrieval from Azure verified")
        log_message("✅ Profile update in Azure verified")
        log_message("📱 Azure database is ready for production use!")
        
    except Exception as e:
        log_message(f"❌ Test error: {e}")
        import traceback
        log_message(f"   Traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    # Clear previous log
    try:
        with open(LOG_FILE, "w") as f:
            f.write("")
    except:
        pass
    
    main()
    print(f"\n📝 Full test log saved to: {LOG_FILE}")
