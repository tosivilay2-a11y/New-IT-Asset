# Location Hierarchy Integration Guide

## 🎯 Overview

This guide covers the newly integrated **Location Hierarchy System** from the backup project, including:
- Countries, Provinces, Companies management
- Auto-generated Asset IDs (15-character format)
- QR Code generation
- Main Categories with single-letter codes

## 📋 What's New

### 1. Location Hierarchy Tables

```
Country (e.g., Lao - LA)
  └── Province (e.g., Vientiane - VTE)
      └── Company (e.g., AVIS)
          └── Location (existing table)
```

### 2. Asset ID Format

**New Format**: 15 characters total
```
[Category][Country][Province][Company][Year][Sequence]
Example: MLALPBAVIS25015

M     = Monitor (1 char)
LA    = Lao (2 chars)
LPB   = Luang Prabang (3 chars)
AVIS  = Company (4 chars)
25    = Year 2025 (2 chars)
015   = Sequence number (3 chars)
```

**Sequence Logic**:
- Resets to 001 every year
- Unique per Country + Company combination
- Auto-increments when asset is saved

### 3. Main Categories

Single-letter codes for asset types:
- **C** = Computer
- **L** = Laptop
- **M** = Monitor
- **P** = Printer
- **N** = Network
- **S** = Server
- **W** = Workstation
- **T** = Tablet
- **H** = Phone
- **A** = Accessory
- **D** = Desktop
- **U** = UPS
- **O** = Other

## 🚀 Setup Instructions

### Step 1: Create Tables and Seed Data

Run the setup script:
```bash
setup-location-hierarchy.bat
```

Or manually:
```bash
cd backend
venv\Scripts\activate
python create_location_tables.py
python seed_location_hierarchy.py
```

### Step 2: Restart Backend

Stop and restart the backend server to load new routes:
```bash
# Stop current server (Ctrl+C)
# Then restart:
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```

### Step 3: Verify Installation

Visit API docs: http://localhost:8000/docs

Check new endpoints:
- `/countries` - Country management
- `/provinces` - Province management
- `/companies` - Company management
- `/main-categories` - Category management
- `/asset-utils/preview-asset-id` - Preview asset ID
- `/asset-utils/generate-qr-code` - Generate QR code

## 📡 API Endpoints

### Countries

```http
GET    /countries              # List all countries
GET    /countries/{id}         # Get country by ID
POST   /countries              # Create country
PUT    /countries/{id}         # Update country
DELETE /countries/{id}         # Delete country (soft)
```

**Example Request**:
```json
POST /countries
{
  "countryname": "Lao PDR",
  "countrycode": "LA",
  "isactive": true
}
```

### Provinces

```http
GET    /provinces?country_id=1 # List provinces (filter by country)
GET    /provinces/{id}         # Get province by ID
POST   /provinces              # Create province
PUT    /provinces/{id}         # Update province
DELETE /provinces/{id}         # Delete province (soft)
```

**Example Request**:
```json
POST /provinces
{
  "provincename": "Vientiane Capital",
  "provincecode": "VTE",
  "countryid": 1,
  "isactive": true
}
```

### Companies

```http
GET    /companies?province_id=1 # List companies (filter by province)
GET    /companies/{id}          # Get company by ID
POST   /companies               # Create company
PUT    /companies/{id}          # Update company
DELETE /companies/{id}          # Delete company (soft)
```

**Example Request**:
```json
POST /companies
{
  "companyname": "AVIS Rent A Car",
  "companycode": "AVIS",
  "provinceid": 1,
  "address": "123 Main St",
  "phone": "+856-21-123456",
  "email": "info@avis.la",
  "isactive": true
}
```

### Main Categories

```http
GET    /main-categories        # List all categories
GET    /main-categories/{id}   # Get category by ID
POST   /main-categories        # Create category
PUT    /main-categories/{id}   # Update category
DELETE /main-categories/{id}   # Delete category (soft)
```

**Example Request**:
```json
POST /main-categories
{
  "categoryname": "Monitor",
  "categorycode": "M",
  "description": "Display monitors and screens",
  "isactive": true
}
```

### Asset ID Utilities

#### Preview Asset ID (No Increment)
```http
POST /asset-utils/preview-asset-id
{
  "main_category": "Monitor",
  "country_id": 1,
  "province_id": 2,
  "company_id": 1,
  "purchase_date": "2025-01-15"
}
```

**Response**:
```json
{
  "asset_id": "MLALPBAVIS25015",
  "components": {
    "category_code": "M",
    "country_code": "LA",
    "province_code": "LPB",
    "company_code": "AVIS",
    "year": 2025,
    "sequence": 15
  },
  "format": "CategoryCode(1) + CountryCode(2) + ProvinceCode(3) + CompanyCode(4) + Year(2) + Sequence(3)",
  "example": "MLALPBAVIS25015"
}
```

