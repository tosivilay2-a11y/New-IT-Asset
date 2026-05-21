#!/usr/bin/env python
"""Debug asset creation route"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.user import User
from app.models.main_category import MainCategory
from app.models.country import Country
from app.models.province import Province
from app.models.company import Company

def debug_route_asset_creation():
    """Debug the asset creation route step by step"""
    db = SessionLocal()
    try:
        print("=" * 60)
        print("DEBUGGING ASSET CREATION ROUTE")
        print("=" * 60)
        print()
        
        # Get required data
        user = db.query(User).filter(User.email == "admin@example.com").first()
        main_category = db.query(MainCategory).first()
        country = db.query(Country).first()
        province = db.query(Province).first()
        company = db.query(Company).first()
        
        # Simulate the exact data that would come from frontend
        asset_data = {
            "main_category": main_category.categoryname,
            "country_id": country.countryid,
            "province_id": province.provinceid,
            "company_id": company.companyid,
            "assetname": "Debug Route Asset",
            "manufacturer": "Debug Corp",
            "modelnumber": "DEBUG-001",
            "serialnumber": "DBG123456",
            "purchaseprice": 999.99,
            "cost_center": "DEBUG-ROUTE-001",  # This should be preserved
            "condition": "New",
            "notes": "Debug route test"
        }
        
        print("Original asset_data:")
        for key, value in asset_data.items():
            print(f"  {key}: {value}")
        print()
        
        # Simulate the route processing step by step
        
        # Step 1: Get main category ID
        if 'main_category' in asset_data and isinstance(asset_data['main_category'], str):
            category = db.query(MainCategory).filter(
                MainCategory.categoryname == asset_data['main_category']
            ).first()
            if category:
                asset_data['maincategoryid'] = category.maincategoryid
                del asset_data['main_category']
                print(f"✓ Converted main_category to maincategoryid: {asset_data['maincategoryid']}")
        
        # Step 2: Field mapping
        field_mapping = {
            'country_id': 'countryid',
            'province_id': 'provinceid',
            'company_id': 'companyid',
            'purchase_date': 'purchasedate',
            'purchase_cost': 'purchaseprice',
            'brand': 'manufacturer',
            'model': 'modelnumber',
            'serial_number': 'serialnumber',
        }
        
        for old_name, new_name in field_mapping.items():
            if old_name in asset_data and old_name != new_name:
                asset_data[new_name] = asset_data.pop(old_name)
                print(f"✓ Mapped {old_name} to {new_name}")
        
        # Step 3: Filter allowed fields
        allowed_fields = {
            'assetname', 'assetcode', 'serialnumber', 'modelnumber', 'manufacturer',
            'maincategoryid', 'categoryid', 'countryid', 'provinceid', 'companyid',
            'locationid', 'departmentid', 'assignedto', 'assigneddate', 'purchasedate',
            'purchaseprice', 'currentvalue', 'depreciationrate', 'warrantyexpiry',
            'statusid', 'condition', 'specifications', 'notes', 'po_number', 'po_attachment_path',
            'cost_center'
        }
        
        print(f"Allowed fields: {allowed_fields}")
        print(f"cost_center in allowed_fields: {'cost_center' in allowed_fields}")
        
        filtered_data = {k: v for k, v in asset_data.items() if k in allowed_fields}
        
        print("\nFiltered asset_data:")
        for key, value in filtered_data.items():
            print(f"  {key}: {value}")
        
        print(f"\ncost_center in filtered_data: {'cost_center' in filtered_data}")
        if 'cost_center' in filtered_data:
            print(f"cost_center value: {filtered_data['cost_center']}")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    debug_route_asset_creation()