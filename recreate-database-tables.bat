@echo off
echo ========================================
echo Recreate Database Tables
echo ========================================
echo.
echo WARNING: This will drop all existing tables!
echo WARNING: All data will be lost!
echo.
pause
echo.

cd backend
call venv\Scripts\activate
python recreate_tables.py

echo.
echo ========================================
echo Next Steps
echo ========================================
echo.
echo 1. Seed location hierarchy:
echo    python seed_location_hierarchy.py
echo.
echo 2. Seed asset control data:
echo    python seed_asset_control_data.py
echo.
echo 3. Create test user:
echo    python create_test_user.py
echo.
echo 4. Restart backend:
echo    restart-backend.bat
echo.
pause
