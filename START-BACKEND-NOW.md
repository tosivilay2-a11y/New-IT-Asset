# 🚀 Start Backend - Step by Step

## Current Issue

Backend won't start because database schema is outdated.

**Error:** `column "assetid" referenced in foreign key constraint does not exist`

---

## Fix It (5 Minutes)

### Step 1: Recreate Database Tables

**Option A: Automated (Recommended)**
```bash
recreate-database-tables.bat
```
Press Enter when prompted.

**Option B: Manual**
```bash
cd backend
venv\Scripts\activate
python recreate_tables.py
```
Type `yes` when prompted.

### Step 2: Seed Data

```bash
cd backend
venv\Scripts\activate
python seed_location_hierarchy.py
python seed_asset_control_data.py
python create_test_user.py
```

### Step 3: Start Backend

**Option A: Batch File**
```bash
start-backend-server.bat
```

**Option B: Manual**
```bash
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```

### Step 4: Verify

Open: http://localhost:8000/health

Should show: `{"status":"healthy","version":"2.0.0"}`

---

## Quick Commands (Copy & Paste)

```bash
# 1. Recreate database
cd backend
venv\Scripts\activate
python recreate_tables.py

# Type 'yes' when prompted

# 2. Seed data
python seed_location_hierarchy.py
python seed_asset_control_data.py
python create_test_user.py

# 3. Start backend
uvicorn app.main:app --reload --port 8000
```

---

## What Gets Created

**Countries:** LA, TH, VN, KH, MM
**Provinces:** VTE, LPB, CPS, SVK, APU, BKK, CNX, HKT
**Companies:** AVIS, FORD, EFGL, LARV, RMAG, COMN
**Categories:** C, L, M, P, N, S, W, T, H, A, O, D, U
**Statuses:** Available, In Use, Maintenance, Retired, Disposed, Lost, Damaged, Reserved
**Departments:** Admin, CS, Finance, HR, IT, Marketing, Operations, Sales
**Test User:** admin@example.com / admin123

---

## Why This Is Needed

The old database has simple schema (generic `id` columns).
The new code uses specific IDs (`assetid`, `userid`, etc.).
Database needs to be recreated to match new schema.

---

## After Backend Starts

1. **Test Health:** http://localhost:8000/health
2. **Test API Docs:** http://localhost:8000/docs
3. **Test Countries:** http://localhost:8000/countries
4. **Test Admin Page:** http://localhost:3000/admin/config

---

## Troubleshooting

### "Are you sure?" prompt
Type: `yes` and press Enter

### "Port already in use"
```bash
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### "Connection refused"
PostgreSQL is not running. Start it.

### Still errors?
Read: `FIX-DATABASE-SCHEMA.md`

---

**TL;DR:**
1. Run: `recreate-database-tables.bat`
2. Type: `yes`
3. Run seed scripts
4. Start backend
5. Done! ✅
