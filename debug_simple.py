#!/usr/bin/env python3

from datetime import datetime
import json

def debug_datetime_conversion():
    """Debug datetime conversion issues"""
    
    print('=== DEBUGGING DATETIME CONVERSION ===')
    
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
        'notes': 'Test asset',
        'assigneddate': None,
        'warrantyexpiry': ''
    }

    print('Original test data:')
    for key, value in test_data.items():
        print(f'  {key}: {value} (type: {type(value)})')
    
    print('\n=== FIELD MAPPING ===')
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
        if old_name in test_data and old_name != new_name:
            test_data[new_name] = test_data.pop(old_name)
    
    print('After field mapping:')
    for key, value in test_data.items():
        print(f'  {key}: {value} (type: {type(value)})')
    
    print('\n=== DATETIME FIELD PROCESSING ===')
    
    # Add required fields
    test_data.update({
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
    
    # Process datetime fields
    datetime_fields = ['assigneddate', 'purchasedate', 'warrantyexpiry', 'createdat', 'updatedat']
    
    print('Processing datetime fields:')
    for field in datetime_fields:
        if field in test_data:
            value = test_data[field]
            print(f'  {field}: {value} (type: {type(value)})')
            
            # Check if it's a string that needs conversion
            if isinstance(value, str):
                if value == '':
                    print(f'    -> Empty string, removing field')
                    del test_data[field]
                else:
                    try:
                        converted = datetime.fromisoformat(value)
                        print(f'    -> Converted to: {converted} (type: {type(converted)})')
                        test_data[field] = converted
                    except Exception as e:
                        print(f'    -> Conversion error: {e}')
                        print(f'    -> Removing field due to conversion error')
                        del test_data[field]
            elif value is None:
                print(f'    -> None value, removing field to avoid SQLite issues')
                del test_data[field]
            elif isinstance(value, datetime):
                print(f'    -> Already datetime object, keeping as-is')
    
    print('\n=== FINAL DATA ===')
    print('Final data for Asset creation:')
    for key, value in test_data.items():
        print(f'  {key}: {value} (type: {type(value)})')
    
    print('\n=== TESTING PROBLEMATIC SCENARIOS ===')
    
    # Test the specific error scenario from the logs
    problematic_data = {
        'createdat': datetime.utcnow(),
        'updatedat': datetime.utcnow(),
        'assigneddate': None,  # This might be the issue
        'purchasedate': None,  # This might be the issue
        'warrantyexpiry': None  # This might be the issue
    }
    
    print('Problematic data scenario:')
    for key, value in problematic_data.items():
        print(f'  {key}: {value} (type: {type(value)})')
    
    # Test what happens when we filter out None datetime values
    print('\nAfter filtering out None datetime values:')
    filtered_data = {}
    datetime_fields = ['assigneddate', 'purchasedate', 'warrantyexpiry']
    
    for key, value in problematic_data.items():
        if key in datetime_fields and value is None:
            print(f'  Skipping {key} because it is None')
        else:
            filtered_data[key] = value
            print(f'  Keeping {key}: {value} (type: {type(value)})')
    
    print('\n=== CONCLUSION ===')
    print('The issue is likely that None datetime values are being passed to SQLite.')
    print('SQLite expects actual datetime objects, not None values.')
    print('Solution: Remove datetime fields that are None before creating the Asset object.')

if __name__ == '__main__':
    debug_datetime_conversion()