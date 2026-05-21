#!/usr/bin/env python
"""Debug cost center field handling"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.asset import Asset

def debug_cost_center():
    """Debug cost center field"""
    db = SessionLocal()
    try:
        print("Debugging cost center field...")
        
        # Check if cost_center column exists in database
        from sqlalchemy import text
        result = db.execute(text("PRAGMA table_info(assets)"))
        columns = [row[1] for row in result.fetchall()]
        
        print(f"Asset table columns: {columns}")
        
        if 'cost_center' in columns:
            print("✓ cost_center column exists in database")
        else:
            print("✗ cost_center column missing from database")
        
        # Check Asset model attributes
        asset_attrs = [attr for attr in dir(Asset) if not attr.startswith('_')]
        print(f"Asset model has cost_center: {'cost_center' in asset_attrs}")
        
        # Try creating an asset with cost_center directly
        print("\nTesting direct asset creation with cost_center...")
        
        test_asset = Asset(
            assetcode="DEBUG-001",
            assetname="Debug Asset",
            maincategoryid=1,
            countryid=1,
            provinceid=1,
            companyid=1,
            locationid=1,
            statusid=1,
            cost_center="DEBUG-CC-001",
            isactive=True
        )
        
        db.add(test_asset)
        db.commit()
        db.refresh(test_asset)
        
        print(f"Created asset with cost_center: {test_asset.cost_center}")
        
        # Clean up
        db.delete(test_asset)
        db.commit()
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    debug_cost_center()