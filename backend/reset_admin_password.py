#!/usr/bin/env python
"""Reset admin user password"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

os.chdir(os.path.dirname(__file__))

from dotenv import load_dotenv
load_dotenv()

from app.core.database import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash

def reset_admin():
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == "admin@example.com").first()
        
        if user:
            user.hashed_password = get_password_hash("admin123")
            db.commit()
            print("✅ Admin password reset to: admin123")
        else:
            user = User(
                email="admin@example.com",
                full_name="System Administrator",
                hashed_password=get_password_hash("admin123"),
                role="admin",
                is_active=True
            )
            db.add(user)
            db.commit()
            print("✅ Admin user created: admin@example.com / admin123")
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    reset_admin()
