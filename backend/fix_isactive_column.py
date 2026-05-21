#!/usr/bin/env python
"""
Fix isactive column type in PostgreSQL database
Converts from smallint to integer (or boolean if needed)
"""

import os
import sys
from sqlalchemy import create_engine, text
from app.core.config import settings

def fix_isactive_column():
    """Fix the isactive column type in PostgreSQL"""
    
    try:
        # Create engine
        engine = create_engine(settings.DATABASE_URL)
        
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
                    # For PostgreSQL, we can just use integer which is compatible
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
                return False
        
        print("\n✅ Fix completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = fix_isactive_column()
    sys.exit(0 if success else 1)
