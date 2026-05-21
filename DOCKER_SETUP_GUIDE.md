# Docker Setup Guide - Complete Installation

This guide will help you set up the entire application using Docker, including PostgreSQL.

## Prerequisites

### Install Docker Desktop

1. **Download Docker Desktop**:
   - Go to: https://www.docker.com/products/docker-desktop/
   - Click "Download for Windows"
   - File size: ~500MB

2. **Install Docker Desktop**:
   - Run the installer
   - Follow the installation wizard
   - **Important**: Enable WSL 2 if prompted
   - Restart computer if required

3. **Start Docker Desktop**:
   - Launch Docker Desktop from Start Menu
   - Wait for Docker to start (whale icon in system tray)
   - Icon should be steady (not animated)

4. **Verify Installation**:
   ```cmd
   docker --version
   docker-compose --version
   ```
   Should show version numbers

## Quick Start (Easiest Method)

### Option 1: One-Click Setup

Simply run:
```cmd
docker-start.bat
```

This will:
- Start all services (PostgreSQL, Backend, Frontend)
- Create database and tables
- Seed sample data
- Open the application in your browser

### Option 2: Manual Docker Commands

```cmd
# Start all services
docker-compose up -d

# Wait for services to start (15 seconds)
timeout /t 15

# Initialize database
docker-compose exec backend alembic upgrade head

# Seed sample data
docker-compose exec backend python seed_data.py

# Open application
start http://localhost:3000
```

## What Docker Does For You

✓ **No PostgreSQL installation needed** - Runs in container
✓ **No Python setup needed** - Runs in container  
✓ **No Node.js setup needed** - Runs in container
✓ **Automatic configuration** - Everything pre-configured
✓ **Easy cleanup** - Remove everything with one command
✓ **Consistent environment** - Works the same everywhere

## Services Running

When you run `docker-compose up -d`, three services start:

1. **PostgreSQL Database** (db)
   - Port: 5432
   - Username: postgres
   - Password: postgres
   - Database: assetdb

2. **Backend API** (backend)
   - Port: 8000
   - URL: http://localhost:8000
   - API Docs: http://localhost:8000/docs

3. **Frontend** (frontend)
   - Port: 3000
   - URL: http://localhost:3000

## Step-by-Step Setup

### Step 1: Start Services

```cmd
docker-compose up -d
```

**What this does**:
- Downloads required Docker images (first time only, ~5 minutes)
- Creates containers for database, backend, and frontend
- Starts all services in background

**Check status**:
```cmd
docker-compose ps
```

Should show 3 services running.

### Step 2: Wait for Database

```cmd
# Wait 15 seconds for PostgreSQL to be ready
timeout /t 15
```

### Step 3: Initialize Database

```cmd
# Create tables
docker-compose exec backend alembic upgrade head

# Seed sample data
docker-compose exec backend python seed_data.py
```

### Step 4: Verify Setup

```cmd
# Check backend
curl http://localhost:8000

# Or open in browser
start http://localhost:8000
```

Should show: `{"message":"Asset Management System API"}`

### Step 5: Access Application

```cmd
start http://localhost:3000
```

**Login with**:
- Email: `admin@example.com`
- Password: `admin123`

## Docker Commands Reference

### Starting and Stopping

```cmd
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# Restart services
docker-compose restart

# Stop and remove everything (including database data)
docker-compose down -v
```

### Viewing Logs

```cmd
# View all logs
docker-compose logs

# Follow logs in real-time
docker-compose logs -f

# View specific service logs
docker-compose logs backend
docker-compose logs frontend
docker-compose logs db

# Last 50 lines
docker-compose logs --tail=50
```

### Service Management

```cmd
# Check service status
docker-compose ps

# Restart specific service
docker-compose restart backend

# Stop specific service
docker-compose stop frontend

# Start specific service
docker-compose start frontend

# Rebuild and restart
docker-compose up -d --build
```

### Database Operations

```cmd
# Connect to PostgreSQL
docker-compose exec db psql -U postgres -d assetdb

# Backup database
docker-compose exec db pg_dump -U postgres assetdb > backup.sql

# Restore database
docker-compose exec -T db psql -U postgres assetdb < backup.sql

# View database logs
docker-compose logs db
```

### Backend Operations

```cmd
# Run migrations
docker-compose exec backend alembic upgrade head

# Seed data
docker-compose exec backend python seed_data.py

# Verify setup
docker-compose exec backend python verify_setup.py

# Access backend shell
docker-compose exec backend bash

# Run Python commands
docker-compose exec backend python -c "print('Hello')"
```

### Frontend Operations

```cmd
# Rebuild frontend
docker-compose exec frontend npm run build

# Access frontend shell
docker-compose exec frontend sh

# Install new package
docker-compose exec frontend npm install package-name
```

## Troubleshooting

### Docker Desktop not starting

1. **Check Windows version**:
   - Windows 10 64-bit: Pro, Enterprise, or Education (Build 19041 or higher)
   - Or Windows 11

2. **Enable virtualization**:
   - Restart computer
   - Enter BIOS (usually F2, F10, or Del during startup)
   - Enable Intel VT-x or AMD-V
   - Save and exit

