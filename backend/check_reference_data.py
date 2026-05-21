#!/usr/bin/env python
"""Check what reference data exists"""
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

def check_reference_data():
    """Check what reference data exists in the database"""
    db = SessionLocal()
    try:
        print("=" * 60)
        print("CHECKING REFERENCE DATA")
        print("=" * 60)
        print()
        
        # Check each table
        tables = [
            ("Countries", Country),
            ("Provinces", Province),
            ("Companies", Company),
            ("Main Categories", MainCategory),
            ("Asset Statuses", AssetStatus),
            ("Locations", Location)
        ]
        
        for table_name, model in tables:
            count = db.query(model).count()
            print(f"{table_name}: {count} records")
            
            if count > 0:
                # Show first few records
                records = db.query(model).limit(3).all()
                for record in records:
                    if hasattr(record, 'countryname'):
                        print(f"  - {record.countryname} ({record.countrycode})")
                    elif hasattr(record, 'provincename'):
                        print(f"  - {record.provincename} ({record.provincecode})")
                    elif hasattr(record, 'companyname'):
                        print(f"  - {record.companyname} ({record.companycode})")
                    elif hasattr(record, 'categoryname'):
                        print(f"  - {record.categoryname} ({record.categorycode})")
                    elif hasattr(record, 'statusname'):
                        print(f"  - {record.statusname} ({record.statuscode})")
                    elif hasattr(record, 'name'):
                        print(f"  - {record.name}")
            print()
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    check_reference_data()