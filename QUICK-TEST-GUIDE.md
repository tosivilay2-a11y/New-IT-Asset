# Quick Test Guide - Asset View & Edit

## System Status
✅ Backend: http://localhost:8000 (Running)
✅ Frontend: http://localhost:3000 (Running)

## Test the New Features

### 1. Login
1. Go to http://localhost:3000
2. Login with:
   - Email: `admin@example.com`
   - Password: `admin123`

### 2. Navigate to Assets Page
- Click on **"Assets"** or **"Asset Management"** in the navigation menu
- Or go directly to: http://localhost:3000/assets-enhanced

### 3. Test View Functionality
1. Find any asset in the table
2. Click the **👁️ (eye icon)** button
3. **Expected Result**:
   - Modal opens with full asset details
   - Asset code displayed in large text at top
   - QR code displayed (if available)
   - All sections show data: Basic Info, Location, Assignment, Financial, Notes
   - Metadata shows created/updated timestamps
4. Click **"Edit Asset"** button to switch to edit mode
5. Click **"Close"** to dismiss

### 4. Test Edit Functionality
1. Find any asset in the table
2. Click the **✏️ (pencil icon)** button
3. **Expected Result**:
   - Modal opens with pre-filled form
   - Asset code shown in header
   - All 5 tabs available: Basic Info, Technical, Assignment, Purchase, QR Code
   - Form fields contain existing data
4. Make changes to any field (e.g., change status, update model)
5. Click **"Update Asset"**
6. **Expected Result**:
   - Success message appears
   - Modal closes
   - Table refreshes with updated data

### 5. Test Delete Functionality
1. Find any asset in the table
2. Click the **🗑️ (trash icon)** button
3. Confirm deletion
4. **Expected Result**:
   - Success message appears
   - Asset removed from table (soft delete)

### 6. Test Create New Asset
1. Click **"+ Add New Asset"** button
2. Fill in required fields:
   - Main Category (select from dropdown)
   - Location (Country → Province → Company)
   - Purchase Date
3. Optionally fill other tabs
4. Click **"Save Asset"**
5. **Expected Result**:
   - Asset created with auto-generated ID
   - QR code generated
   - New asset appears in table

## What to Look For

### View Modal
- ✅ Asset code displays prominently
- ✅ QR code image shows (if asset has one)
- ✅ Status badge has correct color
- ✅ All fields display data or "N/A"
- ✅ Dates formatted correctly
- ✅ Prices show with $ symbol
- ✅ Modal is scrollable if content is long
- ✅ "Edit Asset" button works
- ✅ "Close" button works

### Edit Modal
- ✅ Form pre-populated with existing data
- ✅ All tabs accessible
- ✅ Location selector shows current location
- ✅ Category selector shows current category
- ✅ Date fields show dates in YYYY-MM-DD format
- ✅ Changes save successfully
- ✅ "Cancel" button discards changes
- ✅ "Update Asset" button saves changes

### Table Display
- ✅ Asset ID column shows generated codes
- ✅ Asset Name column shows names
- ✅ Status badges color-coded
- ✅ All three action buttons visible
- ✅ Hover effects work on buttons
- ✅ Table updates after edit/delete

## Common Issues & Solutions

### Issue: Modal doesn't open
- **Solution**: Check browser console for errors (F12)
- Ensure backend is running on port 8000

### Issue: Data not loading
- **Solution**: Check network tab in browser (F12)
- Verify API endpoint returns data
- Check backend logs for errors

### Issue: Update doesn't save
- **Solution**: Check backend logs for validation errors
- Ensure required fields are filled
- Check network tab for 400/422 errors

### Issue: QR code not showing
- **Solution**: QR codes only show for assets that have them
- New assets get QR codes automatically
- Old assets may need to be re-saved

## Backend Logs
To check backend logs:
```
# Backend is running in background process
# Check logs in the terminal where backend was started
```

## Frontend Console
To check frontend errors:
1. Press F12 in browser
2. Go to "Console" tab
3. Look for red error messages

## API Testing
Test endpoints directly:
- **Get all assets**: http://localhost:8000/assets/
- **Get single asset**: http://localhost:8000/assets/1
- **API Docs**: http://localhost:8000/docs

## Success Indicators
✅ View modal opens and shows data
✅ Edit modal opens with pre-filled form
✅ Updates save and reflect in table
✅ Delete removes asset from table
✅ No console errors
✅ No backend errors in logs

---

**Ready to test!** Start with viewing an asset, then try editing it. 🚀
