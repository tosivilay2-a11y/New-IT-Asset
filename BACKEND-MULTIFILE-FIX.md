# Backend Multi-File Upload Fix

## Problem
The backend was throwing `'str' object has no attribute '_sa_instance_state'` error when trying to update assets with file uploads. This happened because invalid data types (lists, dicts, etc.) were being passed to SQLAlchemy model fields.

## Root Cause
The frontend was sending the entire asset data object to the backend, which included:
- `po_attachment: []` (array)
- `country_name`, `province_name`, etc. (display names, not model fields)
- Other non-model fields

When the backend tried to set these on the SQLAlchemy model using `setattr()`, SQLAlchemy failed because these fields don't exist on the model or have invalid types.

## Solution

### 1. Enhanced `create_asset()` Function
Added step 0 to filter out invalid fields before processing:

```python
# 0. Remove any array/list/object fields that shouldn't be in the model
invalid_fields = ['po_attachment', 'country_name', 'province_name', 'company_name', 
                 'location_name', 'department_name', 'status_name', 'assigned_user_name',
                 'main_category_name', 'category_name']
for field in invalid_fields:
    asset_data.pop(field, None)
```

### 2. Enhanced `update_asset()` Function
Added comprehensive filtering:

```python
# 0. Remove any array/list/object fields that shouldn't be in the model
invalid_fields = ['po_attachment', 'country_name', 'province_name', 'company_name', 
                 'location_name', 'department_name', 'status_name', 'assigned_user_name',
                 'main_category_name', 'category_name', 'assetcode', 'qrcode']
for field in invalid_fields:
    asset_data.pop(field, None)

# ... later when setting fields ...

# 5. Update only provided fields - validate they exist on the model
for key, value in asset_data.items():
    if hasattr(db_asset, key):
        # Skip if value is a list, dict, or other non-scalar type
        if isinstance(value, (list, dict)):
            print(f"Skipping field {key} - invalid type {type(value)}")
            continue
        setattr(db_asset, key, value)
```

### 3. Enhanced Error Handling
Added traceback printing to help debug issues:

```python
except Exception as e:
    db.rollback()
    print(f"Error updating asset: {e}")
    import traceback
    traceback.print_exc()  # Print full stack trace
    raise HTTPException(status_code=400, detail=str(e))
```

## How It Works Now

### Data Flow
1. Frontend sends asset data with files
2. Backend receives JSON data in `asset_data` form field
3. Backend filters out invalid fields (arrays, display names, etc.)
4. Backend validates remaining fields are scalar types
5. Backend sets only valid fields on the model
6. Backend commits changes to database

### Invalid Fields Filtered
- `po_attachment` - Array of files (handled separately)
- `country_name`, `province_name`, etc. - Display names (not model fields)
- `status_name`, `category_name` - Display names (IDs are used instead)
- `assetcode`, `qrcode` - Generated fields (cannot be updated)

### Valid Fields Allowed
- `assetname`, `serialnumber`, `modelnumber`, `manufacturer`
- `categoryid`, `departmentid`, `assignedto`, `assigneddate`
- `purchaseprice`, `currentvalue`, `depreciationrate`
- `warrantyexpiry`, `condition`, `specifications`, `notes`
- `po_number`, `po_attachment_path`, `cost_center`

## Testing

### Manual Testing
1. Create a new asset with 2 PO files
2. Edit the asset and add another file
3. Verify all files are attached

### Expected Behavior
- Asset is created/updated successfully
- Files are appended to `po_attachment_path` as JSON array
- No SQLAlchemy errors occur

## Files Modified
- `backend/app/routes/assets.py`
  - Enhanced `create_asset()` with field filtering
  - Enhanced `update_asset()` with field filtering and type validation
  - Added traceback printing for debugging

## Key Improvements
1. **Field Filtering** - Removes invalid fields before processing
2. **Type Validation** - Skips non-scalar types (lists, dicts)
3. **Better Error Messages** - Prints full traceback for debugging
4. **Defensive Programming** - Checks field existence before setting
