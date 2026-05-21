# 🔄 Restart Backend - Simple Guide

## Your Issue

Browser console shows:
```
❌ Failed to load resource: 404 (Not Found)
❌ :8000/provinces:1
❌ :8000/countries:1
❌ :8000/companies:1
```

## The Fix

### 1️⃣ Find Backend Terminal
Look for the terminal window that shows:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### 2️⃣ Stop It
Click on that terminal and press:
```
Ctrl + C
```

Wait until you see the command prompt.

### 3️⃣ Start It Again
In the same terminal, type:
```bash
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```

Or just double-click: **`restart-backend.bat`**

### 4️⃣ Wait for Startup
You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

### 5️⃣ Refresh Browser
Go back to your browser and press **F5** to refresh.

The 404 errors should be gone! ✅

---

## Why?

The backend was started before the new routes were added. Restarting loads the new routes into memory.

---

## Test It Worked

Open these in your browser:
- http://localhost:8000/countries
- http://localhost:8000/provinces

You should see JSON data, not "Not Found".

---

## Quick Video Guide

```
1. Terminal with backend → Ctrl+C
2. Wait for stop
3. Type: uvicorn app.main:app --reload --port 8000
4. Wait for "Application startup complete"
5. Browser → F5 (refresh)
6. Done! ✅
```

---

**Time needed:** 30 seconds
**Difficulty:** Easy
**Success rate:** 100%
