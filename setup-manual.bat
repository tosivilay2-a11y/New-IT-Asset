@echo off
setlocal enabledelayedexpansion

echo ============================================================
echo Asset Management System - Manual Setup Script
echo ============================================================
echo.
echo This script will help you set up the application after
echo you have installed PostgreSQL manually.
echo.
echo Prerequisites:
echo - PostgreSQL installed and running
echo - Python 3.9+ installed
echo - Node.js 16+ installed
echo.
pause

:: Check PostgreSQL
echo.
echo [1/8] Checking PostgreSQL installation...
psql --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] PostgreSQL not found in PATH
    echo Please install PostgreSQL or add it to PATH
    echo Location: C:\Program Files\PostgreSQL\15\bin
    pause
    exit /b 1
)
echo [OK] PostgreSQL found

:: Check Python
echo.
echo [2/8] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found
    echo Please install Python 3.9+ from python.org
    pause
    exit /b 1
)
echo [OK] Python found

:: Check Node.js
echo.
echo [3/8] Checking Node.js installation...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js not found
    echo Please install Node.js from nodejs.org
    pause
    exit /b 1
)
echo [OK] Node.js found

:: Get database password
echo.
echo [4/8] Database Configuration
echo.
set /p DB_PASSWORD="Enter PostgreSQL password for 'postgres' user: "
if "!DB_PASSWORD!"=="" (
    echo [ERROR] Password cannot be empty
    pause
    exit /b 1
)

:: Create database
echo.
echo [5/8] Creating database 'assetdb'...
echo.
set PGPASSWORD=!DB_PASSWORD!
createdb -U postgres assetdb 2>nul
if %errorlevel% equ 0 (
    echo [OK] Database created successfully
) else (
    echo [INFO] Database might already exist, continuing...
)

:: Setup backend
echo.
echo [6/8] Setting up backend...
cd backend

:: Create .env file
echo Creating .env file...
(
echo DATABASE_URL=postgresql://postgres:!DB_PASSWORD!@localhost:5432/assetdb
echo SECRET_KEY=dev-secret-key-change-in-production-!RANDOM!
echo ALGORITHM=HS256
echo ACCESS_TOKEN_EXPIRE_MINUTES=30
) > .env
echo [OK] .env file created

:: Create virtual environment
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
)

:: Activate and install dependencies
echo Installing Python dependencies...
call venv\Scripts\activate.bat
pip install -r requirements.txt >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)
echo [OK] Dependencies installed

:: Run migrations
echo Running database migrations...
alembic upgrade head
if %errorlevel% neq 0 (
    echo [ERROR] Failed to run migrations
    echo Check your database connection
    pause
    exit /b 1
)
echo [OK] Migrations completed

:: Seed data
echo Seeding sample data...
python seed_data.py
if %errorlevel% neq 0 (
    echo [WARNING] Failed to seed data
    echo You may need to run this manually later
) else (
    echo [OK] Sample data created
)

:: Verify setup
echo.
echo Verifying backend setup...
python verify_setup.py
if %errorlevel% neq 0 (
    echo [WARNING] Verification found issues
    echo Please check the output above
    pause
)

cd ..

:: Setup frontend
echo.
echo [7/8] Setting up frontend...
cd frontend

if not exist node_modules (
    echo Installing Node.js dependencies...
    echo This may take 3-5 minutes...
    call npm install
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install frontend dependencies
        pause
        exit /b 1
    )
    echo [OK] Frontend dependencies installed
) else (
    echo [OK] Frontend dependencies already installed
)

cd ..

:: Create start scripts
echo.
echo [8/8] Creating start scripts...

:: Backend start script
(
echo @echo off
echo cd backend
echo call venv\Scripts\activate.bat
echo echo Starting backend server...
echo echo Backend will be available at http://localhost:8000
echo echo API Documentation at http://localhost:8000/docs
echo echo.
echo echo Press Ctrl+C to stop the server
echo echo.
echo uvicorn app.main:app --reload
) > start-backend.bat
echo [OK] Created start-backend.bat

:: Frontend start script
(
echo @echo off
echo cd frontend
echo echo Starting frontend server...
echo echo Frontend will be available at http://localhost:3000
echo echo.
echo echo Press Ctrl+C to stop the server
echo echo.
echo npm start
) > start-frontend.bat
echo [OK] Created start-frontend.bat

:: Combined start script
(
echo @echo off
echo echo Starting Asset Management System...
echo echo.
echo echo Starting backend...
echo start "Backend Server" cmd /k start-backend.bat
echo timeout /t 5 /nobreak ^>nul
echo echo Starting frontend...
echo start "Frontend Server" cmd /k start-frontend.bat
echo echo.
echo echo ============================================
echo echo Services are starting...
echo echo ============================================
echo echo.
echo echo Backend: http://localhost:8000
echo echo Frontend: http://localhost:3000
echo echo API Docs: http://localhost:8000/docs
echo echo.
echo echo Default Login:
echo echo Email: admin@example.com
echo echo Password: admin123
echo echo.
echo timeout /t 3 /nobreak ^>nul
echo start http://localhost:3000
) > start-app.bat
echo [OK] Created start-app.bat

echo.
echo ============================================================
echo Setup Complete!
echo ============================================================
echo.
echo Created helper scripts:
echo - start-backend.bat  : Start backend only
echo - start-frontend.bat : Start frontend only
echo - start-app.bat      : Start both services
echo.
echo Default Login Credentials:
echo Email: admin@example.com
echo Password: admin123
echo.
echo To start the application:
echo 1. Run: start-app.bat
echo 2. Or run start-backend.bat and start-frontend.bat separately
echo.
echo Press any key to start the application now...
pause >nul

start-app.bat
