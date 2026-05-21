#!/usr/bin/env python3
"""
Direct fix to remove the assignedto foreign key constraint from PostgreSQL
"""
import sys
from sqlalchemy import text
from app.core.database import engine

def fix_fk_constraint():
    """Remove the foreign key constraint on assignedto column"""
    try:
        print("Removing foreign key constraint from assets.assignedto...")
        
        with engine.connect() as connection:
            # Check if constraint exists
            check_query = text("""
                SELECT constraint_name 
                FROM information_schema.table_constraints 
                WHERE table_name = 'assets' 
                AND constraint_type = 'FOREIGN KEY'
                AND constraint_name = 'assets_assignedto_fkey'
            """)
            
            result = connection.execute(check_query)
            constraint_exists = result.fetchone() is not None
            
            if constraint_exists:
                print("✓ Found constraint 'assets_assignedto_fkey'")
                
                # Drop the constraint
                drop_query = text("""
                    ALTER TABLE assets 
                    DROP CONSTRAINT assets_assignedto_fkey
                """)
                connection.execute(drop_query)
                connection.commit()
                
                print("✅ Successfully removed foreign key constraint!")
                return True
            else:
                print("ℹ️  Constraint 'assets_assignedto_fkey' does not exist (already removed)")
                return True
                
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = fix_fk_constraint()
    sys.exit(0 if success else 1)
