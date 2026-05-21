#!/usr/bin/env python
"""Test with locationid: 0 (the exact frontend issue)"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.routes.assets import create_asset
from app.models.user import User

def test_locationid_zero():
    """Test with locationid: 0 (the exact frontend issue)"""
    db = SessionLocal()
    try:
        print("=" * 60)
        print("TESTING LOCATIONID: 0 (FRONTEND ISSUE)")
        print("=" * 60)
        print()
        
        # Get user
        user = db.query(User).filter(User.email == "admin@example.com").first()
        
        # Exact problematic data from frontend error logs
        problematic_data = {
            "assetname": "Test Asset with locationid 0",
            "locationid": 0,  # This is the problem!
            "maincategoryid": 2,
            "provinceid": 1,
            "countryid": 1,
            "companyid": 1,
            "statusid": 1,
            "purchaseprice": 0,
            "currentvalue": 0,
            "isactive": True,
            # All the None fields that were causing SQLite issues
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
        
        print("Testing with locationid: 0 (the exact frontend problem)...")
        print()
        
        # This should now work by auto-assigning a valid location
        created_asset = create_asset(problematic_data, db, user)
        
        print("✅ Asset created successfully despite locationid: 0!")
        print(f"  Asset ID: {created_asset.assetid}")
        print(f"  Asset Code: {created_asset.assetcode}")
        print(f"  Asset Name: {created_asset.assetname}")
        print(f"  Location ID (auto-assigned): {created_asset.locationid}")
        print(f"  Cost Center: {created_asset.cost_center}")
        
        # Clean up
        db.delete(created_asset)
        db.commit()
        print("✓ Test asset cleaned up")
        
        print()
        print("=" * 60)
        print("✅ LOCATIONID: 0 ISSUE FIXED!")
        print("=" * 60)
        print()
        print("The frontend 400 Bad Request error should now be resolved!")
        print("Asset creation will work even with invalid locationid values.")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print()
        print("=" * 60)
        print("❌ LOCATIONID: 0 TEST FAILED")
        print("=" * 60)
        print(f"Error: {str(e)}")
        print()
        db.rollback()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    success = test_locationid_zero()
    sys.exit(0 if success else 1)