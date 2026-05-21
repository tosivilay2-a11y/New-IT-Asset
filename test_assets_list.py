#!/usr/bin/env python3

import requests
import json

def test_assets_list():
    """Test the assets list API to see if category and location names are returned"""
    
    # First login to get token
    login_url = "http://localhost:8000/auth/login"
    login_data = {
        'username': 'admin@example.com',
        'password': 'admin123'
    }
    
    print("=== TESTING ASSETS LIST API ===")
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
        
        # Get assets list
        print("\n2. Getting assets list...")
        response = requests.get("http://localhost:8000/assets/", headers=headers)
        
        if response.status_code == 200:
            assets = response.json()
            print(f"✅ Found {len(assets)} assets")
            
            for i, asset in enumerate(assets):
                print(f"\n--- Asset {i+1} ---")
                print(f"Asset ID: {asset.get('assetid')}")
                print(f"Asset Code: {asset.get('assetcode')}")
                print(f"Asset Name: {asset.get('assetname')}")
                print(f"Main Category ID: {asset.get('maincategoryid')}")
                print(f"Main Category Name: {asset.get('main_category_name')}")
                print(f"Location ID: {asset.get('locationid')}")
                print(f"Location Name: {asset.get('location_name')}")
                print(f"Company ID: {asset.get('companyid')}")
                print(f"Company Name: {asset.get('company_name')}")
                print(f"Status ID: {asset.get('statusid')}")
                print(f"Status Name: {asset.get('status_name')}")
                print(f"Assigned User: {asset.get('assigned_user_name')}")
                
                # Check if the new fields are present
                if asset.get('main_category_name'):
                    print("✅ Main category name is present")
                else:
                    print("❌ Main category name is missing")
                
                if asset.get('location_name'):
                    print("✅ Location name is present")
                else:
                    print("❌ Location name is missing")
        else:
            print(f"❌ Assets list failed: {response.status_code}")
            print("Response:", response.text)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    test_assets_list()