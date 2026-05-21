# 🚨 Fix 404 Errors - URGENT

## What You're Seeing

```
Failed to load resource: 404 (Not Found)
:8000/provinces:1
:8000/countries:1
:8000/companies:1
:8000/main-categories:1
```

## The Problem

The backend server is running but **the new admin routes are NOT loaded**.

## The Solution (30 seconds)

### Step 1: Stop Backend
Find the terminal running the backend and press: **`Ctrl + C`**

### Step 2: Restart Backend
Run this command:
```bash
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```

Or use the batch file:
```bash
restart-backend.bat
```

### Step 3: Refresh Browser
After backend restarts, refresh your browser (F5)

---

## Why This Happens

The backend was started BEFORE the new routes were added to the code. The server needs to restart to load them.

---

## Verify It Worked

After restart, open these URLs in your browser:

1. http://localhost:8000/countries - Should show JSON data
2. http://localhost:8000/provinces - Should show JSON data
3. http://localhost:8000/companies - Should show JSON data
4. http://localhost:8000/main-categories - Should show JSON data

If you see JSON data (not "Not Found"), it worked! ✅

Then refresh your admin page: http://localhost:3000/admin/config

---

## Quick Commands

```bash
# Stop backend: Ctrl+C in backend terminal

# Restart backend:
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload --port 8000

# Or use batch file:
restart-backend.bat
```

---

## Still Not Working?

### Check 1: Is backend running?
```bash
curl http://localhost:8000/health
```
Should return: `{"status":"healthy","version":"2.0.0"}`

### Check 2: Are routes loaded?
Open: http://localhost:8000/docs

Look for these sections:
- countries
- provinces  
- companies
- main-categories

If you don't see them, the routes aren't loaded.

### Check 3: Port conflict?
If you get "port already in use":
```bash
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

---

## Expected Result

**Before restart:**
- ❌ 404 errors in browser console
- ❌ Admin page shows "Failed to load data"
- ❌ Empty dropdowns

**After restart:**
- ✅ No 404 errors
- ✅ Admin page loads data
- ✅ Dropdowns populated
- ✅ Can add/edit/delete

---

**TL;DR:** Stop backend (Ctrl+C), restart it, refresh browser. Done! ✅
