# Docker Setup Options

Choose the setup that works best for you.

## Option 1: All Services in Docker (Recommended for Beginners)

**What runs in Docker:**
- ✅ PostgreSQL Database
- ✅ Backend API
- ✅ Frontend React App

**Advantages:**
- Everything in one command
- No manual installations needed
- Consistent environment

**Setup:**
```cmd
docker-setup-complete.bat
```

**Or manually:**
```cmd
docker-compose build
docker-compose up -d
timeout /t 20
docker-compose exec -T backend alembic upgrade head
docker-compose exec -T backend python seed_data.py
```

**Access:**
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- Database: localhost:5432

---

## Option 2: Backend + Database in Docker, Frontend Manual (Recommended for Development)

**What runs in Docker:**
- ✅ PostgreSQL Database
- ✅ Backend API

**What runs manually:**
- ⚙️ Frontend (npm start)

**Advantages:**
- Faster frontend development (hot reload works better)
- Easier to debug frontend
- Less Docker resource usage

**Setup:**

**Step 1 - Start Backend & Database:**
```cmd
start-backend-docker.bat
```

**Or manually:**
```cmd
docker-compose -f docker-compose-backend-only.yml up -d --build
timeout /t 15
docker-compose -f docker-compose-backend-only.yml exec -T backend alembic upgrade head
docker-compose -f docker-compose-backend-only.yml exec -T backend python seed_data.py
```

**Step 2 - Start Frontend (in new terminal):**
```cmd
cd frontend
npm install
npm start
```

**Access:**
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- Database: localhost:5432

---

## Option 3: Database Only in Docker, Backend + Frontend Manual

**What runs in Docker:**
- ✅ PostgreSQL Database only

**What runs manually:**
- ⚙️ Backend (uvicorn)
- ⚙️ Frontend (npm start)

**Advantages:**
- Maximum development flexibility
- Easiest debugging
- Fastest code changes

**Setup:**

**Step 1 - Start Database:**
```cmd
docker run -d ^
  --name asset-postgres ^
  -e POSTGRES_USER=postgres ^
  -e POSTGRES_PASSWORD=postgres ^
  -e POSTGRES_DB=assetdb ^
  -p 5432:5432 ^
  postgres:15
```

**Step 2 - Start Backend (in new terminal):**
```cmd
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
python seed_data.py
uvicorn app.main:app --reload
```

**Step 3 - Start Frontend (in new terminal):**
```cmd
cd frontend
npm install
npm start
```

**Access:**
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- Database: localhost:5432

---

## Quick Command Reference

### Option 1 (All in Docker)

```cmd
# Start
docker-compose up -d

# Stop
docker-compose down

# View logs
docker-compose logs -f

# Restart
docker-compose restart

# Rebuild
docker-compose build --no-cache
docker-compose up -d
```

### Option 2 (Backend + DB in Docker)

```cmd
# Start
docker-compose -f docker-compose-backend-only.yml up -d

# Stop
docker-compose -f docker-compose-backend-only.yml down

# View logs
docker-compose -f docker-compose-backend-only.yml logs -f

# Frontend (separate terminal)
cd frontend
npm start
```

### Option 3 (DB Only in Docker)

```cmd
# Start database
docker run -d --name asset-postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 postgres:15

# Stop database
docker stop asset-postgres

# Remove database
docker rm asset-postgres

# Backend (separate terminal)
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload

# Frontend (separate terminal)
cd frontend
npm start
```

---

## Troubleshooting

### Port Already in Use

**Check what's using the port:**
```cmd
netstat -ano | findstr :8000
netstat -ano | findstr :3000
netstat -ano | findstr :5432
```

**Kill the process:**
```cmd
taskkill /PID <PID_NUMBER> /F
```

### Docker Build Fails

```cmd
# Clean everything and rebuild
docker-compose down -v
docker system prune -a
docker-compose build --no-cache
docker-compose up -d
```

### Database Connection Error

```cmd
# Check database is running
docker ps

# Check database logs
docker logs asset-db

# Restart database
docker restart asset-db
```

### Backend Won't Start

```cmd
# Check backend logs
docker logs asset-backend

# Rebuild backend
docker-compose build backend
docker-compose up -d backend

# Check if database is ready
docker-compose exec backend python -c "from app.core.database import engine; engine.connect()"
```

### Frontend Won't Start

```cmd
# Clear node modules
cd frontend
rmdir /s /q node_modules
del package-lock.json
npm install

# Or in Docker
docker-compose build frontend
docker-compose up -d frontend
```

---

## Which Option Should I Choose?

### Choose Option 1 (All in Docker) if:
- ✅ You're new to development
- ✅ You want the simplest setup
- ✅ You don't need to modify code frequently
- ✅ You want everything isolated

### Choose Option 2 (Backend + DB in Docker) if:
- ✅ You're developing the frontend
- ✅ You want fast frontend hot-reload
- ✅ You need to debug frontend code
- ✅ You have Node.js installed

### Choose Option 3 (DB Only in Docker) if:
- ✅ You're an experienced developer
- ✅ You want maximum control
- ✅ You need to debug backend code
- ✅ You have Python and Node.js installed

---

## Resource Usage

| Option | Docker Memory | Docker CPU | Disk Space |
|--------|---------------|------------|------------|
| Option 1 | ~2 GB | Medium | ~2 GB |
| Option 2 | ~1 GB | Low | ~1 GB |
| Option 3 | ~500 MB | Very Low | ~500 MB |

---

## Default Credentials

All options use the same credentials:

**Application Login:**
- Email: admin@example.com
- Password: admin123

**Database:**
- Host: localhost
- Port: 5432
- Database: assetdb
- Username: postgres
- Password: postgres

---

## Helper Scripts

| Script | Purpose |
|--------|---------|
| `docker-setup-complete.bat` | Setup Option 1 (all services) |
| `start-backend-docker.bat` | Setup Option 2 (backend + db) |
| `docker-start.bat` | Quick start all services |
| `docker-stop.bat` | Stop all services |
| `docker-reset.bat` | Reset everything |
| `docker-logs.bat` | View logs |
| `fix-backend.bat` | Fix backend issues |

---

## Next Steps

After choosing and setting up your option:

1. ✅ Access http://localhost:3000
2. ✅ Login with admin@example.com / admin123
3. ✅ Explore the application
4. ✅ Start developing!

For more help, see:
- DOCKER_SETUP_GUIDE.md - Detailed Docker guide
- DOCKER_QUICK_REFERENCE.md - Quick commands
- TROUBLESHOOTING.md - Common issues