3. **Enable WSL 2**:
   ```cmd
   wsl --install
   wsl --set-default-version 2
   ```

### Port already in use

**Find what's using the port**:
```cmd
# Check port 8000
netstat -ano | findstr :8000

# Check port 3000
netstat -ano | findstr :3000

# Check port 5432
netstat -ano | findstr :5432
```

**Kill the process**:
```cmd
taskkill /PID <PID_NUMBER> /F
```

**Or change ports in docker-compose.yml**:
```yaml
services:
  backend:
    ports:
      - "8080:8000"  # Use 8080 instead of 8000
```

### Services won't start

```cmd
# Check Docker is running
docker ps

# View error logs
docker-compose logs

# Remove and recreate
docker-compose down -v
docker-compose up -d
```

### Database connection errors

```cmd
# Check database is running
docker-compose ps db

# Check database logs
docker-compose logs db

# Restart database
docker-compose restart db

# Wait longer for database to start
timeout /t 30
```

### "Cannot connect to Docker daemon"

1. Start Docker Desktop
2. Wait for it to fully start (whale icon steady)
3. Try command again

### Slow performance

1. **Increase Docker resources**:
   - Open Docker Desktop
   - Settings → Resources
   - Increase CPU and Memory
   - Apply & Restart

2. **Clean up Docker**:
   ```cmd
   docker system prune -a
   ```

## Development Workflow

### Daily Usage

**Start working**:
```cmd
docker-compose up -d
```

**Stop working**:
```cmd
docker-compose down
```

### Making Code Changes

**Backend changes**:
- Edit files in `backend/` folder
- Changes auto-reload (no restart needed)

**Frontend changes**:
- Edit files in `frontend/src/` folder  
- Changes auto-reload (no restart needed)

**Database changes**:
```cmd
# Create migration
docker-compose exec backend alembic revision --autogenerate -m "description"

# Apply migration
docker-compose exec backend alembic upgrade head
```

### Resetting Everything

**Complete reset**:
```cmd
# Stop and remove everything
docker-compose down -v

# Start fresh
docker-compose up -d

# Wait for database
timeout /t 15

# Initialize
docker-compose exec backend alembic upgrade head
docker-compose exec backend python seed_data.py
```

## Advanced Configuration

### Custom Environment Variables

Edit `docker-compose.yml`:

```yaml
services:
  backend:
    environment:
      DATABASE_URL: postgresql://postgres:newpassword@db:5432/assetdb
      SECRET_KEY: your-custom-secret-key
      ACCESS_TOKEN_EXPIRE_MINUTES: 60
```

### Persistent Data

Database data is stored in Docker volume `postgres_data`.

**Backup volume**:
```cmd
docker run --rm -v asset-management_postgres_data:/data -v %cd%:/backup ubuntu tar czf /backup/db-backup.tar.gz /data
```

**Restore volume**:
```cmd
docker run --rm -v asset-management_postgres_data:/data -v %cd%:/backup ubuntu tar xzf /backup/db-backup.tar.gz -C /
```

### Production Deployment

For production, update `docker-compose.yml`:

```yaml
services:
  backend:
    environment:
      DATABASE_URL: ${DATABASE_URL}
      SECRET_KEY: ${SECRET_KEY}
    restart: always
  
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.prod
    restart: always
```

## Useful Docker Commands

```cmd
# View running containers
docker ps

# View all containers
docker ps -a

# View images
docker images

# Remove unused images
docker image prune

# Remove unused volumes
docker volume prune

# View disk usage
docker system df

# Clean everything
docker system prune -a --volumes

# View container resource usage
docker stats
```

## Accessing Services

### URLs

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Alternative API Docs**: http://localhost:8000/redoc

### Default Credentials

- **Admin**: admin@example.com / admin123
- **Staff**: staff@example.com / staff123

### Database Access

**Using Docker**:
```cmd
docker-compose exec db psql -U postgres -d assetdb
```

**Using external tool** (pgAdmin, DBeaver):
- Host: localhost
- Port: 5432
- Database: assetdb
- Username: postgres
- Password: postgres

## Benefits of Docker Setup

✓ **No manual installations** - Everything in containers
✓ **Consistent environment** - Same setup everywhere
✓ **Easy cleanup** - Remove everything with one command
✓ **Isolated** - Doesn't affect your system
✓ **Portable** - Works on any machine with Docker
✓ **Quick reset** - Start fresh anytime
✓ **Production-ready** - Same setup for dev and prod

## Next Steps

1. ✓ Docker Desktop installed and running
2. ✓ Services started with docker-compose
3. ✓ Database initialized
4. ✓ Application accessible
5. ✓ Logged in successfully

Now you can:
- Develop features
- Test the application
- Deploy to production
- Share with team members

## Getting Help

If you encounter issues:

1. **Check logs**: `docker-compose logs`
2. **Check status**: `docker-compose ps`
3. **Restart services**: `docker-compose restart`
4. **Full reset**: `docker-compose down -v && docker-compose up -d`
5. **Check Docker Desktop** is running

For more help, see:
- TROUBLESHOOTING.md
- LOGIN_CHECKLIST.md
- Docker documentation: https://docs.docker.com/
