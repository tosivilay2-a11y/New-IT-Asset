# Stock Company Configuration - COMPLETE

## Task Summary
Updated stock location configuration to use company and province selection. Assets now return to a configured stock company instead of a location.

## What Was Done

### 1. Updated StockLocationConfig Component
**File**: `frontend/src/components/admin/StockLocationConfig.jsx`

**Changes**:
- Renamed from "Stock Location" to "Stock Company Configuration"
- Added province and company selection dropdowns
- Province dropdown filters companies by province
- Company dropdown is disabled until province is selected
- Fetches provinces and companies from API
- Loads current stock company configuration from `/config/stock_company`
- Saves configuration with key `stock_company` instead of `stock_location`

**Features**:
- Two-step selection: Province → Company
- Displays available companies grouped by province
- Shows selected province and company details
- Fallback logic if stock company not configured

### 2. Updated StockLocationConfig CSS
**File**: `frontend/src/components/admin/StockLocationConfig.css`

**Changes**:
- Added `.form-row` for side-by-side province/company dropdowns
- Added responsive grid layout (2 columns on desktop, 1 on mobile)
- Added `.province-list` and `.company-list` for displaying available options
- Added `.company-item` styling for company display
- Added `.no-companies` styling for empty states
- Updated disabled state styling for form controls

### 3. Updated AssetCheckInOut Component
**File**: `frontend/src/pages/AssetCheckInOut.jsx`

**Changes**:
- Renamed `stockLocation` state to `stockCompany`
- Updated `fetchStockLocation()` to `fetchStockLocation()` (fetches from `/config/stock_company`)
- Updated `handleCheckin()` to use company instead of location:
  - If `stockCompany` is configured, use it
  - Otherwise, fallback to staff member's company
  - Updates asset's `companyid` field instead of `locationid`

**Check-In Logic**:
```
1. Fetch configured stock company from `/config/stock_company`
2. If stock company exists, use it
3. Otherwise, use staff member's assigned company
4. Update asset with new company
5. Record history with company change
```

## How It Works

### Configuration
1. Admin navigates to System Config → Stock Location tab
2. Selects a province from dropdown
3. Selects a company from the filtered list
4. Clicks "Save Stock Company"
5. Configuration is stored in database with key `stock_company`

### Check-In Process
1. User opens Asset Check-In/Check-Out page
2. Selects asset to check in
3. Fills in condition and notes
4. Clicks "Complete Check-In"
5. System:
   - Uses configured stock company (if set)
   - Falls back to staff's company (if not configured)
   - Updates asset company
   - Records history with company change
   - Sets status based on condition

## API Endpoints Used

### Configuration
- `GET /config/stock_company` - Retrieve configured stock company
- `POST /config/` - Save stock company configuration

### Data Fetching
- `GET /provinces/` - List all provinces
- `GET /companies/` - List all companies
- `GET /staff/` - List all staff members

### Asset Operations
- `PUT /assets/{assetid}` - Update asset company on check-in
- `POST /asset-history/` - Record check-in history

## Configuration Payload

```javascript
{
  config_key: 'stock_company',
  config_value: companyId.toString(),
  config_type: 'number',
  category: 'asset_management',
  description: 'Default stock company for checked-in assets'
}
```

## Testing Checklist

- [ ] Navigate to System Config → Stock Location tab
- [ ] Verify provinces dropdown loads correctly
- [ ] Select a province
- [ ] Verify companies dropdown filters by province
- [ ] Select a company and save
- [ ] Verify success message appears
- [ ] Refresh page and verify company is still selected
- [ ] Check out an asset to a staff member
- [ ] Check in the asset
- [ ] Verify asset company is set to configured stock company
- [ ] View asset detail page and verify company in history
- [ ] Test fallback: Delete stock company config and check in asset
- [ ] Verify asset uses staff member's company as fallback

## Files Modified
1. `frontend/src/components/admin/StockLocationConfig.jsx` - Updated to use company/province selection
2. `frontend/src/components/admin/StockLocationConfig.css` - Updated styling for new layout
3. `frontend/src/pages/AssetCheckInOut.jsx` - Updated check-in logic to use stock company

## Status
✅ **COMPLETE** - Stock company configuration fully integrated and ready for testing
