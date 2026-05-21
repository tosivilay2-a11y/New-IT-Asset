@echo off
echo ========================================
echo Fix Database and Start Backend
echo ========================================
echo.
echo This will:
echo   1. Drop all existing tables
echo   2. Create new tables with correct schema
echo   3. Seed initial data
echo   4. Start backend server
echo.
echo WARNING: All existing data will be lost!
echo.
pause
echo.

cd backend
call venv\Scripts\activate

echo Step 1: Recreating database tables...
echo yes | python recreate_tables.py
echo.

echo Step 2: Seeding location hierarchy...
python seed_location_hierarchy.py
echo.

echo Step 3: Seeding asset control data...
python seed_asset_control_data.py
echo.

echo Step 4: Creating test user...
python create_test_user.py
echo.

echo Step 5: Starting backend server...
echo.
echo Backend will start on http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.
uvicorn app.main:app --reload --port 8000
