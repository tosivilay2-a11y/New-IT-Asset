# 🚀 Start Frontend and Backend

## Current Status

✅ **Frontend is running!**
- URL: http://localhost:3000
- Status: Working

❌ **Backend needs database fix**
- Error: Database schema mismatch
- Solution: Run fix script first

---

## How to Start Both

### Step 1: Fix Database (One Time Only)

Run this file:
```bash
FIX-AND-START.bat
```

This will:
1. Fix database schema
2. Seed all data
3. Start backend automatically

### Step 2: Start Frontend (Separate Window)

In another terminal:
```bash
cd frontend
npm start
```

Or I've already started it for you! ✅

---

## Quick Start (After Database is Fixed)

### Option 1: Manual (Two Terminals)

**Terminal 1 - Backend:**
```bash
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

### Option 2: Background Processes

I can start both in background for you (after database is fixed).

---

## Current Situation

**Frontend:** ✅ Running on http://localhost:3000

**Backend:** ❌ Needs database fix

**Next Step:** Run `FIX-AND-START.bat` to fix backend

---

## After Fix

Both will be running:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## Test Everything Works

1. **Backend Health:** http://localhost:8000/health
2. **API Docs:** http://localhost:8000/docs
3. **Frontend:** http://localhost:3000
4. **Login:** admin@example.com / admin123
5. **Admin Page:** http://localhost:3000/admin/config

---

**TL;DR:**
1. Frontend is already running ✅
2. Run `FIX-AND-START.bat` to start backend
3. Done! Both running! 🎉
