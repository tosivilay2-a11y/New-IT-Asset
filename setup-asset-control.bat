@echo off
echo ========================================
echo Setup Asset Control Features
echo ========================================
echo.

echo This will:
echo   1. Create database tables
echo   2. Seed asset statuses and departments
echo   3. Verify setup
echo.

cd backend
call venv\Scripts\activate

echo Step 1: Creating database tables...
python -c "from app.core.database import Base, engine; from app.models import Department, AssetStatus, AssetTransfer; Base.metadata.create_all(bind=engine)"
echo ✓ Tables created
echo.

echo Step 2: Seeding asset control data...
python seed_asset_control_data.py
echo.

echo Step 3: Verifying setup...
echo.
echo Testing departments endpoint:
curl -s http://localhost:8000/departments
echo.
echo.
echo Testing asset statuses endpoint:
curl -s http://localhost:8000/asset-statuses
echo.
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo   1. Restart backend: restart-backend.bat
echo   2. Check API docs: http://localhost:8000/docs
echo   3. Read guide: ASSET-CONTROL-FEATURES.md
echo.
pause
