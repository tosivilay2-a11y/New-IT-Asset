"""
Verify Database Tables and Connections
Checks that all tables are created and relationships are correct
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import engine, SessionLocal
from sqlalchemy import inspect, text

def verify_tables():
    print("=" * 60)
    print("DATABASE TABLE VERIFICATION")
    print("=" * 60)
    
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    print(f"\n✅ Connected to database: {engine.url.database}")
    print(f"✅ Total tables found: {len(tables)}\n")
    
    # Expected tables
    expected_tables = {
        # Original tables
        'users': 'User accounts',
        'categories': 'Asset categories',
        'locations': 'Physical locations',
        'assets': 'Asset records',
        'inventory_items': 'Inventory items',
        'inventory_transactions': 'Inventory transactions',
        'audit_sessions': 'Audit sessions',
        'audit_records': 'Audit records',
        
        # New location hierarchy tables
        'countries': 'Countries (2-char codes)',
        'provinces': 'Provinces (3-char codes)',
        'companies': 'Companies (4-char codes)',
        'maincategories': 'Main categories (1-char codes)',
        'assetsequences': 'Asset ID sequences',
    }
    
    print("📋 TABLE STATUS:")
    print("-" * 60)
    
    missing_tables = []
    for table_name, description in expected_tables.items():
        if table_name in tables:
            print(f"✅ {table_name:<25} - {description}")
        else:
            print(f"❌ {table_name:<25} - MISSING!")
            missing_tables.append(table_name)
    
    print("\n" + "=" * 60)
    
    if missing_tables:
        print(f"\n⚠️  WARNING: {len(missing_tables)} tables are missing!")
        print("Missing tables:", ", ".join(missing_tables))
        print("\n💡 To create missing tables, run:")
        print("   python backend/create_location_tables.py")
        return False
    else:
        print("\n✅ All expected tables exist!")
    
    # Check table relationships
    print("\n" + "=" * 60)
    print("🔗 CHECKING TABLE RELATIONSHIPS")
    print("=" * 60)
    
    db = SessionLocal()
    try:
        # Check foreign keys
        relationships = {
            'provinces': [('countryid', 'countries')],
            'companies': [('provinceid', 'provinces')],
            'assetsequences': [
                ('countryid', 'countries'),
                ('companyid', 'companies')
            ]
        }
        
        for table, fks in relationships.items():
            if table in tables:
                table_fks = inspector.get_foreign_keys(table)
                print(f"\n📊 {table}:")
                for fk_col, ref_table in fks:
                    fk_exists = any(
                        fk_col in fk['constrained_columns'] and 
                        ref_table == fk['referred_table']
                        for fk in table_fks
                    )
                    status = "✅" if fk_exists else "❌"
                    print(f"  {status} {fk_col} → {ref_table}")
        
        # Check data counts
        print("\n" + "=" * 60)
        print("📊 DATA COUNTS")
        print("=" * 60)
        
        data_tables = ['countries', 'provinces', 'companies', 'maincategories', 'users', 'assets']
        for table in data_tables:
            if table in tables:
                result = db.execute(text(f"SELECT COUNT(*) FROM {table}"))
                count = result.scalar()
                print(f"  {table:<25} : {count} records")
        
        print("\n" + "=" * 60)
        print("✅ DATABASE VERIFICATION COMPLETE")
        print("=" * 60)
        
        if missing_tables:
            print("\n⚠️  Action required: Create missing tables")
            return False
        else:
            print("\n✅ All tables and relationships verified!")
            return True
            
    except Exception as e:
        print(f"\n❌ Error during verification: {e}")
        return False
    finally:
        db.close()

def check_admin_routes():
    """Check if admin routes are accessible"""
    print("\n" + "=" * 60)
    print("🔌 CHECKING API ROUTES")
    print("=" * 60)
    
    expected_routes = [
        '/countries',
        '/provinces',
        '/companies',
        '/main-categories',
        '/asset-utils/preview-asset-id',
        '/asset-utils/generate-qr-code',
    ]
    
    print("\nExpected admin routes:")
    for route in expected_routes:
        print(f"  📍 {route}")
    
    print("\n💡 To test routes, visit: http://localhost:8000/docs")
    print("=" * 60)

if __name__ == "__main__":
    print("\n")
    success = verify_tables()
    check_admin_routes()
    
    if success:
        print("\n✅ Database is ready for admin pages!")
        print("\n📝 Next steps:")
        print("   1. Ensure backend is running: uvicorn app.main:app --reload")
        print("   2. Seed data if needed: python backend/seed_location_hierarchy.py")
        print("   3. Access admin page: http://localhost:3000/admin/config")
    else:
        print("\n⚠️  Database setup incomplete!")
        print("\n📝 Required steps:")
        print("   1. Run: python backend/create_location_tables.py")
        print("   2. Run: python backend/seed_location_hierarchy.py")
        print("   3. Restart backend server")
    
    print("\n")
