# Stock Company Configuration - FIXED

## Issue
Provinces and companies dropdowns were showing as blank because the component was using incorrect field names.

## Root Cause
- Backend returns: `provinceid`, `provincename`, `companyid`, `companyname`
- Component was looking for: `id`, `name`

## Solution
Updated all field references in `StockLocationConfig.jsx`:

### Province Fields
- Changed `province.id` → `province.provinceid`
- Changed `province.name` → `province.provincename`

### Company Fields
- Changed `company.id` → `company.companyid` (already correct)
- Changed `company.name` → `company.companyname` (already correct)

### Updated Locations
1. Province dropdown options - now uses `provinceid` and `provincename`
2. Province filtering - now uses `provinceid`
3. Selected province display - now uses `provincename`
4. Province list display - now uses `provinceid` and `provincename`

## Testing
The component should now:
1. ✅ Load provinces from API
2. ✅ Display provinces in dropdown
3. ✅ Filter companies by selected province
4. ✅ Display companies in dropdown
5. ✅ Save selected company to config
6. ✅ Display available companies grouped by province

## Files Modified
- `frontend/src/components/admin/StockLocationConfig.jsx` - Fixed all field name references

## Status
✅ **FIXED** - Provinces and companies should now load and display correctly
