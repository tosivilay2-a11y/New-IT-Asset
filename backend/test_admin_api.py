"""
Test Admin API Endpoints
Verifies all admin routes are working correctly
"""
import requests
import json

API_BASE_URL = 'http://localhost:8000'

def test_endpoint(method, endpoint, data=None, description=""):
    """Test a single endpoint"""
    url = f"{API_BASE_URL}{endpoint}"
    
    try:
        if method == 'GET':
            response = requests.get(url)
        elif method == 'POST':
            response = requests.post(url, json=data)
        else:
            return False, "Unknown method"
        
        if response.status_code in [200, 201]:
            return True, f"✅ {description}"
        else:
            return False, f"❌ {description} - Status: {response.status_code}"
    except requests.exceptions.ConnectionError:
        return False, f"❌ {description} - Cannot connect to backend"
    except Exception as e:
        return False, f"❌ {description} - Error: {str(e)}"

def main():
    print("=" * 70)
    print("ADMIN API ENDPOINT TESTS")
    print("=" * 70)
    print()
    
    # Check if backend is running
    print("🔌 Checking backend connection...")
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Backend is running")
            print(f"   Version: {response.json().get('version', 'unknown')}")
        else:
            print("❌ Backend returned unexpected status")
            return
    except:
        print("❌ Cannot connect to backend at http://localhost:8000")
        print("   Please start the backend server first:")
        print("   cd backend")
        print("   venv\\Scripts\\activate")
        print("   uvicorn app.main:app --reload --port 8000")
        return
    
    print()
    print("=" * 70)
    print("TESTING ADMIN ENDPOINTS")
    print("=" * 70)
    print()
    
    tests = [
        # Countries
        ('GET', '/countries', None, 'Get all countries'),
        
        # Provinces
        ('GET', '/provinces', None, 'Get all provinces'),
        ('GET', '/provinces?country_id=1', None, 'Get provinces by country'),
        
        # Companies
        ('GET', '/companies', None, 'Get all companies'),
        ('GET', '/companies?province_id=1', None, 'Get companies by province'),
        
        # Main Categories
        ('GET', '/main-categories', None, 'Get all main categories'),
        
        # Asset Utils
        ('POST', '/asset-utils/preview-asset-id', {
            'main_category': 'Monitor',
            'country_id': 1,
            'province_id': 1,
            'company_id': 1
        }, 'Preview asset ID'),
        
        ('POST', '/asset-utils/generate-qr-code', {
            'asset_id': 'MLALPBAVIS25001',
            'asset_name': 'Test Monitor'
        }, 'Generate QR code'),
        
        ('GET', '/asset-utils/next-sequence/1/1', None, 'Get next sequence'),
        
        ('GET', '/asset-utils/validate-asset-id/MLALPBAVIS25001', None, 'Validate asset ID'),
    ]
    
    passed = 0
    failed = 0
    
    for method, endpoint, data, description in tests:
        success, message = test_endpoint(method, endpoint, data, description)
        print(message)
        if success:
            passed += 1
        else:
            failed += 1
    
    print()
    print("=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Total tests: {passed + failed}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print()
    
    if failed == 0:
        print("🎉 All admin API endpoints are working correctly!")
        print()
        print("You can now:")
        print("  1. Access admin page: http://localhost:3000/admin/config")
        print("  2. View API docs: http://localhost:8000/docs")
        print("  3. Test endpoints interactively in the docs")
    else:
        print("⚠️  Some endpoints failed. Please check:")
        print("  1. Backend is running")
        print("  2. Database tables are created")
        print("  3. Data is seeded")
        print()
        print("Run setup script:")
        print("  setup-admin-complete.bat")
    
    print()
    print("=" * 70)

if __name__ == "__main__":
    main()
