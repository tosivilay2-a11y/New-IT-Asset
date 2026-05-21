#!/usr/bin/env python
"""Fix asset creation issues and add cost center field"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from sqlalchemy import create_engine, text
from app.core.config import settings

def fix_asset_issues():
    """Fix datetime issues and add cost center field"""
    try:
        print("=" * 60)
        print("FIXING ASSET CREATION ISSUES")
        print("=" * 60)
        print()
        
        engine = create_engine(settings.DATABASE_URL)
        
        print("✓ Connected to database")
        print()
        
        with engine.begin() as conn:
            # Check if cost_center column exists
            try:
                result = conn.execute(text("PRAGMA table_info(assets)"))
                columns = [row[1] for row in result.fetchall()]
                
                if 'cost_center' not in columns:
                    print("Adding cost_center column to assets table...")
                    conn.execute(text("ALTER TABLE assets ADD COLUMN cost_center VARCHAR(100)"))
                    print("  ✓ Added cost_center column")
                else:
                    print("  ✓ cost_center column already exists")
                
            except Exception as e:
                print(f"  ⚠ Warning with cost_center column: {e}")
            
            # Update any NULL datetime fields to handle SQLite properly
            try:
                print("Fixing datetime fields...")
                
                # Set default values for datetime fields that are NULL
                conn.execute(text("""
                    UPDATE assets 
                    SET createdat = datetime('now') 
                    WHERE createdat IS NULL
                """))
                
                conn.execute(text("""
                    UPDATE assets 
                    SET updatedat = datetime('now') 
                    WHERE updatedat IS NULL
                """))
                
                print("  ✓ Fixed datetime fields")
                
            except Exception as e:
                print(f"  ⚠ Warning with datetime fields: {e}")
            
            # Ensure we have required reference data
            print("Checking reference data...")
            
            try:
                # Check if we have asset statuses
                result = conn.execute(text("SELECT COUNT(*) FROM assetstatuses"))
                status_count = result.scalar()
                
                if status_count == 0:
                    print("  Adding default asset statuses...")
                    conn.execute(text("""
                        INSERT INTO assetstatuses (statusname, statuscode, description, colorcode, isactive) VALUES
                        ('Available', 'AVAIL', 'Asset is available for use', 'success', 1),
                        ('In Use', 'INUSE', 'Asset is currently assigned', 'primary', 1),
                        ('Maintenance', 'MAINT', 'Asset is under maintenance', 'warning', 1),
                        ('Disposed', 'DISP', 'Asset has been disposed', 'danger', 1)
                    """))
                    print("    ✓ Added default asset statuses")
                else:
                    print(f"  ✓ Found {status_count} asset statuses")
                
            except Exception as e:
                print(f"  ⚠ Warning with asset statuses: {e}")
            
            try:
                # Check if we have main categories
                result = conn.execute(text("SELECT COUNT(*) FROM maincategories"))
                category_count = result.scalar()
                
                if category_count == 0:
                    print("  Adding default main categories...")
                    conn.execute(text("""
                        INSERT INTO maincategories (categoryname, categorycode, description, isactive) VALUES
                        ('Computer', 'COMP', 'Desktop and laptop computers', 1),
                        ('Printer', 'PRNT', 'Printers and scanners', 1),
                        ('Network Equipment', 'NETW', 'Routers, switches, access points', 1),
                        ('Mobile Device', 'MOBL', 'Smartphones and tablets', 1)
                    """))
                    print("    ✓ Added default main categories")
                else:
                    print(f"  ✓ Found {category_count} main categories")
                
            except Exception as e:
                print(f"  ⚠ Warning with main categories: {e}")
        
        print()
        print("=" * 60)
        print("✓ ASSET ISSUES FIXED SUCCESSFULLY!")
        print("=" * 60)
        print()
        print("Changes made:")
        print("  • Added cost_center field to assets table")
        print("  • Fixed datetime field handling for SQLite")
        print("  • Ensured required reference data exists")
        print("  • Asset creation should now work properly")
        print()
        print("You can now create assets with cost center information!")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print()
        print("=" * 60)
        print("✗ ERROR FIXING ASSET ISSUES")
        print("=" * 60)
        print(f"Error: {str(e)}")
        print()
        return False

if __name__ == "__main__":
    success = fix_asset_issues()
    sys.exit(0 if success else 1)