# PostgreSQL Setup Guide

Quick guide to set up the IT Asset Management System with PostgreSQL.

## Prerequisites

You already have PostgreSQL running in Docker from your existing setup!

## Quick Start

### 1. Start PostgreSQL (if not running)

```bash
docker-compose up -d db
```

This starts PostgreSQL on port 5432 with:
- Database: postgres (we'll create it_asset_db)
- User: postgres
- Password: postgres

### 2. Install Dependencies

```bash
cd it-asset-system/backend
npm install
```

### 3. Create Database and Tables

```bash
npm run db:setup
```

This will:
- Create all 30 tables
- Set up indexes
- Configure relationships

### 4. Seed Initial Data

```bash
npm run db:seed
```

This will create:
- Default users (admin, manager, user)
- Countries, provinces, companies
- Locations and departments
- Roles and permissions
- Asset categories and statuses

### 5. Start the Backend

```bash
npm run dev
```

Server will run at: `http://localhost:5000`

## Default Login Credentials

| Role    | Email                  | Password    |
|---------|------------------------|-------------|
| Admin   | admin@example.com      | admin123    |
| Manager | manager@example.com    | manager123  |
| User    | user@example.com       | user123     |

## Database Schema

The system uses **30 tables** organized into 8 categories:

### 1. Geographic & Organizational (5 tables)
- Countries
- Provinces  
- Companies
- Locations
- Departments

### 2. User Management (6 tables)
- UserTypes
- Users
- UserRoles
- Permissions
- RolePermissions

### 3. Asset Categories (3 tables)
- MainCategories
- Categories
- AssetStatuses

### 4. Asset Management (5 tables)
- AssetSequences
- Assets
- AssetAssignments
- AssetAuditLog
- AssetEvents

### 5. Stock Count & Reconciliation (4 tables)
- StockCountSessions
- StockCounts
- StockCountItems
- Reconciliations

### 6. Workflow & Approvals (2 tables)
- ApprovalLevels
- Approvals

### 7. Budget Management (1 table)
- BudgetPlans

### 8. System Tables (2 tables)
- AuditLogs
- Notifications

## Configuration

The `.env` file is already configured:

```env
# Database Configuration (PostgreSQL)
DB_HOST=localhost
DB_PORT=5432
DB_DATABASE=it_asset_db
DB_USER=postgres
DB_PASSWORD=postgres

# JWT Configuration
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production-12345
JWT_EXPIRES_IN=24h

# Server Configuration
PORT=5000
NODE_ENV=development
```

## Verify Setup

### Check Database Connection

```bash
docker exec -it asset-db psql -U postgres -c "\l"
```

You should see `it_asset_db` in the list.

### Check Tables

```bash
docker exec -it asset-db psql -U postgres -d it_asset_db -c "\dt"
```

You should see 30 tables.

### Check Users

```bash
docker exec -it asset-db psql -U postgres -d it_asset_db -c "SELECT username, email FROM users;"
```

You should see admin, manager, and user.

## Troubleshooting

### Error: "database it_asset_db does not exist"

Create it manually:
```bash
docker exec -it asset-db psql -U postgres -c "CREATE DATABASE it_asset_db;"
```

Then run `npm run db:setup` again.

### Error: "Connection refused"

Make sure PostgreSQL is running:
```bash
docker ps | grep postgres
```

If not running:
```bash
docker-compose up -d db
```

### Error: "permission denied"

Check PostgreSQL logs:
```bash
docker logs asset-db
```

### Reset Database

If you need to start fresh:
```bash
docker exec -it asset-db psql -U postgres -c "DROP DATABASE IF EXISTS it_asset_db;"
docker exec -it asset-db psql -U postgres -c "CREATE DATABASE it_asset_db;"
npm run db:setup
npm run db:seed
```

## Database Management Tools

### Option 1: pgAdmin (GUI)
1. Download: https://www.pgadmin.org/download/
2. Connect to: localhost:5432
3. User: postgres, Password: postgres

### Option 2: DBeaver (GUI)
1. Download: https://dbeaver.io/download/
2. Create PostgreSQL connection
3. Host: localhost, Port: 5432

### Option 3: Command Line
```bash
# Connect to database
docker exec -it asset-db psql -U postgres -d it_asset_db

# List tables
\dt

# Describe table
\d assets

# Run query
SELECT * FROM users;

# Exit
\q
```

## Useful Commands

### Docker Commands
```bash
# Start PostgreSQL
docker-compose up -d db

# Stop PostgreSQL
docker-compose stop db

# View logs
docker logs asset-db

# Connect to PostgreSQL
docker exec -it asset-db psql -U postgres
```

### SQL Commands
```sql
-- List databases
\l

-- Connect to database
\c it_asset_db

-- List tables
\dt

-- Describe table
\d assets

-- Count records
SELECT COUNT(*) FROM users;

-- View all users
SELECT username, email, usertype FROM users;
```

## Next Steps

After setup is complete:

1. ✅ PostgreSQL running
2. ✅ Database and tables created
3. ✅ Initial data seeded
4. ✅ Backend running
5. 🔄 Test API endpoints (see TESTING_GUIDE.md)
6. 🔄 Build frontend

## API Endpoints

Once the backend is running, you can test:

- Health: `GET http://localhost:5000/health`
- Login: `POST http://localhost:5000/api/auth/login`
- Assets: `GET http://localhost:5000/api/assets`

See `TESTING_GUIDE.md` for complete API documentation.

## Resources

- PostgreSQL Documentation: https://www.postgresql.org/docs/
- Node.js pg Driver: https://node-postgres.com/
- Docker PostgreSQL: https://hub.docker.com/_/postgres
