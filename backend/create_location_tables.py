"""
Create Location Hierarchy Tables
Run this to create the new tables in the database
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import engine, Base
from app.models.country import Country
from app.models.province import Province
from app.models.company import Company
from app.models.main_category import MainCategory
from app.models.asset_sequence import AssetSequence

def create_tables():
    print("🔧 Creating location hierarchy tables...")
    
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        
        print("✅ Tables created successfully!")
        print("\nCreated tables:")
        print("  - countries")
        print("  - provinces")
        print("  - companies")
        print("  - maincategories")
        print("  - assetsequences")
        
        print("\n📝 Next steps:")
        print("  1. Run: python backend/seed_location_hierarchy.py")
        print("  2. Restart the backend server")
        print("  3. Test the new API endpoints at http://localhost:8000/docs")
        
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        raise

if __name__ == "__main__":
    create_tables()
