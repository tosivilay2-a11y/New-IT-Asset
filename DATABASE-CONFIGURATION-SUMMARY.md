# Database Configuration Summary

## Current Database

### Primary Database: **SQLite**
- **Type:** SQLite (file-based relational database)
- **Location:** `backend/assetdb.db`
- **Connection String:** `sqlite:///./assetdb.db`
- **Status:** ✅ Active and Running

### File Storage: **Cloudflare R2**
- **Type:** Cloud object storage (S3-compatible)
- **Bucket:** `uploadassetfile`
- **Public URL:** `https://pub-1fbaa356c50a4981bd7a2077dce7da6c.r2.dev`
- **Status:** ✅ Configured and Active

## Configuration Details

### Backend Environment (.env)
```
DATABASE_URL=sqlite:///./assetdb.db
STORAGE_TYPE=r2
R2_BUCKET_NAME=uploadassetfile
R2_ENDPOINT_URL=https://e100a0cfe124fdf7d88b279b7be79a95.r2.cloudflarestorage.com
R2_PUBLIC_URL=https://pub-1fbaa356c50a4981bd7a2077dce7da6c.r2.dev
```

### Database Engine
- **ORM:** SQLAlchemy
- **Driver:** SQLite (built-in)
- **Session Management:** SQLAlchemy SessionLocal

## Database Structure

### Main Tables
1. **assets** - Asset records
   - assetid (PK)
   - assetcode
   - assetname
   - po_attachment_path (JSON array of file URLs)
   - specifications (JSON)
   - And 30+ other fields

2. **users** - User accounts
   - userid (PK)
   - email
   - password_hash
   - firstname, lastname

3. **asset_status** - Asset status types
   - statusid (PK)
   - statusname

4. **categories** - Asset categories
   - categoryid (PK)
   - name

5. **main_category** - Main categories
   - maincategoryid (PK)
   - categoryname

6. **locations** - Asset locations
   - id (PK)
   - name
   - companyid (FK)

7. **companies** - Companies
   - companyid (PK)
   - companyname

8. **countries** - Countries
   - countryid (PK)
   - countryname

9. **provinces** - Provinces/States
   - provinceid (PK)
   - provincename
   - countryid (FK)

10. **departments** - Departments
    - departmentid (PK)
    - departmentname

11. **asset_transfers** - Asset transfer history
    - transferid (PK)
    - assetid (FK)
    - from_location
    - to_location

12. **audits** - Audit logs
    - auditid (PK)
    - action
    - timestamp

13. **inventory** - Inventory tracking
    - inventoryid (PK)
    - assetid (FK)
    - quantity

14. **system_config** - System configuration
    - configid (PK)
    - key
    - value

## File Storage

### Local Files (Uploads)
- **Location:** `backend/uploads/po_attachments/`
- **Files:** PO attachment files
- **Format:** `{ASSETCODE}_{HASH}.{EXT}`
- **Example:** `COMPLAVTERMAL26036_2fd34292.pdf`

### Cloud Storage (R2)
- **Bucket:** `uploadassetfile`
- **Path:** `po_attachments/{filename}`
- **Access:** Public via R2 public URL
- **Status:** ✅ Active

## Data Flow

### Asset Creation with Files
```
Frontend
  ↓
Create Asset (POST /assets/)
  ↓
SQLite: Insert asset record
  ↓
Upload Files (PUT /assets/{id}/with-file)
  ↓
R2: Upload file
  ↓
SQLite: Update po_attachment_path with file URL
  ↓
Response: Asset with file URLs
```

### Asset Update with Files
```
Frontend
  ↓
Update Asset (PUT /assets/{id}/with-file)
  ↓
SQLite: Update asset record
  ↓
R2: Upload new file (if provided)
  ↓
SQLite: Update po_attachment_path (append new file)
  ↓
Response: Updated asset
```

## Database Features

