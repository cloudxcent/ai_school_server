# 📱 Android App Setup Instructions

## 🛠️ Required Steps to Run on Your Mobile Device

### 1. **Import Project in Android Studio**
1. Open Android Studio
2. Click "Open an existing project"
3. Navigate to: `D:\AI School App for TV and Mobile\ai_school\android`
4. Click "OK" to import

### 2. **Configure Network Connection**

#### For Android Emulator:
- Keep the current setting in `ApiClient.java`: `http://10.0.2.2:8000/`

#### For Physical Device:
1. **Find your computer's IP address:**
   ```cmd
   ipconfig
   ```
   Look for "IPv4 Address" (usually starts with 192.168.x.x)

2. **Update ApiClient.java:**
   - Open `android/app/src/main/java/com/aischool/app/ApiClient.java`
   - Change line 9:
   ```java
   // From:
   private static final String BASE_URL = "http://10.0.2.2:8000/";
   
   // To (replace with your actual IP):
   private static final String BASE_URL = "http://192.168.1.100:8000/";
   ```

### 3. **Start Backend Server**
Ensure your FastAPI backend is running:
```cmd
cd "D:\AI School App for TV and Mobile\ai_school\backend"
python fastapi_app.py
```

### 4. **Device Preparation**

#### For Physical Device:
1. **Enable Developer Options:**
   - Go to Settings > About Phone
   - Tap "Build Number" 7 times
   - Developer Options will appear in Settings

2. **Enable USB Debugging:**
   - Go to Settings > Developer Options
   - Turn on "USB Debugging"

3. **Connect Device:**
   - Connect phone to computer via USB
   - Allow USB debugging when prompted

### 5. **Network Configuration**

#### For Physical Device Testing:
1. **Same WiFi Network:** Ensure both your computer and phone are on the same WiFi network
2. **Firewall:** Windows may block the connection - allow Python through firewall if prompted
3. **Test Connection:** Visit `http://YOUR_IP:8000/docs` on your phone's browser to verify

### 6. **Build and Run**
1. In Android Studio, select your device (emulator or physical)
2. Click the green "Run" button (▶️)
3. App will install and launch automatically

## 📱 App Features

### Registration Screen:
- Username, Password, Email, Full Name, Date of Birth, Location
- Connects to your FastAPI `/register` endpoint

### Login Screen:
- Username and Password
- Connects to your FastAPI `/login` endpoint
- Stores JWT token locally

### Profile Screen:
- Displays user information from `/profile` endpoint
- Logout functionality

## 🔧 Troubleshooting

### Common Issues:

1. **"Network Error"**
   - Check if backend server is running on port 8000
   - Verify IP address in ApiClient.java
   - Ensure same WiFi network

2. **"Connection Refused"**
   - Check Windows Firewall settings
   - Try accessing `http://YOUR_IP:8000/docs` from phone browser

3. **Build Errors**
   - Sync project with Gradle files
   - Clean and rebuild project

### Testing Steps:
1. Start FastAPI server: `python fastapi_app.py`
2. Build and run Android app
3. Try registering a new user
4. Test login with the registered credentials
5. View profile information
6. Test logout functionality

## 📋 File Structure Created:
```
android/
├── app/
│   ├── build.gradle                    # App dependencies
│   └── src/main/
│       ├── AndroidManifest.xml         # App permissions
│       ├── java/com/aischool/app/
│       │   ├── MainActivity.java       # Login/Register UI
│       │   ├── ProfileActivity.java    # User profile
│       │   ├── User.java              # User model
│       │   ├── ApiResponse.java       # API response model
│       │   ├── ApiService.java        # API endpoints
│       │   └── ApiClient.java         # Network configuration
│       └── res/
│           ├── layout/
│           │   ├── activity_main.xml   # Login/Register layout
│           │   └── activity_profile.xml # Profile layout
│           ├── drawable/               # Button styles
│           └── values/
│               └── strings.xml         # App strings
└── build.gradle                       # Project configuration
```

Your Android app is now ready to connect to your FastAPI backend! 🚀
