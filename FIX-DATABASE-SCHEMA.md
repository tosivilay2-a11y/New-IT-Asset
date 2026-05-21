# 🔧 Fix Database Schema Issues

## Problem

The backend won't start because of database schema mismatches:
- Old tables use `id` as primary key
- New models use specific IDs like `assetid`, `userid`, etc.
- Foreign key references don't match

## Solution

Recreate the database tables with the correct schema.

---

## ⚠️ WARNING

**This will delete all existing data!**

If you have important data, back it up first.

---

## Steps to Fix

### 1. Recreate Database Tables

Run this command:
```bash
recreate-database-tables.bat
```

This will:
- Drop all existing tables
- Create new tables with correct schema
- Show you what to do next

### 2. Seed Location Hierarchy

```bash
cd backend
venv\Scripts\activate
python seed_location_hierarchy.py
```

This creates:
- 5 Countries
- 8 Provinces
- 7 Companies
- 13 Main Categories

### 3. Seed Asset Control Data

```bash
python seed_asset_control_data.py
```

This creates:
- 8 Asset Statuses
- 8 Departments

### 4. Create Test User

```bash
python create_test_user.py
```

This creates:
- Admin user: admin@example.com / admin123

### 5. Start Backend

```bash
cd ..
restart-backend.bat
```

Or manually:
```bash
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```

---

## Verify It Worked

### Test 1: Backend Starts
Backend should start without errors and show:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

### Test 2: Health Check
```bash
curl http://localhost:8000/health
```
Should return: `{"status":"healthy","version":"2.0.0"}`

### Test 3: Admin Routes
```bash
curl http://localhost:8000/countries
curl http://localhost:8000/provinces
curl http://localhost:8000/companies
curl http://localhost:8000/main-categories
```
Should return JSON data (not "Not Found")

### Test 4: Frontend
Open: http://localhost:3000/admin/config

Should load without 404 errors.

---

## What Changed

### Old Schema
```sql
CREATE TABLE assets (
    id INTEGER PRIMARY KEY,  -- ❌ Generic id
    ...
);

CREATE TABLE users (
    id INTEGER PRIMARY KEY,  -- ❌ Generic id
    ...
);
```

### New Schema
```sql
CREATE TABLE assets (
    assetid INTEGER PRIMARY KEY,  -- ✅ Specific assetid
    assetcode VARCHAR(50),
    assetname VARCHAR(200),
    maincategoryid INTEGER,
    countryid INTEGER,
    provinceid INTEGER,
    companyid INTEGER,
    locationid INTEGER,
    departmentid INTEGER,
    statusid INTEGER,
    ...40+ fields
);

CREATE TABLE users (
    userid INTEGER PRIMARY KEY,  -- ✅ Specific userid
    ...
);

CREATE TABLE departments (
    departmentid INTEGER PRIMARY KEY,
    departmentname VARCHAR(100),
    companyid INTEGER,
    ...
);

CREATE TABLE assetstatuses (
    statusid INTEGER PRIMARY KEY,
    statusname VARCHAR(50),
    color VARCHAR(20),
    ...
);

CREATE TABLE assettransfers (
    transferid INTEGER PRIMARY KEY,
    assetid INTEGER,
    fromlocationid INTEGER,
    tolocationid INTEGER,
    ...
);
```

---

## Troubleshooting

### Error: "Table already exists"

The old tables are still there. Run:
```bash
recreate-database-tables.bat
```

### Error: "No module named 'app'"

Make sure you're in the backend directory and venv is activated:
```bash
cd backend
venv\Scripts\activate
```

### Error: "Connection refused"

PostgreSQL is not running. Start it:
```bash
# Check if PostgreSQL service is running
# Start it if needed
```

### Backend still won't start

Check the error message. Common issues:
1. **Import errors** - Check all model imports in `__init__.py`
2. **Foreign key errors** - Check column names match
3. **Duplicate table errors** - Run recreate script again

---

## Quick Commands

```bash
# Full setup from scratch
recreate-database-tables.bat

cd backend
venv\Scripts\activate
python seed_location_hierarchy.py
python seed_asset_control_data.py
python create_test_user.py

cd ..
restart-backend.bat
```

---

## Files Modified

**Models:**
- `backend/app/models/asset.py` - Enhanced with 40+ fields
- `backend/app/models/user.py` - Added userid column
- `backend/app/models/department.py` - New model
- `backend/app/models/asset_status.py` - New model
- `backend/app/models/asset_transfer.py` - New model
- `backend/app/models/enhanced_asset.py` - Removed duplicates

**Routes:**
- `backend/app/routes/admin.py` - Fixed imports
- `backend/app/routes/departments.py` - New routes
- `backend/app/routes/asset_statuses.py` - New routes
- `backend/app/routes/asset_transfers.py` - New routes

**Main:**
- `backend/app/main.py` - Added new route registrations

---

## Success Indicators

✅ Backend starts without errors
✅ No "table already exists" errors
✅ No "column does not exist" errors
✅ `/countries` returns data
✅ `/provinces` returns data
✅ `/companies` returns data
✅ `/main-categories` returns data
✅ `/departments` returns data
✅ `/asset-statuses` returns data
✅ Admin page loads without 404 errors

---

## Next Steps After Fix

1. **Test Admin Page**
   - Open: http://localhost:3000/admin/config
   - Try adding a category
   - Try adding a country
   - Try adding a province
   - Try adding a company

2. **Test Asset Management**
   - Create an asset
   - Assign to location
   - Assign to user
   - Change status

3. **Test Transfer Workflow**
   - Request a transfer
   - Approve transfer
   - Complete transfer

---

**Summary:**
- ❌ Old schema had generic `id` columns
- ✅ New schema has specific IDs (`assetid`, `userid`, etc.)
- 🔧 Solution: Recreate tables with correct schema
- ⏱️ Time: 5 minutes
- 📊 Result: Clean database with proper relationships

**Run:** `recreate-database-tables.bat` to fix!
