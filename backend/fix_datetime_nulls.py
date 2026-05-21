#!/usr/bin/env python
"""Fix NULL datetime values in database"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from sqlalchemy import create_engine, text
from app.core.config import settings

def fix_datetime_nulls():
    """Fix NULL datetime values in all tables"""
    try:
        print("=" * 60)
        print("FIXING NULL DATETIME VALUES")
        print("=" * 60)
        print()
        
        engine = create_engine(settings.DATABASE_URL)
        
        with engine.begin() as conn:
            # List of tables and their datetime columns
            tables_to_fix = [
                ('countries', ['createdat', 'updatedat']),
                ('provinces', ['createdat', 'updatedat']),
                ('companies', ['createdat', 'updatedat']),
                ('maincategories', ['createdat', 'updatedat']),
                ('departments', ['createdat', 'updatedat']),
                ('assetstatuses', ['createdat', 'updatedat']),
                ('users', ['createdat', 'updatedat']),
                ('assets', ['createdat', 'updatedat'])
            ]
            
            for table_name, datetime_columns in tables_to_fix:
                try:
                    # Check if table exists
                    result = conn.execute(text(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'"))
                    if not result.fetchone():
                        print(f"  ⚠ Table {table_name} does not exist, skipping...")
                        continue
                    
                    print(f"Fixing {table_name}...")
                    
                    for column in datetime_columns:
                        # Check if column exists
                        result = conn.execute(text(f"PRAGMA table_info({table_name})"))
                        columns = [row[1] for row in result.fetchall()]
                        
                        if column not in columns:
                            print(f"    ⚠ Column {column} does not exist in {table_name}, skipping...")
                            continue
                        
                        # Update NULL values to current timestamp
                        result = conn.execute(text(f"""
                            UPDATE {table_name} 
                            SET {column} = datetime('now') 
                            WHERE {column} IS NULL
                        """))
                        
                        rows_updated = result.rowcount
                        if rows_updated > 0:
                            print(f"    ✓ Updated {rows_updated} NULL {column} values in {table_name}")
                        else:
                            print(f"    ✓ No NULL {column} values found in {table_name}")
                
                except Exception as e:
                    print(f"    ⚠ Warning fixing {table_name}: {e}")
        
        print()
        print("=" * 60)
        print("✓ DATETIME NULL VALUES FIXED!")
        print("=" * 60)
        print()
        print("All NULL datetime values have been updated to current timestamp.")
        print("Data loading should now work properly.")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print()
        print("=" * 60)
        print("✗ ERROR FIXING DATETIME VALUES")
        print("=" * 60)
        print(f"Error: {str(e)}")
        print()
        return False

if __name__ == "__main__":
    success = fix_datetime_nulls()
    sys.exit(0 if success else 1)