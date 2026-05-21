# 🚀 Start Phase 2 - Quick Guide

## ⚡ Quick Start (5 Minutes)

### Step 1: Setup Backend (If Not Done)
```bash
# Run this once
run-setup.bat
```

### Step 2: Start Backend
```bash
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```

### Step 3: Start Frontend
```bash
cd frontend
npm start
```

### Step 4: Open Browser
Navigate to: **http://localhost:3000/assets**

### Step 5: Test It!
1. Click "+ Add New Asset"
2. Select category (e.g., [M] Monitor)
3. Select location (Country → Province → Company)
4. Watch Asset ID preview update!
5. Fill form and save

## ✅ What You'll See

### 1. Asset ID Preview Card
Beautiful purple gradient card showing:
```
MLALPBAVIS25015
M  LA  LPB  AVIS  25  015
```

### 2. Location Selector
Three cascading dropdowns:
```
[Lao PDR (LA) ▼]  [Luang Prabang (LPB) ▼]  [AVIS ▼]
```

### 3. Category Selector
Dropdown with codes:
```
[M] Monitor
[C] Computer
[L] Laptop
...
```

### 4. Enhanced Form
5 tabs:
- Basic Info (with ID preview)
- Technical Specs
- Assignment
- Purchase Info
- QR Code

## 🎯 Try These Features

### Create a Monitor
1. Category: `[M] Monitor`
2. Country: `Lao PDR (LA)`
3. Province: `Luang Prabang (LPB)`
4. Company: `AVIS`
5. Purchase Date: Today
6. **Preview shows**: `MLALPBAVIS25015`
7. Save!

### Create a Laptop
1. Category: `[L] Laptop`
2. Country: `Lao PDR (LA)`
3. Province: `Vientiane Capital (VTE)`
4. Company: `FORD`
5. Purchase Date: Today
6. **Preview shows**: `LLAVTEFORD26001`
7. Save!

## 📱 Test Responsive

### Desktop
- Open in full screen
- See 3-column layout
- All features visible

### Mobile
- Resize browser to mobile size
- See single column
- Touch-friendly buttons

## 🔍 Verify Everything Works

### Checklist
- [ ] Backend running (http://localhost:8000/docs)
- [ ] Frontend running (http://localhost:3000)
- [ ] Can access /assets page
- [ ] Location selector loads countries
- [ ] Provinces load when country selected
- [ ] Companies load when province selected
- [ ] Category selector shows categories
- [ ] Asset ID preview updates
- [ ] Can create asset
- [ ] Asset appears in table

## 🐛 Troubleshooting

### "Cannot connect to backend"
```bash
# Check backend is running
curl http://localhost:8000/health

# If not, start it:
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```

### "No countries in dropdown"
```bash
# Run seed script
cd backend
venv\Scripts\activate
python seed_location_hierarchy.py
```

### "Asset ID preview not showing"
- Make sure you selected category
- Make sure you selected all location fields
- Check browser console for errors

### "Frontend not loading"
```bash
# Restart frontend
cd frontend
npm start
```

## 📚 Documentation

**Quick Reference**: `QUICK-REFERENCE.md`  
**Full Guide**: `INTEGRATION-PHASE2-COMPLETE.md`  
**UI Guide**: `PHASE2-UI-GUIDE.md`  
**Summary**: `PHASE2-SUMMARY.md`

## 🎉 Success!

If you can:
1. ✅ See the enhanced asset page
2. ✅ Select category and location
3. ✅ See asset ID preview update
4. ✅ Create an asset
5. ✅ See it in the table

**You're ready to go!** 🚀

## 🔗 URLs

- **Frontend**: http://localhost:3000
- **Enhanced Assets**: http://localhost:3000/assets
- **Original Assets**: http://localhost:3000/assets/original
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 💡 Pro Tips

1. **Use Tab Key** - Navigate form quickly
2. **Watch Preview** - See ID update in real-time
3. **Save Often** - Don't lose your work
4. **Use Tabs** - Organize data logically
5. **Check Console** - For any errors

## 🎯 What's Next?

After testing Phase 2:
- **Phase 3**: Excel Import/Export
- **Phase 4**: Asset Detail Page
- **Phase 5**: Advanced Features

## 📞 Need Help?

Check these files:
- `TROUBLESHOOTING.md` - Common issues
- `INTEGRATION-PHASE2-COMPLETE.md` - Complete guide
- `QUICK-REFERENCE.md` - Quick commands

---

**Ready?** Run the commands above and start testing! 🚀
