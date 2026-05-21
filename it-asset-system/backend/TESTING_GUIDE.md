# Backend API Testing Guide

Complete guide to test all backend endpoints.

## Prerequisites

1. Backend server running at `http://localhost:5000`
2. Database setup and seeded
3. API testing tool (Postman, curl, or similar)

## Quick Start

```bash
# 1. Install dependencies
npm install

# 2. Setup database
npm run db:setup

# 3. Seed data
npm run db:seed

# 4. Start server
npm run dev
```

## Test Sequence

### 1. Health Check

**Request:**
```bash
GET http://localhost:5000/health
```

**Expected Response:**
```json
{
  "success": true,
  "message": "Server is running",
  "timestamp": "2026-05-05T..."
}
```

---

### 2. User Login

**Request:**
```bash
POST http://localhost:5000/api/auth/login
Content-Type: application/json

{
  "username": "admin@example.com",
  "password": "admin123"
}
```

**Expected Response:**
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "userId": 1,
      "username": "admin",
      "email": "admin@example.com",
      "fullName": "System Administrator",
      "role": "Admin"
    }
  }
}
```

**Save the token** - You'll need it for all subsequent requests!

---

### 3. Get User Profile

**Request:**
```bash
GET http://localhost:5000/api/auth/profile
Authorization: Bearer YOUR_TOKEN_HERE
```

**Expected Response:**
```json
{
  "success": true,
  "data": {
    "UserID": 1,
    "Username": "admin",
    "Email": "admin@example.com",
    "FullName": "System Administrator",
    "IsActive": true,
    "RoleName": "Admin",
    "DepartmentName": "IT"
  }
}
```

---

### 4. Preview Asset ID

**Request:**
```bash
GET http://localhost:5000/api/assets/preview-id?mainCategoryId=1&countryId=1&provinceId=1&companyId=1
Authorization: Bearer YOUR_TOKEN_HERE
```

**Expected Response:**
```json
{
  "success": true,
  "data": {
    "assetId": "COMP-TH-BKK-ABC-2026-0001"
  }
}
```

---

### 5. Create Asset

**Request:**
```bash
POST http://localhost:5000/api/assets
Authorization: Bearer YOUR_TOKEN_HERE
Content-Type: application/json

