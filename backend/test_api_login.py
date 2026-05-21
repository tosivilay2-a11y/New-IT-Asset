#!/usr/bin/env python
"""Test login API endpoint"""
import requests
import json

def test_api_login():
    url = "http://localhost:8000/auth/login"
    
    # Test credentials
    credentials = {
        "username": "admin@example.com",  # FastAPI OAuth2 uses 'username' field
        "password": "admin123"
    }
    
    print("Testing login API endpoint...")
    print(f"URL: {url}")
    print(f"Credentials: {credentials['username']}")
    
    try:
        # Send login request
        response = requests.post(
            url,
            data=credentials,  # OAuth2 expects form data, not JSON
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        print(f"\nResponse Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✓ Login successful!")
            print(f"  Access Token: {data.get('access_token', 'N/A')[:50]}...")
            print(f"  Token Type: {data.get('token_type', 'N/A')}")
            return True
        else:
            print("✗ Login failed!")
            print(f"  Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

if __name__ == "__main__":
    import sys
    success = test_api_login()
    sys.exit(0 if success else 1)
