@echo off
echo ================================================
echo IT Asset Management - Complete Setup
echo ================================================
echo.

cd /d "%~dp0"

echo Step 1: Installing dependencies...
echo ================================================
call npm install
if errorlevel 1 (
    echo.
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo.
echo SUCCESS: Dependencies installed
echo.

echo Step 2: Creating database tables...
echo ================================================
call npm run db:setup
if errorlevel 1 (
    echo.
    echo ERROR: Failed to create database tables
    pause
    exit /b 1
)
echo.
echo SUCCESS: Database tables created
echo.

echo Step 3: Seeding initial data...
echo ================================================
call npm run db:seed
if errorlevel 1 (
    echo.
    echo ERROR: Failed to seed data
    pause
    exit /b 1
)
echo.

echo ================================================
echo SETUP COMPLETED SUCCESSFULLY!
echo ================================================
echo.
echo Default Users:
echo   Admin:   admin@example.com / admin123
echo   Manager: manager@example.com / manager123
echo   User:    user@example.com / user123
echo.
echo To start the server, run: npm run dev
echo ================================================
echo.
pause
