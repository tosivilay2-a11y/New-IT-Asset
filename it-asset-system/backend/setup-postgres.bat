@echo off
echo ========================================
echo IT Asset System - PostgreSQL Setup
echo ========================================
echo.

echo [1/3] Installing dependencies...
call npm install
echo.

echo [2/3] Creating database tables...
call npm run db:setup
echo.

echo [3/3] Seeding initial data...
call npm run db:seed
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo You can now start the server with: npm run dev
echo.
pause
