# IT Asset Management System - Backend API

Enterprise-grade IT Asset Management System built with Node.js, Express, and MS SQL Server.

## Features

✅ **Asset Management**
- Complete CRUD operations with pagination and filters
- Auto-generated Asset IDs (format: COMP-TH-BKK-ABC-2026-0001)
- QR code generation and scanning
- Asset assignment and transfer
- Asset lifecycle tracking
- Audit trail for all operations

✅ **Authentication & Authorization**
- JWT-based authentication
- Role-based access control (RBAC)
- Permission-based authorization
- Secure password hashing with bcrypt

✅ **Database**
- MS SQL Server with 23 tables
- Complete relational schema
- Automatic audit logging
- Optimized indexes

## Tech Stack

- **Runtime:** Node.js
- **Framework:** Express.js
- **Database:** MS SQL Server
- **Authentication:** JWT + bcryptjs
- **QR Codes:** qrcode library
- **Security:** Helmet, CORS

## Prerequisites

- Node.js 16+ installed
- MS SQL Server 2019+ installed
- npm or yarn package manager

## Quick Start

### 1. Install Dependencies

```bash
cd it-asset-system/backend
npm install
```

### 2. Configure Environment

```bash
# Copy .env.example to .env
copy .env.example .env

# Edit .env with your database credentials
```

### 3. Setup Database

```bash
# Create database and tables
npm run db:setup

# Seed initial data
npm run db:seed
```

### 4. Start Server

```bash
# Development mode (with auto-reload)
npm run dev

# Production mode
npm start
```

Server will run at: `http://localhost:5000`

## Default Users

After seeding, you can login with:

| Role    | Email                  | Password    |
|---------|------------------------|-------------|
| Admin   | admin@example.com      | admin123    |
| Manager | manager@example.com    | manager123  |
| User    | user@example.com       | user123     |

## API Endpoints

### Authentication

```
POST   /api/auth/login              - User login
POST   /api/auth/register           - User registration
GET    /api/auth/profile            - Get current user profile
PUT    /api/auth/profile            - Update profile
POST   /api/auth/change-password    - Change password
POST   /api/auth/refresh-token      - Refresh JWT token
```

### Assets

```
GET    /api/assets                  - Get all assets (with filters)
GET    /api/assets/statistics       - Get dashboard statistics
GET    /api/assets/preview-id       - Preview next Asset ID
GET    /api/assets/:id              - Get asset by ID
GET    /api/assets/code/:code       - Get asset by code
GET    /api/assets/:id/history      - Get asset history
GET    /api/assets/location/:id     - Get assets by location
GET    /api/assets/user/:id         - Get assets by user

POST   /api/assets                  - Create new asset
PUT    /api/assets/:id              - Update asset
DELETE /api/assets/:id              - Delete asset

POST   /api/assets/:id/assign       - Assign asset to user
POST   /api/assets/:id/unassign     - Unassign asset
POST   /api/assets/:id/transfer     - Transfer asset location

POST   /api/assets/:id/qr-code      - Generate QR code
POST   /api/assets/qr-codes/bulk    - Bulk generate QR codes
POST   /api/assets/qr-codes/scan    - Scan QR code
POST   /api/assets/qr-codes/labels  - Get printable labels
```

## API Usage Examples

### Login

```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin@example.com",
    "password": "admin123"
  }'
```

### Get All Assets

```bash
curl -X GET "http://localhost:5000/api/assets?page=1&limit=50" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Create Asset

```bash
curl -X POST http://localhost:5000/api/assets \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "mainCategoryId": 1,
    "categoryId": 1,
    "countryId": 1,
    "provinceId": 1,
    "companyId": 1,
    "locationId": 1,
    "statusId": 1,
    "brand": "Dell",
    "modelName": "Latitude 5420",
    "serialNumber": "SN123456",
    "cpu": "Intel i7-1185G7",
    "ram": "16GB DDR4",
    "hdd": "512GB SSD",
    "price": 45000.00
  }'
