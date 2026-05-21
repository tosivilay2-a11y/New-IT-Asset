@echo off
echo ========================================
echo QUICK FIX - Database Schema
echo ========================================
echo.
echo This will fix the database schema error.
echo All data will be lost!
echo.
echo Press Ctrl+C to cancel, or
pause
echo.

cd backend
call venv\Scripts\activate

echo Recreating tables...
python recreate_tables.py --yes

echo.
echo Seeding data...
python seed_location_hierarchy.py
python seed_asset_control_data.py
python create_test_user.py

echo.
echo ========================================
echo Database Fixed!
echo ========================================
echo.
echo Now start the backend:
echo   start-backend-server.bat
echo.
pause
