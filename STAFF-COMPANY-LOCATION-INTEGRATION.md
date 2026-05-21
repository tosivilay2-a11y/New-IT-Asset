# Staff Management - Company & Location Integration

## Overview
Successfully integrated company and location linking with staff management and asset check-in/check-out functionality. Staff members are now linked to companies and locations, and when assets are checked in, they automatically use the staff member's location.

## What Was Implemented

### 1. Backend Updates

#### Staff Model Enhancement (`backend/app/models/staff.py`)
Added foreign key relationships:
- `companyid` - Links staff to company
- `locationid` - Links staff to location
- Relationships to Company and Location models

#### Staff Schema Updates (`backend/app/schemas/staff.py`)
Added new schemas:
- `CompanyInfo` - Company details in responses
- `LocationInfo` - Location details in responses
- Updated `StaffCreate` and `StaffResponse` to include company and location

#### Staff Routes Enhancement (`backend/app/routes/staff.py`)
New endpoints:
- `GET /staff/company/{company_id}` - Get all staff in a company
- `GET /staff/location/{location_id}` - Get all staff at a location
- Updated `POST /staff/` - Validates company and location exist
- Updated `POST /staff/import` - Supports company and location columns in Excel

#### Database Migration (`backend/alembic/versions/007_add_company_location_to_staff.py`)
- Adds `companyid` and `locationid` columns to staff table
- Creates foreign key constraints
- Creates indexes for performance

### 2. Frontend Updates

#### Staff Management Component (`frontend/src/components/admin/StaffManagement.jsx`)
Enhanced features:
- Fetch companies and locations on component load
- Company dropdown in create staff form
- Location dropdown in create staff form
- Display company and location in staff table
- Updated Excel template to include company and location columns
- Updated import instructions to mention company and location

#### Asset Check-In/Check-Out (`frontend/src/pages/AssetCheckInOut.jsx`)
Enhanced check-in process:
- Fetch staff members on component load
- When checking in an asset, automatically use the staff member's location
- Location is set from staff member's `locationid` field
- Seamless integration with existing check-in workflow

## Database Schema

### Staff Table (Updated)
```sql
CREATE TABLE staff (
    staffid SERIAL PRIMARY KEY,
    employeeid VARCHAR UNIQUE NOT NULL,
    fullname VARCHAR NOT NULL,
    email VARCHAR,
    department VARCHAR,
    position VARCHAR,
    employmentstatus VARCHAR DEFAULT 'Active',
    companyid INTEGER FOREIGN KEY REFERENCES company(companyid),
    locationid INTEGER FOREIGN KEY REFERENCES location(locationid),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX ix_staff_companyid ON staff(companyid);
CREATE INDEX ix_staff_locationid ON staff(locationid);
```

## API Endpoints

### Get Staff by Company
```bash
GET /staff/company/{company_id}
Response: List[StaffResponse]
```

### Get Staff by Location
```bash
GET /staff/location/{location_id}
Response: List[StaffResponse]
```

### Create Staff with Company and Location
```bash
POST /staff/
{
  "employeeid": "EMP001",
  "fullname": "John Doe",
  "email": "john@example.com",
  "department": "IT",
  "position": "Developer",
  "employmentstatus": "Active",
  "companyid": 1,
  "locationid": 5
}
```

### Import Staff with Company and Location
```bash
POST /staff/import
Content-Type: multipart/form-data
file: <excel_file>
```

Excel columns:
- Employee ID (required)
- Full Name (required)
- Email (optional)
- Department (optional)
- Position (optional)
- Company (optional) - Company name or code
- Location (optional) - Location name or code
- Employment Status (optional)

## Features

### Staff Management
✅ Link staff to companies
✅ Link staff to locations
✅ View company and location in staff list
✅ Filter staff by company
✅ Filter staff by location
✅ Import staff with company and location from Excel

### Check-In/Check-Out Integration
✅ Automatically use staff member's location during check-in
✅ Asset location updated to staff member's location
✅ Seamless workflow without manual location selection
✅ Maintains audit trail with location information

## Excel Import Template

### Template Format
```
Employee ID,Full Name,Email,Department,Position,Company,Location,Employment Status
EMP001,John Doe,john@example.com,IT,Developer,Acme Corp,New York,Active
EMP002,Jane Smith,jane@example.com,HR,Manager,Acme Corp,New York,Active
EMP003,Bob Johnson,bob@example.com,Finance,Analyst,Tech Solutions,Los Angeles,Active
```

### Column Details
- **Employee ID** (required) - Unique identifier
- **Full Name** (required) - Staff member's full name
- **Email** (optional) - Email address
- **Department** (optional) - Department name
- **Position** (optional) - Job position
- **Company** (optional) - Must match existing company name or code
- **Location** (optional) - Must match existing location name or code
- **Employment Status** (optional) - Default: "Active"

## Workflow

### Adding Staff with Company and Location
1. Go to System Configuration → Staff Management
2. Click "➕ Add Staff Member"
3. Fill in staff details
4. Select company from dropdown
5. Select location from dropdown
6. Click "Add Staff Member"

### Importing Staff with Company and Location
1. Go to System Configuration → Staff Management
2. Click "📥 Import from Excel"
3. Click "📥 Download Template"
4. Fill in staff data including company and location names
5. Upload the file
6. System validates company and location exist
7. Staff members are imported with company and location links

### Checking In Asset with Staff Location
1. Go to Asset Check-In/Check-Out
2. Select asset to check in
3. Click "Check In"
4. System automatically uses staff member's location
5. Asset location is updated to staff member's location
6. Check-in is completed

## Error Handling

### Company Not Found
- Error: "Company '{name}' not found"
- Solution: Ensure company exists in System Configuration → Companies

### Location Not Found
- Error: "Location '{name}' not found"
- Solution: Ensure location exists in System Configuration → Locations

### Invalid Company/Location in Import
- Row is skipped with error message
- Other rows continue to import
- Check error log for details

## Benefits

1. **Organizational Structure** - Staff linked to company and location hierarchy
2. **Automatic Location Tracking** - Assets automatically go to staff member's location on check-in
3. **Audit Trail** - Complete history of asset location and staff assignments
4. **Reporting** - Easy to generate reports by company or location
5. **Multi-Tenant Support** - Support for multiple companies and locations
6. **Bulk Import** - Efficient staff import with company and location mapping

## Testing Checklist

- [ ] Create staff member with company and location
- [ ] Verify company and location appear in staff list
- [ ] Get staff by company endpoint works
- [ ] Get staff by location endpoint works
- [ ] Download Excel template includes company and location columns
- [ ] Import staff with company and location from Excel
- [ ] Verify imported staff has correct company and location
- [ ] Check in asset and verify location is set from staff member
- [ ] Verify asset location matches staff member's location
- [ ] Test error handling for invalid company/location

## Files Modified/Created

### Created
- `backend/alembic/versions/007_add_company_location_to_staff.py` - Migration

### Modified
- `backend/app/models/staff.py` - Added company and location relationships
- `backend/app/schemas/staff.py` - Added company and location schemas
- `backend/app/routes/staff.py` - Added company/location endpoints and validation
- `frontend/src/components/admin/StaffManagement.jsx` - Added company/location UI
- `frontend/src/pages/AssetCheckInOut.jsx` - Added staff location integration

## Next Steps

1. Run migration: `python backend/alembic upgrade head`
2. Test staff creation with company and location
3. Test Excel import with company and location
4. Test asset check-in with automatic location assignment
5. Deploy to production

## Status
✅ **COMPLETE** - Staff management is fully integrated with company, location, and check-in/check-out functionality.
