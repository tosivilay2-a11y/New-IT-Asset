# ✅ Switch to it_asset_db - Complete!

## What's Been Updated

✅ **docker-compose.yml**
- Database: `assetdb` → `it_asset_db`
- Backend DATABASE_URL updated

✅ **Migration Scripts Created**
- `migrate-to-it-asset-db.bat` - One-click migration
- `backup-assetdb.bat` - Backup current data
- `restore-to-it-asset-db.bat` - Restore data to new database

✅ **Documentation**
- `MIGRATION-GUIDE.md` - Complete migration guide

---

## 🚀 Quick Start

### If you DON'T need to keep data from assetdb:

```bash
migrate-to-it-asset-db.bat
```

Done! Your system now uses `it_asset_db`.

---

### If you WANT to keep data from assetdb:

```bash
# 1. Backup
backup-assetdb.bat

# 2. Migrate
migrate-to-it-asset-db.bat

# 3. Restore (use the backup file name shown)
restore-to-it-asset-db.bat assetdb_backup_YYYYMMDD_HHMMSS.sql
```

---

## 🔍 Verify It Works

```bash
# Check database
docker exec -it asset-db psql -U postgres -c "\l" | findstr it_asset_db

# Check services
docker-compose ps

# Test API
curl http://localhost:8000/

# Open frontend
start http://localhost:3000
```

---

## 📊 System Overview

**Before:**
- Database: `assetdb`
- Backend: Python/FastAPI → `assetdb`
- Frontend: React → Backend API

**After:**
- Database: `it_asset_db`
- Backend: Python/FastAPI → `it_asset_db`
- Frontend: React → Backend API

Everything else stays the same!

---

## 🔐 Default Users

- admin@example.com / admin123
- staff@example.com / staff123

---

## 📚 Documentation

- **MIGRATION-GUIDE.md** - Detailed migration steps
- **README.md** - Project overview
- **docker-compose.yml** - Updated configuration

---

**Ready? Run `migrate-to-it-asset-db.bat` now!** 🎉
