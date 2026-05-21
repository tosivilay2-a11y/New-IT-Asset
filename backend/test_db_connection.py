"""
Simple script to test PostgreSQL database connection
Run this to verify your database is accessible
"""
import sys

def test_connection():
    print("=" * 60)
    print("PostgreSQL Connection Test")
    print("=" * 60)
    
    # Get database URL
    print("\nEnter your database connection details:")
    print("(Press Enter to use defaults)")
    
    host = input("Host [localhost]: ").strip() or "localhost"
    port = input("Port [5432]: ").strip() or "5432"
    database = input("Database [assetdb]: ").strip() or "assetdb"
    username = input("Username [postgres]: ").strip() or "postgres"
    password = input("Password: ").strip()
    
    if not password:
        print("\n[ERROR] Password is required")
        return False
    
    # Build connection URL
    DATABASE_URL = f"postgresql://{username}:{password}@{host}:{port}/{database}"
    
    print("\n" + "=" * 60)
    print("Testing connection...")
    print("=" * 60)
    
    try:
        from sqlalchemy import create_engine, text
        
        print(f"\nConnecting to: {host}:{port}/{database}")
        print(f"Username: {username}")
        
        engine = create_engine(DATABASE_URL)
        
        with engine.connect() as conn:
            # Test basic query
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            
            print("\n✓ Connection successful!")
            print(f"\nPostgreSQL version:")
            print(f"  {version[:80]}...")
            
            # Check if database has tables
            result = conn.execute(text("""
                SELECT COUNT(*) 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """))
            table_count = result.fetchone()[0]
            
            print(f"\nTables in database: {table_count}")
            
            if table_count == 0:
                print("\n[INFO] No tables found. You need to run migrations:")
                print("  alembic upgrade head")
            else:
                # List tables
                result = conn.execute(text("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public'
                    ORDER BY table_name
                """))
                tables = [row[0] for row in result]
                print("\nExisting tables:")
                for table in tables:
                    print(f"  - {table}")
            
            print("\n" + "=" * 60)
            print("Connection test completed successfully!")
            print("=" * 60)
            
            # Show .env format
            print("\nAdd this to your backend/.env file:")
            print("-" * 60)
            print(f"DATABASE_URL={DATABASE_URL}")
            print("SECRET_KEY=your-secret-key-change-in-production")
            print("ALGORITHM=HS256")
            print("ACCESS_TOKEN_EXPIRE_MINUTES=30")
            print("-" * 60)
            
            return True
            
    except ImportError:
        print("\n[ERROR] SQLAlchemy not installed")
        print("Install it with: pip install sqlalchemy psycopg2-binary")
        return False
        
    except Exception as e:
        print(f"\n[ERROR] Connection failed!")
        print(f"Error: {e}")
        print("\nCommon issues:")
        print("1. PostgreSQL is not running")
        print("   - Check Windows Services for 'postgresql' service")
        print("2. Wrong password")
        print("   - Verify the password you set during installation")
        print("3. Database doesn't exist")
        print("   - Create it with: createdb -U postgres assetdb")
        print("4. Wrong host/port")
        print("   - Default is localhost:5432")
        return False

if __name__ == "__main__":
    try:
        success = test_connection()
        input("\nPress Enter to exit...")
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest cancelled by user")
        sys.exit(1)
