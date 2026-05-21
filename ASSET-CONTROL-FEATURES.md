# 🎯 Asset Control Features - Complete Guide

## Overview

Enhanced asset management system with comprehensive control features including departments, asset statuses, and transfer management.

---

## 🆕 New Features Added

### 1. **Departments Management**
- Link departments to companies
- Assign assets to departments
- Track departmental asset allocation

### 2. **Asset Status Management**
- 8 predefined statuses with color coding
- Custom status creation
- Status-based filtering and reporting

### 3. **Asset Transfer System**
- Request asset transfers between locations/users
- Approval workflow
- Transfer history tracking
- Audit trail for all movements

### 4. **Enhanced Asset Model**
- 40+ fields for comprehensive tracking
- Location hierarchy integration (Country → Province → Company → Location → Department)
- Financial tracking (purchase price, depreciation, current value)
- Assignment tracking (user, date, department)
- Technical specifications
- QR code integration

---

## 📊 Database Schema

### New Tables

#### 1. **departments**
```sql
- departmentid (PK)
- departmentname
- departmentcode (unique)
- companyid (FK → companies)
- description
- isactive
```

#### 2. **assetstatuses**
```sql
- statusid (PK)
- statusname (unique)
- statuscode (unique)
- description
- color (hex color for UI)
- isactive
```

#### 3. **assettransfers**
```sql
- transferid (PK)
- assetid (FK → assets)
- fromlocationid (FK → locations)
- fromuserid (FK → users)
- tolocationid (FK → locations)
- touserid (FK → users)
- transferdate
- transfertype (location/user/both)
- reason
- notes
- requestedby (FK → users)
- approvedby (FK → users)
- approvaldate
- status (pending/approved/rejected/completed)
```

#### 4. **assets** (Enhanced)
```sql
- assetid (PK)
- assetcode (unique, generated)
- assetname
- serialnumber
- modelnumber
- manufacturer
- maincategoryid (FK)
- categoryid (FK)
- countryid (FK)
- provinceid (FK)
- companyid (FK)
- locationid (FK)
- departmentid (FK)
- assignedto (FK → users)
- assigneddate
- purchasedate
- purchaseprice
- currentvalue
- depreciationrate
- warrantyexpiry
- statusid (FK → assetstatuses)
- condition
- specifications (JSON/Text)
- qrcode
- isactive
- createdat
- updatedat
- createdby (FK → users)
- notes
```

---

## 🔌 API Endpoints

### Departments

```
GET    /departments                    # Get all departments
GET    /departments/company/{id}       # Get departments by company
GET    /departments/{id}               # Get department by ID
POST   /departments                    # Create department
PUT    /departments/{id}               # Update department
DELETE /departments/{id}               # Delete department (soft)
```

### Asset Statuses

```
GET    /asset-statuses                 # Get all statuses
GET    /asset-statuses/{id}            # Get status by ID
POST   /asset-statuses                 # Create status
PUT    /asset-statuses/{id}            # Update status
DELETE /asset-statuses/{id}            # Delete status (soft)
```

### Asset Transfers

```
GET    /asset-transfers                # Get all transfers
GET    /asset-transfers/asset/{id}     # Get transfer history for asset
GET    /asset-transfers/pending        # Get pending transfers
GET    /asset-transfers/{id}           # Get transfer by ID
POST   /asset-transfers                # Create transfer request
PUT    /asset-transfers/{id}           # Update transfer
POST   /asset-transfers/{id}/approve   # Approve transfer
POST   /asset-transfers/{id}/reject    # Reject transfer
POST   /asset-transfers/{id}/complete  # Complete transfer
```

---

## 🎨 Asset Statuses

### Predefined Statuses

| Status | Code | Color | Description |
|--------|------|-------|-------------|
| Available | AVAIL | 🟢 Green | Asset is available for use |
| In Use | INUSE | 🔵 Blue | Currently assigned and in use |
| Maintenance | MAINT | 🟡 Yellow | Under maintenance or repair |
| Retired | RETIR | ⚫ Gray | Retired from service |
| Disposed | DISP | 🔴 Red | Disposed of |
| Lost | LOST | 🟣 Pink | Lost or missing |
| Damaged | DAMAG | 🟠 Orange | Damaged, needs repair |
| Reserved | RESERV | 🔷 Cyan | Reserved for future use |

---

## 🔄 Asset Transfer Workflow