```

### Preview Asset ID

```bash
curl -X GET "http://localhost:5000/api/assets/preview-id?mainCategoryId=1&countryId=1&provinceId=1&companyId=1" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Scan QR Code

```bash
curl -X POST http://localhost:5000/api/assets/qr-codes/scan \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "assetCode": "COMP-TH-BKK-ABC-2026-0001"
  }'
```

## Project Structure

```
backend/
├── scripts/
│   ├── setupDatabase.js      # Database schema creation
│   └── seedData.js            # Initial data seeding
├── src/
│   ├── config/
│   │   └── database.js        # Database connection
│   ├── controllers/
│   │   ├── authController.js  # Authentication logic
│   │   └── assetController.js # Asset management logic
│   ├── middleware/
│   │   ├── authMiddleware.js  # JWT validation
│   │   ├── permissionMiddleware.js # RBAC checks
│   │   └── auditMiddleware.js # Audit logging
│   ├── models/
│   │   └── assetModel.js      # Asset database operations
│   ├── routes/
│   │   ├── authRoutes.js      # Auth endpoints
│   │   └── assetRoutes.js     # Asset endpoints
│   └── services/
│       ├── assetIdGenerator.js # Asset ID generation
│       └── qrCodeService.js    # QR code operations
├── server.js                   # Main server file
├── package.json
├── .env.example
└── README.md
```

## Database Schema

The system uses 23 tables:

**Core Tables:**
- Countries, Provinces, Companies, Locations
- Users, UserRoles, Permissions, RolePermissions
- Departments

**Asset Tables:**
- MainCategories, Categories, AssetStatuses
- Assets, AssetSequences

**Workflow Tables:**
- StockCountSessions, StockCounts, Reconciliations
- ApprovalLevels, Approvals

**System Tables:**
- AuditLogs, Notifications

## Security Features

- JWT token authentication
- Password hashing with bcrypt
- Role-based access control (RBAC)
- Permission-based authorization
- SQL injection prevention (parameterized queries)
- Helmet security headers
- CORS configuration
- Automatic audit logging

## Permissions

| Permission        | Description           |
|-------------------|-----------------------|
| asset.view        | View assets           |
| asset.create      | Create assets         |
| asset.update      | Update assets         |
| asset.delete      | Delete assets         |
| asset.assign      | Assign assets         |
| asset.transfer    | Transfer assets       |
| user.manage       | Manage users          |

## Role Permissions

| Role    | Permissions                                                    |
|---------|----------------------------------------------------------------|
| Admin   | All permissions                                                |
| Manager | All except user.manage                                         |
| User    | asset.view only                                                |

## Environment Variables

```env
# Database
DB_SERVER=localhost
DB_PORT=1433
DB_DATABASE=ITAssetManagement
DB_USER=sa
DB_PASSWORD=YourStrong@Passw0rd
DB_ENCRYPT=true
DB_TRUST_SERVER_CERTIFICATE=true

# JWT
JWT_SECRET=your-super-secret-jwt-key
JWT_EXPIRES_IN=24h

# Server
PORT=5000
NODE_ENV=development
```

## Development

```bash
# Install dependencies
npm install

# Run in development mode (auto-reload)
npm run dev

# Run in production mode
npm start

# Setup database
npm run db:setup

# Seed data
npm run db:seed
```

## Troubleshooting

### Database Connection Failed

1. Verify SQL Server is running
2. Check credentials in .env file
3. Ensure TCP/IP is enabled in SQL Server Configuration Manager
4. Check firewall settings

### Authentication Failed

1. Verify JWT_SECRET is set in .env
2. Check token expiration
3. Ensure user is active in database

### Permission Denied

1. Check user role and permissions
2. Verify RolePermissions table is seeded
3. Check permission name in route

## Next Steps

1. ✅ Backend API complete
2. 🔄 Build frontend React/TypeScript application
3. 🔄 Add stock count functionality
4. 🔄 Add approval workflow
5. 🔄 Add Excel import/export
6. 🔄 Add notifications system

## Support

For issues or questions:
1. Check this README
2. Review API documentation
3. Check database schema in setupDatabase.js
4. Review implementation guide

## License

ISC
