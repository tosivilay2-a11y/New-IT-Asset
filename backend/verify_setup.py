"""
Quick verification script to check if the system is set up correctly
"""
import sys
from sqlalchemy import create_engine, text
from app.core.config import settings
from app.core.security import verify_password

def verify_setup():
    print("=" * 60)
    print("Asset Management System - Setup Verification")
    print("=" * 60)
    
    # Check database connection
    print("\n1. Checking database connection...")
    try:
        engine = create_engine(settings.DATABASE_URL)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("   ✓ Database connection successful")
    except Exception as e:
        print(f"   ✗ Database connection failed: {e}")
        print("   → Make sure PostgreSQL is running")
        print("   → Check DATABASE_URL in .env file")
        return False
    
    # Check if tables exist
    print("\n2. Checking database tables...")
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """))
            tables = [row[0] for row in result]
            
            required_tables = ['users', 'assets', 'categories', 'locations', 
                             'inventory_items', 'inventory_transactions', 
                             'audit_sessions', 'audit_records']
            
            missing_tables = [t for t in required_tables if t not in tables]
            
            if missing_tables:
                print(f"   ✗ Missing tables: {', '.join(missing_tables)}")
                print("   → Run: alembic upgrade head")
                return False
            else:
                print(f"   ✓ All required tables exist ({len(tables)} tables)")
    except Exception as e:
        print(f"   ✗ Error checking tables: {e}")
        return False
    
    # Check if users exist
    print("\n3. Checking for users...")
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT email, role FROM users"))
            users = result.fetchall()
            
            if not users:
                print("   ✗ No users found in database")
                print("   → Run: python seed_data.py")
                return False
            else:
                print(f"   ✓ Found {len(users)} user(s):")
                for email, role in users:
                    print(f"      - {email} ({role})")
    except Exception as e:
        print(f"   ✗ Error checking users: {e}")
        return False
    
    # Test password verification
    print("\n4. Testing authentication...")
    try:
        from app.core.database import SessionLocal
        from app.models.user import User
        
        db = SessionLocal()
        admin = db.query(User).filter(User.email == "admin@example.com").first()
        
        if admin:
            # Test password
            is_valid = verify_password("admin123", admin.hashed_password)
            if is_valid:
                print("   ✓ Admin credentials verified")
                print("   → Email: admin@example.com")
                print("   → Password: admin123")
            else:
                print("   ✗ Admin password verification failed")
        else:
            print("   ⚠ Admin user not found (but other users exist)")
            
        db.close()
    except Exception as e:
        print(f"   ✗ Error testing authentication: {e}")
        return False
    
    # Check configuration
    print("\n5. Checking configuration...")
    print(f"   Database URL: {settings.DATABASE_URL.split('@')[1] if '@' in settings.DATABASE_URL else 'configured'}")
    print(f"   Secret Key: {'configured' if settings.SECRET_KEY else 'NOT SET'}")
    print(f"   Token Expiry: {settings.ACCESS_TOKEN_EXPIRE_MINUTES} minutes")
    
    print("\n" + "=" * 60)
    print("✓ Setup verification completed successfully!")
    print("=" * 60)
    print("\nYou can now:")
    print("1. Start the backend: uvicorn app.main:app --reload")
    print("2. Access API docs: http://localhost:8000/docs")
    print("3. Login with: admin@example.com / admin123")
    print("\n")
    
    return True

if __name__ == "__main__":
    try:
        success = verify_setup()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ Verification failed with error: {e}")
        sys.exit(1)
