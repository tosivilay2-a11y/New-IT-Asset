# IT Asset Management System — Project Documentation

> Generated overview of the **New-Asset-management** repository.  
> Last reviewed: May 2026

---

## 1. Overview

This is a **full-stack IT Asset Management & Inventory Tracking** application. It manages hardware/assets across a geographic and organizational hierarchy, supports QR codes and auto-generated asset IDs, check-in/check-out workflows, staff assignment, stock locations, audits, and admin configuration.

| Item | Value |
|------|--------|
| API title | IT Asset Management System |
| API version | 2.0.0 |
| Default API URL | `http://localhost:8000` |
| Default frontend URL | `http://localhost:3000` |
| Primary database | PostgreSQL (`assetdb`) |

---

## 2. Tech Stack

### Backend
- **Python** + **FastAPI** (REST API, OpenAPI at `/docs`)
- **SQLAlchemy 2** (ORM)
- **Alembic** (migrations)
- **PostgreSQL** via `psycopg2-binary`
- **JWT auth** (`python-jose`, OAuth2 password flow)
- **Passlib + bcrypt** (password hashing; bcrypt pinned to 4.0.1)
- **QR codes** (`qrcode`, Pillow)
- **File storage**: local filesystem or **Cloudflare R2** (boto3)

### Frontend
- **React 18** (Create React App / `react-scripts`)
- **React Router v6**
- **Axios** for API calls
- **qrcode** (client-side QR generation in some views)

### DevOps
- **Docker Compose**: `postgres:15`, backend, frontend
- Many Windows `.bat` scripts for setup, backup, and troubleshooting

---

## 3. Repository Layout

```
New-Asset-management/
├── backend/                 # FastAPI application
│   ├── app/
│   │   ├── core/            # config, database, security
│   │   ├── models/          # SQLAlchemy models
│   │   ├── routes/          # API routers
│   │   ├── schemas/         # Pydantic schemas
│   │   ├── services/        # ID gen, QR, uploads, R2
│   │   └── main.py          # App entry + router registration
│   ├── alembic/             # DB migrations (001–009)
│   ├── uploads/             # Local file uploads (mounted at /uploads)
│   ├── requirements.txt
│   └── venv/                # Python virtualenv (local dev)
├── frontend/
│   ├── src/
│   │   ├── components/      # Navbar, admin panels, QR, selectors
│   │   ├── pages/             # Route screens
│   │   ├── services/        # api.js (primary), api.ts (legacy TS)
│   │   └── App.js           # Routes + auth gate
│   └── package.json
├── docs/                    # Additional guides
├── it-asset-system/         # Related / alternate tree (if present)
├── Bakcup project/          # Backup copy of older work
├── docker-compose.yml
├── README.md                # Quick start guide
└── *.md / *.bat             # Many feature-specific notes & scripts
```

---

## 4. Backend Architecture

### 4.1 Entry point (`backend/app/main.py`)

Registers routers and creates tables on startup via `Base.metadata.create_all`. Serves uploaded files at `/uploads`.

**Registered route modules:**

| Module | Prefix / area | Purpose |
|--------|----------------|---------|
| `auth` | `/auth` | Login, register |
| `users` | `/users` | User CRUD, `/users/me` |
| `countries`, `provinces`, `companies`, `main_categories` | Various | Location & category hierarchy |
| `departments`, `asset_statuses`, `asset_transfers` | Various | Asset control |
| `assets_enhanced` | `/api/assets` | Enhanced asset API (ID preview, lifecycle) |
| `assets` | `/assets` | Primary asset CRUD, check-in/out, condition reports |
| `asset_utils` | — | Asset ID & QR utilities |
| `inventory` | — | Inventory items & transactions |
| `audits` | — | Audit sessions & records |
| `admin` | `/api/admin` | System config, asset ID formats (admin only) |
| `config` | — | Runtime configuration |
| `staff` | `/staff` | Staff directory |
| `asset_checkinout_history` | — | Check-in/out audit trail |
| `stock_location` | `/stock-locations` | Warehouse/stock locations |

