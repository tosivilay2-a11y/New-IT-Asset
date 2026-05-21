# Staff Management - Company & Location - Quick Reference

## What's New

Staff members are now linked to companies and locations. When you check in an asset, it automatically uses the staff member's location.

## Quick Setup

### 1. Apply Migration
```bash
cd backend
python -m alembic upgrade head
```

### 2. Start Services
```bash
# Terminal 1
cd backend
python start_server.py

# Terminal 2
cd frontend
npm start
```

## Using the Feature

### Add Staff with Company and Location
1. System Configuration → Staff Management
2. Click "➕ Add Staff Member"
3. Fill form:
   - Employee ID (required)
   - Full Name (required)
   - Email (optional)
   - Department (optional)
   - Position (optional)
   - **Company** (optional) - Select from dropdown
   - **Location** (optional) - Select from dropdown
   - Employment Status
4. Click "Add Staff Member"

### Import Staff from Excel
1. System Configuration → Staff Management
2. Click "📥 Import from Excel"
3. Click "📥 Download Template"
4. Fill template:
   ```
   Employee ID,Full Name,Email,Department,Position,Company,Location,Employment Status
   EMP001,John Doe,john@example.com,IT,Developer,Acme Corp,New York,Active
   ```
5. Upload file
6. Staff imported with company and location

### Check In Asset (Automatic Location)
1. Asset Check-In/Check-Out
2. Select asset to check in
3. Click "Check In"
4. ✅ Location automatically set from staff member's location

## API Endpoints

### Get Staff by Company
```bash
GET /staff/company/1
```

### Get Staff by Location
```bash
GET /staff/location/5
```

### Create Staff with Company/Location
```bash
POST /staff/
{
  "employeeid": "EMP001",
  "fullname": "John Doe",
  "companyid": 1,
  "locationid": 5
}
```

### Import Staff
```bash
POST /staff/import
Content-Type: multipart/form-data
file: staff_data.xlsx
```

## Excel Template Format

| Employee ID | Full Name | Email | Department | Position | Company | Location | Employment Status |
|---|---|---|---|---|---|---|---|
| EMP001 | John Doe | john@example.com | IT | Developer | Acme Corp | New York | Active |
| EMP002 | Jane Smith | jane@example.com | HR | Manager | Acme Corp | New York | Active |

**Required:** Employee ID, Full Name
**Optional:** Email, Department, Position, Company, Location, Employment Status

## Staff Table Display

| Employee ID | Full Name | Email | Department | Position | **Company** | **Location** | Status | Actions |
|---|---|---|---|---|---|---|---|---|
| EMP001 | John Doe | john@example.com | IT | Developer | Acme Corp | New York | Active | Delete |
| EMP002 | Jane Smith | jane@example.com | HR | Manager | Acme Corp | New York | Active | Delete |

## Check-In Workflow

```
Asset Check-In
    ↓
Get Staff Member
    ↓
Get Staff Member's Location
    ↓
Update Asset Location = Staff Location
    ↓
Check-In Complete ✅
```

## Error Messages

| Error | Solution |
|---|---|
| Company not found | Ensure company exists in System Configuration → Companies |
| Location not found | Ensure location exists in System Configuration → Locations |
| Employee ID already exists | Use a different employee ID |
| Email already exists | Use a different email or leave blank |

## Database Changes

### New Columns in Staff Table
- `companyid` - Foreign key to company
- `locationid` - Foreign key to location

### New Indexes
- `ix_staff_companyid` - For fast company lookups
- `ix_staff_locationid` - For fast location lookups

## Files Changed

### Backend
- `backend/app/models/staff.py` - Added company/location relationships
- `backend/app/schemas/staff.py` - Added company/location schemas
- `backend/app/routes/staff.py` - Added company/location endpoints
- `backend/alembic/versions/007_add_company_location_to_staff.py` - Migration

### Frontend
- `frontend/src/components/admin/StaffManagement.jsx` - Added company/location UI
- `frontend/src/pages/AssetCheckInOut.jsx` - Added staff location integration

## Testing

### Test 1: Create Staff with Company and Location
✅ Staff created with company and location links
✅ Company and location visible in staff list

### Test 2: Import Staff from Excel
✅ Staff imported with company and location
✅ Company and location validated
✅ Errors logged for invalid company/location

### Test 3: Check In Asset
✅ Asset location automatically set from staff member
✅ No manual location selection needed
✅ Location matches staff member's location

## Troubleshooting

### Staff not showing company/location
- Ensure migration was applied: `python -m alembic upgrade head`
- Restart backend: `python start_server.py`

### Company/Location dropdown empty
- Ensure companies and locations exist in System Configuration
- Refresh page to reload data

### Check-in not using staff location
- Ensure staff member has location assigned
- Verify staff member is linked to asset
- Check browser console for errors

## Support

For issues or questions:
1. Check error messages in UI
2. Check browser console (F12)
3. Check backend logs
4. Review documentation files

## Quick Links

- Staff Management: System Configuration → Staff Management
- Check-In/Check-Out: Asset Check-In/Check-Out
- Companies: System Configuration → Companies
- Locations: System Configuration → Locations

---

**Status:** ✅ Ready to Use
**Last Updated:** May 11, 2026
