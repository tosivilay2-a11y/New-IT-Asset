# Frontend Integration Guide

## Overview

You have copied asset management components from your old Node.js project. This guide explains how to adapt them to work with the Python FastAPI backend.

---

## API Endpoint Mapping

### Old Node.js Backend → New Python FastAPI Backend

| Old Endpoint | New Endpoint | Notes |
|-------------|--------------|-------|
| `GET /assets` | `GET /api/assets/?skip=0&limit=50` | Now uses pagination |
| `GET /assets/{id}` | `GET /api/assets/{asset_id}` | Same structure |
| `POST /assets` | `POST /api/assets/` | Different request format |
| `PUT /assets/{id}` | `PUT /api/assets/{asset_id}` | Different request format |
| `DELETE /assets/{id}` | `DELETE /api/assets/{asset_id}` | Admin only |
| `GET /assets/{id}/qrcode` | `GET /api/assets/{asset_id}/qr-code` | Returns base64 QR |
| `POST /assetid/preview` | `POST /api/assets/preview-id` | Different request format |
| `POST /assetid/generate` | Automatic on create | No separate endpoint |
| `GET /locations` | `GET /api/locations/` | To be implemented |
| `GET /config/maincategories` | `GET /api/admin/config` | Different structure |
| `GET /config/countries` | Database query | Seed data available |
| `GET /config/provinces` | Database query | Seed data available |
| `GET /config/companies` | Database query | Seed data available |

---

## Data Structure Changes

### Asset Object

**Old Structure (Node.js):**
```typescript
interface Asset {
  AssetID: string;
  MainCategory: string;
  Brand: string;
  ModelName: string;
  Status: string;
  LocationID: number;
  LocationName: string;
  DatePurchase: string;
  Price: number;
  // ... many more fields
}
```

**New Structure (Python FastAPI):**
```typescript
interface Asset {
  id: number;                    // NEW: Database ID
  asset_id: string;              // Was: AssetID
  name: string;                  // NEW: Asset name
  status: string;                // lowercase
  brand?: string;                // Optional
  model?: string;                // Was: ModelName
  cpu?: string;
  ram?: string;
  hdd?: string;
  purchase_date?: string;        // Was: DatePurchase
  value?: number;                // Was: Price
  location_id?: number;          // Was: LocationID
  assigned_user_id?: number;     // NEW
  qr_code?: string;              // NEW: Base64 QR code
  created_at: string;            // NEW
  updated_at: string;            // NEW
}
```

---

## Components to Adapt

### 1. AssetList.tsx ✅ Can be adapted
**Changes needed:**
- Update API endpoints to use `/api/assets/`
- Add pagination parameters (`skip`, `limit`)
- Update field names (AssetID → asset_id, etc.)
- Remove features not yet in backend (import/export, advanced filters)

### 2. AssetDetail.tsx ✅ Already created
**Status:** New version created at `frontend/src/pages/AssetDetail.tsx`
- Works with Python backend
- Displays QR codes
- Shows all asset information

### 3. AssetForm.tsx ⚠️ Needs significant changes
**Changes needed:**
- Simplify to match Python backend fields
- Remove complex ID generation (now automatic)
- Update to use new asset creation endpoint
- Remove country/province/company selection (use seeded data)

### 4. QRCodeDisplay.tsx ✅ Can be adapted
**Changes needed:**
- Update API endpoint to `/api/assets/{asset_id}/qr-code`
- QR code is now base64 string, not file path
- Simplify (no server-side QR generation needed)

### 5. AssetCheckInOut.tsx ⚠️ Not yet supported
**Status:** Backend endpoints not implemented yet
**Required backend endpoints:**
- `POST /api/assets/{asset_id}/assign`
- `POST /api/assets/{asset_id}/return`
- `POST /api/assets/{asset_id}/transfer`

---

## Quick Adaptation Steps

### Step 1: Update API Service

Create or update `frontend/src/services/api.ts`:

```typescript
import axios from 'axios';

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token interceptor
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
```

