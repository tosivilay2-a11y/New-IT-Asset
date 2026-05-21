#!/usr/bin/env python
"""Test asset creation directly via route function"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.routes.assets import create_asset
from app.models.user import User
from app.models.main_category import MainCategory
from app.models.country import Country
from app.models.province import Province
from app.models.company import Company

def test_direct_asset_creation():
    """Test asset creation directly via route function"""
    db = SessionLocal()
    try:
        print("=" * 60)
        print("TESTING DIRECT ASSET CREATION")
        print("=" * 60)
        print()
        
        # Get required data
        user = db.query(User).filter(User.email == "admin@example.com").first()
        main_category = db.query(MainCategory).first()
        country = db.query(Country).first()
        province = db.query(Province).first()
        company = db.query(Company).first()
        
        if not all([user, main_category, country, province, company]):
            print("✗ Missing required data")
            return False
        
        print(f"Using user: {user.email}")
        print(f"Using category: {main_category.categoryname}")
        print()
        
        # Create asset data similar to what frontend would send
        asset_data = {
            "main_category": main_category.categoryname,
            "country_id": country.countryid,
            "province_id": province.provinceid,
            "company_id": company.companyid,
            "assetname": "Test Direct API Asset",
            "manufacturer": "HP",
            "modelnumber": "EliteBook 840",
            "serialnumber": "HP123456789",
            "purchaseprice": 1200.00,
            "cost_center": "DIRECT-TEST-001",
            "condition": "Excellent",
            "notes": "Created via direct route test"
            # Deliberately not including datetime fields
        }
        
        print("Creating asset via direct route call...")
        
        # Call the route function directly
        created_asset = create_asset(asset_data, db, user)
        
        print("✓ Asset created successfully!")
        print(f"  Asset ID: {created_asset.assetid}")
        print(f"  Asset Code: {created_asset.assetcode}")
        print(f"  Asset Name: {created_asset.assetname}")
        print(f"  Cost Center: {created_asset.cost_center}")
        print(f"  Manufacturer: {created_asset.manufacturer}")
        print(f"  Model: {created_asset.modelnumber}")
        print(f"  Serial: {created_asset.serialnumber}")
        print(f"  Created At: {created_asset.createdat}")
        print(f"  Updated At: {created_asset.updatedat}")
        
        # Clean up
        db.delete(created_asset)
        db.commit()
        print("✓ Test asset cleaned up")
        
        print()
        print("=" * 60)
        print("✓ DIRECT ASSET CREATION TEST PASSED!")
        print("=" * 60)
        print()
        print("Asset creation works without SQLite datetime errors.")
        print("The fix is working properly!")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print()
        print("=" * 60)
        print("✗ DIRECT ASSET CREATION TEST FAILED")
        print("=" * 60)
        print(f"Error: {str(e)}")
        print()
        db.rollback()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    success = test_direct_asset_creation()
    sys.exit(0 if success else 1)