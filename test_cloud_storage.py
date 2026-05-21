#!/usr/bin/env python3

import requests
import json
import io

def test_cloud_storage():
    """Test the new cloud storage service"""
    
    # First login to get token
    login_url = "http://localhost:8000/auth/login"
    login_data = {
        'username': 'admin@example.com',
        'password': 'admin123'
    }
    
    print("=== TESTING CLOUD STORAGE SERVICE ===")
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
        print("\n2. Testing cloud storage with file upload...")
        
        # Create a test PDF file content
        test_pdf_content = b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Pages\n/Kids [3 0 R]\n/Count 1\n>>\nendobj\n3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/MediaBox [0 0 612 792]\n>>\nendobj\nxref\n0 4\n0000000000 65535 f \n0000000009 00000 n \n0000000074 00000 n \n0000000120 00000 n \ntrailer\n<<\n/Size 4\n/Root 1 0 R\n>>\nstartxref\n179\n%%EOF"
        
        # Asset data
        asset_data = {
            'main_category': 'Computer',
            'country_id': 1,
            'province_id': 1,
            'company_id': 1,
            'purchase_date': '2026-05-07',
            'assetname': 'Cloud Storage Test Asset',
            'status': 'Available',
            'manufacturer': 'Dell',
            'modelnumber': 'OptiPlex 7090',
            'serialnumber': 'CLOUDTEST123',
            'purchaseprice': 2000,
            'currentvalue': 1800,
            'condition': 'Excellent',
            'notes': 'Test asset for cloud storage integration',
            'po_number': 'PO-2026-CLOUD-001',
            'cost_center': 'IT-CLOUD'
        }
        
        # Prepare multipart form data
        files = {
            'po_attachment': ('cloud_test_po.pdf', io.BytesIO(test_pdf_content), 'application/pdf')
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
            print("✅ Asset with cloud storage created successfully!")
            asset_response = response.json()
            print(f"Asset ID: {asset_response.get('assetid')}")
            print(f"Asset Code: {asset_response.get('assetcode')}")
            print(f"Asset Name: {asset_response.get('assetname')}")
            print(f"PO Number: {asset_response.get('po_number')}")
            print(f"PO Attachment Path/URL: {asset_response.get('po_attachment_path')}")
            
            # Check storage type
            attachment_path = asset_response.get('po_attachment_path')
            if attachment_path:
                if attachment_path.startswith(('http://', 'https://')):
                    print("✅ File stored in cloud storage (URL returned)")
                else:
                    print("✅ File stored in local storage (path returned)")
            
        else:
            print(f"❌ Asset creation with cloud storage failed: {response.status_code}")
            print("Response:", response.text)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    test_cloud_storage()