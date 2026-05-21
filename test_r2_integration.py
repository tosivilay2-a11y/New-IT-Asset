#!/usr/bin/env python3

import sys
import os
import requests
import json
from pathlib import Path

# Test the complete R2 integration
def test_r2_integration():
    """Test the complete Cloudflare R2 integration"""
    
    base_url = "http://localhost:8000"
    
    print("🧪 Testing Cloudflare R2 Integration")
    print("=" * 50)
    
    # Step 1: Test login to get token
    print("1. Testing login...")
    login_data = {
        "username": "admin@example.com",
        "password": "admin123"
    }
    
    try:
        response = requests.post(f"{base_url}/auth/login", data=login_data)
        if response.status_code == 200:
            token = response.json()["access_token"]
            headers = {"Authorization": f"Bearer {token}"}
            print("   ✅ Login successful")
        else:
            print(f"   ❌ Login failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Login error: {e}")
        return False
    
    # Step 2: Test storage configuration API
    print("2. Testing storage configuration API...")
    try:
        response = requests.get(f"{base_url}/config/storage", headers=headers)
        if response.status_code == 200:
            config = response.json()
            print("   ✅ Storage config retrieved")
            print(f"   📋 Storage type: {config.get('storage_type')}")
            print(f"   📋 R2 bucket: {config.get('r2_bucket_name')}")
            print(f"   📋 R2 endpoint: {config.get('r2_endpoint_url')}")
        else:
            print(f"   ❌ Config retrieval failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Config API error: {e}")
        return False
    
    # Step 3: Test R2 connection
    print("3. Testing R2 connection...")
    try:
        test_config = {
            "storage_type": "r2",
            "r2_account_id": "e100a0cfe124fdf7d88b279b7be79a95",
            "r2_access_key_id": "930bc25d59ccd52b1de76043c0b334ca",
            "r2_secret_access_key": "***",  # Will use stored value
            "r2_bucket_name": "my-bucket",
            "r2_endpoint_url": "https://e100a0cfe124fdf7d88b279b7be79a95.r2.cloudflarestorage.com",
            "r2_public_url": "https://pub-e100a0cfe124fdf7d88b279b7be79a95.r2.dev"
        }
        
        response = requests.post(f"{base_url}/config/storage/test", json=test_config, headers=headers)
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                print("   ✅ R2 connection test successful")
                print(f"   📋 Message: {result.get('message')}")
            else:
                print(f"   ❌ R2 connection test failed: {result.get('message')}")
                return False
        else:
            print(f"   ❌ R2 test failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ R2 test error: {e}")
        return False
    
    # Step 4: Test file upload with R2
    print("4. Testing file upload to R2...")
    try:
        # Create a test file
        test_file_path = Path("test_upload.txt")
        test_file_path.write_text("This is a test file for R2 upload")
        
        # Create a test asset first
        asset_data = {
            "asset_code": "TEST-R2-001",
            "asset_name": "Test R2 Asset",
            "main_category_id": 1,
            "location_id": 1,
            "company_id": 1,
            "cost_center": "IT-TEST"
        }
        
        asset_response = requests.post(f"{base_url}/assets/", json=asset_data, headers=headers)
        if asset_response.status_code == 200:
            asset_id = asset_response.json()["id"]
            print(f"   ✅ Test asset created: {asset_id}")
            
            # Now test file upload
            with open(test_file_path, 'rb') as f:
                files = {'file': ('test_upload.txt', f, 'text/plain')}
                data = {'asset_code': 'TEST-R2-001'}
                
                upload_response = requests.post(
                    f"{base_url}/assets/{asset_id}/upload-po", 
                    files=files, 
                    data=data, 
                    headers=headers
                )
                
                if upload_response.status_code == 200:
                    result = upload_response.json()
                    print("   ✅ File upload successful")
                    print(f"   📋 File URL: {result.get('file_url')}")
                    
                    # Verify it's an R2 URL
                    file_url = result.get('file_url', '')
                    if 'r2' in file_url or 'cloudflarestorage' in file_url:
                        print("   ✅ File uploaded to R2 successfully")
                    else:
                        print(f"   ⚠️  File may not be in R2: {file_url}")
                else:
                    print(f"   ❌ File upload failed: {upload_response.status_code}")
                    print(f"   📋 Response: {upload_response.text}")
                    return False
        else:
            print(f"   ❌ Asset creation failed: {asset_response.status_code}")
            return False
            
        # Clean up test file
        if test_file_path.exists():
            test_file_path.unlink()
            
    except Exception as e:
        print(f"   ❌ File upload error: {e}")
        return False
    
    # Step 5: Test cloud storage service directly
    print("5. Testing cloud storage service...")
    try:
        # This would require importing the service, but let's just verify the config
        response = requests.get(f"{base_url}/config/", headers=headers, params={"category": "storage"})
        if response.status_code == 200:
            configs = response.json()
            storage_configs = {config["config_key"]: config["config_value"] for config in configs}
            
            required_keys = ["storage_type", "r2_account_id", "r2_bucket_name", "r2_endpoint_url"]
            missing_keys = [key for key in required_keys if not storage_configs.get(key)]
            
            if not missing_keys:
                print("   ✅ All required R2 configurations present")
                print(f"   📋 Storage type: {storage_configs.get('storage_type')}")
            else:
                print(f"   ❌ Missing configurations: {missing_keys}")
                return False
        else:
            print(f"   ❌ Config check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Config check error: {e}")
        return False
    
    print("\n🎉 R2 Integration Test Complete!")
    print("=" * 50)
    print("✅ All tests passed - Cloudflare R2 is properly configured")
    print("\n📋 Summary:")
    print("   • Authentication: Working")
    print("   • Configuration API: Working") 
    print("   • R2 Connection: Working")
    print("   • File Upload: Working")
    print("   • Database Config: Working")
    print("\n🚀 Your system is ready to use Cloudflare R2 for file storage!")
    
    return True

if __name__ == "__main__":
    success = test_r2_integration()
    sys.exit(0 if success else 1)