#!/usr/bin/env python3

import requests
import json
import io

def test_file_upload():
    """Test file upload functionality"""
    
    # First login to get token
    login_url = "http://localhost:8000/auth/login"
    login_data = {
        'username': 'admin@example.com',
        'password': 'admin123'
    }
    
    print("=== TESTING FILE UPLOAD ===")
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
            'Authorization': f'Bearer {token}'
        }
        
        # Create test asset with file upload
        print("\n2. Creating asset with file upload...")
        
        # Create a test PDF file content
        test_pdf_content = b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Pages\n/Kids [3 0 R]\n/Count 1\n>>\nendobj\n3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/MediaBox [0 0 612 792]\n>>\nendobj\nxref\n0 4\n0000000000 65535 f \n0000000009 00000 n \n0000000074 00000 n \n0000000120 00000 n \ntrailer\n<<\n/Size 4\n/Root 1 0 R\n>>\nstartxref\n179\n%%EOF"
        
        # Asset data
        asset_data = {
            'main_category': 'Computer',
            'country_id': 1,
            'province_id': 1,
            'company_id': 1,
            'purchase_date': '2026-05-07',
            'assetname': 'Test Asset with File',
            'status': 'Available',
            'manufacturer': 'HP',
            'modelnumber': 'EliteBook 840',
            'serialnumber': 'TESTFILE123',
            'purchaseprice': 1800,
            'currentvalue': 1500,
            'condition': 'Excellent',
            'notes': 'Test asset with PO attachment',
            'po_number': 'PO-2026-001',
            'cost_center': 'IT-002'
        }
        
        # Prepare multipart form data
        files = {
            'po_attachment': ('test_po.pdf', io.BytesIO(test_pdf_content), 'application/pdf')
        }
        
        data = {
            'asset_data': json.dumps(asset_data)
        }
        
        # Test the with-file endpoint
        response = requests.post(
            "http://localhost:8000/assets/with-file", 
            files=files,
            data=data,
            headers=headers
        )
        
        if response.status_code in [200, 201]:
            print("✅ Asset with file created successfully!")
            asset_response = response.json()
            print(f"Asset ID: {asset_response.get('assetid')}")
            print(f"Asset Code: {asset_response.get('assetcode')}")
            print(f"Asset Name: {asset_response.get('assetname')}")
            print(f"PO Number: {asset_response.get('po_number')}")
            print(f"PO Attachment Path: {asset_response.get('po_attachment_path')}")
        else:
            print(f"❌ Asset creation with file failed: {response.status_code}")
            print("Response:", response.text)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    test_file_upload()