# IT Asset Management System

Enterprise-grade IT Asset Management System with comprehensive features for tracking, managing, and auditing IT assets across multiple locations and departments.

## 🚀 Quick Start with Docker (Recommended)

### One Command Setup
```bash
cd it-asset-system
docker-start.bat
```

That's it! Everything runs in Docker:
- ✅ PostgreSQL database with `it_asset_db`
- ✅ Backend API on port 5000
- ✅ All tables created automatically
- ✅ Initial data seeded
- ✅ Ready to use!

**Access:** http://localhost:5000

---

## 📋 Alternative: Manual Setup

If you prefer step-by-step:

### 1. Create Database
```bash
create-database-docker.bat
```

### 2. Setup Backend
```bash
cd backend
setup-complete.bat
```

### 3. Start Server
```bash
cd backend
start.bat
```

---

## 🔐 Default Login Credentials

| Role    | Email                  | Password    |
|---------|------------------------|-------------|
| Admin   | admin@example.com      | admin123    |
| Manager | manager@example.com    | manager123  |
| User    | user@example.com       | user123     |

---

## ✨ Features

- **Asset Management**: Complete lifecycle tracking from acquisition to disposal
- **QR Code Integration**: Generate and scan QR codes for quick asset identification
- **Multi-level Approvals**: Configurable approval workflows for asset requests
- **Stock Counting**: Physical inventory verification and reconciliation
- **Hierarchical Locations**: Multi-level location management (Country > Province > Company > Location)
- **Role-Based Access Control**: Granular permissions system with 8 core permissions
- **Audit Trail**: Complete history of all asset-related activities
- **Reporting**: Comprehensive reports and analytics

---

## 🏗️ Technology Stack

- **Backend**: Node.js + Express
- **Database**: PostgreSQL 12+
- **Authentication**: JWT with bcrypt
- **QR Codes**: QRCode library
- **Security**: Helmet, CORS, Rate Limiting

---

## 📊 Database Structure

30 tables organized into:
- **Geographic & Organizational**: Countries, Provinces, Companies, Locations, Departments
- **User Management**: Users, UserTypes, UserRoles, Permissions, RolePermissions
- **Asset Management**: Assets, Categories, Statuses, Assignments, Transfers, Maintenance, Disposals
- **Inventory**: Items, Stock Movements, Stock Counts
- **Approval & Audit**: Workflows, Steps, History, Audit Logs
- **Additional**: Notifications, Documents, QR Codes, Settings, Activity Logs

---

## 🧪 Test the API

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

### Get Assets
```bash
curl http://localhost:5000/api/assets ^
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## 📁 Project Structure

```
it-asset-system/
├── SETUP-NOW.bat              # One-click complete setup
├── create-database-docker.bat # Create database only
├── verify-database.bat        # Verify database setup
├── QUICK-START-GUIDE.md       # Detailed quick start
└── backend/
    ├── .env                   # Configuration
    ├── server.js              # Express server
    ├── setup-complete.bat     # Backend setup
    ├── start.bat             # Start server
    ├── scripts/
    │   ├── schema-postgres.sql    # 30-table schema
    │   ├── setupDatabase.js       # Table creation
    │   └── seedData.js           # Initial data
    └── src/
        ├── config/           # Database connection
        ├── controllers/      # Business logic
        ├── middleware/       # Auth, permissions, audit
        ├── models/          # Database queries
        ├── routes/          # API endpoints
        └── services/        # QR codes, asset IDs
```

---

## 🔧 Troubleshooting

### Database Connection Failed
```bash
# Check if PostgreSQL is running
docker ps | findstr asset-db

# Create database if needed
create-database-docker.bat

# Verify database exists
verify-database.bat
```

### Port Already in Use
Edit `backend/.env` and change:
```
PORT=5001
```

### Module Not Found
```bash
cd backend
npm install
```

---

## 📚 Documentation

- **[DOCKER-GUIDE.md](DOCKER-GUIDE.md)** - Docker setup and commands (RECOMMENDED)
- **[QUICK-START-GUIDE.md](QUICK-START-GUIDE.md)** - Quick setup guide
- **[DATABASE_MIGRATION_COMPLETE.md](DATABASE_MIGRATION_COMPLETE.md)** - Migration details
- **[POSTGRES_SETUP.md](POSTGRES_SETUP.md)** - PostgreSQL configuration
- **[MANUAL_SETUP_STEPS.md](MANUAL_SETUP_STEPS.md)** - Detailed manual setup
- **[backend/TESTING_GUIDE.md](backend/TESTING_GUIDE.md)** - API testing guide
- **[IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md)** - Full implementation guide

---

## 🎯 Next Steps

1. ✅ Run `SETUP-NOW.bat` to complete setup
2. ✅ Test API endpoints with default users
3. 🔨 Build frontend application
4. 🔨 Integrate with backend API
5. 🔨 Customize for your organization

---

## 🆘 Need Help?

Run the verification script:
```bash
verify-database.bat
```

Check the logs:
- Server logs: Console output
- Database logs: `docker logs asset-db`
- npm logs: `backend/npm_cache/_logs/`

---

**Ready to start? Run `SETUP-NOW.bat` now!** 🚀
