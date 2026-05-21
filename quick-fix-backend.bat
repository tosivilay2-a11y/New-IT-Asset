@echo off
echo ================================================
echo Quick Fix: Copy assetdb to it_asset_db
echo ================================================
echo.

docker-compose stop backend
docker exec -it asset-db psql -U postgres -c "DROP DATABASE IF EXISTS it_asset_db;"
docker exec -it asset-db psql -U postgres -c "CREATE DATABASE it_asset_db WITH TEMPLATE assetdb;"
docker-compose up -d backend

echo.
echo Done! Testing...
timeout /t 5 /nobreak >nul
curl http://localhost:8000/

echo.
pause
