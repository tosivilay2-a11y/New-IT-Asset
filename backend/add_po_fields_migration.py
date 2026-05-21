#!/usr/bin/env python3
"""
Add PO fields to assets table
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import text
from app.core.database import engine

def add_po_fields():
    """Add PO number and attachment path fields to assets table"""
    try:
        with engine.connect() as connection:
            # Check if columns already exist
            result = connection.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'assets' 
                AND column_name IN ('po_number', 'po_attachment_path')
            """))
            existing_columns = [row[0] for row in result.fetchall()]
            
            # Add po_number if it doesn't exist
            if 'po_number' not in existing_columns:
                print("Adding po_number column...")
                connection.execute(text("""
                    ALTER TABLE assets 
                    ADD COLUMN po_number VARCHAR(100)
                """))
                connection.commit()
                print("✓ po_number column added")
            else:
                print("✓ po_number column already exists")
            
            # Add po_attachment_path if it doesn't exist
            if 'po_attachment_path' not in existing_columns:
                print("Adding po_attachment_path column...")
                connection.execute(text("""
                    ALTER TABLE assets 
                    ADD COLUMN po_attachment_path VARCHAR(500)
                """))
                connection.commit()
                print("✓ po_attachment_path column added")
            else:
                print("✓ po_attachment_path column already exists")
            
            print("\n✅ Migration completed successfully!")
            
    except Exception as e:
        print(f"❌ Error during migration: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🔄 Adding PO fields to assets table...")
    success = add_po_fields()
    if success:
        print("🎉 Database migration completed!")
    else:
        print("💥 Migration failed!")
        sys.exit(1)