# ⚠️ READ ME FIRST - Backend Won't Start

## The Error You're Seeing

```
column "assetid" referenced in foreign key constraint does not exist
```

## What This Means

Your database has old tables that don't match the new code.

## The Fix (2 Minutes)

### Option 1: Automated (Easiest)

Just run this:
```bash
QUICK-FIX-DATABASE.bat
```

This will:
1. ✅ Recreate database tables
2. ✅ Seed all data
3. ✅ Tell you to start backend

Then run:
```bash
start-backend-server.bat
```

### Option 2: All-in-One

Run this to fix AND start backend:
```bash
fix-database-and-start.bat
```

### Option 3: Manual

```bash
cd backend
venv\Scripts\activate
python recreate_tables.py --yes
python seed_location_hierarchy.py
python seed_asset_control_data.py
python create_test_user.py
uvicorn app.main:app --reload --port 8000
```

---

## What Gets Created

After running the fix:

**Data:**
- 5 Countries (LA, TH, VN, KH, MM)
- 8 Provinces (VTE, LPB, etc.)
- 7 Companies (AVIS, FORD, etc.)
- 13 Categories (C, L, M, etc.)
- 8 Statuses (Available, In Use, etc.)
- 8 Departments (IT, HR, etc.)
- 1 Test User (admin@example.com / admin123)

**Tables:**
- ✅ Correct schema with `assetid`, `userid`, etc.
- ✅ All relationships working
- ✅ 40+ fields in Asset table

---

## After Fix

Backend will start successfully:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

Test it:
- http://localhost:8000/health
- http://localhost:8000/docs
- http://localhost:8000/countries

---

## Why This Happened

The database was created with old schema (simple `id` columns).
The new code uses specific IDs (`assetid`, `userid`, `departmentid`, etc.).
Database needs to be recreated to match.

---

## Quick Commands

```bash
# Fix database
QUICK-FIX-DATABASE.bat

# Start backend
start-backend-server.bat

# Or do both at once
fix-database-and-start.bat
```

---

**TL;DR:**
1. Run: `QUICK-FIX-DATABASE.bat`
2. Run: `start-backend-server.bat`
3. Done! ✅

---

**Files to Read:**
- `START-BACKEND-NOW.md` - Detailed instructions
- `FIX-DATABASE-SCHEMA.md` - Complete troubleshooting
- `HOW-TO-RUN-BACKEND.md` - How to run backend normally
