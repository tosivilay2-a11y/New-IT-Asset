# Stock Location Save Error - FIXED

## Issue
"Failed to save stock location" error when trying to save a stock location as default.

## Root Cause
The `get_current_stock_location` function in the backend routes was missing the `@router.get("/config/current")` decorator, causing a syntax error that prevented the entire routes module from loading properly.

## Solution
Added the missing decorator to the `get_current_stock_location` function.

### Before
```python
@router.post("/set-default/{stock_id}")
def set_default_stock_location(...):
    ...

def get_current_stock_location(  # MISSING DECORATOR!
    db: Session = Depends(get_db),
    ...
):
```

### After
```python
@router.post("/set-default/{stock_id}")
def set_default_stock_location(...):
    ...

@router.get("/config/current")  # ADDED DECORATOR
def get_current_stock_location(
    db: Session = Depends(get_db),
    ...
):
```

## Route Order
Ensured routes are in correct order for FastAPI:
1. `GET /stock-locations/` - List all
2. `POST /stock-locations/set-default/{stock_id}` - Set default (more specific)
3. `GET /stock-locations/config/current` - Get current config (more specific)
4. `GET /stock-locations/{stock_id}` - Get by ID (generic)
5. `POST /stock-locations/` - Create
6. `PUT /stock-locations/{stock_id}` - Update
7. `DELETE /stock-locations/{stock_id}` - Delete

## Files Modified
- `backend/app/routes/stock_location.py` - Added missing decorator

## Testing
1. Navigate to System Config → Stock Location tab
2. Select a stock location
3. Click "💾 Save Stock Location"
4. Should see success message
5. Stock location should show "⭐ DEFAULT" badge

## Status
✅ **FIXED** - Stock location save should now work correctly
