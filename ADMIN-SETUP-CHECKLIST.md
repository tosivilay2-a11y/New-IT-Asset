# Admin System Configuration - Setup Checklist

## 🎯 Quick Setup (Automated)

Run this single command:
```bash
setup-admin-complete.bat
```

This will:
1. ✅ Verify database tables
2. ✅ Create missing tables
3. ✅ Seed initial data
4. ✅ Verify everything is working

## 📋 Manual Setup Checklist

### Step 1: Database Tables

**Check if tables exist:**
```bash
cd backend
venv\Scripts\activate
python verify_tables.py
```

**Expected tables:**
- ✅ countries
- ✅ provinces
- ✅ companies
- ✅ maincategories
- ✅ assetsequences

**If tables are missing:**
```bash
python create_location_tables.py
```

### Step 2: Seed Data

**Check if data exists:**
```bash
python -c "from app.core.database import SessionLocal; from app.models.country import Country; db = SessionLocal(); print(f'Countries: {db.query(Country).count()}'); db.close()"
```

**If no data:**
```bash
python seed_location_hierarchy.py
```

**Expected data:**
- ✅ 5 Countries (LA, TH, VN, KH, MM)
- ✅ 8 Provinces (VTE, LPB, CPS, SVK, APU, BKK, CNX, HKT)
- ✅ 7 Companies (AVIS, FORD, EFGL, LARV, RMAG, COMN)
- ✅ 13 Categories (C, L, M, P, N, S, W, T, H, A, O, D, U)

### Step 3: Backend Server

**Start backend:**
```bash
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```

**Verify backend is running:**
- Open: http://localhost:8000/health
- Should see: `{"status": "healthy", "version": "2.0.0"}`

### Step 4: Test API Endpoints

**Run API tests:**
```bash
cd backend
venv\Scripts\activate
python test_admin_api.py
```

**Expected results:**
- ✅ All 10 tests pass
- ✅ Backend connection successful
- ✅ All endpoints responding

**Manual API test:**
- Open: http://localhost:8000/docs
- Try: GET /countries
- Should return list of countries

### Step 5: Frontend

**Start frontend:**
```bash
cd frontend
npm start
```

**Access admin page:**
- Open: http://localhost:3000/admin/config
- Should see 5 tabs
- Should be able to navigate between tabs

### Step 6: Verify Each Tab

**Asset ID Generator Tab:**
- [ ] Can select category
- [ ] Can select country
- [ ] Can select province
- [ ] Can select company
- [ ] Preview shows asset ID
- [ ] Breakdown displays correctly

**Countries Tab:**
- [ ] Table shows countries
- [ ] Can click "Add Country"
- [ ] Modal opens
- [ ] Can fill form
- [ ] Can save
- [ ] New country appears in table
- [ ] Can edit country
- [ ] Can delete country

**Provinces Tab:**
- [ ] Table shows provinces
- [ ] Can add new province
- [ ] Country dropdown works
- [ ] Can link to country
- [ ] Can edit province
- [ ] Can delete province

**Companies Tab:**
- [ ] Table shows companies
- [ ] Can add new company
- [ ] Province dropdown works
- [ ] Can add contact info
- [ ] Can edit company
- [ ] Can delete company

**Categories Tab:**
- [ ] Table shows categories
- [ ] Can add new category
- [ ] Code validation works (1 char)
- [ ] Can edit category
- [ ] Can delete category

## 🔍 Troubleshooting

### Backend won't start

**Error: "ModuleNotFoundError"**
```bash
cd backend
venv\Scripts\activate
pip install -r requirements.txt
```

**Error: "Table doesn't exist"**
```bash
python create_location_tables.py
```

### Tables not created

**Check models are imported:**
```bash
python -c "from app.models import Country, Province, Company, MainCategory, AssetSequence; print('✅ All models imported')"
```

**Recreate tables:**
```bash
python create_location_tables.py
```

### No data in tables

**Run seed script:**
```bash
python seed_location_hierarchy.py
```

**Verify data:**
```bash
python verify_tables.py
```

### API endpoints not working

**Check routes are registered:**
- Open: http://localhost:8000/docs
- Look for: /countries, /provinces, /companies, /main-categories

**Check backend logs:**
- Look for errors in terminal
- Check for import errors
- Verify all routes loaded

### Frontend can't connect

**Check CORS settings:**
- Backend should allow http://localhost:3000
- Check main.py CORS configuration

**Check API URL:**
- Components use: http://localhost:8000
- Verify backend is on port 8000

### Admin page not loading

**Check route:**
- URL should be: /admin/config
- Check App.js has route defined

**Check imports:**
- SystemConfig component imported
- All admin components exist

**Check console:**
- Open browser console (F12)
- Look for JavaScript errors
- Check network tab for failed requests

## ✅ Final Verification

Run all checks:

```bash
# 1. Verify tables
cd backend
venv\Scripts\activate
python verify_tables.py

# 2. Test API
python test_admin_api.py

# 3. Check backend
curl http://localhost:8000/health

# 4. Check countries endpoint
curl http://localhost:8000/countries
```

Expected results:
- ✅ All tables exist
- ✅ All API tests pass
- ✅ Backend health check passes
- ✅ Countries endpoint returns data

## 📊 Success Criteria

### Database
- [x] 5 new tables created
- [x] Foreign keys configured
- [x] Data seeded
- [x] Relationships working

### Backend
- [x] 5 new routes registered
- [x] All endpoints responding
- [x] CRUD operations working
- [x] Validation working

### Frontend
- [x] Admin page accessible
- [x] All 5 tabs working
- [x] Forms submitting
- [x] Data displaying
- [x] Mobile responsive

## 🎉 You're Ready When...

- ✅ Backend starts without errors
- ✅ All API tests pass
- ✅ Admin page loads
- ✅ Can view all tabs
- ✅ Can add/edit/delete data
- ✅ Asset ID generator works
- ✅ Location hierarchy cascades correctly

## 📞 Need Help?

**Check these files:**
- `ADMIN-SYSTEM-CONFIG-GUIDE.md` - Complete usage guide
- `ADMIN-SECTION-COMPLETE.md` - Implementation details
- `LOCATION-HIERARCHY-GUIDE.md` - Backend API guide
- `TROUBLESHOOTING.md` - General troubleshooting

**Common issues:**
1. **Tables missing** → Run `create_location_tables.py`
2. **No data** → Run `seed_location_hierarchy.py`
3. **API errors** → Check backend logs
4. **Frontend errors** → Check browser console

---

**Quick Start**: `setup-admin-complete.bat`  
**Verify**: `python backend/verify_tables.py`  
**Test API**: `python backend/test_admin_api.py`  
**Access**: http://localhost:3000/admin/config
