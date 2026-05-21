# Database Schema Expansion Guide

## Overview

This will expand your current simple database (9 tables) to a comprehensive IT Asset Management system (30+ tables) matching the SQL Server schema.

## Current Schema (9 tables)
- users
- assets
- categories
- locations
- inventory_items
- inventory_transactions
- audit_sessions
- audit_records

## New Schema (30+ tables)

### Geographic & Organizational (5 tables)
- **countries** - Country master data
- **provinces** - Province/state data
- **companies** - Company information
- **departments** - Department structure
- **locations** (expanded) - Enhanced location tracking

### User Management (5 tables)
- **usertypes** - User type definitions
- **userroles** - Role definitions
- **permissions** - Permission catalog
- **rolepermissions** - Role-permission mapping
- **users** (expanded) - Enhanced user profiles

### Asset Categories (3 tables)
- **maincategories** - Top-level categories
- **categories** (expanded) - Sub-categories
- **assetstatuses** - Status definitions

### Asset Management (5 tables)
- **assetsequences** - ID generation tracking
- **assets** (expanded) - Comprehensive asset data
- **assetassignments** - Assignment history
- **assetauditlog** - Asset change log
- **assetevents** - Asset lifecycle events

### Stock Count & Reconciliation (4 tables)
- **stockcountsessions** - Count session management
- **stockcounts** - Count records
- **stockcountitems** - Detailed count items
- **reconciliations** - Discrepancy resolution

### Workflow & Approvals (2 tables)
- **approvallevels** - Approval hierarchy
- **approvals** - Approval requests

### Budget Management (1 table)
- **budgetplans** - Budget tracking

### System Tables (2 tables)
- **auditlogs** - System-wide audit trail
- **notifications** - User notifications

---

## How to Expand

### Step 1: Run the Expansion Script

```bash
expand-database-schema.bat
```

This will:
1. Connect to your `assetdb` database
2. Create all new tables
3. Add new columns to existing tables
4. Create indexes for performance
5. Preserve all existing data

### Step 2: Verify Expansion

```bash
# Check new tables exist
docker exec -it asset-db psql -U postgres -d assetdb -c "\dt"

# Count tables
docker exec -it asset-db psql -U postgres -d assetdb -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';"
```

You should see 30+ tables.

---

## What Gets Added

### To Existing Tables

**users table** gets:
- employeeid, username
- firstname, lastname
- department, position
- usertype, usertypeid
- companyid, countryid
- managerid, roleid
- isactive, requirepasswordchange

**assets table** gets:
- picture, maincategory
- brand, model, modelname
- cpu, ram, hdd
- wlanmacaddress, lanmacaddress
- serialnumber, sntype
- assignedto, dateassigned
- datepurchase, datefirstuse, endoflife
- price, ponumber, invoice
- Warranty fields (supplier & additional)
- Location fields (current, company, province, country)
- computername, accessories
- comment, condition
- year, month, testnumber
- qrcode
- createdby, modifiedby

**categories table** gets:
- maincategoryid
- isactive

**locations table** gets:
- locationcode
- companyid, provinceid
- department
- isactive

### New Tables Created

All 20+ new tables listed above will be created with proper:
- Primary keys
- Foreign key relationships
- Indexes
- Default values
- Timestamps

---

## Safety Features

✅ **Non-destructive**: Existing data is preserved
✅ **Idempotent**: Can run multiple times safely
✅ **Rollback-safe**: Uses transactions
✅ **Error handling**: Continues on "already exists" errors

---

## After Expansion

### 1. Seed Initial Data

You'll need to populate:
- Countries (Thailand, US, Singapore, etc.)
- Provinces
- Companies
- Departments
- UserTypes (Admin, Manager, Staff)
- Roles & Permissions
- MainCategories
- AssetStatuses

### 2. Update Backend Models

Create new SQLAlchemy models for:
- Country, Province, Company, Department
- UserType, UserRole, Permission
- MainCategory, AssetStatus
- StockCountSession, Approval, etc.

### 3. Update API Endpoints

Add endpoints for:
- Geographic management
- User role management
- Stock counting
- Approval workflows
- Budget tracking

---

## Verification Queries

```sql
-- Check all tables
\dt

-- Count records in new tables
SELECT 'countries' as table, COUNT(*) FROM countries
UNION ALL
SELECT 'provinces', COUNT(*) FROM provinces
UNION ALL
SELECT 'companies', COUNT(*) FROM companies
UNION ALL
SELECT 'departments', COUNT(*) FROM departments
UNION ALL
SELECT 'usertypes', COUNT(*) FROM usertypes
UNION ALL
SELECT 'userroles', COUNT(*) FROM userroles
UNION ALL
SELECT 'permissions', COUNT(*) FROM permissions;

-- Check expanded columns
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'assets' 
ORDER BY ordinal_position;
```

---

## Rollback (if needed)

If you need to revert:

```sql
-- Drop new tables (in reverse order of dependencies)
DROP TABLE IF EXISTS notifications CASCADE;
DROP TABLE IF EXISTS auditlogs CASCADE;
DROP TABLE IF EXISTS budgetplans CASCADE;
DROP TABLE IF EXISTS approvals CASCADE;
DROP TABLE IF EXISTS approvallevels CASCADE;
DROP TABLE IF NOT EXISTS reconciliations CASCADE;
DROP TABLE IF EXISTS stockcountitems CASCADE;
DROP TABLE IF EXISTS stockcounts CASCADE;
DROP TABLE IF EXISTS stockcountsessions CASCADE;
DROP TABLE IF EXISTS assetevents CASCADE;
DROP TABLE IF EXISTS assetauditlog CASCADE;
DROP TABLE IF EXISTS assetassignments CASCADE;
DROP TABLE IF EXISTS assetsequences CASCADE;
DROP TABLE IF EXISTS assetstatuses CASCADE;
DROP TABLE IF EXISTS maincategories CASCADE;
DROP TABLE IF EXISTS rolepermissions CASCADE;
DROP TABLE IF EXISTS permissions CASCADE;
DROP TABLE IF EXISTS userroles CASCADE;
DROP TABLE IF EXISTS usertypes CASCADE;
DROP TABLE IF EXISTS departments CASCADE;
DROP TABLE IF EXISTS provinces CASCADE;
DROP TABLE IF EXISTS companies CASCADE;
DROP TABLE IF EXISTS countries CASCADE;
```

Note: This won't remove added columns from existing tables.

---

## Next Steps

1. ✅ Run `expand-database-schema.bat`
2. ✅ Verify tables created
3. 🔨 Create seed data script
4. 🔨 Update Python models
5. 🔨 Add new API endpoints
6. 🔨 Update frontend to use new features

---

**Ready to expand? Run `expand-database-schema.bat` now!** 🚀