### 4.2 Data models (`backend/app/models/`)

| Model | Table | Role |
|-------|--------|------|
| `User` | `users` | Login accounts (roles: admin, staff, etc.) |
| `Asset` | `assets` | Core IT assets |
| `AssetStatus` | `assetstatuses` | Available, In Use, Retired, etc. |
| `Staff` | `staff` | Employees who receive checked-out assets |
| `StockLocation` | `stocklocation` | Physical stock/warehouse per location |
| `AssetCheckInOutHistory` | — | History of check-in/out events |
| `AssetConditionReport` | — | Condition captured on check-in |
| `AssetTransfer` | — | Inter-location transfers |
| `Country`, `Province`, `Company`, `Location` | — | Geographic hierarchy |
| `MainCategory`, `Category` | — | Asset categorization |
| `Department` | — | Organizational units |
| `AssetSequence` | — | Sequence numbers for ID generation |
| `SystemConfig` | — | Key/value system settings |
| `InventoryItem`, `InventoryTransaction` | — | Non-asset inventory & stock moves |
| `AuditSession`, `AuditRecord` | — | Physical inventory audits |

**Asset model highlights** (`asset.py`):
- `assetcode` — unique generated ID
- Location FKs: country, province, company, location, department
- `stockid` — PostgreSQL `integer[]` (array of stock location IDs)
- `assignedto` — staff/user ID (FK to users removed in migration 009)
- Financial: purchase price, PO number, cost center, depreciation
- `statusid`, `condition`, `qrcode`, `specifications`

### 4.3 Services (`backend/app/services/`)

| Service | Responsibility |
|---------|----------------|
| `asset_id_generator.py` | Structured asset codes from country/company/category |
| `qr_code_service.py` | QR image generation for assets |
| `file_upload_service.py` | PO attachments (local) |
| `cloud_storage_service.py` | Cloudflare R2 uploads |

### 4.4 Configuration (`backend/app/core/config.py`)

Environment via `.env` (pydantic-settings):

- `DATABASE_URL`
- `SECRET_KEY`, `ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES`
- `STORAGE_TYPE` — `local` or `r2`
- R2: `R2_ACCOUNT_ID`, `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`, `R2_BUCKET_NAME`, `R2_ENDPOINT_URL`, `R2_PUBLIC_URL`

### 4.5 Database migrations (`backend/alembic/versions/`)

| Version | Topic |
|---------|--------|
| 001 | PO fields on assets |
| 002 | Cost center field |
| 003 | Cost center column |
| 004 | Fix `isactive` type |
| 005 | `firstname` / `lastname` on users |
| 006 | Staff table |
| 007 | Company/location on staff |
| 008 | Check-in/out history |
| 009 | Remove `assignedto` FK constraint |

---

## 5. Frontend Architecture

### 5.1 Routing (`frontend/src/App.js`)

Protected routes require JWT in `localStorage` (`token`). Unauthenticated users redirect to `/login`.

| Path | Page | Description |
|------|------|-------------|
| `/login` | `Login.jsx` | OAuth2-style login |
| `/` | `Dashboard.jsx` | Stats & low-stock alerts |
| `/assets` | `AssetsManagementEnhanced.jsx` | Main asset list (primary UI) |
| `/assets/new` | `AssetFormNew.jsx` | Create asset |
| `/assets/:id` | `AssetDetailView.jsx` | Asset detail |
| `/assets/:id/edit` | `AssetFormNew.jsx` | Edit asset |
| `/assets/checkinout` | `AssetCheckInOut.jsx` | Check-in / check-out |
| `/assets/original` | `AssetsManagement.jsx` | Legacy list |
| `/assets/simple` | `Assets.jsx` | Simple list |
| `/inventory` | `Inventory.jsx` | Inventory management |
| `/audits` | `Audits.jsx` | Audit sessions |
| `/admin/config` | `SystemConfig.jsx` | Countries, categories, stock, staff, etc. |
| `/admin/storage` | `StorageConfig.jsx` | Local vs R2 storage |
| `/admin/users` | `UserManagement.jsx` | User admin |
| `/profile/change-password` | `ChangePassword.jsx` | Password change |

