# Asset Management & Inventory Tracking System

Full-stack web application for managing assets and inventory with ORM-based architecture.

## Tech Stack

- **Backend**: Python with FastAPI
- **ORM**: SQLAlchemy
- **Database**: PostgreSQL (easily switchable to SQL Server)
- **Frontend**: React with modern dashboard UI

## Features

- User authentication with role-based access (Admin, Staff)
- Asset management (CRUD operations)
- Inventory tracking with stock transactions
- Audit sessions for stock verification
- Low stock alerts
- Search and filtering
- Data export (CSV)
- Activity logging

## Project Structure

```
asset-management/
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── schemas/
│   │   ├── core/
│   │   └── main.py
│   ├── alembic/
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── App.jsx
│   └── package.json
└── docker-compose.yml
```

## Quick Start

### Option 1: Docker Setup (Recommended - Easiest)

**Prerequisites**: Install Docker Desktop from https://www.docker.com/products/docker-desktop/

**One-command setup**:
```bash
docker-start.bat
```

That's it! The script will:
- Start PostgreSQL, Backend, and Frontend
- Initialize database and create tables
- Seed sample data
- Open the application in your browser

**Manual Docker commands**:
```bash
# Start all services
docker-compose up -d

# Wait for database (15 seconds)
timeout /t 15

# Initialize database
docker-compose exec backend alembic upgrade head
docker-compose exec backend python seed_data.py

# Open application
start http://localhost:3000
```

### Option 2: Manual Setup

**Prerequisites**:
- Python 3.9+
- Node.js 16+
- PostgreSQL 13+

**Backend Setup**:
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
# Edit .env with your database credentials
alembic upgrade head
python seed_data.py
uvicorn app.main:app --reload
```

**Frontend Setup** (in new terminal):
```bash
cd frontend
npm install
npm start
```

See **MANUAL_SETUP_GUIDE.md** for detailed instructions.

## Database Configuration

### PostgreSQL (Default)
```env
DATABASE_URL=postgresql://user:password@localhost:5432/assetdb
```

### SQL Server (Alternative)
```env
DATABASE_URL=mssql+pyodbc://user:password@localhost:1433/assetdb?driver=ODBC+Driver+17+for+SQL+Server
```

## Default Credentials

After running setup (Docker or manual):

- **Admin**: admin@example.com / admin123
- **Staff**: staff@example.com / staff123

## Useful Commands

### Docker Commands

```bash
# Start services
docker-start.bat

# Stop services
docker-stop.bat

# View logs
docker-logs.bat

# Reset everything
docker-reset.bat

# Manual commands
docker-compose up -d          # Start
docker-compose down           # Stop
docker-compose logs -f        # View logs
docker-compose ps             # Check status
```

### Manual Setup Commands

```bash
# Backend
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload

# Frontend
cd frontend
npm start

# Database operations
alembic upgrade head          # Run migrations
python seed_data.py           # Seed data
python verify_setup.py        # Verify setup
```

## Documentation

- **DOCKER_SETUP_GUIDE.md** - Complete Docker setup guide
- **DOCKER_QUICK_REFERENCE.md** - Quick Docker commands
- **MANUAL_SETUP_GUIDE.md** - Manual installation guide
- **INSTALLATION_CHECKLIST.md** - Step-by-step checklist
- **TROUBLESHOOTING.md** - Common issues and solutions
- **LOGIN_CHECKLIST.md** - Login troubleshooting

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user

### Users
- `GET /users/` - List users (Admin only)
- `GET /users/me` - Get current user

### Assets
- `GET /assets/` - List assets (with filters)
- `POST /assets/` - Create asset
- `GET /assets/{id}` - Get asset details
- `PUT /assets/{id}` - Update asset
- `DELETE /assets/{id}` - Delete asset

### Inventory
- `GET /inventory/` - List inventory items
- `POST /inventory/` - Create inventory item
- `POST /inventory/transaction` - Record transaction
- `GET /inventory/alerts` - Get low stock alerts

### Audits
- `GET /audits/` - List audit sessions
- `POST /audits/` - Create audit session
- `POST /audits/{id}/records` - Add audit records
- `GET /audits/{id}/report` - Generate audit report

## License

MIT
