#!/usr/bin/env python
"""Create asset statuses"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.asset_status import AssetStatus
from app.models.location import Location
from app.models.company import Company

def create_asset_statuses():
    """Create asset statuses"""
    db = SessionLocal()
    try:
        print("Creating asset statuses...")
        
        # Check if already exist
        count = db.query(AssetStatus).count()
        if count > 0:
            print(f"✓ Asset statuses already exist ({count} records)")
            return True
        
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
        print(f"✓ Created {len(statuses)} asset statuses")
        
        # Also create locations
        location_count = db.query(Location).count()
        if location_count == 0:
            print("Creating default locations...")
            companies = db.query(Company).all()
            
            for company in companies:
                location = Location(
                    name=f"{company.companyname} - Main Location",
                    companyid=company.companyid
                )
                db.add(location)
            
            db.commit()
            print(f"✓ Created {len(companies)} default locations")
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        db.rollback()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    create_asset_statuses()