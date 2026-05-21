# ⚡ Quick Fix for Admin "Not Found" Error

## What's Wrong?

Your backend server is running but **doesn't have the new admin routes loaded**.

## The Fix (30 seconds)

### 1️⃣ Stop Backend
Press `Ctrl + C` in the backend terminal window

### 2️⃣ Restart Backend
Double-click: **`restart-backend.bat`**

### 3️⃣ Test It
Double-click: **`verify-admin-routes.bat`**

You should see JSON data (not "Not Found").

### 4️⃣ Try Admin Page
Open: http://localhost:3000/admin/config

Try adding a category - it should work now! ✅

---

## Why This Fixes It

The backend server loads routes when it starts. Your server was started BEFORE the new admin routes were added to the code. Restarting loads the new routes.

---

## Alternative: Manual Restart

If the batch file doesn't work:

```bash
# Stop backend (Ctrl+C in backend terminal)

# Then run:
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```

---

## Verify Success

✅ Backend shows: "Application startup complete"
✅ http://localhost:8000/docs shows admin routes
✅ http://localhost:8000/countries returns JSON data
✅ Admin page works without errors

---

## Need More Help?

Read: **FIX-ADMIN-404-ERROR.md** for detailed troubleshooting
