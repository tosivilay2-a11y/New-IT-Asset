# Stock Location Config Endpoint - FIXED

## Issue
Frontend was getting 404 error when trying to fetch `/config/stock_location`:
```
GET /config/stock_location HTTP/1.1" 404 Not Found
```

## Root Cause
The frontend was trying to fetch the config from the generic `/config/` endpoint, but:
1. The config endpoint expects the key as a path parameter: `/config/{config_key}`
2. When the config doesn't exist, it returns 404
3. The frontend had no dedicated endpoint to fetch the current stock location

## Solution
Created a dedicated endpoint in the stock_location routes to handle fetching the current stock location configuration.

### Changes Made

**File**: `backend/app/routes/stock_location.py`

Added new endpoint:
```python
@router.get("/config/current")
def get_current_stock_location(db, current_user):
    """Get the currently configured stock location"""
    # Fetches from system_configs table
    # Returns stock location details if configured
    # Returns empty object if not configured
```

**File**: `frontend/src/components/admin/StockLocationConfig.jsx`

Updated to use new endpoint:
```javascript
const configResponse = await api.get('/stock-locations/config/current');
```

**File**: `frontend/src/pages/AssetCheckInOut.jsx`

Updated to use new endpoint:
```javascript
const response = await api.get('/stock-locations/config/current');
```

## API Endpoints

### Stock Location Management
- `GET /stock-locations/` - List all stock locations
- `GET /stock-locations/config/current` - Get currently configured stock location
- `GET /stock-locations/{stock_id}` - Get specific stock location
- `POST /stock-locations/` - Create new stock location
- `PUT /stock-locations/{stock_id}` - Update stock location
- `DELETE /stock-locations/{stock_id}` - Delete stock location

## Response Format

### GET /stock-locations/config/current
```json
{
  "stockid": 1,
  "stockname": "Main Stock",
  "locationid": 5
}
```

If not configured:
```json
{
  "stockid": null,
  "stockname": null,
  "locationid": null
}
```

## Testing
1. Navigate to System Config → Stock Location tab
2. Should load without errors
3. Should display list of stock locations
4. Should allow selecting and saving a stock location
5. Should persist the selection

## Files Modified
1. `backend/app/routes/stock_location.py` - Added `/config/current` endpoint
2. `frontend/src/components/admin/StockLocationConfig.jsx` - Updated to use new endpoint
3. `frontend/src/pages/AssetCheckInOut.jsx` - Updated to use new endpoint

## Status
✅ **FIXED** - Stock location configuration page should now load without 404 errors