{
  "mainCategoryId": 1,
  "categoryId": 1,
  "countryId": 1,
  "provinceId": 1,
  "companyId": 1,
  "locationId": 1,
  "statusId": 1,
  "brand": "Dell",
  "modelName": "Latitude 5420",
  "serialNumber": "SN123456789",
  "cpu": "Intel Core i7-1185G7",
  "ram": "16GB DDR4",
  "hdd": "512GB NVMe SSD",
  "datePurchase": "2026-01-15",
  "price": 45000.00,
  "notes": "New laptop for IT department"
}
```

**Expected Response:**
```json
{
  "success": true,
  "message": "Asset created successfully",
  "data": {
    "assetId": 1,
    "assetCode": "COMP-TH-BKK-ABC-2026-0001",
    "qrCode": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...",
    "asset": { ... }
  }
}
```

---

### 6. Get All Assets

**Request:**
```bash
GET http://localhost:5000/api/assets?page=1&limit=50
Authorization: Bearer YOUR_TOKEN_HERE
```

**Expected Response:**
```json
{
  "success": true,
  "data": [
    {
      "AssetID": 1,
      "AssetCode": "COMP-TH-BKK-ABC-2026-0001",
      "Brand": "Dell",
      "ModelName": "Latitude 5420",
      "MainCategoryName": "Computer",
      "StatusName": "Available",
      "LocationName": "Bangkok HQ",
      ...
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 50,
    "total": 1,
    "totalPages": 1
  }
}
```

---

### 7. Get Asset by ID

**Request:**
```bash
GET http://localhost:5000/api/assets/1
Authorization: Bearer YOUR_TOKEN_HERE
```

**Expected Response:**
```json
{
  "success": true,
  "data": {
    "AssetID": 1,
    "AssetCode": "COMP-TH-BKK-ABC-2026-0001",
    "Brand": "Dell",
    "ModelName": "Latitude 5420",
    "SerialNumber": "SN123456789",
    "CPU": "Intel Core i7-1185G7",
    "RAM": "16GB DDR4",
    "HDD": "512GB NVMe SSD",
    "Price": 45000.00,
    "MainCategoryName": "Computer",
    "CategoryName": "Laptop",
    "StatusName": "Available",
    "LocationName": "Bangkok HQ",
    "CompanyName": "ABC Corporation",
    "QRCode": "data:image/png;base64,..."
  }
}
```

---

### 8. Search Assets

**Request:**
```bash
GET http://localhost:5000/api/assets?search=Dell&page=1&limit=50
Authorization: Bearer YOUR_TOKEN_HERE
```

**Expected Response:**
```json
{
  "success": true,
  "data": [ ... filtered assets ... ],
  "pagination": { ... }
}
```

---

### 9. Filter Assets by Status

**Request:**
```bash
GET http://localhost:5000/api/assets?statusId=1&page=1&limit=50
Authorization: Bearer YOUR_TOKEN_HERE
```

---

### 10. Assign Asset to User

**Request:**
```bash
POST http://localhost:5000/api/assets/1/assign
Authorization: Bearer YOUR_TOKEN_HERE
Content-Type: application/json

{
  "userId": 2
}
```

**Expected Response:**
```json
{
  "success": true,
  "message": "Asset assigned successfully",
  "data": {
    "assetId": 1,
    "asset": {
      "AssetID": 1,
      "AssignedTo": 2,
      "AssignedToName": "IT Manager",
      "StatusName": "In Use",
      ...
    }
  }
}
```

---

### 11. Transfer Asset Location

**Request:**
```bash
POST http://localhost:5000/api/assets/1/transfer
Authorization: Bearer YOUR_TOKEN_HERE
Content-Type: application/json

{
  "locationId": 2
}
```

**Expected Response:**
```json
{
  "success": true,
  "message": "Asset transferred successfully",
  "data": {
    "assetId": 1,
    "asset": {
      "CurrentLocationName": "Bangkok - Floor 1",
      ...
    }
  }
}
```

---

### 12. Unassign Asset

**Request:**
```bash
POST http://localhost:5000/api/assets/1/unassign
Authorization: Bearer YOUR_TOKEN_HERE
```

**Expected Response:**
```json
{
  "success": true,
  "message": "Asset unassigned successfully",
  "data": {
    "assetId": 1,
    "asset": {
      "AssignedTo": null,
      "StatusName": "Available",
      ...
    }
  }
}
```

---

### 13. Get Asset History

**Request:**
```bash
GET http://localhost:5000/api/assets/1/history
Authorization: Bearer YOUR_TOKEN_HERE
```

**Expected Response:**
```json
{
  "success": true,
  "data": [
    {
      "AuditLogID": 3,
      "Action": "UPDATE",
      "TableName": "Assets",
      "RecordID": 1,
      "OldValue": "{...}",
      "NewValue": "{...}",
      "UserName": "System Administrator",
      "Timestamp": "2026-05-05T..."
    },
    ...
  ]
}
```

---

### 14. Generate QR Code

**Request:**
```bash
POST http://localhost:5000/api/assets/1/qr-code
Authorization: Bearer YOUR_TOKEN_HERE
```

**Expected Response:**
```json
{
  "success": true,
  "message": "QR code generated successfully",
  "data": {
    "assetId": 1,
    "qrCode": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..."
  }
}
```

---

### 15. Scan QR Code

**Request:**
```bash
POST http://localhost:5000/api/assets/qr-codes/scan
Authorization: Bearer YOUR_TOKEN_HERE
Content-Type: application/json

{
  "assetCode": "COMP-TH-BKK-ABC-2026-0001"
}
```

**Expected Response:**
```json
{
  "success": true,
  "data": {
    "AssetID": 1,
    "AssetCode": "COMP-TH-BKK-ABC-2026-0001",
    "Brand": "Dell",
    "ModelName": "Latitude 5420",
    ...
  }
}
```

---

### 16. Bulk Generate QR Codes

**Request:**
```bash
POST http://localhost:5000/api/assets/qr-codes/bulk
Authorization: Bearer YOUR_TOKEN_HERE
Content-Type: application/json

{
  "assetIds": [1, 2, 3]
}
```

**Expected Response:**
```json
{
  "success": true,
  "message": "QR codes generated",
  "data": [
    {
      "assetId": 1,
      "assetCode": "COMP-TH-BKK-ABC-2026-0001",
      "success": true,
      "qrCode": "data:image/png;base64,..."
    },
    ...
  ]
}
```

---

### 17. Get Dashboard Statistics

**Request:**
```bash
GET http://localhost:5000/api/assets/statistics
Authorization: Bearer YOUR_TOKEN_HERE
```

**Expected Response:**
```json
{
  "success": true,
  "data": {
    "TotalAssets": 10,
    "Available": 5,
    "InUse": 3,
    "Maintenance": 1,
    "Disposed": 1,
    "TotalValue": 450000.00
  }
}
```

---

### 18. Update Asset

**Request:**
```bash
PUT http://localhost:5000/api/assets/1
Authorization: Bearer YOUR_TOKEN_HERE
Content-Type: application/json

{
  "mainCategoryId": 1,
  "categoryId": 1,
  "brand": "Dell",
  "modelName": "Latitude 5420 (Updated)",
  "statusId": 1,
  "locationId": 1,
  "price": 42000.00,
  "notes": "Price updated after negotiation"
}
```

**Expected Response:**
```json
{
  "success": true,
  "message": "Asset updated successfully",
  "data": {
    "assetId": 1,
    "asset": { ... updated data ... }
  }
}
```

---

### 19. Get Assets by Location

**Request:**
```bash
GET http://localhost:5000/api/assets/location/1
Authorization: Bearer YOUR_TOKEN_HERE
```

---

### 20. Get Assets by User

**Request:**
```bash
GET http://localhost:5000/api/assets/user/2
Authorization: Bearer YOUR_TOKEN_HERE
```

---

## Testing with Postman

### Import Collection

1. Create new collection: "IT Asset Management API"
2. Add environment variables:
   - `base_url`: `http://localhost:5000`
   - `token`: (will be set after login)

3. Add pre-request script to collection:
```javascript
pm.request.headers.add({
    key: 'Authorization',
    value: 'Bearer ' + pm.environment.get('token')
});
```

4. After login, save token:
```javascript
pm.environment.set('token', pm.response.json().data.token);
```

### Test Scenarios

**Scenario 1: Complete Asset Lifecycle**
1. Login as admin
2. Preview Asset ID
3. Create asset
4. View asset details
5. Assign to user
6. Transfer location
7. View history
8. Unassign
9. Update asset
10. Delete asset

**Scenario 2: QR Code Workflow**
1. Login
2. Create asset
3. Generate QR code
4. Scan QR code
5. Get printable labels

**Scenario 3: Search & Filter**
1. Login
2. Get all assets
3. Search by brand
4. Filter by status
5. Filter by location
6. Get statistics

## Common Issues

### 401 Unauthorized
- Token expired or invalid
- Login again to get new token

### 403 Forbidden
- User doesn't have required permission
- Check user role and permissions

### 404 Not Found
- Asset ID doesn't exist
- Check asset ID in database

### 500 Internal Server Error
- Database connection issue
- Check server logs
- Verify .env configuration

## Success Criteria

✅ All endpoints return expected responses
✅ Authentication works correctly
✅ Asset CRUD operations successful
✅ QR code generation works
✅ Asset assignment/transfer works
✅ Audit logging captures changes
✅ Permissions enforced correctly
✅ Statistics calculated correctly

## Next Steps

After successful testing:
1. Document any issues found
2. Test with different user roles
3. Test edge cases and error handling
4. Proceed to frontend development
