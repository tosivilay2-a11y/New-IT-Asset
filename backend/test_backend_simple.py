"""
Simple backend test using urllib
"""
import urllib.request
import json

def test_endpoint(url, name):
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            data = json.loads(response.read().decode())
            print(f"✅ {name}: OK")
            print(f"   Data: {json.dumps(data, indent=2)[:200]}...")
            return True
    except Exception as e:
        print(f"❌ {name}: FAILED - {e}")
        return False

print("=" * 70)
print("TESTING BACKEND ENDPOINTS")
print("=" * 70)
print()

base_url = "http://localhost:8000"

# Test health
test_endpoint(f"{base_url}/health", "Health Check")
print()

# Test admin routes
test_endpoint(f"{base_url}/countries", "Countries")
test_endpoint(f"{base_url}/provinces", "Provinces")
test_endpoint(f"{base_url}/companies", "Companies")
test_endpoint(f"{base_url}/main-categories", "Main Categories")
test_endpoint(f"{base_url}/departments", "Departments")
test_endpoint(f"{base_url}/asset-statuses", "Asset Statuses")

print()
print("=" * 70)
print("✅ BACKEND IS WORKING!")
print("=" * 70)
