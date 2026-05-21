"""
Test login endpoint directly
"""
import urllib.request
import urllib.parse
import json

def test_login():
    print("=" * 70)
    print("TESTING LOGIN ENDPOINT")
    print("=" * 70)
    print()
    
    # Test data
    login_data = {
        'username': 'admin@example.com',  # OAuth2 uses 'username' field
        'password': 'admin123'
    }
    
    # Encode as form data (OAuth2PasswordRequestForm expects form data)
    data = urllib.parse.urlencode(login_data).encode('utf-8')
    
    url = 'http://localhost:8000/auth/login'
    
    try:
        print(f"Sending POST request to: {url}")
        print(f"Data: {login_data}")
        print()
        
        req = urllib.request.Request(url, data=data, method='POST')
        req.add_header('Content-Type', 'application/x-www-form-urlencoded')
        
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode())
            print("✅ LOGIN SUCCESSFUL!")
            print()
            print(f"Access Token: {result.get('access_token', 'N/A')[:50]}...")
            print(f"Token Type: {result.get('token_type', 'N/A')}")
            print()
            print("=" * 70)
            print("✅ LOGIN ENDPOINT IS WORKING!")
            print("=" * 70)
            return True
            
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP Error: {e.code} - {e.reason}")
        try:
            error_body = e.read().decode()
            print(f"Error details: {error_body}")
        except:
            pass
        return False
        
    except urllib.error.URLError as e:
        print(f"❌ Connection Error: {e.reason}")
        print()
        print("Backend is not accessible at http://localhost:8000")
        print("Make sure the backend is running!")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return False

if __name__ == "__main__":
    test_login()