### 1. Request Transfer
```javascript
POST /asset-transfers
{
  "assetid": 123,
  "tolocationid": 5,
  "touserid": 10,
  "transfertype": "both",
  "reason": "Employee relocation",
  "requestedby": 1
}
```

### 2. Approve Transfer
```javascript
POST /asset-transfers/1/approve
{
  "approver_id": 2
}
```

### 3. Complete Transfer
```javascript
POST /asset-transfers/1/complete
```
This automatically updates the asset's location and assigned user.

### Transfer States

```
pending → approved → completed
        ↓
      rejected
```

---

## 🏢 Location Hierarchy Flow

### Complete Flow

```
Country (2-char)
  ↓
Province (3-char)
  ↓
Company (4-char)
  ↓
Location (specific site)
  ↓
Department (within company)
  ↓
Asset
```

### Example

```
LA (Laos)
  ↓
VTE (Vientiane)
  ↓
AVIS (Avis Company)
  ↓
Vientiane HQ
  ↓
IT Department
  ↓
Laptop MLALPBAVIS25015
```

### Province → Company Relationship

**Key Rule:** Companies belong to provinces

```javascript
// When selecting province, filter companies
GET /companies?provinceid=1

// When creating company, must specify province
POST /companies
{
  "companyname": "Avis Vientiane",
  "companycode": "AVIS",
  "provinceid": 1  // Required
}
```

### Company → Department Relationship

**Key Rule:** Departments belong to companies

```javascript
// When selecting company, filter departments
GET /departments/company/1

// When creating department, must specify company
POST /departments
{
  "departmentname": "IT Department",
  "departmentcode": "IT",
  "companyid": 1  // Required
}
```

---

## 📝 Setup Instructions

### 1. Create Database Tables

```bash
cd backend
venv\Scripts\activate
python -c "from app.core.database import Base, engine; Base.metadata.create_all(bind=engine)"
```

### 2. Seed Asset Control Data

```bash
python seed_asset_control_data.py
```

This will create:
- 8 Asset Statuses
- 8 Sample Departments (for first company)

### 3. Restart Backend

```bash
restart-backend.bat
```

Or manually:
```bash
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```

### 4. Verify Setup

```bash
# Check statuses
curl http://localhost:8000/asset-statuses

# Check departments
curl http://localhost:8000/departments

# Check API docs
# Open: http://localhost:8000/docs
```

---

## 🎯 Usage Examples

### Create Department

```javascript
POST /departments
{
  "departmentname": "Information Technology",
  "departmentcode": "IT",
  "companyid": 1,
  "description": "IT support and infrastructure"
}
```

### Create Custom Status

```javascript
POST /asset-statuses
{
  "statusname": "On Loan",
  "statuscode": "LOAN",
  "description": "Asset is on loan to external party",
  "color": "#20c997"
}
```

### Request Asset Transfer

```javascript
POST /asset-transfers
{
  "assetid": 123,
  "fromlocationid": 1,
  "tolocationid": 2,
  "fromuserid": 5,
  "touserid": 10,
  "transfertype": "both",
  "reason": "Employee relocation to new office",
  "notes": "Handle with care - contains sensitive data",
  "requestedby": 5
}
```

### Get Asset Transfer History

```javascript
GET /asset-transfers/asset/123

Response:
[
  {
    "transferid": 1,
    "assetid": 123,
    "fromlocationid": 1,
    "tolocationid": 2,
    "transferdate": "2026-05-06T10:30:00",
    "status": "completed",
    "reason": "Employee relocation"
  },
  ...
]
```

---

## 🔍 Frontend Integration

### Department Selector Component

```javascript
// Get departments for selected company
const [departments, setDepartments] = useState([]);

useEffect(() => {
  if (selectedCompanyId) {
    fetch(`http://localhost:8000/departments/company/${selectedCompanyId}`)
      .then(res => res.json())
      .then(data => setDepartments(data));
  }
}, [selectedCompanyId]);
```

### Status Badge Component

```javascript
const StatusBadge = ({ status }) => {
  return (
    <span 
      className="badge" 
      style={{ backgroundColor: status.color }}
    >
      {status.statusname}
    </span>
  );
};
```

### Transfer Request Form

```javascript
const requestTransfer = async (assetId, toLocationId, toUserId) => {
  const response = await fetch('http://localhost:8000/asset-transfers', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      assetid: assetId,
      tolocationid: toLocationId,
      touserid: toUserId,
      transfertype: 'both',
      reason: 'User request',
      requestedby: currentUserId
    })
  });
  
  return response.json();
};
```

---

## 📊 Reporting Queries

### Assets by Department

```sql
SELECT 
  d.departmentname,
  COUNT(a.assetid) as asset_count,
  SUM(a.currentvalue) as total_value
