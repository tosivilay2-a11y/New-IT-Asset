# Docker Quick Reference

## One-Command Setup

```cmd
docker-start.bat
```

That's it! Everything will be set up automatically.

## Helper Scripts

| Script | Purpose |
|--------|---------|
| `docker-start.bat` | Start all services and initialize database |
| `docker-stop.bat` | Stop all services |
| `docker-reset.bat` | Reset everything (deletes all data) |
| `docker-logs.bat` | View service logs |

## Manual Commands

### Starting & Stopping

```cmd
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# Stop and remove all data
docker-compose down -v

# Restart all services
docker-compose restart

# Restart specific service
docker-compose restart backend
```

### Viewing Status

```cmd
# Check service status
docker-compose ps

# View logs (last 100 lines)
docker-compose logs --tail=100

# Follow logs in real-time
docker-compose logs -f

# View specific service logs
docker-compose logs backend
docker-compose logs frontend
docker-compose logs db
```

### Database Operations

```cmd
# Initialize database (create tables)
docker-compose exec backend alembic upgrade head

# Seed sample data
docker-compose exec backend python seed_data.py

# Verify setup
docker-compose exec backend python verify_setup.py

# Connect to PostgreSQL
docker-compose exec db psql -U postgres -d assetdb

# Backup database
docker-compose exec db pg_dump -U postgres assetdb > backup.sql

# Restore database
docker-compose exec -T db psql -U postgres assetdb < backup.sql
```

### Development

```cmd
# Rebuild services after code changes
docker-compose up -d --build

# View backend logs
docker-compose logs -f backend

# View frontend logs
docker-compose logs -f frontend

# Access backend container shell
docker-compose exec backend bash

# Access database container shell
docker-compose exec db bash

# Run Python command in backend
docker-compose exec backend python -c "print('Hello')"
```

## URLs

| Service | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| API Documentation | http://localhost:8000/docs |
| Alternative API Docs | http://localhost:8000/redoc |

## Default Credentials

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@example.com | admin123 |
| Staff | staff@example.com | staff123 |

## Database Connection

| Parameter | Value |
|-----------|-------|
| Host | localhost |
| Port | 5432 |
| Database | assetdb |
| Username | postgres |
| Password | postgres |

## Troubleshooting

### Services won't start

```cmd
# Check Docker is running
docker ps

# View error logs
docker-compose logs

# Full reset
docker-compose down -v
docker-compose up -d
```

### Port already in use

```cmd
# Find process using port
netstat -ano | findstr :8000

# Kill process
taskkill /PID <PID> /F

# Or change port in docker-compose.yml
```

### Database connection error

```cmd
# Check database is running
docker-compose ps db

# Restart database
docker-compose restart db

# Wait longer for database
timeout /t 30
docker-compose exec backend alembic upgrade head
```

### Can't login

```cmd
# Reseed database
docker-compose exec backend python seed_data.py

# Check backend logs
docker-compose logs backend

# Verify setup
docker-compose exec backend python verify_setup.py
```

## Common Workflows

### Daily Development

**Start working:**
```cmd
docker-compose up -d
```

**Stop working:**
```cmd
docker-compose down
```

### After Code Changes

**Backend changes:**
- Changes auto-reload, no restart needed
- If dependencies changed: `docker-compose up -d --build backend`

**Frontend changes:**
- Changes auto-reload, no restart needed
- If dependencies changed: `docker-compose up -d --build frontend`

**Database schema changes:**
```cmd
docker-compose exec backend alembic revision --autogenerate -m "description"
docker-compose exec backend alembic upgrade head
```

### Complete Reset

```cmd
docker-reset.bat
```

Or manually:
```cmd
docker-compose down -v
docker-compose up -d
timeout /t 15
docker-compose exec backend alembic upgrade head
docker-compose exec backend python seed_data.py
```

## Docker Desktop

### Check Status
- Look for whale icon in system tray
- Icon should be steady (not animated)
- Right-click icon → Dashboard to see containers

### Increase Resources
1. Open Docker Desktop
2. Settings → Resources
3. Increase CPU/Memory if needed
4. Apply & Restart

### Clean Up Space
```cmd
# Remove unused images
docker image prune

# Remove unused volumes
docker volume prune

# Remove everything unused
docker system prune -a
```

## File Locations

### Configuration
- `docker-compose.yml` - Service configuration
- `backend/.env` - Backend environment (auto-generated)
- `backend/Dockerfile` - Backend container definition
- `frontend/Dockerfile` - Frontend container definition

### Data
- Database data: Docker volume `postgres_data`
- Backend code: `./backend` (mounted)
- Frontend code: `./frontend` (mounted)

## Tips

✓ **Always use `docker-compose`** - Don't use `docker run` directly
✓ **Check logs first** - Most issues show up in logs
✓ **Wait for database** - Give it 15 seconds after starting
✓ **Use helper scripts** - Easier than remembering commands
✓ **Keep Docker Desktop running** - Required for containers to work

## Getting Help

1. Run: `docker-compose logs`
2. Check: `docker-compose ps`
3. Try: `docker-compose restart`
4. Reset: `docker-reset.bat`
5. See: DOCKER_SETUP_GUIDE.md for detailed help
