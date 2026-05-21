# Quick Reference Card

## 🚀 Quick Start

### 1. Setup Location Hierarchy (One-time)
```bash
run-setup.bat
```

### 2. Start Backend
```bash
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```

### 3. Start Frontend
```bash
cd frontend
npm start
```

## 📡 Key API Endpoints

### Location Hierarchy
```
GET  /countries                    # List countries
GET  /provinces?country_id=1       # List provinces
GET  /companies?province_id=1      # List companies
GET  /main-categories              # List categories
```

### Asset ID & QR Code
```
POST /asset-utils/preview-asset-id    # Preview ID (no increment)
POST /asset-utils/generate-asset-id   # Generate ID (increments)
POST /asset-utils/generate-qr-code    # Generate QR code
```

## 🔢 Asset ID Format

```
Format: [C][CC][CCC][CCCC][YY][NNN]
Example: MLALPBAVIS25015

M     = Monitor (category)
LA    = Lao (country)
LPB   = Luang Prabang (province)
AVIS  = Company
25    = Year 2025
015   = Sequence number
```

## 📦 Main Categories

| Code | Category    | Code | Category   |
|------|-------------|------|------------|
| C    | Computer    | N    | Network    |
| L    | Laptop      | S    | Server     |
| M    | Monitor     | W    | Workstation|
| P    | Printer     | T    | Tablet     |
| D    | Desktop     | H    | Phone      |
| U    | UPS         | A    | Accessory  |
| O    | Other       |      |            |

## 🌍 Seeded Data

### Countries
- LA = Lao PDR
- TH = Thailand
- VN = Vietnam
- KH = Cambodia
- MM = Myanmar

### Provinces (Lao)
- VTE = Vientiane Capital
- LPB = Luang Prabang
- CPS = Champasak
- SVK = Savannakhet
- APU = Attapeu

### Companies
- AVIS = AVIS Rent A Car
- FORD = Ford Motor Company
- EFGL = Efgl Corporation
- LARV = Larv Company
- RMAG = Rmag Industries
- COMN = Common Services

## 🔗 URLs

- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Frontend: http://localhost:3000

## 📝 Common Tasks

### Preview Asset ID
```json
POST /asset-utils/preview-asset-id
{
  "main_category": "Monitor",
  "country_id": 1,
  "province_id": 2,
  "company_id": 1
}
```

### Generate QR Code
```json
POST /asset-utils/generate-qr-code
{
  "asset_id": "MLALPBAVIS25015",
  "asset_name": "Dell Monitor"
}
```

### Get Provinces for Country
```
GET /provinces?country_id=1
```

### Get Companies for Province
```
GET /companies?province_id=1
```

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| Routes not found | Restart backend server |
| No data returned | Run `seed_location_hierarchy.py` |
| Import errors | Activate virtual environment |
| Tables not created | Run `create_location_tables.py` |

## 📚 Documentation

- Full Guide: `LOCATION-HIERARCHY-GUIDE.md`
- Phase 1 Complete: `INTEGRATION-PHASE1-COMPLETE.md`
- Integration Plan: `BACKUP-INTEGRATION-PLAN.md`

---

**Quick Help**: Open http://localhost:8000/docs for interactive API testing
