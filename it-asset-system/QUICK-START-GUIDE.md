# IT Asset Management System - Quick Start Guide

## Prerequisites

✅ **PostgreSQL** running on `localhost:5432`
- Container name: `asset-db` (from docker-compose.yml)
- Database: `it_asset_db` (will be created)
- User: `postgres`
- Password: `postgres`

✅ **Node.js** installed (v14 or higher)

---

## 🚀 Quick Setup (3 Steps)

### Step 1: Navigate to Backend Directory
```bash
cd it-asset-system/backend
```

### Step 2: Run Complete Setup
```bash
setup-complete.bat
```

This will:
- Install all npm dependencies
- Create all 30 database tables
- Seed initial data (users, categories, locations, etc.)

### Step 3: Start the Server
```bash
start.bat
```

Or manually:
```bash
npm run dev
```

---

## 📋 Manual Setup (If Needed)

If you prefer to run commands individually:

```bash
# 1. Install dependencies
npm install

# 2. Create database tables
npm run db:setup

# 3. Seed initial data
npm run db:seed

# 4. Start server
npm run dev
```

---

## 🔐 Default Users

After seeding, you can login with:

| Role    | Email                  | Password    |
|---------|------------------------|-------------|
| Admin   | admin@example.com      | admin123    |
| Manager | manager@example.com    | manager123  |
| User    | user@example.com       | user123     |

---

## 🧪 Test the API

Once the server is running on `http://localhost:5000`:

### Health Check
```bash
curl http://localhost:5000/health
```

### Login
```bash
curl -X POST http://localhost:5000/api/auth/login ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"admin@example.com\",\"password\":\"admin123\"}"
```

### Get Assets (with token)
```bash
curl http://localhost:5000/api/assets ^
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## 📊 Database Structure

The system includes 30 tables organized into:

### Geographic & Organizational (4 tables)
- Countries, Provinces, Companies, Locations, Departments

### User Management (5 tables)
- Users, UserTypes, UserRoles, Permissions, RolePermissions

### Asset Management (8 tables)
- Assets, MainCategories, Categories, AssetStatuses, AssetAssignments, AssetTransfers, AssetMaintenance, AssetDisposals

### Inventory & Stock (4 tables)
- InventoryItems, StockMovements, StockCounts, StockCountDetails

### Approval & Audit (4 tables)
- ApprovalWorkflows, ApprovalSteps, ApprovalHistory, AuditLogs

### Additional Features (5 tables)
- Notifications, Documents, QRCodes, SystemSettings, ActivityLogs

---

## 🔧 Troubleshooting

### Database Connection Failed
1. Verify PostgreSQL is running:
   ```bash
   docker ps
   ```
2. Check if `it_asset_db` exists:
   ```bash
   docker exec -it postgres-db psql -U postgres -c "\l"
   ```
3. Create database if needed:
   ```bash
   docker exec -it postgres-db psql -U postgres -c "CREATE DATABASE it_asset_db;"
   ```

### Port Already in Use
If port 5000 is busy, change it in `.env`:
```
PORT=5001
```

### Module Not Found
Run:
```bash
npm install
```

---

## 📁 Project Structure

```
it-asset-system/backend/
├── .env                    # Environment configuration
├── server.js               # Express server entry point
├── package.json            # Dependencies
├── setup-complete.bat      # Complete setup script
├── start.bat              # Start server script
├── scripts/
│   ├── schema-postgres.sql # Database schema (30 tables)
│   ├── setupDatabase.js    # Table creation script
│   └── seedData.js         # Initial data seeding
└── src/
    ├── config/
    │   └── database.js     # PostgreSQL connection
    ├── controllers/        # Business logic
    ├── middleware/         # Auth, permissions, audit
    ├── models/            # Database queries
    ├── routes/            # API endpoints
    └── services/          # QR codes, asset IDs
```

---

## 🎯 Next Steps

1. ✅ Complete setup using `setup-complete.bat`
2. ✅ Start server using `start.bat`
3. ✅ Test login with default users
4. 🔨 Build frontend application
5. 🔨 Integrate with backend API
6. 🔨 Customize for your organization

---

## 📚 Additional Documentation

- `DATABASE_MIGRATION_COMPLETE.md` - Migration details
- `POSTGRES_SETUP.md` - PostgreSQL configuration
- `MANUAL_SETUP_STEPS.md` - Detailed setup instructions
- `TESTING_GUIDE.md` - API testing guide
- `README.md` - Full documentation

---

## 🆘 Need Help?

Check the logs for detailed error messages:
- Server logs: Console output
- Database logs: Check PostgreSQL container logs
- npm logs: `npm_cache/_logs/`

---

**Ready to start? Run `setup-complete.bat` now!** 🚀
