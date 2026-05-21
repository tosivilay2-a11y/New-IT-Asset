@echo off
echo ========================================
echo Verifying IT Asset Management Setup
echo ========================================
echo.

echo [1] Checking Docker...
docker --version
if errorlevel 1 (
    echo ERROR: Docker is not installed or not running!
    goto :end
)
echo.

echo [2] Checking PostgreSQL container...
docker ps | findstr postgres
if errorlevel 1 (
    echo ERROR: PostgreSQL container is not running!
    echo Run: docker-compose up -d db
    goto :end
)
echo.

echo [3] Checking database...
docker exec asset-db psql -U postgres -c "\l" | findstr it_asset_db
if errorlevel 1 (
    echo ERROR: Database 'it_asset_db' does not exist!
    echo Run: docker exec asset-db psql -U postgres -c "CREATE DATABASE it_asset_db;"
    goto :end
)
echo.

echo [4] Checking tables...
docker exec asset-db psql -U postgres -d it_asset_db -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';"
echo.

echo [5] Checking users...
docker exec asset-db psql -U postgres -d it_asset_db -c "SELECT username, email FROM users;"
echo.

echo [6] Checking Node.js...
cd backend
node --version
if errorlevel 1 (
    echo ERROR: Node.js is not installed!
    goto :end
)
echo.

echo [7] Checking dependencies...
if exist "node_modules" (
    echo Dependencies are installed
) else (
    echo ERROR: Dependencies not installed!
    echo Run: npm install
    goto :end
)
echo.

echo ========================================
echo All checks passed!
echo ========================================
echo.
echo You can now start the server with:
echo   cd backend
echo   npm run dev
echo.

:end
pause