#### Generate Asset ID (Increments Sequence)
```http
POST /asset-utils/generate-asset-id
{
  "main_category": "Computer",
  "country_id": 1,
  "province_id": 1,
  "company_id": 1,
  "purchase_date": "2025-01-15"
}
```

**Response**:
```json
{
  "asset_id": "CLAVTEAVIS25001",
  "message": "Asset ID generated successfully"
}
```

#### Generate QR Code
```http
POST /asset-utils/generate-qr-code
{
  "asset_id": "MLALPBAVIS25015",
  "asset_name": "Dell Monitor 24inch"
}
```

**Response**:
```json
{
  "qr_code": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...",
  "asset_id": "MLALPBAVIS25015",
  "format": "base64 PNG image"
}
```

#### Get Next Sequence
```http
GET /asset-utils/next-sequence/{country_id}/{company_id}
```

**Response**:
```json
{
  "country_id": 1,
  "company_id": 1,
  "next_sequence": 16
}
```

#### Validate Asset ID
```http
GET /asset-utils/validate-asset-id/MLALPBAVIS25015
```

**Response**:
```json
{
  "valid": true,
  "asset_id": "MLALPBAVIS25015",
  "components": {
    "category_code": "M",
    "country_code": "LA",
    "province_code": "LPB",
    "company_code": "AVIS",
    "year": 2025,
    "sequence": 15
  }
}
```

## 🎨 Frontend Integration

### Example: Location Selector Component

```javascript
// LocationSelector.jsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';

function LocationSelector({ onLocationChange }) {
  const [countries, setCountries] = useState([]);
  const [provinces, setProvinces] = useState([]);
  const [companies, setCompanies] = useState([]);
  
  const [selectedCountry, setSelectedCountry] = useState('');
  const [selectedProvince, setSelectedProvince] = useState('');
  const [selectedCompany, setSelectedCompany] = useState('');

  useEffect(() => {
    // Load countries
    axios.get('http://localhost:8000/countries')
      .then(res => setCountries(res.data));
  }, []);

  useEffect(() => {
    if (selectedCountry) {
      // Load provinces for selected country
      axios.get(`http://localhost:8000/provinces?country_id=${selectedCountry}`)
        .then(res => setProvinces(res.data));
    }
  }, [selectedCountry]);

  useEffect(() => {
    if (selectedProvince) {
      // Load companies for selected province
      axios.get(`http://localhost:8000/companies?province_id=${selectedProvince}`)
        .then(res => setCompanies(res.data));
    }
  }, [selectedProvince]);

  const handleCompanyChange = (companyId) => {
    setSelectedCompany(companyId);
    onLocationChange({
      countryId: selectedCountry,
      provinceId: selectedProvince,
      companyId: companyId
    });
  };

  return (
    <div className="location-selector">
      <select onChange={(e) => setSelectedCountry(e.target.value)}>
        <option value="">Select Country</option>
        {countries.map(c => (
          <option key={c.countryid} value={c.countryid}>
            {c.countryname} ({c.countrycode})
          </option>
        ))}
      </select>

      <select onChange={(e) => setSelectedProvince(e.target.value)} disabled={!selectedCountry}>
        <option value="">Select Province</option>
        {provinces.map(p => (
          <option key={p.provinceid} value={p.provinceid}>
            {p.provincename} ({p.provincecode})
          </option>
        ))}
      </select>

      <select onChange={(e) => handleCompanyChange(e.target.value)} disabled={!selectedProvince}>
        <option value="">Select Company</option>
        {companies.map(c => (
          <option key={c.companyid} value={c.companyid}>
            {c.companyname} ({c.companycode})
          </option>
        ))}
      </select>
    </div>
  );
}

export default LocationSelector;
```

### Example: Asset ID Preview

```javascript
// AssetIDPreview.jsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';

function AssetIDPreview({ mainCategory, countryId, provinceId, companyId, purchaseDate }) {
  const [previewId, setPreviewId] = useState('');

  useEffect(() => {
    if (mainCategory && countryId && provinceId && companyId) {
      axios.post('http://localhost:8000/asset-utils/preview-asset-id', {
        main_category: mainCategory,
        country_id: countryId,
        province_id: provinceId,
        company_id: companyId,
        purchase_date: purchaseDate
      })
      .then(res => setPreviewId(res.data.asset_id))
      .catch(err => console.error(err));
    }
  }, [mainCategory, countryId, provinceId, companyId, purchaseDate]);

  return (
    <div className="asset-id-preview">
      <label>Asset ID Preview:</label>
      <input type="text" value={previewId} readOnly />
      <small>This ID will be generated when you save the asset</small>
    </div>
  );
}

export default AssetIDPreview;
```

### Example: QR Code Display

```javascript
// QRCodeDisplay.jsx
import React, { useState } from 'react';
import axios from 'axios';

