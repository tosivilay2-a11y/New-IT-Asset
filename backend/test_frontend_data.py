#!/usr/bin/env python
"""Test with frontend-like data structure"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.routes.assets import create_asset
from app.models.user import User

def test_frontend_data():
    """Test with data structure similar to what frontend sends"""
    db = SessionLocal()
    try:
        print("=" * 60)
        print("TESTING FRONTEND-LIKE DATA STRUCTURE")
        print("=" * 60)
        print()
        
        # Get user
        user = db.query(User).filter(User.email == "admin@example.com").first()
        
        # Simulate exact data structure from frontend (based on error logs)
        frontend_data = {
            "assetname": "Frontend Test Asset",
            "locationid": 1,  # Changed from 0 to valid location
            "maincategoryid": 2,
            "provinceid": 1,
            "countryid": 1,
            "companyid": 1,
            "statusid": 1,
            "purchaseprice": 0,
            "currentvalue": 0,
            "isactive": True,
            # These fields are coming as None from frontend
            "assigneddate": None,
            "purchasedate": None,
            "warrantyexpiry": None,
            "assignedto": None,
            "categoryid": None,
            "departmentid": None,
            "depreciationrate": None,
            "manufacturer": None,
            "specifications": None,
            "modelnumber": None,
            "serialnumber": None,
            "notes": None,
            "po_number": None,
            "po_attachment_path": None,
            "cost_center": None,
            "condition": None
        }
        
        print("Frontend data structure:")
        for key, value in frontend_data.items():
            print(f"  {key}: {value}")
        print()
        
        print("Creating asset with frontend-like data...")
        
        # This should work without SQLite datetime errors
        created_asset = create_asset(frontend_data, db, user)
        
        print("✓ Asset created successfully!")
        print(f"  Asset ID: {created_asset.assetid}")
        print(f"  Asset Code: {created_asset.assetcode}")
        print(f"  Asset Name: {created_asset.assetname}")
        
        # Clean up
        db.delete(created_asset)
        db.commit()
        print("✓ Test asset cleaned up")
        
        print()
        print("=" * 60)
        print("✅ FRONTEND DATA TEST SUCCESSFUL!")
        print("=" * 60)
        print()
        print("Frontend asset creation should now work without errors!")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print()
        print("=" * 60)
        print("❌ FRONTEND DATA TEST FAILED")
        print("=" * 60)
        print(f"Error: {str(e)}")
        print()
        db.rollback()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    success = test_frontend_data()
    sys.exit(0 if success else 1)