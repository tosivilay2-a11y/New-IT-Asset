# Database Quick Reference

## Current Setup

### Database: SQLite
- **File:** `backend/assetdb.db`
- **Type:** File-based relational database
- **Status:** ✅ Active

### File Storage: Cloudflare R2
- **Bucket:** `uploadassetfile`
- **Type:** Cloud object storage
- **Status:** ✅ Active

## Key Tables

| Table | Purpose | Key Fields |
|-------|---------|-----------|
| assets | Asset records | assetid, assetcode, po_attachment_path |
| users | User accounts | userid, email, password_hash |
| asset_status | Status types | statusid, statusname |
| categories | Asset categories | categoryid, name |
| locations | Asset locations | id, name, companyid |
| companies | Companies | companyid, companyname |
| countries | Countries | countryid, countryname |
| provinces | Provinces | provinceid, provincename |
| departments | Departments | departmentid, departmentname |

## File Storage

### Local Uploads
```
backend/uploads/po_attachments/
├── COMPLAVTERMAL26036_2fd34292.pdf
├── MLAVTERMAL26037_500cca15.jpg
└── ...
```

### Cloud Storage (R2)
```
https://pub-1fbaa356c50a4981bd7a2077dce7da6c.r2.dev/po_attachments/
├── COMPLAVTERMAL26036_2fd34292.pdf
├── MLAVTERMAL26037_500cca15.jpg
└── ...
```

## Configuration

### .env File
```
DATABASE_URL=sqlite:///./assetdb.db
STORAGE_TYPE=r2
R2_BUCKET_NAME=uploadassetfile
R2_PUBLIC_URL=https://pub-1fbaa356c50a4981bd7a2077dce7da6c.r2.dev
```

## Common Operations

### Backup Database
```bash
# Windows
copy backend\assetdb.db backup-assetdb.db

# Linux/Mac
cp backend/assetdb.db backup-assetdb.db
```

### Restore Database
```bash
# Windows
copy backup-assetdb.db backend\assetdb.db

# Linux/Mac
cp backup-assetdb.db backend/assetdb.db
```

### Check Database Size
```bash
# Windows
dir backend\assetdb.db

# Linux/Mac
ls -lh backend/assetdb.db
```

## Asset Data Structure

### po_attachment_path Field
```json
["https://pub-xxx.r2.dev/po_attachments/file1.pdf", "https://pub-xxx.r2.dev/po_attachments/file2.jpg"]
```

### specifications Field
```json
{
  "cpu": "Intel Core i7",
  "ram": "16GB DDR4",
  "hdd": "512GB SSD",
  "wlan_mac": "XX:XX:XX:XX:XX:XX",
  "lan_mac": "XX:XX:XX:XX:XX:XX",
  "computer_name": "LAPTOP-001",
  "accessories": "Mouse, Keyboard"
}
```

## Database Limits

| Aspect | Limit | Notes |
|--------|-------|-------|
| File Size | 10 MB | Per file upload |
| Database Size | ~1 GB | SQLite practical limit |
| Concurrent Users | 5-10 | SQLite limitation |
| Records | 100,000+ | Depends on hardware |

## Troubleshooting

### Database Locked
**Error:** `database is locked`
**Solution:** Restart backend server

### File Not Found
**Error:** `file not found in R2`
**Solution:** Check R2 configuration and bucket name

### Connection Failed
**Error:** `cannot connect to database`
**Solution:** Check DATABASE_URL in .env

## Status Check

### Database Health
```bash
# Check if database file exists
ls -la backend/assetdb.db

# Check file size
du -h backend/assetdb.db

# Check R2 connectivity
# (Check backend logs for R2 errors)
```

## Upgrade Path

### To PostgreSQL
1. Install PostgreSQL
2. Update DATABASE_URL
3. Run migrations
4. Migrate data

### To MySQL
1. Install MySQL
2. Update DATABASE_URL
3. Run migrations
4. Migrate data

## Support

### Documentation
- `DATABASE-CONFIGURATION-SUMMARY.md` - Full details
- `BACKEND-RUNNING.md` - Backend setup
- `CLOUDFLARE-R2-SETUP.md` - R2 configuration

### Logs
- Backend logs: Check console output
- Database logs: SQLite doesn't have separate logs
- R2 logs: Check Cloudflare dashboard

---

**Quick Answer:** We use **SQLite** for the database and **Cloudflare R2** for file storage.
