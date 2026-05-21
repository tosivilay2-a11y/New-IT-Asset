# 🔧 Fix "Not Found" Error in Admin Page

## Current Status

**Problem Identified:** ✅
- Backend server is running
- New admin routes are in the code
- But routes are NOT loaded in the running server

**Root Cause:**
The backend was started BEFORE the new routes were added to `main.py`. The server needs to be restarted to load the new routes.

---

## 🚀 Quick Fix (3 Steps)

### Step 1: Stop Backend

Find the terminal where backend is running and press `Ctrl + C`

### Step 2: Restart Backend

Run this command:
```bash
restart-backend.bat
```

Or manually:
```bash
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```

### Step 3: Verify It Worked

Run this command:
```bash
verify-admin-routes.bat
```

You should see JSON data (not "Not Found" errors).

---

## 📋 Detailed Instructions

### For Windows Users

1. **Find Backend Terminal**
   - Look for the terminal window running the backend
   - It should show: `Uvicorn running on http://127.0.0.1:8000`

2. **Stop Backend**
   - Click on that terminal window
   - Press `Ctrl + C`
   - Wait for it to stop (you'll see the command prompt)

3. **Restart Backend**
   - Double-click: `restart-backend.bat`
   - OR run manually:
     ```bash
     cd backend
     venv\Scripts\activate
     uvicorn app.main:app --reload --port 8000
     ```

4. **Wait for Startup**
   - You should see:
     ```
     INFO:     Uvicorn running on http://127.0.0.1:8000
     INFO:     Application startup complete.
     ```

5. **Test Routes**
   - Open: http://localhost:8000/docs
   - Look for these endpoints:
     - GET /countries
     - GET /provinces
     - GET /companies
     - GET /main-categories
   - If you see them, it worked! ✅

6. **Test Admin Page**
   - Open: http://localhost:3000/admin/config
   - Click "Categories" tab
   - Click "Add Category"
   - Fill form and save
   - Should work without errors! ✅

---

## 🔍 Verification Steps

### Test 1: Backend Health

Open in browser: http://localhost:8000/health

**Expected:**
```json
{"status":"healthy","version":"2.0.0"}
```

**If fails:** Backend is not running. Start it with `restart-backend.bat`

### Test 2: API Documentation

Open in browser: http://localhost:8000/docs

**Expected:** You should see sections for:
- countries
- provinces
- companies
- main-categories
- asset-utils

**If missing:** Routes not loaded. Restart backend.

### Test 3: Countries Endpoint

Open in browser: http://localhost:8000/countries

**Expected:**
```json
[
  {
    "countryid": 1,
    "countrycode": "LA",
    "countryname": "Laos",
    "isactive": true
  },
  ...
]
```

**If "Not Found":** Routes not loaded. Restart backend.

### Test 4: Categories Endpoint

Open in browser: http://localhost:8000/main-categories

**Expected:**
```json
[
  {
    "maincategoryid": 1,
    "categorycode": "C",
    "categoryname": "Computer",
    "description": "Desktop computers, laptops, tablets",
    "isactive": true
  },
  ...
]
```

**If "Not Found":** Routes not loaded. Restart backend.

### Test 5: Admin Page

Open in browser: http://localhost:3000/admin/config

**Expected:**
- Page loads without errors
- 5 tabs visible
- Can click between tabs
- Tables show data

**If errors:** Check browser console (F12) for details.

---

## 🐛 Troubleshooting

### Problem: "Port already in use"

**Symptom:**
```
ERROR: [Errno 10048] error while attempting to bind on address ('127.0.0.1', 8000)
```

**Solution:**
```bash
# Find process on port 8000
netstat -ano | findstr :8000

# Kill it (replace <PID> with actual number)
taskkill /PID <PID> /F

# Start backend again
restart-backend.bat
```

### Problem: "ModuleNotFoundError"

**Symptom:**
```
ModuleNotFoundError: No module named 'fastapi'
```

**Solution:**
```bash
cd backend
venv\Scripts\activate
pip install -r requirements.txt
```

### Problem: Routes still showing "Not Found"

**Check 1: Routes in main.py**

Open `backend/app/main.py` and verify these lines exist:

```python
# Near top of file
from .routes import countries, provinces, companies, main_categories, asset_utils

# In the middle of file
app.include_router(countries.router)
app.include_router(provinces.router)
app.include_router(companies.router)
app.include_router(main_categories.router)
app.include_router(asset_utils.router)
```

**Check 2: Route files exist**

Verify these files exist:
- `backend/app/routes/countries.py`
- `backend/app/routes/provinces.py`
- `backend/app/routes/companies.py`
- `backend/app/routes/main_categories.py`
- `backend/app/routes/asset_utils.py`

**Check 3: Backend actually restarted**

Make sure you:
1. Stopped the old backend (Ctrl+C)
2. Started a new backend
3. Saw "Application startup complete" message

### Problem: No data in tables

**Symptom:**
Endpoints work but return empty arrays `[]`

**Solution:**
```bash
cd backend
venv\Scripts\activate
python seed_location_hierarchy.py
```

This will add:
- 5 Countries
- 8 Provinces
- 7 Companies
- 13 Categories

### Problem: Tables don't exist

**Symptom:**
```
sqlalchemy.exc.ProgrammingError: (psycopg2.errors.UndefinedTable) relation "countries" does not exist
```

**Solution:**
```bash
cd backend
venv\Scripts\activate
python create_location_tables.py
```

### Problem: Frontend can't connect

**Symptom:**
Browser console shows:
```
Failed to fetch
Network error
```

**Check 1: Backend running?**
```bash
curl http://localhost:8000/health
```

Should return: `{"status":"healthy","version":"2.0.0"}`

**Check 2: CORS enabled?**

Open `backend/app/main.py` and verify:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Check 3: Correct URL?**

Frontend should use: `http://localhost:8000`
Check in browser console what URL is being called.

---

## 📊 Diagnostic Commands

Run these to diagnose issues:

```bash
# Check if backend is running
curl http://localhost:8000/health

# Check if routes are loaded
curl http://localhost:8000/countries

# Check database tables
cd backend
venv\Scripts\activate
python verify_tables.py

# Check if data exists
python -c "from app.core.database import SessionLocal; from app.models.country import Country; db = SessionLocal(); print(f'Countries: {db.query(Country).count()}'); db.close()"

# Test all admin endpoints
python test_admin_api.py

# Run full diagnostic
fix-admin-routes.bat
```

---

## ✅ Success Checklist

After fixing, verify:

- [ ] Backend starts without errors
- [ ] http://localhost:8000/health returns healthy
- [ ] http://localhost:8000/docs shows admin routes
- [ ] http://localhost:8000/countries returns data
- [ ] http://localhost:8000/main-categories returns data
- [ ] http://localhost:3000/admin/config loads
- [ ] Can navigate between tabs
- [ ] Can add new category
- [ ] Can edit category
- [ ] Can delete category
- [ ] Can add new country
- [ ] Can add new province
- [ ] Can add new company

---

## 🎯 Expected Behavior

### Before Fix
- ❌ Admin page shows "Not Found"
- ❌ "Failed to load data" errors
- ❌ Can't add categories
- ❌ Tables are empty
- ❌ http://localhost:8000/countries returns 404

### After Fix
- ✅ Admin page loads correctly
- ✅ All tabs work
- ✅ Can add/edit/delete data
- ✅ Tables show data
- ✅ http://localhost:8000/countries returns JSON

---

## 📞 Still Need Help?

### Check These Files

1. **RESTART-BACKEND-NOW.md** - Detailed restart instructions
2. **ADMIN-SETUP-CHECKLIST.md** - Complete setup verification
3. **ADMIN-SYSTEM-CONFIG-GUIDE.md** - Usage guide
4. **LOCATION-HIERARCHY-GUIDE.md** - Backend API reference

### Run Diagnostic Scripts

```bash
# Verify routes loaded
verify-admin-routes.bat

# Full diagnostic
fix-admin-routes.bat

# Check database
cd backend
venv\Scripts\activate
python verify_tables.py

# Test API
python test_admin_api.py
```

### Check Logs

**Backend logs:**
- Look at terminal where backend is running
- Check for errors or warnings
- Look for "Application startup complete"

**Frontend logs:**
- Open browser console (F12)
- Look for red errors
- Check Network tab for failed requests

---

## 💡 Prevention

To avoid this in the future:

1. **Always restart backend after adding new routes**
2. **Use `--reload` flag** (already in our commands)
3. **Check /docs** after restart to verify routes loaded
4. **Test endpoints** before testing frontend

---

**Quick Commands:**

```bash
# Restart backend
restart-backend.bat

# Verify it worked
verify-admin-routes.bat

# Test admin page
# Open: http://localhost:3000/admin/config
```

**That's it!** 🎉