### 5.2 Key components

| Component | Role |
|-----------|------|
| `Navbar.jsx` | Main navigation |
| `LocationSelector.jsx`, `CategorySelector.jsx` | Hierarchical pickers |
| `QRCodeGenerator.jsx`, `QRCodeDisplay.tsx` | QR display/generation |
| `AssetIDPreview.jsx` | Preview generated asset ID |
| `admin/CountryManagement.jsx` | Countries CRUD |
| `admin/ProvinceManagement.jsx` | Provinces CRUD |
| `admin/CompanyManagement.jsx` | Companies CRUD |
| `admin/CategoryManagement.jsx` | Main categories |
| `admin/StaffManagement.jsx` | Staff CRUD |
| `admin/StockLocationConfig.jsx` | Stock locations & default |
| `admin/AssetIDGenerator.jsx` | ID format configuration |

### 5.3 API client (`frontend/src/services/api.js`)

- Base URL: `http://localhost:8000`
- Bearer token on all requests
- 401 → clears token and redirects to login
- Exports: `authAPI`, `assetsAPI`, `inventoryAPI`, etc.

> Note: Some older TypeScript files (`AssetList.tsx`, `api.ts`) coexist with the main JSX stack.

---

## 6. Core Features

### 6.1 Authentication & users
- Register and login (`/auth/login` uses form-urlencoded username/password)
- JWT bearer tokens
- Roles (e.g. `admin`) enforced on admin routes
- User profile: first name, last name, email, role

### 6.2 Asset lifecycle
- Create / read / update / delete assets
- Auto-generated `assetcode` from hierarchy codes + sequence
- QR code stored on asset record
- Multi-file PO attachments (local or R2)
- Status workflow via `assetstatuses` table
- Asset transfers between locations
- Enhanced API at `/api/assets` for previews and extended flows

### 6.3 Check-in / Check-out

**Frontend rules** (`AssetCheckInOut.jsx`):
1. Asset must exist (`assetcode` lookup)
2. `statusid` must be **1** (hardcoded as “Available”) — otherwise error: *Only "Available" assets can be checked out*
3. Must not already be `assignedto` someone
4. `condition` must be **"Good"** (case-insensitive)

**Backend checkout** (`POST /assets/{asset_id}/checkout`):
- Validates condition is `"good"` (backend message references condition, not status)
- Sets `stockid` to `[0]`, assigns staff, sets status to “In Use”
- Records optional history and condition reports on check-in

**Check-in** returns asset to stock location, updates status, writes `AssetConditionReport`.

> **Note:** Frontend enforces `statusid === 1` for Available; backend checkout primarily enforces **condition = Good**. If status IDs in the database do not match (e.g. “Available” is not ID 1), users see errors like *Current status: Status 4*.

### 6.4 Location hierarchy
```
Country → Province → Company → Location → Department
```
Used for asset placement, reporting, and ID generation.

### 6.5 Staff management
- Staff records: employee ID, name, email, department, company/location links
- Checkout assigns assets to `staffid` (stored in `assets.assignedto`)

### 6.6 Stock locations
- Named stock areas tied to a `locationid`
- One location can be marked `stockdefault`
- Check-in selects target stock; checkout clears stock (`stockid = [0]`)

### 6.7 Inventory & audits
- **Inventory**: SKU-based items, quantities, min levels, stock in/out transactions
- **Audits**: Sessions comparing expected vs actual counts with discrepancy types

### 6.8 Admin & system config
- System key/value config (categories, defaults)
- Asset ID format patterns
- Storage backend switch (local / Cloudflare R2)
- Reference data CRUD (countries, provinces, companies, categories)

---

## 7. API Summary (main prefixes)

