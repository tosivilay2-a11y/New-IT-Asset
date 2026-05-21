# Fix: SQLAlchemy Mapper Initialization Error

## Problem
After removing the foreign key constraint, you get this error:
```
sqlalchemy.exc.InvalidRequestError: One or more mappers failed to initialize - can't proceed with initialization of other mappers. 
Triggering mapper: 'Mapper[User(users)]'. 
Original exception was: Could not determine join condition between parent/child tables on relationship User.assigned_assets - 
there are no foreign keys linking these tables.
```

## Root Cause
The User model still had a relationship `assigned_assets` that referenced the foreign key we removed from the Asset model. When SQLAlchemy tries to initialize the mappers, it can't find the foreign key to establish the relationship.

## Solution
Remove the `assigned_assets` relationship from the User model since the foreign key no longer exists.

---

## Changes Made

### 1. Updated User Model
**File**: `backend/app/models/user.py`

**Before**:
```python
# Relationships
assigned_assets = relationship("Asset", foreign_keys="Asset.assignedto", back_populates="assigned_user", overlaps="creator")
audit_sessions = relationship("AuditSession", back_populates="created_by_user")
```

**After**:
```python
# Relationships
audit_sessions = relationship("AuditSession", back_populates="created_by_user")
```

### 2. Asset Model (Already Fixed)
**File**: `backend/app/models/asset.py`

Already removed:
- `assignedto` foreign key constraint
- `assigned_user` relationship

---

## How to Apply

### Step 1: Verify Changes
The changes have already been made to:
- `backend/app/models/user.py` - Removed `assigned_assets` relationship
- `backend/app/models/asset.py` - Already has no FK constraint

### Step 2: Restart Backend
```bash
# Stop current backend (Ctrl+C)
python start_server.py
```

### Step 3: Verify No Errors
You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

No mapper initialization errors!

---

## What Was Fixed

### Before
- User model had `assigned_assets` relationship
- Asset model had no foreign key for `assignedto`
- SQLAlchemy couldn't initialize mappers (relationship without FK)

### After
- User model has no `assigned_assets` relationship
- Asset model has `assignedto` as simple integer column
- SQLAlchemy initializes successfully

---

## Files Modified

| File | Change |
|------|--------|
| `backend/app/models/user.py` | Removed `assigned_assets` relationship |
| `backend/app/models/asset.py` | Already fixed (no FK, no relationship) |

---

## Testing

### Verify Backend Starts
```bash
cd backend
python start_server.py
```

Should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Test Check-In/Check-Out
1. Go to "Asset Check-In/Check-Out" page
2. Check out an asset to a staff member
3. Check in the asset
4. ✅ Should work without errors

### Verify Data Display
- [ ] Asset detail page loads without errors
- [ ] Asset list loads without errors
- [ ] Staff information displays correctly
- [ ] History displays correctly

---

## Summary

The `assigned_assets` relationship has been removed from the User model to match the removal of the foreign key constraint from the Asset model. This allows SQLAlchemy to initialize mappers successfully.

**Status**: ✅ READY TO USE

**Next Steps**:
1. Restart backend
2. Test check-in/check-out workflow
3. Verify no errors in console

