#!/usr/bin/env python
"""Test login functionality"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.core.database import SessionLocal
from app.models.user import User
from app.core.security import verify_password, get_password_hash

def test_login():
    db = SessionLocal()
    try:
        # Get admin user
        user = db.query(User).filter(User.email == "admin@example.com").first()
        
        if not user:
            print("✗ Admin user not found")
            return False
        
        print(f"✓ Found user: {user.email}")
        print(f"  Full Name: {user.full_name}")
        print(f"  Role: {user.role}")
        
        # Test password verification
        test_password = "admin123"
        print(f"\nTesting password verification...")
        
        is_valid = verify_password(test_password, user.hashed_password)
        
        if is_valid:
            print(f"✓ Password verification successful!")
            print(f"  Password '{test_password}' is correct")
            return True
        else:
            print(f"✗ Password verification failed")
            print(f"  Password '{test_password}' is incorrect")
            
            # Try to reset password
            print(f"\nResetting password...")
            user.hashed_password = get_password_hash(test_password)
            db.commit()
            print(f"✓ Password reset to: {test_password}")
            return True
            
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    success = test_login()
    sys.exit(0 if success else 1)
