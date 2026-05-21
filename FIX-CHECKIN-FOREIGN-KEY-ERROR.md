# Fix: Check-In Foreign Key Constraint Error

## Problem
When checking in an asset a second time, you get this error:
```
psycopg2.errors.ForeignKeyViolation: insert or update on table "assets" violates foreign key constraint "assets_assignedto_fkey"
DETAIL: Key (assignedto)=(2) is not present in table "users".
```

## Root Cause
The `assignedto` column in the `assets` table has a foreign key constraint pointing to `users.userid`. However, we're now assigning assets to **staff members** (using staffid), not users. When trying to set `assignedto` to a staff ID that doesn't exist in the users table, the constraint fails.

## Solution
Remove the foreign key constraint from the `assignedto` column since it can now reference either users or staff members.

---

## Steps to Fix

### Step 1: Update the Asset Model
The model has already been updated to remove the foreign key constraint:

**File**: `backend/app/models/asset.py`

```python
# Before:
assignedto = Column(Integer, ForeignKey("users.userid"))

# After:
assignedto = Column(Integer, nullable=True)  # Staff member ID (no FK constraint)
```

### Step 2: Apply the Database Migration
Run the migration to remove the constraint from the database:

```bash
cd backend
alembic upgrade head
```

Or use the provided script:
```bash
cd backend
python apply_fk_fix.py
```

### Step 3: Restart the Backend
```bash
# Stop the current backend process
# Then restart it
python start_server.py
```

---

## What Changed

### Database Schema
- **Before**: `assignedto` column had FK constraint → `users.userid`
- **After**: `assignedto` column has no FK constraint (can be any integer)

### Asset Model
- **Before**: `assignedto = Column(Integer, ForeignKey("users.userid"))`
- **After**: `assignedto = Column(Integer, nullable=True)`

### Relationships
- **Before**: Had `assigned_user` relationship
- **After**: Removed `assigned_user` relationship (no longer needed)

---

## Migration Details

**File**: `backend/alembic/versions/009_remove_assignedto_fk.py`

```python
def upgrade() -> None:
    # Drop the foreign key constraint on assignedto
    op.drop_constraint('assets_assignedto_fkey', 'assets', type_='foreignkey')

def downgrade() -> None:
    # Recreate the foreign key constraint
    op.create_foreign_key('assets_assignedto_fkey', 'assets', 'users', ['assignedto'], ['userid'])
```

---

## Testing

### Test Check-In/Check-Out Workflow
1. Start backend: `python backend/start_server.py`
2. Start frontend: `npm start` (in frontend folder)
3. Login to system
4. Go to "Asset Check-In/Check-Out" page
5. Check out an asset to a staff member
6. Check in the asset
7. ✅ Should work without foreign key error
8. Check in the asset again
9. ✅ Should work without foreign key error

### Verify Assignment Display
- [ ] Asset detail page shows staff member info
- [ ] Asset list shows staff member name and employee ID
- [ ] History shows staff member assignments

---

## Files Modified

| File | Change |
|------|--------|
| `backend/app/models/asset.py` | Removed FK constraint from assignedto column |
| `backend/alembic/versions/009_remove_assignedto_fk.py` | New migration to remove FK constraint |
| `backend/apply_fk_fix.py` | Helper script to apply migration |

---

## Why This Fix Works

### Before
- `assignedto` could only reference users
- Assigning to staff (staffid) violated the constraint
- Second check-in failed because staffid wasn't in users table

### After
- `assignedto` can reference any integer (staff or user)
- No constraint violation when assigning to staff
- Check-in/check-out works multiple times
- System is more flexible for future enhancements

---

## Important Notes

1. **Data Integrity**: While we removed the FK constraint, the application logic still validates that the staff member exists before assignment
2. **Backward Compatibility**: Existing user assignments still work (they're just integers now)
3. **Migration**: The migration is reversible (can downgrade if needed)
4. **No Data Loss**: This change doesn't affect existing data, only removes the constraint

---

## Troubleshooting

### Migration Fails
**Error**: `alembic.util.exc.CommandError: Can't locate revision identified by 'head'`

**Solution**: Make sure you're in the backend directory:
```bash
cd backend
alembic upgrade head
```

### Still Getting Foreign Key Error
**Cause**: Migration wasn't applied

**Solution**: 
1. Check migration status: `alembic current`
2. Apply migration: `alembic upgrade head`
3. Restart backend

### Need to Rollback
```bash
cd backend
alembic downgrade -1
```

---

## Next Steps

After applying this fix:
1. ✅ Check-in/check-out works multiple times
2. ✅ Assets can be assigned to staff members
3. ✅ Asset detail page shows staff information
4. ✅ Asset list shows staff information
5. ✅ History tracking works correctly

---

## Summary

The foreign key constraint on `assignedto` has been removed to allow assignment to staff members instead of just users. This enables the new staff-based asset assignment system to work correctly without constraint violations.

**Status**: ✅ READY TO APPLY

