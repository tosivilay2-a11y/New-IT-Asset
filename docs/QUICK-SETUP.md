# Quick Setup Guide - Enhanced Asset Management

## Step 1: Expand Database Schema

Run this to add all 30+ tables:

```bash
expand-database-schema.bat
```

This adds:
- Geographic tables (Countries, Provinces, Companies)
- Enhanced user management (UserTypes, Roles, Permissions)
- Asset management tables (Sequences, Assignments, Events)
- System configuration tables

## Step 2: Restart Backend

```bash
docker-compose restart backend
```

## Step 3: Seed Initial Data

Create a seed script or manually add:

### Countries
```sql
INSERT INTO countries (countryname, countrycode) VALUES
('Thailand', 'TH'),
('United States', 'US'),
('Singapore', 'SG');
```

### Companies
```sql
INSERT INTO companies (companyname, companycode) VALUES
('ABC Corporation', 'ABC'),
('XYZ Limited', 'XYZ');
```

### Main Categories
```sql
INSERT INTO maincategories (categoryname, categorycode) VALUES
('Computer', 'COMP'),
('Printer', 'PRNT'),
('Network Equipment', 'NETW'),
('Furniture', 'FURN');
```

## Step 4: Test API

### Access API Documentation
```
http://localhost:8000/docs
```

### Test Asset Creation
```bash
curl -X POST http://localhost:8000/api/assets/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Dell Laptop",
    "category_code": "COMP",
    "country_id": 1,
    "province_code": "BKK",
    "company_id": 1,
    "country_code": "TH",
    "company_code": "ABC",
    "brand": "Dell",
    "model": "Latitude 5420"
  }'
```

### Test Asset ID Preview
```bash
curl -X POST http://localhost:8000/api/assets/preview-id \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "category_code": "COMP",
    "country_code": "TH",
    "province_code": "BKK",
    "company_code": "ABC"
  }'
```

## Step 5: Configure System (Admin)

### Set Asset ID Format
```bash
curl -X POST http://localhost:8000/api/admin/config \
  -H "Authorization: Bearer ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "configkey": "asset_id_format",
    "configvalue": "{\"pattern\": \"{category}-{country}-{province}-{company}-{year}-{sequence}\", \"sequence_length\": 4}",
    "category": "asset_management",
    "datatype": "json"
  }'
```

## All Features Ready!

✅ Asset CRUD with auto-generated IDs
✅ QR Code generation
✅ Asset lifecycle management
✅ Admin configuration
✅ System statistics

**API Docs:** http://localhost:8000/docs
