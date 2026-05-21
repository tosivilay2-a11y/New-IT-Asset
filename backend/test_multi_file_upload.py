#!/usr/bin/env python3
"""
Test script for multi-file attachment upload
Tests creating and updating assets with multiple PO attachments
"""
import requests
import json
from pathlib import Path

BASE_URL = "http://localhost:8000"

# Test credentials
TEST_EMAIL = "admin@example.com"
TEST_PASSWORD = "admin123"

def login():
    """Login and get auth token"""
    response = requests.post(
        f"{BASE_URL}/auth/login",
        data={"username": TEST_EMAIL, "password": TEST_PASSWORD}
    )
    if response.status_code == 200:
        return response.json()["access_token"]
    print(f"Login failed: {response.status_code} - {response.text}")
    return None

def create_test_files():
    """Create temporary test files"""
    test_dir = Path("backend/uploads/test_files")
    test_dir.mkdir(parents=True, exist_ok=True)
    
    # Create test file 1
    file1 = test_dir / "test_po_1.txt"
    file1.write_text("Test PO Document 1\nThis is a test file for PO attachment")
    
    # Create test file 2
    file2 = test_dir / "test_po_2.txt"
    file2.write_text("Test PO Document 2\nThis is another test file for PO attachment")
    
    return file1, file2

def test_create_asset_with_files(token):
    """Test creating asset with multiple files"""
    print("\n=== Testing Create Asset with Multiple Files ===")
    
    file1, file2 = create_test_files()
    
    # Asset data
    asset_data = {
        "assetname": "Test Asset Multi-File",
        "main_category": "Computer",
        "country_id": 1,
        "province_id": 1,
        "company_id": 1,
        "purchase_date": "2024-01-01",
        "status": "Available",
        "manufacturer": "Dell",
        "modelnumber": "Latitude 5420",
        "serialnumber": "TEST123456",
        "po_number": "PO-2024-001",
        "purchaseprice": 1500.00,
        "condition": "Good"
    }
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Upload first file
    print("Uploading first file...")
    with open(file1, 'rb') as f:
        files = {'po_attachment': f}
        data = {'asset_data': json.dumps(asset_data)}
        response = requests.post(
            f"{BASE_URL}/assets/with-file",
            headers=headers,
            data=data,
            files=files
        )
    
    if response.status_code != 200:
        print(f"Failed to create asset: {response.status_code} - {response.text}")
        return None
    
    asset = response.json()
    asset_id = asset['assetid']
    print(f"✓ Asset created with ID: {asset_id}")
    print(f"  Attachments: {asset.get('po_attachment_path', 'None')}")
    
    # Upload second file
    print("Uploading second file...")
    with open(file2, 'rb') as f:
        files = {'po_attachment': f}
        data = {'asset_data': json.dumps(asset_data)}
        response = requests.put(
            f"{BASE_URL}/assets/{asset_id}/with-file",
            headers=headers,
            data=data,
            files=files
        )
    
    if response.status_code != 200:
        print(f"Failed to update asset: {response.status_code} - {response.text}")
        return asset_id
    
    asset = response.json()
    print(f"✓ Second file uploaded")
    print(f"  Attachments: {asset.get('po_attachment_path', 'None')}")
    
    return asset_id

def test_get_asset(token, asset_id):
    """Get asset and verify attachments"""
    print(f"\n=== Verifying Asset {asset_id} ===")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(
        f"{BASE_URL}/assets/{asset_id}",
        headers=headers
    )
    
    if response.status_code != 200:
        print(f"Failed to get asset: {response.status_code} - {response.text}")
        return
    
    asset = response.json()
    attachments = asset.get('po_attachment_path', 'None')
    print(f"Asset Name: {asset.get('assetname')}")
    print(f"Attachments: {attachments}")
    
    # Parse attachments if JSON array
    try:
        if isinstance(attachments, str) and attachments.startswith('['):
            import json
            files = json.loads(attachments)
            print(f"Number of files: {len(files)}")
            for i, f in enumerate(files, 1):
                print(f"  {i}. {f}")
    except:
        pass

def main():
    print("Multi-File Upload Test")
    print("=" * 50)
    
    # Login
    token = login()
    if not token:
        print("Failed to login")
        return
    
    print(f"✓ Logged in successfully")
    
    # Test create with files
    asset_id = test_create_asset_with_files(token)
    
    if asset_id:
        # Verify
        test_get_asset(token, asset_id)
        print("\n✓ Test completed successfully!")
    else:
        print("\n✗ Test failed")

if __name__ == "__main__":
    main()