### Step 2: Create Type Definitions

Create `frontend/src/types/asset.ts`:

```typescript
export interface Asset {
  id: number;
  asset_id: string;
  name: string;
  status: string;
  brand?: string;
  model?: string;
  cpu?: string;
  ram?: string;
  hdd?: string;
  purchase_date?: string;
  value?: number;
  location_id?: number;
  assigned_user_id?: number;
  qr_code?: string;
  serial_number?: string;
  category?: string;
  condition?: string;
  description?: string;
  created_at: string;
  updated_at: string;
}

export interface AssetCreateRequest {
  name: string;
  category_code: string;
  country_id: number;
  province_code: string;
  company_id: number;
  country_code: string;
  company_code: string;
  brand?: string;
  model?: string;
  cpu?: string;
  ram?: string;
  hdd?: string;
  purchase_date?: string;
  value?: number;
  location_id?: number;
}
```

### Step 3: Adapt AssetList Component

Key changes:
```typescript
// OLD
const response = await api.get<Asset[]>('/assets');
setAssets(response.data);

// NEW
const response = await api.get('/api/assets/?skip=0&limit=100');
const data = response.data;
setAssets(data.data); // Response has { total, skip, limit, data }
```

### Step 4: Adapt Asset Creation

```typescript
// OLD
await api.post('/assets', {
  assetId: finalAssetId,
  mainCategory: asset.MainCategory,
  // ... many fields
});

// NEW
await api.post('/api/assets/', {
  name: "Dell Laptop",
  category_code: "COMP",
  country_id: 1,
  province_code: "BKK",
  company_id: 1,
  country_code: "TH",
  company_code: "ABC",
  brand: "Dell",
  model: "Latitude 5420",
  // ... other fields
});
```

---

## Features Available Now

✅ **Working Features:**
- Asset CRUD operations
- Auto-generated Asset IDs
- QR code generation
- Asset detail view
- Basic search and filtering
- Pagination

⏳ **Coming Soon:**
- Asset assignment/return
- Location management
- Advanced filtering
- Import/Export
- Check-in/Check-out workflow
- Transaction history

---

## Recommended Approach

### Phase 1: Core Features (Now)
1. ✅ Use the new `AssetDetail.tsx` component
2. Adapt `AssetList.tsx` for basic listing
3. Create simple asset creation form
4. Display QR codes

### Phase 2: Enhanced Features (Next)
1. Implement asset assignment endpoints in backend
2. Add location management
3. Add advanced filtering
4. Implement check-in/check-out

### Phase 3: Advanced Features (Later)
1. Import/Export functionality
2. Transaction history
3. Reporting
4. Mobile QR scanning

---

## Example: Adapted AssetList Component

See `frontend/src/pages/AssetList.tsx` for a simplified version that works with the Python backend.

Key differences:
- Uses `/api/assets/` endpoint
- Handles pagination
- Uses snake_case field names
- Simplified filtering
- Removed features not yet in backend

---

## Testing Your Adapted Components

1. **Start the backend:**
   ```bash
   docker-compose up -d
   ```

2. **Verify API is running:**
   ```bash
   curl http://localhost:8000/
   ```

3. **Test asset creation:**
   ```bash
   curl -X POST http://localhost:8000/api/assets/ \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -d '{
       "name": "Test Laptop",
       "category_code": "COMP",
       "country_id": 1,
       "province_code": "BKK",
       "company_id": 1,
       "country_code": "TH",
       "company_code": "ABC"
     }'
   ```

4. **Start frontend:**
   ```bash
   cd frontend
   npm start
   ```

---

## Need Help?

- **API Documentation:** http://localhost:8000/docs
- **Backend Status:** See `STATUS.md`
- **Feature List:** See `docs/ASSET-MANAGEMENT-FEATURES.md`

---

**Summary:** Your old components can be adapted, but they need significant changes to work with the Python backend's different API structure and field names. Start with the core features and gradually add more functionality as the backend implements additional endpoints.
