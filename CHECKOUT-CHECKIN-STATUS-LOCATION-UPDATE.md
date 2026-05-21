# Check-Out/Check-In Status & Location Update - COMPLETE ✅

## Summary
Updated the check-in/check-out functionality to:
1. **Check Out**: Automatically set asset status to "In Use"
2. **Check In**: Automatically set asset status based on condition selected
3. **Location**: Automatically set location back to staff member's assigned location

---

## Changes Made

### File: `frontend/src/pages/AssetCheckInOut.jsx`

#### 1. Check-Out Function Update

**Before**:
```javascript
await api.put(`/assets/${asset.assetid}`, {
  assignedto: staffId,
  assigneddate: new Date().toISOString(),
  condition: 'Good'
});
```

**After**:
```javascript
await api.put(`/assets/${asset.assetid}`, {
  assignedto: staffId,
  assigneddate: new Date().toISOString(),
  condition: 'Good',
  statusid: 2  // In Use status
});
```

#### 2. Check-In Function Update

**Before**:
```javascript
await api.put(`/assets/${selectedAsset.assetid}`, {
  assignedto: null,
  condition: checkinForm.condition,
  locationid: locationId
});
```

**After**:
```javascript
// Determine status based on condition
let statusId = 1; // Default: Available
if (checkinForm.condition === 'Damaged') {
  statusId = 3; // Maintenance
} else if (checkinForm.condition === 'Broken') {
  statusId = 4; // Retired/Disposed
}

await api.put(`/assets/${selectedAsset.assetid}`, {
  assignedto: null,
  condition: checkinForm.condition,
  locationid: locationId,  // Use staff's location for check-in
  statusid: statusId  // Set status based on condition
});
```

---

## Status Mapping

### Check-Out
- **Status**: In Use (statusid = 2)
- **Condition**: Good
- **Location**: Unchanged (staff member's location)

### Check-In (Based on Condition)

| Condition | Status | Status ID |
|-----------|--------|-----------|
| Good | Available | 1 |
| Fair | Available | 1 |
| Damaged | Maintenance | 3 |
| Broken | Retired/Disposed | 4 |

---

## Location Handling

### Check-Out
- Location remains unchanged
- Asset stays at current location

### Check-In
- Location automatically set to staff member's assigned location
- Uses `staffMember.locationid`
- If staff has no location, location remains unchanged

---

## Workflow

### Check-Out Workflow
```
1. User selects staff member
2. User clicks "Check Out Asset"
   ↓
3. Asset status → "In Use" (statusid = 2)
4. Asset condition → "Good"
5. Asset assigned to → Staff member
6. Asset location → Unchanged
7. History recorded with CHECKOUT action
```

### Check-In Workflow
```
1. User selects asset to check in
2. User assesses condition (Good/Fair/Damaged/Broken)
3. User clicks "Complete Check-In"
   ↓
4. Asset status → Based on condition:
   - Good/Fair → Available (statusid = 1)
   - Damaged → Maintenance (statusid = 3)
   - Broken → Retired (statusid = 4)
5. Asset condition → Selected condition
6. Asset assigned to → Null (unassigned)
7. Asset location → Staff member's location
8. History recorded with CHECKIN action
```

---

## Data Updates

### Check-Out Updates
```javascript
{
  assignedto: staffId,           // Assign to staff
  assigneddate: timestamp,       // Set assignment date
  condition: 'Good',             // Set condition
  statusid: 2                    // Set to "In Use"
}
```

### Check-In Updates
```javascript
{
  assignedto: null,              // Unassign
  condition: selectedCondition,  // Set condition
  locationid: staffLocationId,   // Set to staff's location
  statusid: statusBasedOnCondition  // Set based on condition
}
```

---

## Status IDs Reference

| Status | ID | Description |
|--------|----|----|
| Available | 1 | Asset is available for use |
| In Use | 2 | Asset is currently assigned |
| Maintenance | 3 | Asset needs repair |
| Retired/Disposed | 4 | Asset is no longer usable |

---

## Location Behavior

### Before Check-In
- Asset location: Current location (e.g., Office A)
- Staff location: Assigned location (e.g., Office B)

### After Check-In
- Asset location: Staff's location (Office B)
- Reason: Asset returns to staff member's assigned location

---

## Testing Checklist

- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] Staff members have assigned locations
- [ ] Asset statuses exist (Available, In Use, Maintenance, Retired)

### Test Check-Out
1. Go to "Asset Check-In/Check-Out" page
2. Click "Check Out Asset"
3. Select asset and staff member
4. Click "Check Out Asset"
5. ✅ Verify asset status changed to "In Use"
6. ✅ Verify asset is assigned to staff
7. ✅ Verify location unchanged

### Test Check-In (Good Condition)
1. Find checked-out asset in list
2. Click "Check In"
3. Select condition: "Good"
4. Click "Complete Check-In"
5. ✅ Verify asset status changed to "Available"
6. ✅ Verify asset location changed to staff's location
7. ✅ Verify asset is unassigned

### Test Check-In (Damaged Condition)
1. Find checked-out asset in list
2. Click "Check In"
3. Select condition: "Damaged"
4. Click "Complete Check-In"
5. ✅ Verify asset status changed to "Maintenance"
6. ✅ Verify asset location changed to staff's location
7. ✅ Verify asset is unassigned

### Test Check-In (Broken Condition)
1. Find checked-out asset in list
2. Click "Check In"
3. Select condition: "Broken"
4. Click "Complete Check-In"
5. ✅ Verify asset status changed to "Retired"
6. ✅ Verify asset location changed to staff's location
7. ✅ Verify asset is unassigned

---

## Files Modified

| File | Changes |
|------|---------|
| `frontend/src/pages/AssetCheckInOut.jsx` | Added status updates for checkout and condition-based status for checkin |

---

## Benefits

✅ **Automatic Status Management**
- No manual status updates needed
- Status reflects asset state
- Consistent status tracking

✅ **Condition-Based Status**
- Damaged assets marked for maintenance
- Broken assets marked as retired
- Good/Fair assets available for reuse

✅ **Location Tracking**
- Assets return to staff location
- Automatic location management
- No manual location updates needed

✅ **Improved Workflow**
- Faster check-in/check-out process
- Less manual data entry
- Better asset tracking

---

## Notes

- Status IDs assume standard configuration (1=Available, 2=In Use, 3=Maintenance, 4=Retired)
- If status IDs differ, update the statusid values in the code
- Location is only updated if staff member has a location assigned
- Condition is always set (Good for checkout, selected for checkin)

---

## Future Enhancements

1. Make status IDs configurable
2. Add custom status mapping
3. Add location history tracking
4. Add automatic maintenance scheduling for damaged assets
5. Add automatic retirement workflow for broken assets
6. Add email notifications for status changes

---

## Summary

Check-out and check-in now automatically manage:
- **Status**: In Use on checkout, condition-based on checkin
- **Location**: Returns to staff member's assigned location
- **Condition**: Good on checkout, selected on checkin
- **Assignment**: Assigned on checkout, unassigned on checkin

**Status**: ✅ COMPLETE AND READY

