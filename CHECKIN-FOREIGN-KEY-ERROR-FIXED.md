# Check-In Foreign Key Error - FIXED ✅

## Problem

**Error**: `ForeignKeyViolation: Key (locationid)=(4) is not present in table "locations"`

**Root Cause**: The code was using `stockid` (4) as the `locationid`, but the database expects a valid location ID from the `locations` table.

**What Was Wrong**:
```javascript
// WRONG - Using stockid as locationid
if (selectedStockLocation) {
  locationId = selectedStockLocation;  // This is stockid (4)
}
```

**Why It Failed**:
- `stockid = 4` (from stocklocation table)
- `locationid` in assets table has FK constraint to `locations` table
- Location ID 4 doesn't exist in `locations` table
- Database rejects the update

## Solution

**Use the `locationid` from the stock_location table, not the `stockid`**:

```javascript
// CORRECT - Using locationid from stock_location table
if (selectedStockLocation) {
  const selectedStock = stockLocations.find(s => s.stockid === selectedStockLocation);
  if (selectedStock) {
    locationId = selectedStock.locationid;  // Use locationid, not stockid
  }
}
```

## Data Structure

### Stock Location Table
```
stockid | stockname        | locationid | stockdefault
--------|------------------|------------|-------------
   3    | RMAL IT Stock    |     1      |    true
   4    | Ford office      |     2      |    false
```

### Locations Table
```
id | name
---|------
1  | RMAL HQ
2  | Ford Office
3  | Secondary
```

### Assets Table (FK Constraint)
```
assetid | locationid (FK to locations.id)
--------|--------------------------------
   1    | 1 (valid - exists in locations)
   2    | 2 (valid - exists in locations)
```

## Code Changes

### Before (Broken)
```javascript
// Determine location: use selected stock location, fallback to default, then staff's location
let locationId = null;

// Use selected stock location
if (selectedStockLocation) {
  locationId = selectedStockLocation;  // ❌ WRONG - This is stockid
} 
// Fallback to default stock location
else if (defaultStockLocation) {
  locationId = defaultStockLocation;  // ❌ WRONG - This is stockid
} 
// Fallback to staff member's location if stock location not available
else if (selectedAsset.assignedto) {
  const staffMember = staff.find(s => s.staffid === selectedAsset.assignedto);
  if (staffMember && staffMember.locationid) {
    locationId = staffMember.locationid;  // ✅ CORRECT
  }
}
```

### After (Fixed)
```javascript
// Determine location: use selected stock location, fallback to default, then staff's location
let locationId = null;

// Use selected stock location's locationid
if (selectedStockLocation) {
  const selectedStock = stockLocations.find(s => s.stockid === selectedStockLocation);
  if (selectedStock) {
    locationId = selectedStock.locationid;  // ✅ CORRECT - Use locationid
  }
} 
// Fallback to default stock location's locationid
else if (defaultStockLocation) {
  const defaultStock = stockLocations.find(s => s.stockid === defaultStockLocation);
  if (defaultStock) {
    locationId = defaultStock.locationid;  // ✅ CORRECT - Use locationid
  }
} 
// Fallback to staff member's location if stock location not available
else if (selectedAsset.assignedto) {
  const staffMember = staff.find(s => s.staffid === selectedAsset.assignedto);
  if (staffMember && staffMember.locationid) {
    locationId = staffMember.locationid;  // ✅ CORRECT
  }
}
```

## Key Changes

1. **Find the stock location object** from `stockLocations` array
2. **Extract the `locationid`** from that object
3. **Use `locationid`** (not `stockid`) for the asset update

## Example Flow

### User Selects "Ford office" Stock Location

**Step 1**: User selects from dropdown
```
selectedStockLocation = 4  // This is stockid
```

**Step 2**: Find the stock location object
```javascript
const selectedStock = stockLocations.find(s => s.stockid === 4);
// Result: { stockid: 4, stockname: "Ford office", locationid: 2, stockdefault: false }
```

**Step 3**: Extract locationid
```javascript
locationId = selectedStock.locationid;  // locationId = 2
```

**Step 4**: Update asset with valid locationid
```javascript
UPDATE assets SET locationid = 2 WHERE assetid = 1
// ✅ SUCCESS - locationid 2 exists in locations table
```

## Testing

### Test 1: Check-In with Selected Stock Location
1. Open check-in modal
2. Select "Ford office" stock location
3. Complete check-in
4. ✅ Asset should be at location 2 (Ford Office)
5. ✅ No foreign key error

### Test 2: Check-In with Default Stock Location
1. Open check-in modal
2. Don't change stock location (use default)
3. Complete check-in
4. ✅ Asset should be at default location
5. ✅ No foreign key error

### Test 3: Check-In with Fallback to Staff Location
1. Delete all stock locations
2. Open check-in modal
3. Complete check-in
4. ✅ Asset should be at staff member's location
5. ✅ No foreign key error

## Files Modified

- `frontend/src/pages/AssetCheckInOut.jsx`
  - Updated check-in location determination logic
  - Now correctly uses `locationid` from stock_location table

## Database Verification

### Check Valid Locations
```sql
SELECT id, name FROM locations;
```

### Check Stock Locations
```sql
SELECT stockid, stockname, locationid FROM stocklocation;
```

### Verify Asset Location After Check-In
```sql
SELECT assetid, locationid FROM assets WHERE assetid = 1;
```

## Error Prevention

### What to Remember
- `stockid` = Primary key of stocklocation table
- `locationid` = Foreign key in stocklocation table (points to locations table)
- `assets.locationid` = Foreign key (must exist in locations table)

### Always Use
```javascript
// Get the locationid from stock_location, not the stockid
const stock = stockLocations.find(s => s.stockid === selectedStockLocation);
const locationId = stock.locationid;  // ✅ CORRECT
```

### Never Use
```javascript
// Don't use stockid as locationid
const locationId = selectedStockLocation;  // ❌ WRONG
```

## Status

**FIXED** ✅

The foreign key error has been resolved by correctly using the `locationid` from the stock_location table instead of the `stockid`.

---

**Error**: RESOLVED ✅
**Date**: 2026-05-13
**File**: frontend/src/pages/AssetCheckInOut.jsx
**Status**: PRODUCTION READY
