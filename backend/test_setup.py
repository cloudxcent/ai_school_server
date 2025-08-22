#!/usr/bin/env python3
"""
Test script to verify AI School backend setup
"""

import sys
import os

def test_imports():
    """Test that all required packages can be imported"""
    print("Testing package imports...")
    
    try:
        import flask
        print("✓ Flask imported successfully")
    except ImportError as e:
        print(f"✗ Flask import failed: {e}")
        return False
    
    try:
        import bcrypt
        print("✓ bcrypt imported successfully")
    except ImportError as e:
        print(f"✗ bcrypt import failed: {e}")
        return False
    
    try:
        import jwt
        print("✓ PyJWT imported successfully")
    except ImportError as e:
        print(f"✗ PyJWT import failed: {e}")
        return False
    
    try:
        from azure.data.tables import TableServiceClient
        print("✓ Azure Data Tables imported successfully")
    except ImportError as e:
        print(f"✗ Azure Data Tables import failed: {e}")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✓ python-dotenv imported successfully")
    except ImportError as e:
        print(f"✗ python-dotenv import failed: {e}")
        return False
    
    return True

def test_project_structure():
    """Test that project structure is correct"""
    print("\nTesting project structure...")
    
    required_files = [
        'app.py',
        'requirements.txt',
        '.env.example',
        'config/settings.py',
        'models/user.py',
        'auth/utils.py'
    ]
    
    all_files_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✓ {file_path} exists")
        else:
            print(f"✗ {file_path} missing")
            all_files_exist = False
    
    return all_files_exist

def test_configuration():
    """Test configuration setup"""
    print("\nTesting configuration...")
    
    if os.path.exists('.env.example'):
        print("✓ .env.example template exists")
    else:
        print("✗ .env.example template missing")
        return False
    
    if os.path.exists('.env'):
        print("✓ .env file exists")
        print("⚠️  Remember to update .env with your Azure credentials")
    else:
        print("⚠️  .env file not found - you'll need to create it from .env.example")
    
    return True

def main():
    """Main test function"""
    print("AI School Backend Setup Test")
    print("=" * 40)
    
    # Test imports
    imports_ok = test_imports()
    
    # Test project structure
    structure_ok = test_project_structure()
    
    # Test configuration
    config_ok = test_configuration()
    
    print("\n" + "=" * 40)
    if imports_ok and structure_ok and config_ok:
        print("🎉 All tests passed! Backend setup is complete.")
        print("\nNext steps:")
        print("1. Copy .env.example to .env")
        print("2. Update .env with your Azure Storage credentials")
        print("3. Run 'python app.py' to start the server")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == '__main__':
    main()
