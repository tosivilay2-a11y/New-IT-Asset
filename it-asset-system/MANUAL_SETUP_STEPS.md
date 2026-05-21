# Manual Setup Steps

Follow these steps to set up the IT Asset Management System with PostgreSQL.

## Step 1: Start PostgreSQL

### Option A: Using Docker (Recommended)
Open Command Prompt and run:
```bash
docker-compose up -d db
```

### Option B: Check if already running
```bash
docker ps
```

Look for a container with PostgreSQL (usually named `asset-db` or contains `postgres`).

## Step 2: Create Database

Open Command Prompt and run:
```bash
docker exec -it asset-db psql -U postgres -c "CREATE DATABASE it_asset_db;"
```

Or if your container has a different name:
```bash
docker ps
# Find the PostgreSQL container name, then:
docker exec -it <container-name> psql -U postgres -c "CREATE DATABASE it_asset_db;"
```

## Step 3: Apply Schema

### Option A: Using the SQL file directly
```bash
docker exec -i asset-db psql -U postgres -d it_asset_db < backend/scripts/schema-postgres.sql
```

### Option B: Using psql interactive
```bash
docker exec -it asset-db psql -U postgres -d it_asset_db
```

Then paste the contents of `backend/scripts/schema-postgres.sql` or run:
```sql
\i /path/to/schema-postgres.sql
```

### Option C: Using pgAdmin or DBeaver
1. Connect to PostgreSQL (localhost:5432, user: postgres, password: postgres)
2. Create database `it_asset_db`
3. Open and execute `backend/scripts/schema-postgres.sql`

## Step 4: Install Node.js Dependencies

```bash
cd it-asset-system/backend
npm install
```

## Step 5: Run Database Setup Script

```bash
npm run db:setup
```

This will create all 30 tables.

## Step 6: Seed Initial Data

```bash
npm run db:seed
```

This will create:
- 3 default users (admin, manager, user)
- Countries, provinces, companies
- Locations and departments
- Roles and permissions
- Asset categories and statuses

## Step 7: Start the Backend

```bash
npm run dev
```

The server will start at `http://localhost:5000`

## Verify Setup

### Check Database
```bash
docker exec -it asset-db psql -U postgres -d it_asset_db -c "\dt"
```

You should see 30 tables.

### Check Users
```bash
docker exec -it asset-db psql -U postgres -d it_asset_db -c "SELECT username, email FROM users;"
```

You should see:
- admin
- manager
- user

### Test API
Open browser or use curl:
```bash
curl http://localhost:5000/health
```

Should return:
```json
{
  "success": true,
  "message": "Server is running"
}
```

## Troubleshooting

### Error: "database it_asset_db already exists"
That's fine! Continue to Step 5.

### Error: "relation already exists"
Tables are already created. Skip to Step 6 (seed data).

### Error: "Cannot find module 'pg'"
Run: `npm install` in the backend directory.

### Error: "Connection refused"
PostgreSQL is not running. Start it with:
```bash
docker-compose up -d db
```

### Error: "password authentication failed"
Check your `.env` file has correct credentials:
```
DB_HOST=localhost
DB_PORT=5432
DB_DATABASE=it_asset_db
DB_USER=postgres
DB_PASSWORD=postgres
```

## Quick Commands Reference

```bash
# Start PostgreSQL
docker-compose up -d db

# Check if running
docker ps | grep postgres

# Create database
docker exec -it asset-db psql -U postgres -c "CREATE DATABASE it_asset_db;"

# List databases
docker exec -it asset-db psql -U postgres -c "\l"

# Connect to database
docker exec -it asset-db psql -U postgres -d it_asset_db

# List tables
docker exec -it asset-db psql -U postgres -d it_asset_db -c "\dt"

# Count tables
docker exec -it asset-db psql -U postgres -d it_asset_db -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';"

# View users
docker exec -it asset-db psql -U postgres -d it_asset_db -c "SELECT * FROM users;"

# Drop database (if you need to start over)
docker exec -it asset-db psql -U postgres -c "DROP DATABASE IF EXISTS it_asset_db;"
```

## Alternative: One-Line Setup

If you want to run everything at once:

```bash
cd it-asset-system/backend && npm install && npm run db:setup && npm run db:seed && npm run dev
```

## Next Steps

After setup is complete:
1. ✅ PostgreSQL running
2. ✅ Database created
3. ✅ Tables created (30 tables)
4. ✅ Data seeded
5. ✅ Backend running
6. 🔄 Test API endpoints
7. 🔄 Build frontend

See `TESTING_GUIDE.md` for API testing instructions.
