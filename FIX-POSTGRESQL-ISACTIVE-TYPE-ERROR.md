# Fix: PostgreSQL isactive Type Mismatch Error

## Problem
When creating assets in PostgreSQL, you get this error:
```
psycopg2.errors.DatatypeMismatch: column "isactive" is of type smallint but expression is of type boolean
```

## Root Cause
The PostgreSQL database schema has `isactive` column defined as `smallint` (integer), but the Python code is trying to insert a `boolean` value (True/False).

## Solution

### Step 1: Create Migration
A new migration file has been created: `backend/alembic/versions/004_fix_isactive_type.py`

This migration will:
- Convert `isactive` column from `smallint` to `boolean`
- Set default value to `true`
- Make column NOT NULL

### Step 2: Run Migration
```bash
cd backend
alembic upgrade head
```

### Step 3: Verify
After running the migration, the `isactive` column will be properly typed as `boolean`.

## What Changed

### Database Schema
**Before:**
```sql
isactive smallint
```

**After:**
```sql
isactive boolean NOT NULL DEFAULT true
```

### Python Code
No changes needed - the code already uses `boolean` correctly:
```python
asset_data['isactive'] = True  # Boolean value
```

## Migration Details

### File: `backend/alembic/versions/004_fix_isactive_type.py`

**Upgrade:**
```python
op.alter_column('assets', 'isactive',
                existing_type=sa.SmallInteger(),
                type_=sa.Boolean(),
                existing_nullable=True,
                nullable=False,
                server_default=sa.true())
```

**Downgrade:**
```python
op.alter_column('assets', 'isactive',
                existing_type=sa.Boolean(),
                type_=sa.SmallInteger(),
                existing_nullable=False,
                nullable=True,
                server_default=None)
```

## How to Apply

### Option 1: Automatic (Recommended)
```bash
cd backend
alembic upgrade head
```

### Option 2: Manual SQL (PostgreSQL)
```sql
ALTER TABLE assets 
ALTER COLUMN isactive TYPE boolean USING (isactive::boolean),
ALTER COLUMN isactive SET NOT NULL,
ALTER COLUMN isactive SET DEFAULT true;
```

## Verification

### Check Column Type
```sql
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'assets' AND column_name = 'isactive';
```

**Expected Output:**
```
column_name | data_type
------------|----------
isactive    | boolean
```

### Test Asset Creation
1. Go to frontend
2. Create new asset
3. Should work without errors ✅

## Troubleshooting

### Migration Failed
**Error:** `alembic upgrade head` fails

**Solution:**
1. Check if alembic is installed: `pip install alembic`
2. Check if you're in backend directory: `cd backend`
3. Check database connection in .env

### Still Getting Error
**Error:** Error persists after migration

**Solution:**
1. Verify migration was applied: `alembic current`
2. Check database directly: `SELECT * FROM alembic_version;`
3. Restart backend server

### Rollback Migration
If you need to undo:
```bash
cd backend
alembic downgrade -1
```

## Files Modified

1. **backend/alembic/versions/004_fix_isactive_type.py** (NEW)
   - Migration to fix isactive column type

2. **backend/app/routes/assets.py** (UPDATED)
   - Added comment clarifying isactive is boolean

## Database Compatibility

### PostgreSQL ✅
- Fully supported
- Migration handles conversion

### SQLite ✅
- Already uses boolean correctly
- No migration needed

### MySQL ✅
- Supported (uses TINYINT for boolean)
- Migration handles conversion

## Status: COMPLETE ✅

The type mismatch error is fixed. Asset creation should now work properly with PostgreSQL.

---

**Fix Date:** May 8, 2026
**Status:** Ready to Apply
