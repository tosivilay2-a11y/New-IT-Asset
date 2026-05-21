# 🐳 Docker Setup Guide - IT Asset Management System

## Quick Start

### One Command to Start Everything
```bash
docker-start.bat
```

That's it! The system will:
1. Build the backend container
2. Start PostgreSQL with `it_asset_db` database
3. Create all 30 tables automatically
4. Seed initial data (users, categories, etc.)
5. Start the API server

---

## 🎯 What Gets Created

### Containers
- **it-asset-db**: PostgreSQL 15 database
- **it-asset-backend**: Node.js Express API

### Network
- **it-asset-network**: Bridge network for container communication

### Volumes
- **it_asset_postgres_data**: Persistent database storage

### Ports
- **5433**: PostgreSQL (mapped to avoid conflict with port 5432)
- **5000**: Backend API

---

## 📋 Available Commands

### Start System
```bash
docker-start.bat
```
Builds and starts all containers.

### Stop System
```bash
docker-stop.bat
```
Stops all containers (data is preserved).

### View Logs
```bash
docker-logs.bat
```
Shows real-time logs from all containers.

### Restart System
```bash
docker-restart.bat
```
Stops and starts containers (useful after code changes).

### Reset System
```bash
docker-reset.bat
```
⚠️ **WARNING**: Deletes all data and starts fresh!

### Manual Commands
```bash
# Start
docker-compose up -d

# Stop
docker-compose down

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend

# Rebuild
docker-compose up -d --build

# Check status
docker-compose ps
```

---

## 🔐 Default Users

After startup, login with:

| Email                  | Password    | Role    |
|------------------------|-------------|---------|
| admin@example.com      | admin123    | Admin   |
| manager@example.com    | manager123  | Manager |
| user@example.com       | user123     | User    |

---

## 🧪 Test the System

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

## 🗄️ Database Access

### Connect to PostgreSQL
```bash
docker exec -it it-asset-db psql -U postgres -d it_asset_db
```

### List Tables
```bash
docker exec -it it-asset-db psql -U postgres -d it_asset_db -c "\dt"
```

### View Users
```bash
docker exec -it it-asset-db psql -U postgres -d it_asset_db -c "SELECT userid, email, firstname, lastname, usertype FROM users;"
```

### Backup Database
```bash
docker exec -it it-asset-db pg_dump -U postgres it_asset_db > backup.sql
```

### Restore Database
```bash
docker exec -i it-asset-db psql -U postgres it_asset_db < backup.sql
```

---

## 📁 Project Structure

```
it-asset-system/
├── docker-compose.yml          # Docker configuration
├── docker-start.bat           # Start system
├── docker-stop.bat            # Stop system
├── docker-logs.bat            # View logs
├── docker-restart.bat         # Restart system
├── docker-reset.bat           # Reset everything
└── backend/
    ├── Dockerfile             # Backend container config
    ├── .dockerignore          # Files to exclude
    ├── .env                   # Docker environment
    ├── .env.local             # Local development
    └── scripts/
        ├── schema-postgres.sql    # Auto-runs on init
        └── seedData.js           # Auto-runs on startup
```

---

## 🔧 Configuration

### Environment Variables

**Docker (.env)**
```env
DB_HOST=db                    # Container name
DB_PORT=5432                  # Internal port
DB_DATABASE=it_asset_db
DB_USER=postgres
DB_PASSWORD=postgres
```

**Local Development (.env.local)**
```env
DB_HOST=localhost             # Localhost
DB_PORT=5433                  # External port
DB_DATABASE=it_asset_db
DB_USER=postgres
DB_PASSWORD=postgres
```

### Port Configuration

If port 5433 or 5000 is already in use, edit `docker-compose.yml`:

```yaml
services:
  db:
    ports:
      - "5434:5432"  # Change 5433 to 5434
  
  backend:
    ports:
      - "5001:5000"  # Change 5000 to 5001
```

---

## 🐛 Troubleshooting

### Container Won't Start
```bash
# Check logs
docker-compose logs

# Check specific service
docker-compose logs backend
docker-compose logs db
```

### Database Connection Failed
```bash
# Check if database is ready
docker exec -it it-asset-db pg_isready -U postgres

# Check database exists
docker exec -it it-asset-db psql -U postgres -c "\l"
```

### Port Already in Use
```bash
# Check what's using the port
netstat -ano | findstr :5000
netstat -ano | findstr :5433

# Kill the process or change port in docker-compose.yml
```

### Backend Not Responding
```bash
# Restart backend only
docker-compose restart backend

# Rebuild backend
docker-compose up -d --build backend
```

### Reset Everything
```bash
# Nuclear option - removes everything
docker-compose down -v --rmi local
docker-start.bat
```

---

## 🔄 Development Workflow

### Making Code Changes

1. Edit files in `backend/src/`
2. Changes are reflected immediately (nodemon watches files)
3. If changes don't appear, restart:
   ```bash
   docker-compose restart backend
   ```

### Adding Dependencies

1. Edit `backend/package.json`
2. Rebuild container:
   ```bash
   docker-compose up -d --build backend
   ```

### Database Schema Changes

1. Edit `backend/scripts/schema-postgres.sql`
2. Reset database:
   ```bash
   docker-reset.bat
   ```

---

## 📊 Monitoring

### Check Container Status
```bash
docker-compose ps
```

### Check Resource Usage
```bash
docker stats
```

### Check Container Health
```bash
docker inspect it-asset-backend --format='{{.State.Health.Status}}'
docker inspect it-asset-db --format='{{.State.Health.Status}}'
```

---

## 🚀 Production Deployment

For production, update:

1. **Change secrets** in `.env`:
   ```env
   JWT_SECRET=your-production-secret-key-here
   POSTGRES_PASSWORD=strong-password-here
   ```

2. **Remove dev tools** from Dockerfile:
   ```dockerfile
   CMD ["npm", "start"]  # Instead of npm run dev
   ```

3. **Add reverse proxy** (nginx/traefik)

4. **Enable SSL/TLS**

5. **Set up backups**

---

## 📚 Additional Resources

- **Docker Compose Docs**: https://docs.docker.com/compose/
- **PostgreSQL Docker**: https://hub.docker.com/_/postgres
- **Node.js Docker**: https://hub.docker.com/_/node

---

## ✅ Success Checklist

- [ ] Run `docker-start.bat`
- [ ] Wait for "Services Status" message
- [ ] Test health check: `curl http://localhost:5000/health`
- [ ] Test login with admin@example.com
- [ ] View logs: `docker-logs.bat`
- [ ] Access database: `docker exec -it it-asset-db psql -U postgres -d it_asset_db`

---

**Ready to start? Run `docker-start.bat` now!** 🎉
