#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import get_db
from app.models.main_category import MainCategory
from app.models.country import Country
from app.models.province import Province
from app.models.company import Company
from app.models.location import Location

def check_reference_data():
    """Check what reference data is available"""
    
    db = next(get_db())
    
    print("=== CHECKING REFERENCE DATA ===")
    
    print("\n1. Main Categories:")
    categories = db.query(MainCategory).all()
    for cat in categories:
        print(f"  ID: {cat.maincategoryid}, Name: {cat.categoryname}")
    
    print("\n2. Countries:")
    countries = db.query(Country).all()
    for country in countries:
        print(f"  ID: {country.countryid}, Name: {country.countryname}")
    
    print("\n3. Provinces:")
    provinces = db.query(Province).all()
    for province in provinces:
        print(f"  ID: {province.provinceid}, Name: {province.provincename}")
    
    print("\n4. Companies:")
    companies = db.query(Company).all()
    for company in companies:
        print(f"  ID: {company.companyid}, Name: {company.companyname}")
    
    print("\n5. Locations:")
    locations = db.query(Location).all()
    for location in locations:
        print(f"  ID: {location.id}, Name: {location.name}, Company ID: {location.companyid}")

if __name__ == '__main__':
    check_reference_data()