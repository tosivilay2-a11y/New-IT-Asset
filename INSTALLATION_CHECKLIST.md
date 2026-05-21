# Installation Checklist - Manual Setup

Follow this checklist to install and configure everything manually.

## ☐ Phase 1: Install PostgreSQL

### Download and Install

1. ☐ Go to https://www.postgresql.org/download/windows/
2. ☐ Download PostgreSQL 15.x or 16.x installer
3. ☐ Run the installer
4. ☐ During installation:
   - ☐ Select all components (PostgreSQL Server, pgAdmin 4, Command Line Tools)
   - ☐ Set password for `postgres` user (write it down!)
   - ☐ Keep default port: 5432
   - ☐ Complete installation

### Verify Installation

5. ☐ Open Command Prompt
6. ☐ Run: `psql --version`
7. ☐ Should show: `psql (PostgreSQL) 15.x`
8. ☐ Check Windows Services:
   - ☐ Press Win+R, type `services.msc`
   - ☐ Find "postgresql-x64-15" service
   - ☐ Status should be "Running"

### Create Database

**Option A - Using pgAdmin:**
9. ☐ Open pgAdmin 4 from Start Menu
10. ☐ Connect to PostgreSQL 15 server (enter password)
11. ☐ Right-click "Databases" → Create → Database
12. ☐ Name: `assetdb`
13. ☐ Click Save

**Option B - Using Command Line:**
9. ☐ Open Command Prompt
10. ☐ Run: `createdb -U postgres assetdb`
11. ☐ Enter password when prompted

### Test Connection

12. ☐ Run: `psql -U postgres -d assetdb`
13. ☐ Enter password
14. ☐ Should see: `assetdb=#` prompt
15. ☐ Type `\q` to exit

**✓ PostgreSQL installation complete!**

---

## ☐ Phase 2: Install Python

### Download and Install

1. ☐ Go to https://www.python.org/downloads/
2. ☐ Download Python 3.9 or higher
3. ☐ Run installer
4. ☐ **IMPORTANT**: Check "Add Python to PATH"
5. ☐ Click "Install Now"
6. ☐ Wait for installation to complete

### Verify Installation

7. ☐ Open NEW Command Prompt
8. ☐ Run: `python --version`
9. ☐ Should show: `Python 3.x.x`
10. ☐ Run: `pip --version`
11. ☐ Should show pip version

**✓ Python installation complete!**

---

## ☐ Phase 3: Install Node.js

### Download and Install

1. ☐ Go to https://nodejs.org/
2. ☐ Download LTS version (20.x)
3. ☐ Run installer with default settings
4. ☐ Complete installation

### Verify Installation

5. ☐ Open NEW Command Prompt
6. ☐ Run: `node --version`
7. ☐ Should show: `v20.x.x`
8. ☐ Run: `npm --version`
9. ☐ Should show npm version

**✓ Node.js installation complete!**

---

## ☐ Phase 4: Setup Backend

### Navigate to Project

1. ☐ Open Command Prompt
2. ☐ Navigate to project: `cd path\to\asset-management\backend`

### Test Database Connection

3. ☐ Run: `python test_db_connection.py`
4. ☐ Enter your PostgreSQL password
5. ☐ Should show "Connection successful!"
6. ☐ Copy the DATABASE_URL shown

### Configure Environment

7. ☐ Copy .env.example: `copy .env.example .env`
8. ☐ Open .env file in text editor
9. ☐ Update DATABASE_URL with your password:
   ```
   DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/assetdb
   ```
10. ☐ Save and close .env file

### Create Virtual Environment

11. ☐ Run: `python -m venv venv`
12. ☐ Wait for completion (30 seconds)
13. ☐ Activate: `venv\Scripts\activate`
14. ☐ Should see `(venv)` in prompt

### Install Dependencies

15. ☐ Run: `pip install -r requirements.txt`
16. ☐ Wait for installation (2-3 minutes)
17. ☐ Should complete without errors

### Initialize Database

18. ☐ Run: `alembic upgrade head`
19. ☐ Should create all tables
20. ☐ Run: `python seed_data.py`
21. ☐ Should show "Database seeded successfully!"

### Verify Setup

22. ☐ Run: `python verify_setup.py`
23. ☐ All checks should pass with ✓
24. ☐ Should show default credentials

### Test Backend

25. ☐ Run: `uvicorn app.main:app --reload`
26. ☐ Should show "Application startup complete"
27. ☐ Open browser: http://localhost:8000
28. ☐ Should see: `{"message":"Asset Management System API"}`
29. ☐ Open: http://localhost:8000/docs
30. ☐ Should see API documentation
31. ☐ Press Ctrl+C to stop server

