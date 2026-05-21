"""
Test complete login flow including /users/me
"""
import urllib.request
import urllib.parse
import json

def test_full_login():
    print("=" * 70)
    print("TESTING COMPLETE LOGIN FLOW")
    print("=" * 70)
    print()
    
    # Step 1: Login
    print("Step 1: Testing login...")
    login_data = {
        'username': 'admin@example.com',
        'password': 'admin123'
    }
    
    data = urllib.parse.urlencode(login_data).encode('utf-8')
    url = 'http://localhost:8000/auth/login'
    
    try:
        req = urllib.request.Request(url, data=data, method='POST')
        req.add_header('Content-Type', 'application/x-www-form-urlencoded')
        
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode())
            token = result.get('access_token')
            print(f"✅ Login successful!")
            print(f"   Token: {token[:50]}...")
            print()
            
            # Step 2: Get user info
            print("Step 2: Testing /users/me with token...")
            user_url = 'http://localhost:8000/users/me'
            user_req = urllib.request.Request(user_url)
            user_req.add_header('Authorization', f'Bearer {token}')
            
            with urllib.request.urlopen(user_req, timeout=10) as user_response:
                user_data = json.loads(user_response.read().decode())
                print(f"✅ User info retrieved!")
                print(f"   Email: {user_data.get('email')}")
                print(f"   Role: {user_data.get('role')}")
                print(f"   User ID: {user_data.get('userid')}")
                print()
                print("=" * 70)
                print("✅ COMPLETE LOGIN FLOW WORKING!")
                print("=" * 70)
                print()
                print("The backend is working correctly.")
                print("You can now login from the frontend!")
                return True
            
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP Error: {e.code} - {e.reason}")
        try:
            error_body = e.read().decode()
            print(f"Error details: {error_body}")
        except:
            pass
        return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_full_login()
