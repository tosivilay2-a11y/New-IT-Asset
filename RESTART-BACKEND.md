# 🔄 Restart Backend Server

## ❌ Problem

You're seeing **"Not Found"** or **"Failed to load data"** errors because:
- The backend server was started **before** the new routes were added
- The new routes are not loaded yet

## ✅ Solution

**Restart the backend server** to load the new routes.

## 📝 Steps

### 1. Stop Current Backend

In the terminal where backend is running:
- Press `Ctrl + C`
- Wait for it to stop

### 2. Start Backend Again

```bash
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```

### 3. Verify Routes Loaded

You should see output like:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### 4. Test in Browser

Open: http://localhost:8000/docs

You should see new endpoints:
- `/countries`
- `/provinces`
- `/companies`
- `/main-categories`
- `/asset-utils/preview-asset-id`
- `/asset-utils/generate-qr-code`

### 5. Test Admin Page

Open: http://localhost:3000/admin/config

Try adding a category again - it should work now!

## 🔍 Verify Routes Are Loaded

Run this command:
```bash
cd backend
venv\Scripts\activate
python check_routes.py
```

Should show all admin routes.

## 🐛 Still Not Working?

### Check 1: Backend Running?
```bash
curl http://localhost:8000/health
```

Should return: `{"status":"healthy","version":"2.0.0"}`

### Check 2: Routes Registered?
```bash
cd backend
python check_routes.py
```

Should show admin routes.

### Check 3: Tables Created?
```bash
cd backend
python verify_tables.py
```

Should show all 13 tables.

### Check 4: Data Seeded?
```bash
cd backend
python seed_location_hierarchy.py
```

Should seed initial data.

## 🚀 Quick Fix (All-in-One)

Run this script:
```bash
fix-admin-routes.bat
```

This will:
1. Check routes
2. Verify tables
3. Test endpoints
4. Show diagnostic info

## ✅ Success Indicators

After restart, you should see:
- ✅ No errors in backend terminal
- ✅ Routes visible in /docs
- ✅ Admin page loads without errors
- ✅ Can add/edit/delete data
- ✅ Tables show data

## 📞 Common Issues

### "ModuleNotFoundError"
```bash
cd backend
venv\Scripts\activate
pip install -r requirements.txt
```

### "Table doesn't exist"
```bash
cd backend
python create_location_tables.py
```

### "No data in tables"
```bash
cd backend
python seed_location_hierarchy.py
```

### "Port already in use"
```bash
# Find and kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

## 🎯 Expected Behavior

**Before Restart:**
- ❌ 404 Not Found errors
- ❌ Failed to load data
- ❌ Routes not in /docs

**After Restart:**
- ✅ All endpoints working
- ✅ Data loads correctly
- ✅ Routes visible in /docs
- ✅ Admin page functional

---

**TL;DR**: Stop backend (Ctrl+C), then restart it:
```bash
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```
