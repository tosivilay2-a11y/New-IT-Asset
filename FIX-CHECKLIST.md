# ✅ Fix Backend - Simple Checklist

## Current Situation

- [ ] Backend is running in another CMD window
- [ ] Backend shows error about "assetid" column
- [ ] Need to fix database and restart

---

## Fix Steps

### [ ] Step 1: Stop Backend

**Find the CMD window with backend running**

Look for window showing:
```
ERROR: column "assetid" referenced in foreign key constraint does not exist
```

**Stop it:**
- Click on that CMD window
- Press `Ctrl + C`
- Wait for it to stop

---

### [ ] Step 2: Fix Database

**Double-click this file:**
```
QUICK-FIX-DATABASE.bat
```

**Or run manually:**
```bash
cd backend
venv\Scripts\activate
python recreate_tables.py --yes
python seed_location_hierarchy.py
python seed_asset_control_data.py
python create_test_user.py
```

**Wait for:**
- ✓ Tables recreated
- ✓ Data seeded
- ✓ "Database Fixed!" message

---

### [ ] Step 3: Start Backend

**Double-click this file:**
```
start-backend-server.bat
```

**Or run manually:**
```bash
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```

**Wait for:**
```
INFO: Uvicorn running on http://127.0.0.1:8000
INFO: Application startup complete.
```

---

### [ ] Step 4: Verify

**Test these URLs:**

- [ ] http://localhost:8000/health
  - Should show: `{"status":"healthy","version":"2.0.0"}`

- [ ] http://localhost:8000/docs
  - Should show API documentation

- [ ] http://localhost:8000/countries
  - Should show JSON with countries data

- [ ] http://localhost:3000/admin/config
  - Should load without 404 errors

---

## Success!

When all checkboxes are checked:
- ✅ Backend is running
- ✅ Database has correct schema
- ✅ All routes working
- ✅ Admin page loads
- ✅ No more errors!

---

## Quick Reference

| Step | Command | Expected Result |
|------|---------|----------------|
| 1 | `Ctrl + C` | Backend stops |
| 2 | `QUICK-FIX-DATABASE.bat` | Database fixed |
| 3 | `start-backend-server.bat` | Backend starts |
| 4 | Open URLs | All working |

---

## If Something Goes Wrong

**Backend won't stop:**
```bash
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**Database fix fails:**
- Make sure PostgreSQL is running
- Check backend/.env has correct database credentials

**Backend won't start:**
- Read error message
- Check `TROUBLESHOOTING.md`

---

**Files to Read:**
- `STOP-AND-FIX-BACKEND.md` - Detailed guide
- `READ-ME-FIRST.md` - Overview
- `FIX-DATABASE-SCHEMA.md` - Complete troubleshooting
