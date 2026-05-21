#!/usr/bin/env python3

import requests
import json

def check_main_categories():
    """Check what main categories exist via direct database query"""
    
    # First login to get token
    login_url = "http://localhost:8000/auth/login"
    login_data = {
        'username': 'admin@example.com',
        'password': 'admin123'
    }
    
    print("=== CHECKING MAIN CATEGORIES ===")
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
        
        # Try different endpoints to find main categories
        endpoints_to_try = [
            "/admin/main-categories",
            "/main-categories/",
            "/categories/main",
            "/asset-utils/main-categories"
        ]
        
        for endpoint in endpoints_to_try:
            print(f"\n2. Trying endpoint: {endpoint}")
            try:
                response = requests.get(f"http://localhost:8000{endpoint}", headers=headers)
                print(f"   Status: {response.status_code}")
                if response.status_code == 200:
                    data = response.json()
                    print(f"   Found {len(data)} main categories:")
                    for cat in data:
                        print(f"     - ID: {cat.get('maincategoryid')}, Name: '{cat.get('categoryname')}'")
                    return
                else:
                    print(f"   Error: {response.text}")
            except Exception as e:
                print(f"   Exception: {e}")
        
        print("\n3. No main categories endpoint found. Let's create some test categories.")
        
        # Try to create a main category
        create_url = "http://localhost:8000/admin/main-categories"
        test_category = {
            "categoryname": "Computer",
            "categorycode": "COMP",
            "description": "Desktop and laptop computers",
            "isactive": True
        }
        
        print(f"4. Trying to create category: {test_category}")
        try:
            response = requests.post(create_url, json=test_category, headers=headers)
            print(f"   Create status: {response.status_code}")
            if response.status_code in [200, 201]:
                print("   ✅ Category created successfully!")
                print(f"   Response: {response.json()}")
            else:
                print(f"   ❌ Create failed: {response.text}")
        except Exception as e:
            print(f"   Exception: {e}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    check_main_categories()