function QRCodeDisplay({ assetId, assetName }) {
  const [qrCode, setQrCode] = useState('');

  const generateQR = () => {
    axios.post('http://localhost:8000/asset-utils/generate-qr-code', {
      asset_id: assetId,
      asset_name: assetName
    })
    .then(res => setQrCode(res.data.qr_code))
    .catch(err => console.error(err));
  };

  return (
    <div className="qr-code-display">
      <button onClick={generateQR}>Generate QR Code</button>
      {qrCode && (
        <div>
          <img src={qrCode} alt="Asset QR Code" />
          <button onClick={() => window.print()}>Print</button>
        </div>
      )}
    </div>
  );
}

export default QRCodeDisplay;
```

## 📊 Database Schema

### Countries Table
```sql
CREATE TABLE countries (
    countryid SERIAL PRIMARY KEY,
    countryname VARCHAR(100) NOT NULL,
    countrycode VARCHAR(2) UNIQUE NOT NULL,
    isactive BOOLEAN DEFAULT TRUE,
    createdat TIMESTAMP DEFAULT NOW(),
    updatedat TIMESTAMP DEFAULT NOW()
);
```

### Provinces Table
```sql
CREATE TABLE provinces (
    provinceid SERIAL PRIMARY KEY,
    provincename VARCHAR(100) NOT NULL,
    provincecode VARCHAR(3) NOT NULL,
    countryid INTEGER REFERENCES countries(countryid),
    isactive BOOLEAN DEFAULT TRUE,
    createdat TIMESTAMP DEFAULT NOW(),
    updatedat TIMESTAMP DEFAULT NOW()
);
```

### Companies Table
```sql
CREATE TABLE companies (
    companyid SERIAL PRIMARY KEY,
    companyname VARCHAR(200) NOT NULL,
    companycode VARCHAR(10) UNIQUE NOT NULL,
    provinceid INTEGER REFERENCES provinces(provinceid),
    address VARCHAR(500),
    phone VARCHAR(20),
    email VARCHAR(100),
    isactive BOOLEAN DEFAULT TRUE,
    createdat TIMESTAMP DEFAULT NOW(),
    updatedat TIMESTAMP DEFAULT NOW()
);
```

### Main Categories Table
```sql
CREATE TABLE maincategories (
    maincategoryid SERIAL PRIMARY KEY,
    categoryname VARCHAR(100) UNIQUE NOT NULL,
    categorycode VARCHAR(1) UNIQUE NOT NULL,
    description VARCHAR(500),
    isactive BOOLEAN DEFAULT TRUE,
    createdat TIMESTAMP DEFAULT NOW(),
    updatedat TIMESTAMP DEFAULT NOW()
);
```

### Asset Sequences Table
```sql
CREATE TABLE assetsequences (
    sequenceid SERIAL PRIMARY KEY,
    countryid INTEGER REFERENCES countries(countryid),
    companyid INTEGER REFERENCES companies(companyid),
    sequenceyear INTEGER NOT NULL,
    year INTEGER NOT NULL,
    lastsequence INTEGER DEFAULT 0,
    createdat TIMESTAMP DEFAULT NOW(),
    updatedat TIMESTAMP DEFAULT NOW(),
    UNIQUE(countryid, companyid, sequenceyear)
);
```

## 🔍 Testing

### Test Countries API
```bash
curl http://localhost:8000/countries
```

### Test Asset ID Preview
```bash
curl -X POST http://localhost:8000/asset-utils/preview-asset-id \
  -H "Content-Type: application/json" \
  -d '{
    "main_category": "Monitor",
    "country_id": 1,
    "province_id": 2,
    "company_id": 1
  }'
```

### Test QR Code Generation
```bash
curl -X POST http://localhost:8000/asset-utils/generate-qr-code \
  -H "Content-Type: application/json" \
  -d '{
    "asset_id": "MLALPBAVIS25015",
    "asset_name": "Dell Monitor"
  }'
```

## 📝 Next Steps

1. ✅ **Location Hierarchy** - Complete
2. ✅ **Asset ID Generation** - Complete
3. ✅ **QR Code Service** - Complete
4. 🔄 **Frontend Components** - In Progress
   - Create LocationSelector component
   - Add Asset ID preview to asset form
   - Add QR code display to asset detail page
5. ⏳ **Excel Import/Export** - Pending
6. ⏳ **Stock Count System** - Pending

## 🐛 Troubleshooting

### Tables not created
```bash
cd backend
venv\Scripts\activate
python create_location_tables.py
```

### No data in tables
```bash
cd backend
venv\Scripts\activate
python seed_location_hierarchy.py
```

### Routes not available
- Restart the backend server
- Check http://localhost:8000/docs for available endpoints

### Asset ID generation fails
- Ensure countries, provinces, companies, and main categories are seeded
- Check that the category name matches exactly (case-sensitive)

## 📚 References

- Backup Project: `Bakcup project/backend/src/services/assetIdGenerator.js`
- Integration Plan: `BACKUP-INTEGRATION-PLAN.md`
- Integration Summary: `INTEGRATION-SUMMARY.md`

---

**Status**: ✅ Phase 1 Complete  
**Last Updated**: May 5, 2026  
**Version**: 1.0.0
