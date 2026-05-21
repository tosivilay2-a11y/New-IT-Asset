# SQL Server Setup Guide

Complete guide to set up SQL Server for the IT Asset Management System.

## Option 1: SQL Server with Docker (Recommended - Easiest)

### Step 1: Start SQL Server Container

Open Command Prompt or PowerShell and run:

```bash
docker run -e "ACCEPT_EULA=Y" -e "SA_PASSWORD=YourStrong@Passw0rd" -p 1433:1433 --name it-asset-sqlserver -d mcr.microsoft.com/mssql/server:2019-latest
```

Wait 10-15 seconds for SQL Server to start.

### Step 2: Verify SQL Server is Running

```bash
docker ps
```

You should see `it-asset-sqlserver` in the list.

### Step 3: Create Database and Tables

**Option A: Using SQL Server Management Studio (SSMS)**
1. Download SSMS: https://aka.ms/ssmsfullsetup
2. Connect to: `localhost,1433`
3. Login: `sa` / `YourStrong@Passw0rd`
4. Open `backend/scripts/schema.sql`
5. Execute the script (F5)

**Option B: Using sqlcmd (Command Line)**
```bash
docker exec -it it-asset-sqlserver /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P "YourStrong@Passw0rd" -i /path/to/schema.sql
```

**Option C: Using Azure Data Studio**
1. Download: https://aka.ms/azuredatastudio
2. Connect to: `localhost,1433`
3. Login: `sa` / `YourStrong@Passw0rd`
4. Open and run `backend/scripts/schema.sql`

### Step 4: Verify Database Creation

Connect to SQL Server and run:
```sql
USE ITAssetManagement;
GO

SELECT TABLE_NAME 
FROM INFORMATION_SCHEMA.TABLES 
WHERE TABLE_TYPE = 'BASE TABLE'
ORDER BY TABLE_NAME;
```

You should see 30+ tables.

---

## Option 2: Local SQL Server Installation

### Step 1: Download SQL Server

1. Go to: https://www.microsoft.com/en-us/sql-server/sql-server-downloads
2. Download **SQL Server 2019 Express** (Free)
3. Run the installer
4. Choose **Basic** installation
5. Accept license terms
6. Choose installation location
7. Wait for installation to complete

### Step 2: Enable SQL Server Authentication

1. Open **SQL Server Configuration Manager**
2. Go to **SQL Server Network Configuration** → **Protocols for SQLEXPRESS**
3. Enable **TCP/IP**
4. Restart SQL Server service

### Step 3: Set SA Password

1. Open **SQL Server Management Studio (SSMS)**
2. Connect with Windows Authentication
3. Right-click server → **Properties** → **Security**
4. Select **SQL Server and Windows Authentication mode**
5. Expand **Security** → **Logins** → Right-click **sa** → **Properties**
6. Set password: `YourStrong@Passw0rd`
7. Uncheck **Enforce password policy** (for development only)
8. Restart SQL Server service

### Step 4: Create Database

1. Open SSMS
2. Connect to: `localhost` or `localhost\SQLEXPRESS`
3. Login: `sa` / `YourStrong@Passw0rd`
4. Open `backend/scripts/schema.sql`
5. Execute (F5)

---

## Option 3: Azure SQL Database (Cloud)

### Step 1: Create Azure SQL Database

1. Go to: https://portal.azure.com
2. Create new **SQL Database**
3. Choose pricing tier (Basic for development)
4. Note the server name, database name, and credentials

### Step 2: Configure Firewall

1. Go to SQL Server → **Firewalls and virtual networks**
2. Add your client IP address
3. Allow Azure services to access server

### Step 3: Update Connection String

Edit `backend/.env`:
```env
DB_SERVER=your-server.database.windows.net
DB_PORT=1433
DB_DATABASE=ITAssetManagement
DB_USER=your-admin-username
DB_PASSWORD=your-password
DB_ENCRYPT=true
DB_TRUST_SERVER_CERTIFICATE=false
```

### Step 4: Run Schema

Use Azure Data Studio or SSMS to connect and run `schema.sql`.

---

## Database Schema Overview

The system uses **30+ tables** organized into 8 categories:

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

**Total: 30 tables**

---

## Connection Configuration

Update `backend/.env` with your SQL Server details:

```env
# Database Configuration (SQL Server)
DB_SERVER=localhost
DB_PORT=1433
DB_DATABASE=ITAssetManagement
DB_USER=sa
DB_PASSWORD=YourStrong@Passw0rd
DB_ENCRYPT=true
DB_TRUST_SERVER_CERTIFICATE=true

# JWT Configuration
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production-12345
JWT_EXPIRES_IN=24h

# Server Configuration
PORT=5000
NODE_ENV=development
```

---

## Verify Setup

### 1. Test Database Connection

```bash
cd it-asset-system/backend
npm install
node -e "const {getConnection} = require('./src/config/database'); getConnection().then(() => console.log('Connected!')).catch(console.error);"
```

### 2. Check Tables

Connect to SQL Server and run:
```sql
USE ITAssetManagement;
SELECT COUNT(*) as TableCount FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE';
```

Should return: **30**

### 3. Start Backend

```bash
npm run dev
```

You should see:
```
Database Configuration:
  Server: localhost
  Port: 1433
  Database: ITAssetManagement
  User: sa
✓ Database connected successfully
✓ Server running on port 5000
```

---

## Troubleshooting

### Error: "Login failed for user 'sa'"
- Verify SQL Server Authentication is enabled
- Check password is correct
- Restart SQL Server service

### Error: "Cannot connect to localhost:1433"
- Verify SQL Server is running: `docker ps` or check Windows Services
- Check TCP/IP is enabled in SQL Server Configuration Manager
- Verify port 1433 is not blocked by firewall

### Error: "Database 'ITAssetManagement' does not exist"
- Run the schema.sql script
- Verify you're connected to the correct server

### Docker Container Won't Start
```bash
# Remove old container
docker rm -f it-asset-sqlserver

# Start fresh
docker run -e "ACCEPT_EULA=Y" -e "SA_PASSWORD=YourStrong@Passw0rd" -p 1433:1433 --name it-asset-sqlserver -d mcr.microsoft.com/mssql/server:2019-latest

# Check logs
docker logs it-asset-sqlserver
```

---

## Next Steps

After SQL Server is set up:

1. ✅ SQL Server running
2. ✅ Database and tables created
3. 🔄 Run seed data: `npm run db:seed`
4. 🔄 Start backend: `npm run dev`
5. 🔄 Test API endpoints

---

## Useful Commands

### Docker Commands
```bash
# Start SQL Server
docker start it-asset-sqlserver

# Stop SQL Server
docker stop it-asset-sqlserver

# View logs
docker logs it-asset-sqlserver

# Connect to SQL Server
docker exec -it it-asset-sqlserver /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P "YourStrong@Passw0rd"
```

### SQL Commands
```sql
-- List all databases
SELECT name FROM sys.databases;

-- Use database
USE ITAssetManagement;

-- List all tables
SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE';

-- Count records in a table
SELECT COUNT(*) FROM Users;

-- Drop database (careful!)
DROP DATABASE ITAssetManagement;
```

---

## Resources

- SQL Server Documentation: https://docs.microsoft.com/en-us/sql/
- SQL Server Express Download: https://www.microsoft.com/sql-server/sql-server-downloads
- SSMS Download: https://aka.ms/ssmsfullsetup
- Azure Data Studio: https://aka.ms/azuredatastudio
- Docker SQL Server: https://hub.docker.com/_/microsoft-mssql-server
