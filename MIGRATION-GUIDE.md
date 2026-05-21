# Migration Guide: assetdb → it_asset_db

## What Changed

✅ **docker-compose.yml** updated:
- Database name: `assetdb` → `it_asset_db`
- Backend DATABASE_URL: `postgresql://postgres:postgres@db:5432/it_asset_db`

## Migration Options

### Option 1: Fresh Start (Recommended if no important data)

Simply recreate everything with the new database:

```bash
migrate-to-it-asset-db.bat
```

This will:
1. Stop containers
2. Create `it_asset_db` database
3. Run migrations (create tables)
4. Seed initial data
5. Start all services

**Result:** Fresh database with default users.

---

### Option 2: Backup and Restore (Keep existing data)

If you have data in `assetdb` that you want to keep:

#### Step 1: Backup Current Database
```bash
backup-assetdb.bat
```

This creates a file like: `assetdb_backup_20260505_143022.sql`

#### Step 2: Migrate to New Database
```bash
migrate-to-it-asset-db.bat
```

#### Step 3: Restore Your Data
```bash
restore-to-it-asset-db.bat assetdb_backup_20260505_143022.sql
```

**Result:** `it_asset_db` contains all your data from `assetdb`.

---

### Option 3: Manual Migration

If you prefer manual control:

```bash
# 1. Stop containers
docker-compose down

# 2. Start database only
docker-compose up -d db

# 3. Backup old database (optional)
docker exec -it asset-db pg_dump -U postgres assetdb > backup.sql

# 4. Create new database
docker exec -it asset-db psql -U postgres -c "CREATE DATABASE it_asset_db;"

# 5. Restore data (optional)
docker exec -i asset-db psql -U postgres it_asset_db < backup.sql

# 6. Start all services
docker-compose up -d

# 7. Check status
docker-compose ps
```

---

## Verification

### Check Database Exists
```bash
docker exec -it asset-db psql -U postgres -c "\l" | findstr it_asset_db
```

### Check Tables
```bash
docker exec -it asset-db psql -U postgres -d it_asset_db -c "\dt"
```

### Check Users
```bash
docker exec -it asset-db psql -U postgres -d it_asset_db -c "SELECT id, email, full_name, is_active FROM users;"
```

### Test API
```bash
# Health check
curl http://localhost:8000/

# API docs
start http://localhost:8000/docs

# Login
curl -X POST http://localhost:8000/api/auth/login ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"admin@example.com\",\"password\":\"admin123\"}"
```

### Test Frontend
```bash
start http://localhost:3000
```

---

## Default Users

After fresh migration:
- **Admin**: admin@example.com / admin123
- **Staff**: staff@example.com / staff123

---

## Troubleshooting

### Database Connection Error

**Check if database exists:**
```bash
docker exec -it asset-db psql -U postgres -c "\l"
```

**Create it manually:**
```bash
docker exec -it asset-db psql -U postgres -c "CREATE DATABASE it_asset_db;"
```

### Backend Won't Start

**Check logs:**
```bash
docker-compose logs backend
```

**Common issues:**
- Database not ready: Wait a few seconds and restart
- Migration failed: Check if tables exist
- Connection refused: Verify DATABASE_URL in docker-compose.yml

### Tables Don't Exist

**Run migrations manually:**
```bash
docker-compose exec backend alembic upgrade head
```

Or recreate database:
```bash
docker-compose down -v
docker-compose up -d
```

### Frontend Can't Connect

**Check backend is running:**
```bash
curl http://localhost:8000/
```

**Check frontend environment:**
```bash
docker-compose exec frontend env | findstr API_URL
```

Should show: `REACT_APP_API_URL=http://localhost:8000`

---

## Rollback to assetdb

If you need to go back:

1. Edit `docker-compose.yml`:
   ```yaml
   POSTGRES_DB: assetdb
   DATABASE_URL: postgresql://postgres:postgres@db:5432/assetdb
   ```

2. Restart:
   ```bash
   docker-compose restart
   ```

---

## Quick Reference

```bash
# Migrate (fresh start)
migrate-to-it-asset-db.bat

# Backup current data
backup-assetdb.bat

# Restore backup
restore-to-it-asset-db.bat backup_file.sql

# Check status
docker-compose ps

# View logs
docker-compose logs -f

# Restart
docker-compose restart

# Reset everything
docker-compose down -v
docker-compose up -d
```

---

## What's Next?

After successful migration:

1. ✅ Test login at http://localhost:3000
2. ✅ Verify all features work
3. ✅ Check API docs at http://localhost:8000/docs
4. ✅ Create new users if needed
5. ✅ Import/create assets

---

**Ready to migrate? Run `migrate-to-it-asset-db.bat`** 🚀
