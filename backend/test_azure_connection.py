"""
AI School Backend - Azure Connection Test
Test Azure Table Storage connection and basic functionality
"""

import os
import sys
from dotenv import load_dotenv

print("AI School - Azure Connection Test")
print("=" * 50)

# Load environment variables
load_dotenv()

# Test environment variables
print("\n1. Testing Environment Variables...")
connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
secret_key = os.getenv('SECRET_KEY')

if connection_string:
    print("✓ Azure Storage connection string loaded")
    # Mask the key for security
    masked_string = connection_string[:50] + "..." + connection_string[-20:]
    print(f"  Connection: {masked_string}")
else:
    print("❌ Azure Storage connection string not found")
    sys.exit(1)

if secret_key:
    print("✓ Secret key loaded")
else:
    print("❌ Secret key not found")

# Test Azure imports
print("\n2. Testing Azure Imports...")
try:
    from azure.data.tables import TableServiceClient, TableClient
    print("✓ Azure Data Tables imported successfully")
except ImportError as e:
    print(f"❌ Failed to import Azure Data Tables: {e}")
    sys.exit(1)

# Test Azure connection
print("\n3. Testing Azure Connection...")
try:
    table_service_client = TableServiceClient.from_connection_string(connection_string)
    print("✓ TableServiceClient created successfully")
    
    # Try to list tables (this will test the connection)
    tables = list(table_service_client.list_tables())
    print(f"✓ Connection successful - Found {len(tables)} existing tables")
    
except Exception as e:
    print(f"❌ Azure connection failed: {e}")
    sys.exit(1)

# Test table creation
print("\n4. Testing Table Operations...")
try:
    table_name = "users"
    
    # Try to create table
    try:
        table_service_client.create_table(table_name)
        print(f"✓ Table '{table_name}' created successfully")
    except Exception as e:
        if "already exists" in str(e).lower():
            print(f"✓ Table '{table_name}' already exists")
        else:
            raise e
    
    # Test table client
    table_client = TableClient.from_connection_string(connection_string, table_name)
    print(f"✓ Table client for '{table_name}' created successfully")
    
except Exception as e:
    print(f"❌ Table operations failed: {e}")
    sys.exit(1)

# Test Flask imports
print("\n5. Testing Flask Dependencies...")
try:
    from flask import Flask
    print("✓ Flask imported successfully")
    
    from flask_cors import CORS
    print("✓ Flask-CORS imported successfully")
    
    import bcrypt
    print("✓ bcrypt imported successfully")
    
    import jwt
    print("✓ PyJWT imported successfully")
    
except ImportError as e:
    print(f"❌ Flask dependency import failed: {e}")
    sys.exit(1)

print("\n" + "=" * 50)
print("🎉 All tests passed! Your AI School backend is ready to run.")
print("\nNext steps:")
print("1. Run: python app.py")
print("2. Test API at: http://localhost:5000/api/health")
print("3. Check the API documentation in docs/API.md")
print("=" * 50)
