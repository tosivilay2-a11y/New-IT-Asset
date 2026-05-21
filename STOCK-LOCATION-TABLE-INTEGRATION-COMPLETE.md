# Stock Location Table Integration - COMPLETE

## Overview
Integrated the existing `stocklocation` table into the system configuration for managing default stock locations where assets return after check-in.

## What Was Done

### 1. Backend Model & Routes
**Files Created**:
- `backend/app/models/stock_location.py` - SQLAlchemy model for stocklocation table
- `backend/app/schemas/stock_location.py` - Pydantic schemas for API requests/responses
- `backend/app/routes/stock_location.py` - REST API endpoints for stock location management

**Database Table Structure**:
```
stocklocation
├── stockid (INTEGER, PRIMARY KEY)
├── locationid (INTEGER, FOREIGN KEY → locations.id)
└── stockname (VARCHAR(100))
```

**API Endpoints**:
- `GET /stock-locations/` - List all stock locations
- `GET /stock-locations/{stock_id}` - Get specific stock location
- `POST /stock-locations/` - Create new stock location
- `PUT /stock-locations/{stock_id}` - Update stock location
- `DELETE /stock-locations/{stock_id}` - Delete stock location

### 2. Frontend Configuration Component
**File Updated**: `frontend/src/components/admin/StockLocationConfig.jsx`

**Changes**:
- Simplified from province/company selection to direct stock location selection
- Fetches stock locations from `/stock-locations/` endpoint
- Saves selected stock location to config table with key `stock_location`
- Displays available stock locations with their details

**Features**:
- Dropdown to select stock location
- Displays selected location details (Stock ID, Location ID, Stock Name)
- Shows all available stock locations
- Save and refresh buttons

### 3. Frontend Check-In Integration
**File Updated**: `frontend/src/pages/AssetCheckInOut.jsx`

**Changes**:
- Renamed `stockCompany` state to `stockLocation`
- Updated `fetchStockLocation()` to fetch from `/config/stock_location`
- Updated `handleCheckin()` to use stock location:
  - If stock location configured, use it
  - Otherwise, fallback to staff member's location
  - Updates asset's `locationid` field

### 4. Backend Integration
**File Updated**: `backend/app/main.py`

**Changes**:
- Imported `StockLocation` model
- Imported `stock_location` routes
- Registered stock location router with app

## How It Works

### Configuration
1. Admin navigates to System Config → Stock Location tab
2. Selects a stock location from dropdown
3. Clicks "Save Stock Location"
4. Configuration is stored in system_configs table with key `stock_location`

### Check-In Process
1. User opens Asset Check-In/Check-Out page
2. Selects asset to check in
3. Fills in condition and notes
4. Clicks "Complete Check-In"
5. System:
   - Fetches configured stock location from config
   - If configured, uses that location
   - Otherwise, uses staff member's location
   - Updates asset location
   - Records history with location change
   - Sets status based on condition

## Database Schema

### stocklocation Table
```sql
CREATE TABLE stocklocation (
  stockid INTEGER PRIMARY KEY,
  locationid INTEGER NOT NULL REFERENCES locations(id),
  stockname VARCHAR(100) NOT NULL
);
```

### system_configs Table (for storing selection)
```
config_key: 'stock_location'
config_value: '<stockid>'
config_type: 'number'
category: 'asset_management'
```

## Testing Checklist

- [ ] Navigate to System Config → Stock Location tab
- [ ] Verify stock locations dropdown loads correctly
- [ ] Select a stock location and save
- [ ] Verify success message appears
- [ ] Refresh page and verify location is still selected
- [ ] Check out an asset to a staff member
- [ ] Check in the asset
- [ ] Verify asset location is set to configured stock location
- [ ] View asset detail page and verify location in history
- [ ] Test fallback: Delete stock location config and check in asset
- [ ] Verify asset uses staff member's location as fallback

## Files Created
1. `backend/app/models/stock_location.py` - StockLocation model
2. `backend/app/schemas/stock_location.py` - StockLocation schemas
3. `backend/app/routes/stock_location.py` - StockLocation routes

## Files Modified
1. `backend/app/main.py` - Added stock location imports and router
2. `frontend/src/components/admin/StockLocationConfig.jsx` - Updated to use stocklocation table
3. `frontend/src/components/admin/StockLocationConfig.css` - Simplified styling
4. `frontend/src/pages/AssetCheckInOut.jsx` - Updated to use stock location

## Status
✅ **COMPLETE** - Stock location table fully integrated and ready for testing
