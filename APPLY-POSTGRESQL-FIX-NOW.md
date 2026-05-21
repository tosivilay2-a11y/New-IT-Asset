# Apply PostgreSQL Fix - Quick Steps

## The Error
```
psycopg2.errors.DatatypeMismatch: column "isactive" is of type smallint but expression is of type boolean
```

## Quick Fix (3 Steps)

### Step 1: Navigate to Backend
```bash
cd backend
```

### Step 2: Run Migration
```bash
alembic upgrade head
```

### Step 3: Restart Backend
```bash
# Stop current backend (Ctrl+C if running)
# Then restart it
python start_server.py
```

## Done! ✅

Asset creation should now work without errors.

## What This Does

- Converts `isactive` column from `smallint` to `boolean`
- Sets default value to `true`
- Makes column NOT NULL

## If It Fails

### Check Alembic
```bash
pip install alembic
```

### Check Database Connection
- Verify DATABASE_URL in `.env`
- Verify PostgreSQL is running
- Verify credentials are correct

### Check Migration Status
```bash
alembic current
```

### Rollback If Needed
```bash
alembic downgrade -1
```

## Verify It Worked

1. Try creating an asset in the UI
2. Should work without errors ✅

---

**Time to Apply:** ~1 minute
**Risk Level:** Low (reversible)
