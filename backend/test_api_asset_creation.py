#!/usr/bin/env python
"""Test asset creation via API to simulate frontend calls"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash
import json

def test_api_asset_creation():
    """Test asset creation via API"""
    
    # Create test client
    client = TestClient(app)
    
    try:
        print("=" * 60)
        print("TESTING API ASSET CREATION")
        print("=" * 60)
        print()
        
        # 1. Login to get token
        print("1. Logging in...")
        login_response = client.post("/auth/login", data={
            "username": "admin@example.com",
            "password": "admin123"
        })
        
        if login_response.status_code != 200:
            print(f"✗ Login failed: {login_response.status_code}")
            print(f"Response: {login_response.text}")
            return False
        
        token_data = login_response.json()
        token = token_data["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        print("✓ Login successful")
        
        # 2. Test asset creation with typical frontend data
        print("2. Creating asset via API...")
        
        asset_data = {
            "main_category": "Monitor",  # This should be converted to maincategoryid
            "country_id": 1,
            "province_id": 1,
            "company_id": 1,
            "assetname": "Test Monitor API",
            "manufacturer": "Dell",
            "modelnumber": "U2720Q",
            "serialnumber": "ABC123456",
            "purchaseprice": 500.00,
            "cost_center": "IT-DEPT-001",
            "condition": "Good",
            "notes": "Test asset created via API"
            # Note: Not including datetime fields - they should be handled automatically
        }
        
        create_response = client.post("/assets/", 
                                    json=asset_data, 
                                    headers=headers)
        
        if create_response.status_code != 201:
            print(f"✗ Asset creation failed: {create_response.status_code}")
            print(f"Response: {create_response.text}")
            return False
        
        created_asset = create_response.json()
        print("✓ Asset created successfully via API!")
        print(f"  Asset ID: {created_asset['assetid']}")
        print(f"  Asset Code: {created_asset['assetcode']}")
        print(f"  Asset Name: {created_asset['assetname']}")
        print(f"  Cost Center: {created_asset.get('cost_center', 'N/A')}")
        print(f"  Created At: {created_asset.get('createdat', 'N/A')}")
        
        # 3. Clean up - delete the test asset
        print("3. Cleaning up...")
        delete_response = client.delete(f"/assets/{created_asset['assetid']}", 
                                      headers=headers)
        
        if delete_response.status_code == 200:
            print("✓ Test asset cleaned up")
        else:
            print(f"⚠ Cleanup warning: {delete_response.status_code}")
        
        print()
        print("=" * 60)
        print("✓ API ASSET CREATION TEST PASSED!")
        print("=" * 60)
        print()
        print("Asset creation via API works without SQLite datetime errors.")
        print("Frontend asset creation should now work properly.")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print()
        print("=" * 60)
        print("✗ API ASSET CREATION TEST FAILED")
        print("=" * 60)
        print(f"Error: {str(e)}")
        print()
        return False

if __name__ == "__main__":
    success = test_api_asset_creation()
    sys.exit(0 if success else 1)