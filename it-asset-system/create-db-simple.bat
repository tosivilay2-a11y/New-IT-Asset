@echo off
echo Creating it_asset_db database...
docker exec -it asset-db psql -U postgres -c "CREATE DATABASE it_asset_db;"
echo.
echo Done! Now run: cd backend ^&^& setup-complete.bat
pause
