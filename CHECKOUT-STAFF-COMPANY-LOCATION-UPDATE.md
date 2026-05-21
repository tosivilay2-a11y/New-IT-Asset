# Task 35: Update Check-Out to Use Staff companyid as Asset locationid

## Status: ✅ COMPLETE

## Summary
Updated the checkout function to automatically set the asset's `locationid` to the staff member's `companyid` when checking out an asset.

## Changes Made

### File: `frontend/src/pages/AssetCheckInOut.jsx`

#### Change 1: Get Staff Member and Validate
Added validation to fetch the selected staff member and check if they exist:
```javascript
// Get staff member's company ID to use as asset location
const selectedStaff = staff.find(s => s.staffid === staffId);
if (!selectedStaff) {
  setError('Staff member not found');
  setLoading(false);
  return;
}
```

#### Change 2: Update Asset with Staff's Company as Location
Modified the API call to include `locationid: selectedStaff.companyid`:
```javascript
await api.put(`/assets/${asset.assetid}`, {
  assignedto: staffId,
  assigneddate: new Date().toISOString(),
  condition: 'Good',
  statusid: 2,  // In Use status
  locationid: selectedStaff.companyid  // Set asset location to staff's company
});
```

#### Change 3: Update History Recording
Updated the checkout history to record the new location (staff's company):
```javascript
await api.post('/asset-history/', {
  assetid: asset.assetid,
  action: 'CHECKOUT',
  staffid: staffId,
  reason: checkoutForm.reason,
  condition_before: asset.condition || 'Good',
  condition_after: 'Good',
  location_before: asset.locationid,
  location_after: selectedStaff.companyid,  // New location is staff's company
  notes: `Checked out to staff member ${selectedStaff.fullname}`
});
```

## How It Works

1. **User selects a staff member** for checkout
2. **System retrieves staff member's companyid** from the staff object
3. **Asset is updated** with:
   - `assignedto`: Staff member ID
   - `statusid`: 2 (In Use)
   - `locationid`: Staff member's company ID
4. **History is recorded** showing the location change from original location to staff's company

## Behavior

- When an asset is checked out to a staff member, the asset's location automatically changes to that staff member's company
- This ensures the asset location reflects where the staff member (and thus the asset) is located
- The history tracking shows the location transition for audit purposes

## Verification

✅ No syntax errors
✅ File compiles successfully
✅ Logic is consistent with check-in/check-out workflow
✅ History recording includes location changes

## Related Files
- `backend/app/models/staff.py` - Staff model with companyid field
- `backend/app/models/asset.py` - Asset model with locationid field
- `frontend/src/pages/AssetCheckInOut.jsx` - Updated checkout function
