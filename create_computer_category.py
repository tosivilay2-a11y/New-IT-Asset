#!/usr/bin/env python3

import requests
import json

def create_computer_category():
    """Create the Computer main category"""
    
    # First login to get token
    login_url = "http://localhost:8000/auth/login"
    login_data = {
        'username': 'admin@example.com',
        'password': 'admin123'
    }
    
    print("=== CREATING COMPUTER CATEGORY ===")
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
        
        # Create Computer category
        print("\n2. Creating Computer category...")
        computer_category = {
            "categoryname": "Computer",
            "categorycode": "COMP",
            "description": "Desktop and laptop computers",
            "isactive": True
        }
        
        response = requests.post("http://localhost:8000/main-categories/", json=computer_category, headers=headers)
        
        if response.status_code in [200, 201]:
            print("✅ Computer category created successfully!")
            category_data = response.json()
            print(f"Category ID: {category_data.get('maincategoryid')}")
            print(f"Category Name: {category_data.get('categoryname')}")
            print(f"Category Code: {category_data.get('categorycode')}")
        else:
            print(f"❌ Category creation failed: {response.status_code}")
            print("Response:", response.text)
        
        # Also create other useful categories
        other_categories = [
            {"categoryname": "Printer", "categorycode": "PRNT", "description": "Printers and scanners"},
            {"categoryname": "Network Equipment", "categorycode": "NETW", "description": "Routers, switches, access points"},
            {"categoryname": "Mobile Device", "categorycode": "MOBL", "description": "Smartphones and tablets"},
            {"categoryname": "Server", "categorycode": "SRVR", "description": "Server hardware"}
        ]
        
        print("\n3. Creating additional categories...")
        for cat in other_categories:
            cat["isactive"] = True
            response = requests.post("http://localhost:8000/main-categories/", json=cat, headers=headers)
            if response.status_code in [200, 201]:
                print(f"✅ Created: {cat['categoryname']}")
            else:
                print(f"❌ Failed to create {cat['categoryname']}: {response.status_code}")
        
        # List all categories
        print("\n4. Current categories:")
        response = requests.get("http://localhost:8000/main-categories/", headers=headers)
        if response.status_code == 200:
            categories = response.json()
            for cat in categories:
                print(f"  - ID: {cat.get('maincategoryid')}, Name: '{cat.get('categoryname')}', Code: {cat.get('categorycode')}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    create_computer_category()