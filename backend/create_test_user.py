#!/usr/bin/env python
"""Create a test user for login"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.core.database import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash

def create_test_user():
    db = SessionLocal()
    try:
        # Check if admin user exists
        existing_user = db.query(User).filter(User.email == "admin@example.com").first()
        
        if existing_user:
            print("✓ Admin user already exists")
            print(f"  Email: {existing_user.email}")
            print(f"  Role: {existing_user.role}")
            return
        
        # Create admin user
        admin_user = User(
            email="admin@example.com",
            full_name="System Administrator",
            hashed_password=get_password_hash("admin123"),
            role="admin"
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print("✓ Admin user created successfully!")
        print(f"  Email: admin@example.com")
        print(f"  Password: admin123")
        print(f"  Role: admin")
        
    except Exception as e:
        print(f"✗ Error creating user: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_user()
