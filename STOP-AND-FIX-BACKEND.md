# 🛑 Stop Backend and Fix Database

## You Have Backend Running in Another CMD

I can see you have a backend process running that's showing this error:
```
column "assetid" referenced in foreign key constraint does not exist
```

## Step-by-Step Fix

### Step 1: Stop the Running Backend

1. Find the CMD window with the backend (shows the error)
2. Click on that window
3. Press `Ctrl + C`
4. Wait for it to stop completely

### Step 2: Fix the Database

Run this command:
```bash
QUICK-FIX-DATABASE.bat
```

This will:
- Recreate database tables with correct schema
- Seed all data (countries, provinces, companies, etc.)
- Create test user

### Step 3: Start Backend Again

After the fix completes, run:
```bash
start-backend-server.bat
```

Or in the same CMD window:
```bash
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```

---

## Visual Guide

```
┌─────────────────────────────────────┐
│ CMD Window (Backend Running)        │
│                                     │
│ ERROR: column "assetid" does not   │
│ exist...                            │
│                                     │
│ ► Press Ctrl + C here              │
└─────────────────────────────────────┘

↓ Backend stops

┌─────────────────────────────────────┐
│ Run: QUICK-FIX-DATABASE.bat         │
│                                     │
│ ✓ Recreating tables...             │
│ ✓ Seeding data...                  │
│ ✓ Done!                            │
└─────────────────────────────────────┘

↓ Database fixed

┌─────────────────────────────────────┐
│ Run: start-backend-server.bat       │
│                                     │
│ INFO: Uvicorn running on            │
│ http://127.0.0.1:8000              │
│ INFO: Application startup complete  │
│                                     │
│ ✓ Backend working!                 │
└─────────────────────────────────────┘
```

---

## Quick Commands

```bash
# 1. Stop backend: Ctrl + C in backend CMD window

# 2. Fix database:
QUICK-FIX-DATABASE.bat

# 3. Start backend:
start-backend-server.bat
```

---

## What If I Can't Find the Backend Window?

### Option 1: Kill Process
```bash
# Find backend process
netstat -ano | findstr :8000

# Kill it (replace <PID> with actual number)
taskkill /PID <PID> /F
```

### Option 2: Close All CMD Windows
Just close all CMD windows and start fresh.

---

## After Fix

Backend will start successfully:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

Test it:
- http://localhost:8000/health ✅
- http://localhost:8000/docs ✅
- http://localhost:3000/admin/config ✅

---

## Why This Happens

The backend was started with old database schema.
The code was updated but database wasn't.
Need to recreate database to match new code.

---

**TL;DR:**
1. Stop backend (Ctrl + C)
2. Run: `QUICK-FIX-DATABASE.bat`
3. Run: `start-backend-server.bat`
4. Done! ✅
