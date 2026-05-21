# Login Issue Checklist

Follow these steps in order to diagnose and fix login issues:

## ✅ Pre-Flight Checks

### 1. Is the backend running?
```bash
# Test backend
curl http://localhost:8000
```
**Expected**: `{"message":"Asset Management System API"}`

**If not working**:
- Docker: `docker-compose up -d backend`
- Manual: `cd backend && uvicorn app.main:app --reload`

### 2. Is the frontend running?
Open browser: http://localhost:3000

**If not working**:
- Docker: `docker-compose up -d frontend`
- Manual: `cd frontend && npm start`

### 3. Is the database running?
```bash
# Docker
docker-compose ps

# Manual - check PostgreSQL service
```

## ✅ Database Setup

### 4. Are database tables created?
```bash
# Docker
docker-compose exec backend python verify_setup.py

# Manual
cd backend
python verify_setup.py
```

**If tables missing**:
```bash
# Docker
docker-compose exec backend alembic upgrade head

# Manual
cd backend
alembic upgrade head
```

### 5. Are users created?
```bash
# Docker
docker-compose exec backend python seed_data.py

# Manual
cd backend
python seed_data.py
```

**Expected output**: "✓ Database seeded successfully!"

## ✅ Test Login

### 6. Test via API Documentation
1. Open: http://localhost:8000/docs
2. Find `/auth/login` endpoint
3. Click "Try it out"
4. Enter:
   - username: `admin@example.com`
   - password: `admin123`
5. Click "Execute"

**Expected**: Status 200 with `access_token`

### 7. Test via Frontend
1. Open: http://localhost:3000
2. Press F12 (open Developer Tools)
3. Go to Console tab
4. Enter credentials:
   - Email: `admin@example.com`
   - Password: `admin123`
5. Click Login

**Check Console for errors**

## ✅ Common Issues & Solutions

### Issue: "Cannot connect to server"
**Cause**: Backend not running or wrong URL

**Solution**:
1. Verify backend is running: http://localhost:8000
2. Check `frontend/src/services/api.js` has correct URL
3. Restart backend

### Issue: "Invalid email or password"
**Cause**: User doesn't exist or wrong credentials

**Solution**:
```bash
# Verify users exist
docker-compose exec backend python -c "
from app.core.database import SessionLocal
from app.models.user import User
db = SessionLocal()
users = db.query(User).all()
for u in users:
    print(f'{u.email} - {u.role}')
"
```

### Issue: "CORS policy" error
**Cause**: CORS not configured properly

**Solution**: Already configured in `backend/app/main.py`. Verify:
- Frontend runs on port 3000
- Backend runs on port 8000

### Issue: Database connection error
**Cause**: PostgreSQL not running or wrong credentials

**Solution**:
1. Check `.env` file in backend folder
2. Verify DATABASE_URL is correct
3. Test connection: `psql -U postgres -d assetdb`

## 🚀 Quick Reset (Nuclear Option)

If nothing works, reset everything:

```bash
# Stop and remove everything
docker-compose down -v

# Start fresh
docker-compose up -d

# Wait 15 seconds
timeout /t 15  # Windows
# sleep 15     # Linux/Mac

# Setup database
docker-compose exec backend alembic upgrade head
docker-compose exec backend python seed_data.py

# Verify
docker-compose exec backend python verify_setup.py
```

## 📝 Manual User Creation

If you need to create a user manually:

```bash
docker-compose exec backend python -c "
from app.core.database import SessionLocal
from app.core.security import get_password_hash
from app.models.user import User

db = SessionLocal()

# Create admin user
user = User(
    email='myemail@example.com',
    hashed_password=get_password_hash('mypassword'),
    full_name='My Name',
    role='admin'
)

db.add(user)
db.commit()
print('User created successfully!')
print('Email: myemail@example.com')
print('Password: mypassword')
"
```

## 🔍 Debug Mode

Enable detailed logging:

**Backend** - Check terminal where uvicorn is running
**Frontend** - Check browser console (F12)

Look for:
- Network errors (red in Network tab)
- Console errors (red in Console tab)
- Failed requests (status 400, 401, 500)

## 📞 Still Not Working?

1. Run verification script:
   ```bash
   docker-compose exec backend python verify_setup.py
   ```

2. Check logs:
   ```bash
   docker-compose logs backend
   docker-compose logs frontend
   ```

3. Verify all services are healthy:
   ```bash
   docker-compose ps
   ```

4. Test backend directly:
   ```bash
   curl -X POST "http://localhost:8000/auth/login" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=admin@example.com&password=admin123"
   ```

## ✨ Success Indicators

You should see:
- ✓ Backend responds at http://localhost:8000
- ✓ Frontend loads at http://localhost:3000
- ✓ API docs accessible at http://localhost:8000/docs
- ✓ Login redirects to dashboard
- ✓ Dashboard shows statistics

## 🎯 Default Credentials

After running `seed_data.py`:

**Admin Account**:
- Email: `admin@example.com`
- Password: `admin123`
- Role: admin

**Staff Account**:
- Email: `staff@example.com`
- Password: `staff123`
- Role: staff
