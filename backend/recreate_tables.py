"""
Recreate database tables with new schema
"""
from app.core.database import Base, engine
from app.models import (
    User, Category, Location, Asset,
    InventoryItem, InventoryTransaction,
    AuditSession, AuditRecord,
    Country, Province, Company, MainCategory, AssetSequence,
    Department, AssetStatus, AssetTransfer
)

import sys

print("=" * 70)
print("RECREATING DATABASE TABLES")
print("=" * 70)
print()

print("⚠️  WARNING: This will drop all existing tables!")
print("⚠️  All data will be lost!")
print()

# Check if running in automated mode
if len(sys.argv) > 1 and sys.argv[1] == '--yes':
    response = 'yes'
    print("Running in automated mode...")
else:
    response = input("Are you sure you want to continue? (yes/no): ")

if response.lower() != 'yes':
    print("Operation cancelled.")
    exit()

print()
print("Dropping all tables...")
# Use raw SQL to drop all tables with CASCADE
from sqlalchemy import text
with engine.connect() as conn:
    # Get all table names
    result = conn.execute(text("""
        SELECT tablename FROM pg_tables 
        WHERE schemaname = 'public'
    """))
    tables = [row[0] for row in result]
    
    # Drop each table with CASCADE
    for table in tables:
        try:
            conn.execute(text(f'DROP TABLE IF EXISTS "{table}" CASCADE'))
            print(f"  ✓ Dropped table: {table}")
        except Exception as e:
            print(f"  ! Could not drop {table}: {e}")
    
    conn.commit()

print("✓ All tables dropped")
print()

print("Creating all tables...")
Base.metadata.create_all(bind=engine)
print("✓ Tables created")
print()

print("=" * 70)
print("✓ DATABASE TABLES RECREATED SUCCESSFULLY")
print("=" * 70)
print()
print("Next steps:")
print("  1. Run: python seed_location_hierarchy.py")
print("  2. Run: python seed_asset_control_data.py")
print("  3. Run: python create_test_user.py")
print()