**✓ Backend setup complete!**

---

## ☐ Phase 5: Setup Frontend

### Navigate to Frontend

1. ☐ Open NEW Command Prompt
2. ☐ Navigate: `cd path\to\asset-management\frontend`

### Install Dependencies

3. ☐ Run: `npm install`
4. ☐ Wait for installation (3-5 minutes)
5. ☐ Should complete without errors

### Test Frontend

6. ☐ Run: `npm start`
7. ☐ Should automatically open browser
8. ☐ Or manually open: http://localhost:3000
9. ☐ Should see login page

**✓ Frontend setup complete!**

---

## ☐ Phase 6: Test Complete System

### Start Both Services

1. ☐ Terminal 1 (Backend):
   ```
   cd backend
   venv\Scripts\activate
   uvicorn app.main:app --reload
   ```

2. ☐ Terminal 2 (Frontend):
   ```
   cd frontend
   npm start
   ```

### Test Login

3. ☐ Open: http://localhost:3000
4. ☐ Enter credentials:
   - Email: `admin@example.com`
   - Password: `admin123`
5. ☐ Click "Login"
6. ☐ Should redirect to Dashboard
7. ☐ Should see statistics and data

### Test Features

8. ☐ Click "Assets" - should show asset list
9. ☐ Click "Add Asset" - form should appear
10. ☐ Click "Inventory" - should show inventory items
11. ☐ Click "Audits" - should show audit sessions
12. ☐ All pages load without errors

**✓ Complete system working!**

---

## ☐ Phase 7: Create Helper Scripts (Optional)

### Automated Setup

1. ☐ Run: `setup-manual.bat`
2. ☐ Follow prompts
3. ☐ Creates start scripts automatically

### Or Create Manually

**start-backend.bat:**
```batch
@echo off
cd backend
call venv\Scripts\activate.bat
uvicorn app.main:app --reload
```

**start-frontend.bat:**
```batch
@echo off
cd frontend
npm start
```

**start-app.bat:**
```batch
@echo off
start "Backend" cmd /k start-backend.bat
timeout /t 5 /nobreak >nul
start "Frontend" cmd /k start-frontend.bat
start http://localhost:3000
```

**✓ Helper scripts created!**

---

## Troubleshooting Checklist

### If PostgreSQL won't connect:
- ☐ Check service is running (services.msc)
- ☐ Verify password is correct
- ☐ Test with: `psql -U postgres -d assetdb`
- ☐ Check port 5432 is not blocked

### If backend won't start:
- ☐ Virtual environment activated? (see `(venv)` in prompt)
- ☐ Dependencies installed? (pip install -r requirements.txt)
- ☐ Database connection working? (python test_db_connection.py)
- ☐ Migrations run? (alembic upgrade head)
- ☐ Check .env file has correct DATABASE_URL

### If frontend won't start:
- ☐ Node modules installed? (npm install)
- ☐ Port 3000 available? (close other apps using it)
- ☐ Backend running on port 8000?

### If login fails:
- ☐ Backend running? (http://localhost:8000)
- ☐ Database seeded? (python seed_data.py)
- ☐ Using correct credentials? (admin@example.com / admin123)
- ☐ Check browser console (F12) for errors

---

## Quick Reference

### Daily Startup

**Terminal 1:**
```cmd
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload
```

**Terminal 2:**
```cmd
cd frontend
npm start
```

### Default Credentials

- **Admin**: admin@example.com / admin123
- **Staff**: staff@example.com / staff123

### Important URLs

- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Useful Commands

```cmd
# Test database connection
python backend/test_db_connection.py

# Verify setup
python backend/verify_setup.py

# Recreate database
dropdb -U postgres assetdb
createdb -U postgres assetdb
cd backend
alembic upgrade head
python seed_data.py

# Reset frontend
cd frontend
rmdir /s /q node_modules
del package-lock.json
npm install
```

---

## ✓ Installation Complete!

You now have:
- ✓ PostgreSQL database running
- ✓ Python backend configured
- ✓ React frontend configured
- ✓ Sample data loaded
- ✓ Application accessible

**Next Steps:**
1. Customize the application for your needs
2. Add more features
3. Configure for production deployment
4. Set up regular backups

**Need Help?**
- Check TROUBLESHOOTING.md
- Check LOGIN_CHECKLIST.md
- Run verify_setup.py
- Check application logs
