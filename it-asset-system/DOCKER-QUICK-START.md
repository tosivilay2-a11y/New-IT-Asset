# 🚀 Docker Quick Start

## Start System
```bash
docker-start.bat
```

## Stop System
```bash
docker-stop.bat
```

## View Logs
```bash
docker-logs.bat
```

## Access Points
- **API**: http://localhost:5000
- **Health**: http://localhost:5000/health
- **Database**: localhost:5433

## Default Users
- **Admin**: admin@example.com / admin123
- **Manager**: manager@example.com / manager123
- **User**: user@example.com / user123

## Useful Commands
```bash
# Restart
docker-restart.bat

# Reset (deletes all data)
docker-reset.bat

# Database access
docker exec -it it-asset-db psql -U postgres -d it_asset_db

# View tables
docker exec -it it-asset-db psql -U postgres -d it_asset_db -c "\dt"
```

## Test API
```bash
# Health check
curl http://localhost:5000/health

# Login
curl -X POST http://localhost:5000/api/auth/login -H "Content-Type: application/json" -d "{\"email\":\"admin@example.com\",\"password\":\"admin123\"}"
```

---

**See [DOCKER-GUIDE.md](DOCKER-GUIDE.md) for full documentation.**