FROM departments d
LEFT JOIN assets a ON d.departmentid = a.departmentid
WHERE d.isactive = true AND a.isactive = true
GROUP BY d.departmentid, d.departmentname
ORDER BY asset_count DESC;
```

### Assets by Status

```sql
SELECT 
  s.statusname,
  s.color,
  COUNT(a.assetid) as asset_count
FROM assetstatuses s
LEFT JOIN assets a ON s.statusid = a.statusid
WHERE s.isactive = true
GROUP BY s.statusid, s.statusname, s.color
ORDER BY asset_count DESC;
```

### Pending Transfers

```sql
SELECT 
  t.transferid,
  a.assetcode,
  a.assetname,
  fl.locationname as from_location,
  tl.locationname as to_location,
  u.full_name as requested_by,
  t.transferdate
FROM assettransfers t
JOIN assets a ON t.assetid = a.assetid
LEFT JOIN locations fl ON t.fromlocationid = fl.id
LEFT JOIN locations tl ON t.tolocationid = tl.id
JOIN users u ON t.requestedby = u.userid
WHERE t.status = 'pending'
ORDER BY t.transferdate DESC;
```

---

## 🔐 Security Considerations

### Transfer Approvals

- Only managers/admins can approve transfers
- Requesters cannot approve their own transfers
- Audit trail maintained for all transfers

### Department Access

- Users can only see departments in their company
- Department creation requires admin role
- Soft deletes preserve history

### Status Management

- Only admins can create/modify statuses
- Status changes are logged
- Cannot delete status if assets are using it

---

## 🚀 Next Steps

### Phase 3 Features (Recommended)

1. **Asset Maintenance Tracking**
   - Maintenance schedules
   - Service history
   - Warranty management

2. **Asset Depreciation Calculator**
   - Automatic depreciation calculation
   - Multiple depreciation methods
   - Financial reporting

3. **Asset Check-In/Check-Out**
   - Temporary asset loans
   - Return tracking
   - Overdue notifications

4. **Asset Disposal Workflow**
   - Disposal requests
   - Approval process
   - Disposal documentation

5. **Advanced Reporting**
   - Asset utilization reports
   - Cost analysis
   - Lifecycle reports

---

## 📞 Troubleshooting

### Tables Not Created

```bash
cd backend
python -c "from app.core.database import Base, engine; from app.models import Department, AssetStatus, AssetTransfer; Base.metadata.create_all(bind=engine)"
```

### Routes Not Working

```bash
# Restart backend
restart-backend.bat

# Verify routes
curl http://localhost:8000/departments
curl http://localhost:8000/asset-statuses
```

### No Data

```bash
# Run seed script
cd backend
python seed_asset_control_data.py
```

---

## 📚 Related Documentation

- `LOCATION-HIERARCHY-GUIDE.md` - Location hierarchy details
- `ADMIN-SYSTEM-CONFIG-GUIDE.md` - Admin configuration
- `INTEGRATION-PHASE1-COMPLETE.md` - Phase 1 features
- `INTEGRATION-PHASE2-COMPLETE.md` - Phase 2 features
- `ASSETS-PAGE-GUIDE.md` - Asset management UI

---

## ✅ Verification Checklist

After setup, verify:

- [ ] Backend starts without errors
- [ ] `/departments` endpoint returns data
- [ ] `/asset-statuses` endpoint returns 8 statuses
- [ ] `/asset-transfers` endpoint works
- [ ] Can create department
- [ ] Can create custom status
- [ ] Can request transfer
- [ ] Can approve transfer
- [ ] Transfer updates asset location
- [ ] All relationships work correctly

---

**Summary:**
- ✅ 3 new models (Department, AssetStatus, AssetTransfer)
- ✅ 3 new route files with full CRUD
- ✅ Enhanced Asset model with 40+ fields
- ✅ Complete transfer workflow
- ✅ Province → Company → Department hierarchy
- ✅ 8 predefined asset statuses
- ✅ Seed script for initial data
- ✅ Ready for frontend integration

**Next:** Create frontend components for these features!
