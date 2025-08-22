# 🎓 AI School Server - Kids Learning Platform

**Repository:** `https://github.com/cloudxcent/ai_school_server.git`

A comprehensive educational platform with Android mobile app and Python Flask backend server, featuring user authentication, kids profile management, and Azure cloud integration.

## 📱 **Project Overview**

AI School is a modern educational platform designed for parents to manage their children's learning profiles and track educational progress. The system consists of:

- **🖥️ Python Flask Backend Server**: RESTful API with Azure Table Storage
- **📱 Android Mobile App**: Native Android application for parents and kids  
- **☁️ Azure Cloud Integration**: Secure data storage and scalable infrastructure

## 🚀 **Features**

### 🖥️ **Backend Server Features**
- ✅ RESTful API with Flask & FastAPI alternatives
- ✅ Azure Table Storage integration
- ✅ JWT authentication system  
- ✅ Password hashing with bcrypt
- ✅ Input validation and error handling
- ✅ CORS support for cross-origin requests
- ✅ Comprehensive API testing suite
- ✅ Kids profile management (CRUD operations)

### 📱 **Android App Features**
- ✅ User registration and authentication
- ✅ JWT token-based security
- ✅ Kids profile management interface
- ✅ Real-time server connectivity testing
- ✅ Modern Material Design UI
- ✅ Secure local storage for user sessions

### ☁️ **Azure Integration**
- ✅ Azure Table Storage for data persistence
- ✅ Scalable cloud infrastructure  
- ✅ Secure connection string management
- ✅ Production-ready configuration

## 🏗️ **Architecture**

```
📱 Android App (Frontend)
    ↕️ HTTP/HTTPS (REST API)
🖥️ Flask/FastAPI Server (Backend)
    ↕️ Azure SDK
☁️ Azure Table Storage (Database)
```

## 📊 **API Endpoints**

### Authentication
- `GET /api/health` - Server health check
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/user` - Get user info
- `POST /api/auth/logout` - User logout

### Kids Profiles Management
- `GET /api/profiles` - List all kids profiles
- `POST /api/profiles` - Create new kid profile
- `GET /api/profiles/{id}` - Get specific profile
- `PUT /api/profiles/{id}` - Update profile
- `DELETE /api/profiles/{id}` - Delete profile

## 🛠️ **Technology Stack**

### Backend Server
- **Python 3.13+** - Programming language
- **Flask** - Primary web framework
- **FastAPI** - Alternative async framework
- **Azure Storage SDK** - Cloud storage integration
- **PyJWT** - JWT token management
- **bcrypt** - Password hashing
- **Requests** - HTTP client for testing

### Android Application
- **Java** - Programming language
- **Android SDK 34** - Target platform
- **Retrofit 2** - HTTP client library
- **Gson** - JSON parsing
- **Material Design** - UI components
- **SharedPreferences** - Local storage

### Cloud & DevOps
- **Azure Table Storage** - NoSQL database
- **Git** - Version control
- **GitHub** - Repository hosting
- **VS Code** - Development environment

## 🔧 **Quick Start**

### Prerequisites
- Python 3.13+
- Azure Storage Account
- Android Studio (for mobile app)
- Git

### 🖥️ **Backend Server Setup**
```bash
# Clone repository
git clone https://github.com/cloudxcent/ai_school_server.git
cd ai_school_server

# Navigate to backend
cd backend

# Install dependencies
pip install -r requirements.txt

# Configure Azure (set environment variable)
# AZURE_STORAGE_CONNECTION_STRING=your_connection_string

# Run Flask server
python app.py

# Or run FastAPI server
python fastapi_app.py

# Server runs on http://localhost:5000
```

### 📱 **Android App Setup**
```bash
# Open Android Studio
# Import project from: /android
# Update server IP in ApiClient.java
# Build and run application
```

## 🧪 **Testing**

### Run Comprehensive Tests
```bash
cd backend

# Test Azure connection
python test_azure_connection.py

# Test kids profiles API
python test_kids_profiles.py

# Test all endpoints
python test_api.py

# Run setup verification
python test_setup.py
```

### Test Results
- ✅ Authentication system verified
- ✅ Kids profile CRUD operations tested
- ✅ Azure database integration confirmed
- ✅ API endpoints validated
- ✅ Security measures tested

## 📈 **Project Status**

### ✅ **Completed Features:**
- Complete authentication system with JWT
- Kids profile management with full CRUD
- Azure Table Storage integration
- Android application with Material UI
- Comprehensive API testing suite
- Security implementation (bcrypt, validation)
- Multi-framework support (Flask + FastAPI)
- Production-ready configuration

### 🚧 **Future Development:**
- Learning content management system
- Educational progress tracking
- Interactive learning games
- Push notifications
- Advanced reporting dashboard
- Multi-language support

## 🔐 **Security Features**

- 🔒 JWT token authentication
- 🔐 bcrypt password hashing
- 🛡️ Input validation and sanitization
- 🔑 Azure secure credential management
- 🚫 CORS protection
- 📝 Request logging and monitoring

## 📝 **Configuration**

### Environment Variables
```bash
# Required for Azure integration
AZURE_STORAGE_CONNECTION_STRING=your_azure_connection_string

# Optional configurations
SECRET_KEY=your_secret_key
DEBUG=False
PORT=5000
```

### Android Configuration
```java
// Update in ApiClient.java
private static final String BASE_URL = "http://YOUR_SERVER_IP:5000/api/";
```

## 🤝 **Contributing**

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 **Support & Contact**

- **Repository Issues**: [GitHub Issues](https://github.com/cloudxcent/ai_school_server/issues)
- **Documentation**: Available in `/docs` folder
- **API Documentation**: `/docs/API.md`
- **Azure Setup**: `/docs/Azure-Setup.md`

## 🌟 **Acknowledgments**

- Azure Cloud Platform for reliable storage
- Flask & FastAPI communities
- Android development ecosystem
- Open source contributors

---

**🎓 Built with ❤️ for kids' education and learning**

**👨‍💻 Maintained by:** [cloudxcent](https://github.com/cloudxcent)
- User registration and login
- Azure Table Storage integration
- Secure password hashing
- JWT token authentication
- RESTful API endpoints

## Backend API Endpoints
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/profile` - Get user profile (authenticated)
- `POST /api/auth/logout` - User logout

## Setup Instructions

### Backend Setup
1. Navigate to the backend directory
2. Install dependencies: `pip install -r requirements.txt`
3. Configure Azure Storage connection string
4. Run the server: `python app.py`

### Azure Storage Setup
1. Create an Azure Storage Account
2. Get the connection string
3. Update the configuration file with your credentials

## Environment Variables
Create a `.env` file in the backend directory with:
```
AZURE_STORAGE_CONNECTION_STRING=your_connection_string_here
SECRET_KEY=your_secret_key_here
FLASK_ENV=development
```

## Dependencies
- Flask
- azure-data-tables
- bcrypt
- PyJWT
- python-dotenv

## Development Status
- [x] Project structure created
- [x] Backend authentication server
- [ ] Android app development
- [ ] Testing and deployment
