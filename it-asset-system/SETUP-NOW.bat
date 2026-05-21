@echo off
echo ================================================
echo IT ASSET MANAGEMENT SYSTEM - COMPLETE SETUP
echo ================================================
echo.
echo This script will:
echo   1. Create the database (it_asset_db)
echo   2. Install backend dependencies
echo   3. Create all database tables
echo   4. Seed initial data
echo   5. Start the server
echo.
echo Prerequisites:
echo   - PostgreSQL running in Docker (postgres-db container)
echo   - Node.js installed
echo.
pause

cd /d "%~dp0"

echo.
echo ================================================
echo STEP 1: Creating Database
echo ================================================
call create-database-docker.bat
if errorlevel 1 (
    echo.
    echo Note: Continuing even if database already exists...
)

echo.
echo ================================================
echo STEP 2: Setting up Backend
echo ================================================
cd backend
call setup-complete.bat
if errorlevel 1 (
    echo.
    echo ERROR: Backend setup failed
    cd ..
    pause
    exit /b 1
)

echo.
echo ================================================
echo SETUP COMPLETED SUCCESSFULLY!
echo ================================================
echo.
echo Your IT Asset Management System is ready!
echo.
echo Default Users:
echo   Admin:   admin@example.com / admin123
echo   Manager: manager@example.com / manager123
echo   User:    user@example.com / user123
echo.
echo Server is starting on http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo ================================================
echo.

REM Server will start from the setup-complete.bat script
pause
