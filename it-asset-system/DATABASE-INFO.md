# Database Configuration Info

## Current Setup

Your PostgreSQL container is named `asset-db` and currently has the database `assetdb` (used by the Python/FastAPI system).

The IT Asset Management system needs a separate database called `it_asset_db`.

## Two Databases in One PostgreSQL Instance

```
PostgreSQL Container (asset-db)
├── assetdb          ← Python/FastAPI system (port 8000)
└── it_asset_db      ← Node.js IT Asset system (port 5000)
```

Both systems can run simultaneously on the same PostgreSQL server!

---

## How to Create the New Database

### Option 1: Using the Script (Recommended)
```bash
cd it-asset-system
create-database-docker.bat
```

### Option 2: Manual Command
```bash
docker exec -it asset-db psql -U postgres -c "CREATE DATABASE it_asset_db;"
```

### Option 3: Using psql Interactive
```bash
docker exec -it asset-db psql -U postgres
```
Then in psql:
```sql
CREATE DATABASE it_asset_db;
\l
\q
```

---

## Verify Both Databases Exist

```bash
docker exec -it asset-db psql -U postgres -c "\l"
```

You should see:
- `assetdb` (existing Python system)
- `it_asset_db` (new Node.js system)
- `postgres` (default system database)

---

## Connection Details

### Python/FastAPI System (Existing)
- Database: `assetdb`
- Port: 8000
- URL: `postgresql://postgres:postgres@localhost:5432/assetdb`

### Node.js IT Asset System (New)
- Database: `it_asset_db`
- Port: 5000
- URL: `postgresql://postgres:postgres@localhost:5432/it_asset_db`

---

## Next Steps

1. ✅ Create `it_asset_db` database
2. ✅ Run backend setup: `cd backend && setup-complete.bat`
3. ✅ Start server: `npm run dev`

Both systems will work independently on the same PostgreSQL server!
