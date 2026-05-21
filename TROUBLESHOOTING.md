# Login Troubleshooting Guide

## Common Login Issues

### Issue 1: No users in database

**Problem**: You haven't seeded the database with user data.

**Solution**:
```bash
# If using Docker
docker-compose exec backend python seed_data.py

# If running manually
cd backend
python seed_data.py
```

**Default credentials after seeding**:
- Admin: `admin@example.com` / `admin123`
- Staff: `staff@example.com` / `staff123`

### Issue 2: Backend not running

**Check if backend is running**:
- Open browser: http://localhost:8000
- You should see: `{"message": "Asset Management System API"}`

**If not running**:
```bash
# Docker
docker-compose up -d backend

# Manual
cd backend
uvicorn app.main:app --reload
```

### Issue 3: Database not initialized

**Problem**: Database tables don't exist.

**Solution**:
```bash
# If using Docker
docker-compose exec backend alembic upgrade head

# If running manually
cd backend
alembic upgrade head
```

### Issue 4: CORS errors

**Problem**: Frontend can't connect to backend due to CORS.

**Check browser console** (F12) for errors like:
- "Access to XMLHttpRequest blocked by CORS policy"

**Solution**: Backend CORS is already configured for localhost:3000. Verify:
1. Backend is running on port 8000
2. Frontend is running on port 3000

### Issue 5: Wrong credentials

**Problem**: Using incorrect email/password.

**Solution - Create a new user manually**:

```bash
# Using Docker
docker-compose exec backend python -c "
from app.core.database import SessionLocal
from app.core.security import get_password_hash
from app.models.user import User

db = SessionLocal()
user = User(
    email='test@example.com',
    hashed_password=get_password_hash('test123'),
    full_name='Test User',
    role='admin'
)
db.add(user)
db.commit()
print('User created: test@example.com / test123')
"
```

### Issue 6: Database connection error

**Check .env file**:
```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/assetdb
SECRET_KEY=your-secret-key-change-this-in-production
```

**Verify PostgreSQL is running**:
```bash
# Windows
# Check Services for PostgreSQL

# Linux/Mac
sudo systemctl status postgresql

# Docker
docker-compose ps
```

## Step-by-Step Login Test

1. **Check backend is running**:
   ```bash
   curl http://localhost:8000
   # Should return: {"message":"Asset Management System API"}
   ```

2. **Check API docs**:
   - Open: http://localhost:8000/docs
   - Try the `/auth/login` endpoint directly

3. **Test login via API docs**:
   - Click on `/auth/login`
   - Click "Try it out"
   - Enter:
     - username: `admin@example.com`
     - password: `admin123`
   - Click "Execute"
   - Should return a token

4. **Check browser console**:
   - Open frontend: http://localhost:3000
   - Press F12 to open Developer Tools
   - Go to Console tab
   - Try to login
   - Check for error messages

5. **Check Network tab**:
   - In Developer Tools, go to Network tab
   - Try to login
   - Look for the `/auth/login` request
   - Check the response

## Quick Fix Commands

**Reset everything and start fresh**:

```bash
# Stop all services
docker-compose down -v

# Start services
docker-compose up -d

# Wait for database to be ready (10 seconds)
timeout /t 10  # Windows
# sleep 10     # Linux/Mac

# Run migrations
docker-compose exec backend alembic upgrade head

# Seed data
docker-compose exec backend python seed_data.py

# Check logs
docker-compose logs backend
docker-compose logs frontend
```

**Manual setup reset**:

```bash
# Backend
cd backend
# Drop and recreate database
dropdb assetdb
createdb assetdb

# Run migrations
alembic upgrade head

# Seed data
python seed_data.py

# Start server
uvicorn app.main:app --reload
```

## Still Having Issues?

1. **Check backend logs**:
   ```bash
   # Docker
   docker-compose logs -f backend
   
   # Manual - check terminal where uvicorn is running
   ```

2. **Check frontend logs**:
   ```bash
   # Docker
   docker-compose logs -f frontend
   
   # Manual - check terminal where npm start is running
   ```

3. **Verify database has users**:
   ```bash
   # Connect to database
   psql -U postgres -d assetdb
   
   # Check users
   SELECT email, role FROM users;
   
   # Exit
   \q
   ```

4. **Test backend directly with curl**:
   ```bash
   curl -X POST "http://localhost:8000/auth/login" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=admin@example.com&password=admin123"
   ```

## Contact Information

If you're still experiencing issues:
1. Check the error message in browser console
2. Check backend logs for detailed error information
3. Verify all services are running
4. Ensure database is properly initialized
