# 🚀 Setup Instructions - IT Asset Management System

## Current Situation

✅ You have PostgreSQL running in Docker (container: `asset-db`)
✅ It currently has database: `assetdb` (for Python/FastAPI system)
❌ You need to create: `it_asset_db` (for Node.js IT Asset system)

---

## Quick Setup (3 Commands)

### 1️⃣ Create the Database
```bash
cd it-asset-system
create-db-simple.bat
```

### 2️⃣ Setup Backend
```bash
cd backend
setup-complete.bat
```

### 3️⃣ Start Server
The server will start automatically after setup, or run:
```bash
npm run dev
```

---

## What Each Step Does

### Step 1: Create Database
Creates `it_asset_db` in your existing PostgreSQL container.

**What happens:**
- Connects to `asset-db` container
- Runs: `CREATE DATABASE it_asset_db;`
- Both `assetdb` and `it_asset_db` will exist

### Step 2: Setup Backend
Installs dependencies, creates tables, seeds data.

**What happens:**
- `npm install` - Installs all packages
- `npm run db:setup` - Creates 30 tables
- `npm run db:seed` - Adds initial data (users, categories, etc.)

### Step 3: Start Server
Starts the Express server on port 5000.

**What happens:**
- Connects to PostgreSQL
- Starts API server
- Ready to accept requests

---

## Verify Everything Works

### Check Database Exists
```bash
docker exec -it asset-db psql -U postgres -c "\l" | findstr it_asset_db
```

### Check Tables Created
```bash
docker exec -it asset-db psql -U postgres -d it_asset_db -c "\dt"
```
Should show 30 tables.

### Test API
```bash
curl http://localhost:5000/health
```
Should return: `{"success":true,"message":"Server is running"}`

### Test Login
```bash
curl -X POST http://localhost:5000/api/auth/login -H "Content-Type: application/json" -d "{\"email\":\"admin@example.com\",\"password\":\"admin123\"}"
```
Should return a JWT token.

---

## Default Users After Setup

| Email                  | Password    | Role    |
|------------------------|-------------|---------|
| admin@example.com      | admin123    | Admin   |
| manager@example.com    | manager123  | Manager |
| user@example.com       | user123     | User    |

---

## Troubleshooting

### "database already exists"
✅ This is OK! It means the database was already created. Continue with step 2.

### "container not found"
❌ Make sure PostgreSQL is running:
```bash
docker ps | findstr asset-db
```
If not running:
```bash
docker-compose up -d
```

### "connection refused"
❌ Check if PostgreSQL is listening:
```bash
docker exec -it asset-db psql -U postgres -c "SELECT version();"
```

### "module not found"
❌ Install dependencies:
```bash
cd backend
npm install
```

---

## File Structure

```
it-asset-system/
├── create-db-simple.bat       ← Run this first
├── DATABASE-INFO.md           ← Database explanation
├── SETUP-INSTRUCTIONS.md      ← This file
└── backend/
    ├── setup-complete.bat     ← Run this second
    ├── start.bat             ← Run this third (or automatic)
    ├── .env                  ← Already configured
    └── scripts/
        ├── schema-postgres.sql   ← 30 tables
        ├── setupDatabase.js      ← Creates tables
        └── seedData.js          ← Adds initial data
```

---

## Summary

1. **Create database**: `create-db-simple.bat`
2. **Setup backend**: `cd backend && setup-complete.bat`
3. **Done!** Server runs on http://localhost:5000

Your Python system (`assetdb`) and Node.js system (`it_asset_db`) will both work on the same PostgreSQL server! 🎉
