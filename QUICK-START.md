# Quick Start Guide

## Fastest Way to Run the Application

### Step 1: Make Sure Docker is Running

1. Open Docker Desktop
2. Wait for the whale icon to be steady in the system tray

### Step 2: Run the Application

Double-click or run:
```cmd
START-NOW.bat
```

That's it! The script will:
- ✅ Stop any old containers
- ✅ Start database, backend, and frontend
- ✅ Initialize database tables
- ✅ Create sample data
- ✅ Open the application in your browser

### Step 3: Login

The browser will open automatically to http://localhost:3000

**Login credentials:**
- Email: `admin@example.com`
- Password: `admin123`

---

## Manual Commands

If you prefer to run commands manually:

```cmd
# Start all services
docker-compose up -d

# Wait 20 seconds
timeout /t 20

# Initialize database
docker-compose exec -T backend alembic upgrade head

# Seed data
docker-compose exec -T backend python seed_data.py

# Open browser
start http://localhost:3000
```

---

## Stopping the Application

```cmd
docker-compose down
```

---

## Viewing Logs

```cmd
# All services
docker-compose logs -f

# Backend only
docker-compose logs -f backend

# Frontend only
docker-compose logs -f frontend

# Database only
docker-compose logs -f db
```

---

## Restarting Services

```cmd
# Restart all
docker-compose restart

# Restart backend only
docker-compose restart backend

# Restart frontend only
docker-compose restart frontend
```

---

## Resetting Everything

```cmd
# Stop and remove all data
docker-compose down -v

# Start fresh
START-NOW.bat
```

---

## Troubleshooting

### Application won't start?

1. Make sure Docker Desktop is running
2. Run: `docker ps` to check if containers are running
3. Run: `docker-compose logs` to see errors

### Can't login?

1. Make sure database is seeded:
   ```cmd
   docker-compose exec -T backend python seed_data.py
   ```

2. Check backend logs:
   ```cmd
   docker-compose logs backend
   ```

### Port already in use?

Find and kill the process:
```cmd
netstat -ano | findstr :3000
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Need to rebuild?

```cmd
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

---

## URLs

| Service | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| API Documentation | http://localhost:8000/docs |
| Alternative API Docs | http://localhost:8000/redoc |

---

## Default Accounts

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@example.com | admin123 |
| Staff | staff@example.com | staff123 |

---

## Database Connection

If you want to connect with a database tool:

- **Host:** localhost
- **Port:** 5432
- **Database:** assetdb
- **Username:** postgres
- **Password:** postgres

---

## Next Steps

1. ✅ Explore the dashboard
2. ✅ Create assets
3. ✅ Manage inventory
4. ✅ Run audits
5. ✅ Customize for your needs

---

## Need More Help?

- **Docker Setup:** See DOCKER_SETUP_GUIDE.md
- **All Options:** See DOCKER_OPTIONS.md
- **Troubleshooting:** See TROUBLESHOOTING.md
- **Login Issues:** See LOGIN_CHECKLIST.md

---

## Daily Usage

**Start working:**
```cmd
docker-compose up -d
```

**Stop working:**
```cmd
docker-compose down
```

**That's it!** Your data persists between sessions.
