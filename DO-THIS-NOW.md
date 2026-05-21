# ⚡ DO THIS NOW - Fix Backend Error

## You're seeing this error:
```
column "assetid" referenced in foreign key constraint does not exist
```

## THE FIX (One Command)

### Step 1: Stop Current Backend
Press `Ctrl + C` in the CMD window showing the error

### Step 2: Run This
Double-click this file:
```
FIX-AND-START.bat
```

**That's it!** This will:
1. ✅ Fix database schema
2. ✅ Seed all data  
3. ✅ Start backend automatically

---

## What You'll See

```
========================================
FIX DATABASE AND START BACKEND
========================================

Step 1: Fixing Database Schema
✓ Tables dropped
✓ Tables created

Step 2: Seeding Data
✓ Location hierarchy seeded
✓ Asset control data seeded
✓ Test user created

Step 3: Starting Backend
INFO: Uvicorn running on http://127.0.0.1:8000
INFO: Application startup complete.
```

---

## Test It Worked

Open: http://localhost:8000/health

Should show: `{"status":"healthy","version":"2.0.0"}`

---

## If It Doesn't Work

1. Make sure PostgreSQL is running
2. Check `backend/.env` has correct database credentials
3. Read `FIX-DATABASE-SCHEMA.md` for detailed troubleshooting

---

**TL;DR:**
1. Stop backend (Ctrl + C)
2. Run: `FIX-AND-START.bat`
3. Done! ✅
