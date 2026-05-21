#!/usr/bin/env python
"""Create locations"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.location import Location
from app.models.company import Company

def create_locations():
    """Create default locations for companies"""
    db = SessionLocal()
    try:
        print("Creating default locations...")
        
        # Check if already exist
        count = db.query(Location).count()
        if count > 0:
            print(f"✓ Locations already exist ({count} records)")
            return True
        
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
    create_locations()