### Supported Operations
- ✅ Create assets
- ✅ Read assets
- ✅ Update assets
- ✅ Delete assets (soft delete)
- ✅ Query with filters
- ✅ Relationships (foreign keys)
- ✅ JSON fields (specifications, po_attachment_path)

### Data Integrity
- ✅ Foreign key constraints
- ✅ NOT NULL constraints
- ✅ Unique constraints
- ✅ Data type validation

### Performance
- ✅ Indexed primary keys
- ✅ Efficient queries
- ✅ Connection pooling
- ✅ Transaction support

## Backup & Recovery

### Database File
- **Location:** `backend/assetdb.db`
- **Size:** ~5-10 MB (typical)
- **Backup:** Copy file to safe location
- **Restore:** Replace file and restart backend

### Backup Script
```bash
# Windows
copy backend\assetdb.db backup-assetdb-$(date).db

# Linux/Mac
cp backend/assetdb.db backup-assetdb-$(date +%Y%m%d).db
```

## Migration & Upgrade

### Alembic Migrations
- **Location:** `backend/alembic/versions/`
- **Current Migrations:**
  1. `001_add_po_fields_to_assets.py` - Added PO fields
  2. `002_add_cost_center_field.py` - Added cost center

### Running Migrations
```bash
cd backend
alembic upgrade head
```

## Advantages of Current Setup

### SQLite
- ✅ No server setup needed
- ✅ File-based (easy backup)
- ✅ Good for development
- ✅ Sufficient for small-medium deployments
- ✅ ACID compliant
- ✅ Full SQL support

### Cloudflare R2
- ✅ Reliable cloud storage
- ✅ S3-compatible API
- ✅ Public URL access
- ✅ Cost-effective
- ✅ Automatic backups
- ✅ Global CDN

## Limitations & Considerations

### SQLite Limitations
- Single file database
- Limited concurrent writes
- Not ideal for very large datasets (100GB+)
- No built-in replication

### When to Upgrade
- If you need: PostgreSQL, MySQL, SQL Server
- If you need: High availability, replication
- If you need: Advanced analytics
- If you need: Multi-server deployment

## Migration Path (If Needed)

### To PostgreSQL
1. Install PostgreSQL
2. Update DATABASE_URL in .env
3. Run migrations
4. Migrate data using tools

### To MySQL
1. Install MySQL
2. Update DATABASE_URL in .env
3. Run migrations
4. Migrate data using tools

### To SQL Server
1. Install SQL Server
2. Update DATABASE_URL in .env
3. Run migrations
4. Migrate data using tools

## Current Status

| Component | Status | Details |
|-----------|--------|---------|
| SQLite Database | ✅ Active | `backend/assetdb.db` |
| Cloudflare R2 | ✅ Active | File storage configured |
| Migrations | ✅ Applied | 2 migrations completed |
| Backups | ⚠️ Manual | Need to set up automated backups |
| Replication | ❌ Not configured | Single instance only |
| Monitoring | ⚠️ Basic | Need to add monitoring |

## Recommendations

### Short Term
- ✅ Current setup is good for development/testing
- ✅ Works well for small deployments
- ✅ Easy to backup and restore

### Medium Term
- 📋 Set up automated backups
- 📋 Add database monitoring
- 📋 Document backup procedures
- 📋 Test restore procedures

### Long Term
- 📋 Consider PostgreSQL for production
- 📋 Set up replication/failover
- 📋 Implement automated backups
- 📋 Add monitoring and alerts

## Quick Reference

### Database File
```
Location: backend/assetdb.db
Type: SQLite
Size: ~5-10 MB
Backup: Copy file
```

### Connection String
```
sqlite:///./assetdb.db
```

### File Storage
```
Type: Cloudflare R2
Bucket: uploadassetfile
Public URL: https://pub-1fbaa356c50a4981bd7a2077dce7da6c.r2.dev
```

### Tables
```
14 main tables
30+ asset fields
JSON support for complex data
Foreign key relationships
```

---

**Last Updated:** May 8, 2026
**Status:** Production Ready (for small-medium deployments)
