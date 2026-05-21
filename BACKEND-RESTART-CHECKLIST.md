# ✅ Backend Restart Checklist

## Current Status

✅ Backend is running (health check passes)
❌ Admin routes NOT loaded (404 errors)

## What You Need to Do

### [ ] Step 1: Stop Backend
- Find terminal with backend
- Press `Ctrl + C`
- Wait for it to stop

### [ ] Step 2: Restart Backend
Choose one:

**Option A: Batch File (Easy)**
```bash
restart-backend.bat
```

**Option B: Manual (Reliable)**
```bash
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```

### [ ] Step 3: Verify Startup
Look for these messages:
```
✅ INFO:     Uvicorn running on http://127.0.0.1:8000
✅ INFO:     Application startup complete.
```

### [ ] Step 4: Test Routes
Open in browser:
- http://localhost:8000/countries
- http://localhost:8000/provinces
- http://localhost:8000/companies
- http://localhost:8000/main-categories

Should see JSON data, not "Not Found"

### [ ] Step 5: Test Admin Page
- Open: http://localhost:3000/admin/config
- Check browser console (F12)
- Should have NO 404 errors
- Dropdowns should populate

### [ ] Step 6: Test Functionality
- Click "Categories" tab
- Click "Add Category"
- Fill form
- Click "Save"
- Should work without errors ✅

---

## Troubleshooting

### Backend won't stop
```bash
# Find process
netstat -ano | findstr :8000

# Kill it
taskkill /PID <PID> /F
```

### Port already in use
```bash
# Kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Then restart
restart-backend.bat
```

### Routes still not working
1. Make sure you actually stopped the old backend
2. Make sure you started a new backend
3. Check terminal shows "Application startup complete"
4. Try: http://localhost:8000/docs
5. Look for admin routes in the docs

---

## Success Indicators

✅ Backend terminal shows "Application startup complete"
✅ http://localhost:8000/health returns healthy
✅ http://localhost:8000/countries returns JSON
✅ http://localhost:8000/docs shows admin routes
✅ Browser console has NO 404 errors
✅ Admin page loads data
✅ Can add/edit/delete items

---

## Quick Commands

```bash
# Stop: Ctrl+C in backend terminal

# Restart:
restart-backend.bat

# Test:
curl http://localhost:8000/countries

# Verify:
# Open: http://localhost:8000/docs
```

---

**Current Issue:** Backend running but routes not loaded
**Solution:** Restart backend
**Time:** 30 seconds
**Files to read:** FIX-404-ERRORS-NOW.md, RESTART-BACKEND-SIMPLE.md
