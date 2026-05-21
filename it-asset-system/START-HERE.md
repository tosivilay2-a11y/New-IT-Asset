# 🚀 START HERE - IT Asset Management System

## What You Have Now

✅ **Complete Backend System** with 30-table PostgreSQL database
✅ **All Setup Scripts** ready to execute
✅ **Default Users** configured (admin, manager, user)
✅ **API Endpoints** for authentication and asset management
✅ **Documentation** for every step

---

## 🎯 What To Do Next (3 Simple Steps)

### Step 1: Make Sure PostgreSQL is Running

Check if your PostgreSQL Docker container is running:

```bash
docker ps | findstr asset-db
```

If not running, start it:
```bash
docker-compose up -d
```

---

### Step 2: Run the Complete Setup

**Option A: One-Click Setup (Recommended)**
```bash
SETUP-NOW.bat
```

**Option B: Manual Step-by-Step**
```bash
# 1. Create database
create-database-docker.bat

# 2. Setup backend
cd backend
setup-complete.bat
```

---

### Step 3: Test Your System

Once the server is running on `http://localhost:5000`:

**Test 1: Health Check**
```bash
curl http://localhost:5000/health
```

**Test 2: Login**
```bash
curl -X POST http://localhost:5000/api/auth/login ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"admin@example.com\",\"password\":\"admin123\"}"
```

You should get a response with a JWT token!

---

## 📋 What the Setup Does

1. **Creates Database**: `it_asset_db` in PostgreSQL
2. **Installs Dependencies**: All npm packages (express, pg, bcrypt, etc.)
3. **Creates 30 Tables**: Complete database schema
4. **Seeds Initial Data**:
   - 3 Users (admin, manager, user)
   - 3 Countries (Thailand, US, Singapore)
   - 3 Provinces (Bangkok, Chiang Mai, California)
   - 2 Companies (ABC Corporation, XYZ Limited)
   - 4 Departments (IT, HR, Finance, Operations)
   - 3 Locations (HQ, Floor 1, Floor 2)
   - 3 User Types (Admin, Manager, Staff)
   - 3 User Roles with permissions
   - 4 Main Categories (Computer, Printer, Network, Furniture)
   - 4 Asset Statuses (Available, In Use, Maintenance, Disposed)

---

## 🔐 Login Credentials

After setup, use these credentials:

| Role    | Email                  | Password    | Permissions |
|---------|------------------------|-------------|-------------|
| Admin   | admin@example.com      | admin123    | Full access |
| Manager | manager@example.com    | manager123  | Most features |
| User    | user@example.com       | user123     | View only |

---

## 📊 Database Tables Created

### Geographic & Organizational (5 tables)
- Countries
- Provinces  
- Companies
- Locations
- Departments

### User Management (5 tables)
- Users
- UserTypes
- UserRoles
- Permissions
- RolePermissions

### Asset Management (8 tables)
- Assets
- MainCategories
- Categories
- AssetStatuses
- AssetAssignments
- AssetTransfers
- AssetMaintenance
- AssetDisposals

### Inventory & Stock (4 tables)
- InventoryItems
- StockMovements
- StockCounts
- StockCountDetails

### Approval & Audit (4 tables)
- ApprovalWorkflows
- ApprovalSteps
- ApprovalHistory
- AuditLogs

### Additional Features (4 tables)
- Notifications
- Documents
- QRCodes
- SystemSettings

**Total: 30 Tables**

---

## 🧪 API Endpoints Available

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login
- `GET /api/auth/me` - Get current user
- `PUT /api/auth/profile` - Update profile
- `PUT /api/auth/password` - Change password

### Assets
- `GET /api/assets` - List all assets
- `GET /api/assets/:id` - Get asset details
- `POST /api/assets` - Create new asset
- `PUT /api/assets/:id` - Update asset
- `DELETE /api/assets/:id` - Delete asset
- `POST /api/assets/:id/assign` - Assign asset
- `POST /api/assets/:id/transfer` - Transfer asset
- `GET /api/assets/:id/history` - Asset history

---

## 🔧 Troubleshooting

### Problem: "Database connection failed"

**Solution:**
```bash
# Check PostgreSQL is running
docker ps

# If not running, start it
docker-compose up -d

# Verify database exists
verify-database.bat
```

---

### Problem: "Module not found"

**Solution:**
```bash
cd backend
npm install
```

---

### Problem: "Port 5000 already in use"

**Solution:**
Edit `backend/.env` and change:
```
PORT=5001
```

---

### Problem: "Cannot find .env file"

**Solution:**
The `.env` file is already created at `backend/.env` with correct PostgreSQL settings.

---

## 📚 Documentation Files

- **START-HERE.md** (this file) - Quick start guide
- **README.md** - Full project overview
- **QUICK-START-GUIDE.md** - Detailed setup instructions
- **DATABASE_MIGRATION_COMPLETE.md** - Database migration details
- **POSTGRES_SETUP.md** - PostgreSQL configuration
- **MANUAL_SETUP_STEPS.md** - Manual setup steps
- **backend/TESTING_GUIDE.md** - API testing guide

---

## 🎯 After Setup is Complete

1. ✅ Server running on `http://localhost:5000`
2. ✅ Database with 30 tables and initial data
3. ✅ 3 users ready to login
4. ✅ API endpoints ready to use

### Next Steps:
- Test all API endpoints
- Build frontend application
- Customize for your needs
- Add more features

---

## 🆘 Need Help?

1. **Check if setup completed successfully**
   ```bash
   verify-database.bat
   ```

2. **View server logs**
   - Check console output where server is running

3. **View database logs**
   ```bash
   docker logs asset-db
   ```

4. **Test database connection**
   ```bash
   docker exec -it asset-db psql -U postgres -d it_asset_db -c "\dt"
   ```

---

## ✅ Success Checklist

- [ ] PostgreSQL container is running
- [ ] Database `it_asset_db` is created
- [ ] All 30 tables are created
- [ ] Initial data is seeded
- [ ] Server starts without errors
- [ ] Health check returns success
- [ ] Login works with admin@example.com

---

**Ready? Run `SETUP-NOW.bat` and you're done!** 🎉
