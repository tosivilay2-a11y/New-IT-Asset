#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import get_db
from app.models.asset import Asset
from datetime import datetime
import json

def test_datetime_issue():
    """Test the datetime issue that's causing SQLite errors"""
    
    # Test data similar to what frontend sends
    test_data = {
        'assetname': 'Test Asset',
        'main_category': 'Computer',
        'country_id': 1,
        'province_id': 1,
        'company_id': 1,
        'purchase_date': '2026-05-06',
        'status': 'Available',
        'manufacturer': 'Dell',
        'modelnumber': 'Latitude',
        'serialnumber': 'TEST123',
        'purchaseprice': 1000,
        'currentvalue': 800,
        'condition': 'Good',
        'notes': 'Test asset'
    }

    print('=== DEBUGGING DATETIME ISSUE ===')
    print('Test data:', json.dumps(test_data, indent=2))
    print('\nChecking datetime fields...')
    
    for key, value in test_data.items():
        if 'date' in key.lower():
            print(f'{key}: {value} (type: {type(value)})')
    
    # Test datetime conversion
    print('\n=== TESTING DATETIME CONVERSION ===')
    purchase_date_str = test_data.get('purchase_date')
    if purchase_date_str:
        try:
            # This is what should happen in the backend
            from datetime import datetime
            dt = datetime.fromisoformat(purchase_date_str)
            print(f'String to datetime conversion: {purchase_date_str} -> {dt} (type: {type(dt)})')
        except Exception as e:
            print(f'Error converting datetime: {e}')
    
    # Test what happens when we have None values
    print('\n=== TESTING NONE VALUES ===')
    test_none_data = {
        'assigneddate': None,
        'purchasedate': None,
        'warrantyexpiry': None,
        'createdat': datetime.utcnow(),
        'updatedat': datetime.utcnow()
    }
    
    for key, value in test_none_data.items():
        print(f'{key}: {value} (type: {type(value)})')
    
    # Test the actual asset creation process
    print('\n=== TESTING ASSET CREATION PROCESS ===')
    
    # Simulate the backend processing
    asset_data = test_data.copy()
    
    # Map frontend fields to backend fields
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
    
    print('After field mapping:', json.dumps(asset_data, indent=2, default=str))
    
    # Add required fields
    asset_data.update({
        'maincategoryid': 1,
        'statusid': 1,
        'locationid': 1,
        'assetcode': 'TEST123',
        'qrcode': 'test_qr',
        'createdby': 1,
        'isactive': True,
        'createdat': datetime.utcnow(),
        'updatedat': datetime.utcnow()
    })
    
    # Remove fields that aren't in the model
    allowed_fields = {
        'assetname', 'assetcode', 'serialnumber', 'modelnumber', 'manufacturer',
        'maincategoryid', 'categoryid', 'countryid', 'provinceid', 'companyid',
        'locationid', 'departmentid', 'assignedto', 'assigneddate', 'purchasedate',
        'purchaseprice', 'currentvalue', 'depreciationrate', 'warrantyexpiry',
        'statusid', 'condition', 'specifications', 'notes', 'po_number', 'po_attachment_path',
        'cost_center', 'qrcode', 'isactive', 'createdat', 'updatedat', 'createdby'
    }
    
    filtered_data = {k: v for k, v in asset_data.items() if k in allowed_fields}
    print('\nAfter filtering allowed fields:', json.dumps(filtered_data, indent=2, default=str))
    
    # Check for datetime issues
    print('\n=== CHECKING FOR DATETIME ISSUES ===')
    datetime_fields = ['assigneddate', 'purchasedate', 'warrantyexpiry', 'createdat', 'updatedat']
    
    for field in datetime_fields:
        if field in filtered_data:
            value = filtered_data[field]
            print(f'{field}: {value} (type: {type(value)})')
            
            # Check if it's a string that needs conversion
            if isinstance(value, str):
                try:
                    converted = datetime.fromisoformat(value)
                    print(f'  -> Converted to: {converted} (type: {type(converted)})')
                    filtered_data[field] = converted
                except Exception as e:
                    print(f'  -> Conversion error: {e}')
                    # Remove the field if it can't be converted
                    del filtered_data[field]
    
    print('\nFinal data for Asset creation:', json.dumps(filtered_data, indent=2, default=str))
    
    # Test creating the Asset object (without saving to DB)
    try:
        print('\n=== TESTING ASSET OBJECT CREATION ===')
        test_asset = Asset(**filtered_data)
        print('Asset object created successfully!')
        print(f'Asset name: {test_asset.assetname}')
        print(f'Asset code: {test_asset.assetcode}')
        print(f'Created at: {test_asset.createdat} (type: {type(test_asset.createdat)})')
        print(f'Purchase date: {test_asset.purchasedate} (type: {type(test_asset.purchasedate)})')
    except Exception as e:
        print(f'Error creating Asset object: {e}')
        print(f'Error type: {type(e)}')
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_datetime_issue()