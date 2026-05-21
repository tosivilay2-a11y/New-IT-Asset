#!/usr/bin/env python
"""Check current data state"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.main_category import MainCategory
from app.models.asset_status import AssetStatus
from app.models.country import Country
from app.models.province import Province
from app.models.company import Company
from app.models.location import Location

def check_current_data():
    """Check current data state"""
    db = SessionLocal()
    try:
        print("Current data state:")
        
        # Check each table
        countries = db.query(Country).count()
        provinces = db.query(Province).count()
        companies = db.query(Company).count()
        categories = db.query(MainCategory).count()
        statuses = db.query(AssetStatus).count()
        locations = db.query(Location).count()
        
        print(f"Countries: {countries}")
        print(f"Provinces: {provinces}")
        print(f"Companies: {companies}")
        print(f"Main Categories: {categories}")
        print(f"Asset Statuses: {statuses}")
        print(f"Locations: {locations}")
        
        # Show some sample data
        if statuses > 0:
            status = db.query(AssetStatus).first()
            print(f"Sample status: {status.statusname}")
        
        if locations > 0:
            location = db.query(Location).first()
            print(f"Sample location: {location.name}")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    check_current_data()