| Prefix | Auth | Notes |
|--------|------|-------|
| `GET /` | No | API info |
| `GET /health` | No | Health check |
| `POST /auth/login` | No | Returns `access_token` |
| `POST /auth/register` | No | New user |
| `GET /users/me` | Yes | Current user |
| `GET/POST/PUT/DELETE /assets/` | Yes | Primary asset API |
| `POST /assets/{id}/checkout` | Yes | Checkout |
| `POST /assets/{id}/checkin` | Yes | Check-in with condition payload |
| `GET /assets/{id}/condition-reports` | Yes | Condition history |
| `GET /api/assets/...` | Yes | Enhanced asset routes |
| `GET /api/admin/...` | Admin | System & ID config |
| `GET /staff/` | Yes | Staff list |
| `GET /stock-locations/` | Yes | Stock locations |
| Inventory & audit routes | Yes | See `inventory.py`, `audits.py` |

Interactive docs: **http://localhost:8000/docs**

---

## 8. Running the Project

### Docker (recommended in README)
```bash
docker-compose up -d
# Backend: http://localhost:8000
# Frontend: http://localhost:3000
# PostgreSQL: localhost:5432 (user/pass/db: postgres/postgres/assetdb)
```

### Manual
```bash
# Backend
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
# Configure backend/.env from .env.example
alembic upgrade head
uvicorn app.main:app --reload

# Frontend (separate terminal)
cd frontend
npm install
npm start
```

Common helper scripts at repo root: `start-backend.bat`, `start-frontend.bat`, `quick-start.bat`, `docker-start.bat`.

---

## 9. Environment & secrets

Create `backend/.env` (see `.env.example` if present):

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/assetdb
SECRET_KEY=your-secret-key
STORAGE_TYPE=local
# Optional R2_* variables for cloud storage
```

**Do not commit** real secrets or production credentials.

---

## 10. Supporting folders & artifacts

| Path | Description |
|------|-------------|
| `docs/` | Integration guides, deployment notes, feature lists |
| `Bakcup project/` | Older backup of frontend/backend |
| `it-asset-system/` | Additional related system files |
| Root `*.md` files | 100+ feature/fix implementation notes from development |
| Root `*.bat` / `*.py` | One-off migrations, tests, DB fixes, seed scripts |

For day-to-day onboarding, start with **`README.md`**, then **`docs/QUICK-SETUP.md`** and **`docs/ASSET-MANAGEMENT-FEATURES.md`**.

---

## 11. Troubleshooting reference

| Symptom | Likely cause |
|---------|----------------|
| *Cannot checkout… Status 4… Only Available* | Asset `statusid` ≠ 1; status “Available” may use a different ID in DB |
| *Only Good condition* | `assets.condition` is not `Good` |
| *Asset already assigned* | `assignedto` is set; check in first |
| 401 / redirect to login | Expired or missing JWT |
| Backend connection errors | API not running on port 8000 |
| bcrypt errors | Must use `bcrypt==4.0.1` with passlib |

---

## 12. Version & maintenance notes

- API self-reports **v2.0.0**; frontend package is **v1.0.0**
- Dual asset route sets: legacy `/assets` and enhanced `/api/assets` — frontend primarily uses `/assets`
- `assignedto` intentionally has **no FK** (staff or legacy user IDs)
- `stockid` is a **PostgreSQL integer array**, not a single integer
- Large number of ad-hoc fix scripts in `backend/` root — prefer Alembic for schema changes going forward

---

## 13. Related documentation in this repo

| File | Topic |
|------|--------|
| `README.md` | Quick start, Docker, manual setup |
| `SETUP_GUIDE.md` / `MANUAL_SETUP_GUIDE.md` | Detailed setup |
| `DOCKER_SETUP_GUIDE.md` | Docker specifics |
| `ASSET-CHECKINOUT-FEATURE-COMPLETE.md` | Check-in/out feature |
| `LOCATION-HIERARCHY-GUIDE.md` | Location model |
| `CLOUDFLARE-R2-SETUP.md` | R2 storage |
| `docs/ASSET-MANAGEMENT-FEATURES.md` | Feature catalog |
| `CHECKOUT-AVAILABLE-STATUS-ONLY.md` | Checkout status rules |

---

*This document summarizes the codebase structure and behavior. For API request/response shapes, use the live OpenAPI schema at `/docs` when the backend is running.*
