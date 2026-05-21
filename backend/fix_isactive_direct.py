#!/usr/bin/env python
"""
Fix isactive column type in PostgreSQL database
Run from backend directory: python fix_isactive_direct.py
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

if not DATABASE_URL:
    print("❌ DATABASE_URL not found in .env")
    exit(1)

print(f"Database URL: {DATABASE_URL[:50]}...")

try:
    # Create engine
    engine = create_engine(DATABASE_URL)
    
    print("Connecting to database...")
    with engine.connect() as connection:
        # Check current column type
        print("Checking current column type...")
        result = connection.execute(text("""
            SELECT data_type 
            FROM information_schema.columns 
            WHERE table_name = 'assets' AND column_name = 'isactive'
        """))
        
        row = result.fetchone()
        if row:
            current_type = row[0]
            print(f"Current isactive type: {current_type}")
            
            if current_type == 'smallint':
                print("Converting smallint to integer...")
                connection.execute(text("""
                    ALTER TABLE assets 
                    ALTER COLUMN isactive TYPE integer USING isactive::integer,
                    ALTER COLUMN isactive SET DEFAULT 1,
                    ALTER COLUMN isactive SET NOT NULL
                """))
                connection.commit()
                print("✅ Column type converted successfully!")
                
            elif current_type == 'boolean':
                print("Column is already boolean, setting default to true...")
                connection.execute(text("""
                    ALTER TABLE assets 
                    ALTER COLUMN isactive SET DEFAULT true,
                    ALTER COLUMN isactive SET NOT NULL
                """))
                connection.commit()
                print("✅ Column defaults set successfully!")
                
            else:
                print(f"Column type is {current_type}, no conversion needed")
        else:
            print("❌ Column 'isactive' not found in 'assets' table")
            exit(1)
    
    print("\n✅ Fix completed successfully!")
    print("You can now create assets without errors.")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    exit(1)
