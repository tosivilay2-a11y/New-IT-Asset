@echo off
echo Fixing backend and initializing database...
echo.

echo Step 1: Rebuilding backend with correct dependencies...
docker-compose build backend

echo.
echo Step 2: Restarting all services...
docker-compose down
docker-compose up -d

echo.
echo Step 3: Waiting for services to start (15 seconds)...
timeout /t 15 /nobreak >nul

echo.
echo Step 4: Initializing database...
docker-compose exec -T backend alembic upgrade head

echo.
echo Step 5: Seeding sample data...
docker-compose exec -T backend python seed_data.py

echo.
echo ============================================
echo Setup Complete!
echo ============================================
echo.
echo You can now login at: http://localhost:3000
echo Email: admin@example.com
echo Password: admin123
echo.
pause
