#!/usr/bin/env python
"""Create missing reference data"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.asset_status import AssetStatus
from app.models.location import Location
from app.models.company import Company

def create_missing_data():
    """Create missing asset statuses and locations"""
    db = SessionLocal()
    try:
        print("=" * 60)
        print("CREATING MISSING REFERENCE DATA")
        print("=" * 60)
        print()
        
        # Create asset statuses if missing
        status_count = db.query(AssetStatus).count()
        if status_count == 0:
            print("Creating asset statuses...")
            statuses = [
                AssetStatus(
                    statusname="Available",
                    statuscode="AVAIL",
                    description="Asset is available for use",
                    color="success",
                    isactive=True
                ),
                AssetStatus(
                    statusname="In Use",
                    statuscode="INUSE",
                    description="Asset is currently assigned",
                    color="primary",
                    isactive=True
                ),
                AssetStatus(
                    statusname="Maintenance",
                    statuscode="MAINT",
                    description="Asset is under maintenance",
                    color="warning",
                    isactive=True
                ),
                AssetStatus(
                    statusname="Disposed",
                    statuscode="DISP",
                    description="Asset has been disposed",
                    color="danger",
                    isactive=True
                )
            ]
            
            for status in statuses:
                db.add(status)
            
            db.commit()
            print(f"  ✓ Created {len(statuses)} asset statuses")
        else:
            print(f"  ✓ Asset statuses already exist ({status_count} records)")
        
        # Create locations for companies if missing
        location_count = db.query(Location).count()
        if location_count == 0:
            print("Creating default locations...")
            companies = db.query(Company).all()
            
            for company in companies:
                location = Location(
                    name=f"{company.companyname} - Main Location",
                    companyid=company.companyid,
                    isactive=True
                )
                db.add(location)
            
            db.commit()
            print(f"  ✓ Created {len(companies)} default locations")
        else:
            print(f"  ✓ Locations already exist ({location_count} records)")
        
        print()
        print("=" * 60)
        print("✓ MISSING DATA CREATED SUCCESSFULLY!")
        print("=" * 60)
        print()
        print("All required reference data is now available.")
        print("Asset creation should now work properly.")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print()
        print("=" * 60)
        print("✗ ERROR CREATING MISSING DATA")
        print("=" * 60)
        print(f"Error: {str(e)}")
        print()
        db.rollback()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    success = create_missing_data()
    sys.exit(0 if success else 1)