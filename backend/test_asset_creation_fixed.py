#!/usr/bin/env python3

import requests
import json

def test_asset_creation():
    """Test asset creation with the fixed backend"""
    
    # First login to get token
    login_url = "http://localhost:8000/auth/login"
    login_data = {
        'username': 'admin@example.com',
        'password': 'admin123'
    }
    
    print("=== TESTING ASSET CREATION ===")
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
        
        # Test asset creation with problematic data
        asset_url = "http://localhost:8000/assets/"
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        # This is similar to what the frontend sends
        test_asset = {
            'main_category': 'Computer',  # Now this exists!
            'country_id': 1,
            'province_id': 1,
            'company_id': 1,
            'purchase_date': '2026-05-06',
            'assetname': 'Test Computer Asset',
            'status': 'Available',
            'manufacturer': 'Dell',
            'modelnumber': 'Latitude 5420',
            'serialnumber': 'TESTCOMP123',
            'purchaseprice': 1500,
            'currentvalue': 1200,
            'condition': 'Good',
            'notes': 'Test computer asset with category and location names',
            'assigneddate': '',  # Empty string - should be removed
            'warrantyexpiry': '',  # Empty string - should be removed
            'cost_center': 'IT-001'
        }
        
        print("2. Creating asset with test data...")
        print("Asset data:", json.dumps(test_asset, indent=2))
        
        response = requests.post(asset_url, json=test_asset, headers=headers)
        
        if response.status_code == 200:
            print("✅ Asset created successfully!")
            asset_data = response.json()
            print(f"Asset ID: {asset_data.get('assetid')}")
            print(f"Asset Code: {asset_data.get('assetcode')}")
            print(f"Asset Name: {asset_data.get('assetname')}")
            print(f"Created At: {asset_data.get('createdat')}")
            print(f"Purchase Date: {asset_data.get('purchasedate')}")
            print(f"Assigned Date: {asset_data.get('assigneddate')}")
            print(f"Warranty Expiry: {asset_data.get('warrantyexpiry')}")
        else:
            print(f"❌ Asset creation failed: {response.status_code}")
            print("Response:", response.text)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    test_asset_creation()