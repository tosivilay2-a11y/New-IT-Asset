@echo off
echo ========================================
echo SEEDING INITIAL DATA
echo ========================================
echo.

docker exec -it asset-backend python backend/seed_initial_data.py

echo.
echo ========================================
echo SEED COMPLETE
echo ========================================
echo.
echo Your system now has:
echo   - Countries, Provinces, Companies
echo   - User Types, Roles, Permissions
echo   - Asset Categories and Statuses
echo   - System Configuration
echo.
echo Ready to create assets!
echo.
pause
