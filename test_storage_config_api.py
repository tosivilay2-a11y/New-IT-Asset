#!/usr/bin/env python3

import requests
import json

def test_storage_config_api():
    """Test the storage configuration API"""
    
    # First login to get token
    login_url = "http://localhost:8000/auth/login"
    login_data = {
        'username': 'admin@example.com',
        'password': 'admin123'
    }
    
    print("=== TESTING STORAGE CONFIG API ===")
    print("1. Logging in...")
    
    try:
        login_response = requests.post(login_url, data=login_data, headers={
            'Content-Type': 'application/x-www-form-urlencoded'
        })
        
        if login_response.status_code != 200:
            print(f"Login failed: {login_response.status_code} - {login_response.text}")
            return
        
        token = login_response.json()['access_token']
        print("Login successful!")
        
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        # Test getting storage config
        print("\n2. Getting current storage config...")
        try:
            response = requests.get("http://localhost:8000/config/storage", headers=headers)
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                config = response.json()
                print("Current storage config:")
                print(json.dumps(config, indent=2))
            else:
                print(f"Error: {response.text}")
        except Exception as e:
            print(f"Error getting config: {e}")
        
        # Test updating storage config
        print("\n3. Testing storage config update...")
        test_config = {
            "storage_type": "local",
            "r2_account_id": "",
            "r2_access_key_id": "",
            "r2_secret_access_key": "",
            "r2_bucket_name": "",
            "r2_endpoint_url": "",
            "r2_public_url": ""
        }
        
        try:
            response = requests.post("http://localhost:8000/config/storage", json=test_config, headers=headers)
            print(f"Update status: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                print("Update result:")
                print(json.dumps(result, indent=2))
            else:
                print(f"Update error: {response.text}")
        except Exception as e:
            print(f"Error updating config: {e}")
        
        # Test connection test
        print("\n4. Testing connection test...")
        try:
            response = requests.post("http://localhost:8000/config/storage/test", json=test_config, headers=headers)
            print(f"Test status: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                print("Test result:")
                print(json.dumps(result, indent=2))
            else:
                print(f"Test error: {response.text}")
        except Exception as e:
            print(f"Error testing config: {e}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    test_storage_config_api()