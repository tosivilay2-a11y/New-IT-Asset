# Stock Location Set-Default Testing Guide

## Quick Test

### Option 1: Using the Test Script (Recommended)

The test script now includes authentication. Run it with:

```bash
cd backend
python test_set_default_stock.py
```

**What it does**:
1. Logs in with admin credentials (admin/admin123)
2. Fetches all stock locations
3. Selects a non-default location
4. Sets it as default
5. Verifies the change was successful

**Expected Output**:
```
============================================================
Testing Set Default Stock Location Endpoint
============================================================
Logging in...
✅ Login successful, token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

1. Fetching all stock locations...
✅ Found 3 stock locations:
   ⭐ DEFAULT ID: 1, Name: Main Warehouse, Default: True
      ID: 2, Name: Branch Office, Default: False
      ID: 3, Name: Secondary Storage, Default: False

2. Setting stock location ID 2 (Branch Office) as default...
✅ Response: Stock location 'Branch Office' set as default

3. Verifying the change...
✅ Updated stock locations:
      ID: 1, Name: Main Warehouse, Default: False
   ⭐ DEFAULT ID: 2, Name: Branch Office, Default: True
      ID: 3, Name: Secondary Storage, Default: False

✅ SUCCESS: Set-default function works correctly!
```

### Option 2: Manual Testing with cURL

**Step 1: Login**
```bash
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"
```

**Response**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Step 2: Get Stock Locations**
```bash
curl -X GET http://localhost:8000/stock-locations/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

**Step 3: Set Default**
```bash
curl -X POST http://localhost:8000/stock-locations/set-default/2 \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Option 3: Using Postman

1. **Create Login Request**
   - Method: POST
   - URL: `http://localhost:8000/login`
   - Body (form-data):
     - username: admin
     - password: admin123
   - Send and copy the `access_token`

2. **Create Get Stock Locations Request**
   - Method: GET
   - URL: `http://localhost:8000/stock-locations/`
   - Headers:
     - Authorization: Bearer {access_token}
   - Send

3. **Create Set Default Request**
   - Method: POST
   - URL: `http://localhost:8000/stock-locations/set-default/2`
   - Headers:
     - Authorization: Bearer {access_token}
   - Send

## Troubleshooting

### Error: "Not authenticated" (401)
**Cause**: Missing or invalid authentication token

**Solution**:
- Make sure you're logged in first
- Include the `Authorization: Bearer {token}` header
- Check that the token hasn't expired

### Error: "Stock location not found" (404)
**Cause**: Invalid stock location ID

**Solution**:
- First fetch all stock locations to see valid IDs
- Use a valid ID from the list

### Error: "Internal Server Error" (500)
**Cause**: Database or server issue

**Solution**:
- Check backend logs for detailed error
- Verify database connection
- Restart backend server

## Database Verification

To verify changes directly in PostgreSQL:

```sql
-- Connect to database
psql -U postgres -d it_asset_db

-- Check all stock locations
SELECT stockid, stockname, stockdefault FROM stocklocation ORDER BY stockid;

-- Count defaults (should be exactly 1)
SELECT COUNT(*) as default_count FROM stocklocation WHERE stockdefault = true;

-- Find current default
SELECT stockid, stockname FROM stocklocation WHERE stockdefault = true;

-- Update a specific location to default (direct SQL)
UPDATE stocklocation SET stockdefault = false WHERE stockdefault = true;
UPDATE stocklocation SET stockdefault = true WHERE stockid = 2;
```

## Frontend Testing

The frontend automatically uses the set-default endpoint when you click the "✓ Set Default" button in System Config → Stock Location tab.

**To test**:
1. Open the application
2. Go to Admin → System Config
3. Click "Stock Location" tab
4. Click "✓ Set Default" button on any non-default location
5. Verify the UI updates:
   - Selected location shows "⭐ DEFAULT" badge
   - Button disappears from that location
   - Previous default reverts to normal appearance

## API Response Format

### Success Response (200 OK)
```json
{
  "message": "Stock location 'Branch Office' set as default",
  "stock_location": {
    "stockid": 2,
    "stockname": "Branch Office",
    "locationid": 1,
    "stockdefault": true
  }
}
```

### Error Response (404 Not Found)
```json
{
  "detail": "Stock location not found"
}
```

### Error Response (401 Unauthorized)
```json
{
  "detail": "Not authenticated"
}
```

## Performance Notes

- The set-default operation is atomic (all-or-nothing)
- Uses bulk update for efficiency
- Minimal database queries (2 total)
- Response time: typically < 100ms

## Security Notes

- Requires authentication (admin user)
- Only authenticated users can set default
- No permission checks (any authenticated user can set default)
- Consider adding role-based access control if needed

---

**Status**: Ready for testing ✅
