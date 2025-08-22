#!/usr/bin/env python3
"""
Azure Database Test Runner
Creates user profiles and kids profiles in Azure Table Storage
"""
import subprocess
import sys
import time

def run_azure_test():
    print("🚀 Starting Azure Database Test...")
    print("="*60)
    
    try:
        # Run the test
        result = subprocess.run([
            "C:/Users/Hp/AppData/Local/Programs/Python/Python313/python.exe", 
            "simple_test.py"
        ], 
        cwd="d:\\AI School App for TV and Mobile\\ai_school\\backend",
        capture_output=True, 
        text=True, 
        timeout=60
        )
        
        print("STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("\nSTDERR:")
            print(result.stderr)
        
        print(f"\nReturn code: {result.returncode}")
        
        if result.returncode == 0:
            print("✅ Test completed successfully!")
        else:
            print("❌ Test failed!")
            
    except subprocess.TimeoutExpired:
        print("⏰ Test timed out after 60 seconds")
    except Exception as e:
        print(f"❌ Error running test: {e}")

if __name__ == "__main__":
    run_azure_test()
