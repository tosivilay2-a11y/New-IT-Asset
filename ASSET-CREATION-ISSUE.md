# Asset Creation Issue - Field Mismatch

## Problem

The frontend is sending data with different field names than what the backend expects.

## Frontend Sends (AssetsManagementEnhanced.jsx)

```javascript
{
  main_category: 'Laptop',           // String - category name
  category_code: 'L',                // String - category code
  country_id: 1,                     // Integer ✓
  province_id: 1,                    // Integer ✓
  company_id: 3,                     // Integer ✓
  purchase_date: '2026-05-06',       // String date
  status: 'Available',               // String - status name
  brand: 'Dell',
  model: 'Latitude 5420',
  // ... other fields
}
```

## Backend Expects (asset.py schema)

```python
{
  assetname: str,                    # REQUIRED - Asset name
  maincategoryid: int,               # REQUIRED - Main category ID (not name!)
  categoryid: int | None,            # Optional - Category ID
  countryid: int,                    # REQUIRED ✓
  provinceid: int,                   # REQUIRED ✓
  companyid: int,                    # REQUIRED ✓
  locationid: int,                   # REQUIRED - Location ID
  statusid: int,                     # REQUIRED - Status ID (not name!)
  purchasedate: datetime | None,     # Optional
  manufacturer: str | None,          # Optional (brand)
  modelnumber: str | None,           # Optional (model)
  // ... other fields
}
```

## Missing Mappings

### 1. Asset Name
- **Frontend:** No field for asset name
- **Backend:** Requires `assetname`
- **Fix:** Add asset name field to form

### 2. Main Category ID
- **Frontend:** Sends `main_category` (string name)
- **Backend:** Expects `maincategoryid` (integer ID)
- **Fix:** Frontend needs to get category ID from backend

### 3. Status ID
- **Frontend:** Sends `status` (string name like "Available")
- **Backend:** Expects `statusid` (integer ID)
- **Fix:** Frontend needs to get status ID from backend

### 4. Location ID
- **Frontend:** Doesn't send `locationid`
- **Backend:** Requires `locationid`
- **Fix:** Frontend needs to either:
  - Get location ID from backend based on company
  - Or create a location selector

## Quick Fix Options

### Option 1: Update Frontend (Recommended)
Update `AssetsManagementEnhanced.jsx` to:
1. Add asset name field
2. Fetch and use category IDs instead of names
3. Fetch and use status IDs instead of names
4. Add location selector or use default location

### Option 2: Update Backend Schema
Make the backend more flexible to accept:
1. Category names and look up IDs
2. Status names and look up IDs
3. Auto-assign default location if not provided

### Option 3: Create Adapter Layer
Add a transformation layer in the frontend API service that converts frontend format to backend format.

## Recommended Solution

**Update the backend `/assets/` endpoint to be more flexible:**

```python
@router.post("/", response_model=AssetResponse)
def create_asset(asset_data: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Convert frontend format to backend format
    
    # 1. Get main category ID from name
    if 'main_category' in asset_data:
        category = db.query(MainCategory).filter(
            MainCategory.categoryname == asset_data['main_category']
        ).first()
        asset_data['maincategoryid'] = category.maincategoryid if category else None
    
    # 2. Get status ID from name
    if 'status' in asset_data:
        status = db.query(AssetStatus).filter(
            AssetStatus.statusname == asset_data['status']
        ).first()
        asset_data['statusid'] = status.statusid if status else 1  # Default to first status
    
    # 3. Use company's default location or create one
    if 'locationid' not in asset_data and 'company_id' in asset_data:
        # Get or create default location for company
        location = db.query(Location).filter(
            Location.companyid == asset_data['company_id']
        ).first()
        if not location:
            # Create default location
            location = Location(
                name=f"Default Location",
                companyid=asset_data['company_id']
            )
            db.add(location)
            db.flush()
        asset_data['locationid'] = location.id
    
    # 4. Set asset name from model or generate
    if 'assetname' not in asset_data:
        asset_data['assetname'] = f"{asset_data.get('brand', '')} {asset_data.get('model', '')}".strip() or "New Asset"
    
    # 5. Map field names
    field_mapping = {
        'country_id': 'countryid',
        'province_id': 'provinceid',
        'company_id': 'companyid',
        'purchase_date': 'purchasedate',
        'brand': 'manufacturer',
        'model': 'modelnumber',
    }
    
    for old_name, new_name in field_mapping.items():
        if old_name in asset_data:
            asset_data[new_name] = asset_data.pop(old_name)
    
    # Now create the asset...
```

## Immediate Action

I'll update the backend `/assets/` endpoint to handle the frontend's current data format.

This will allow asset creation to work without changing the frontend.
