#!/usr/bin/env python
"""Apply migration to add firstname and lastname columns to users table"""

import sys
import os
from pathlib import Path

# Load .env file first
from dotenv import load_dotenv
env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)

sys.path.insert(0, os.path.dirname(__file__))

from app.core.database import engine
from sqlalchemy import text

def apply_migration():
    try:
        print("Applying migration to add firstname and lastname columns to users table...")
        
        with engine.connect() as connection:
            # Check if columns already exist
            result = connection.execute(text("""
                SELECT column_name FROM information_schema.columns 
                WHERE table_name='users' AND column_name IN ('firstname', 'lastname')
            """))
            existing_columns = [row[0] for row in result]
            
            if 'firstname' not in existing_columns:
                print("Adding firstname column...")
                connection.execute(text("ALTER TABLE users ADD COLUMN firstname VARCHAR(100) NULL"))
                connection.commit()
                print("✅ firstname column added")
            else:
                print("⚠️  firstname column already exists")
            
            if 'lastname' not in existing_columns:
                print("Adding lastname column...")
                connection.execute(text("ALTER TABLE users ADD COLUMN lastname VARCHAR(100) NULL"))
                connection.commit()
                print("✅ lastname column added")
            else:
                print("⚠️  lastname column already exists")
        
        print("\n✅ Migration completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error applying migration: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = apply_migration()
    sys.exit(0 if success else 1)
