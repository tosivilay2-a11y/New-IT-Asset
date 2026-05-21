@echo off
echo ========================================
echo Verifying Admin Routes
echo ========================================
echo.

echo Testing backend endpoints...
echo.

echo 1. Health Check:
curl -s http://localhost:8000/health
echo.
echo.

echo 2. Countries Endpoint:
curl -s http://localhost:8000/countries
echo.
echo.

echo 3. Main Categories Endpoint:
curl -s http://localhost:8000/main-categories
echo.
echo.

echo 4. Provinces Endpoint:
curl -s http://localhost:8000/provinces
echo.
echo.

echo 5. Companies Endpoint:
curl -s http://localhost:8000/companies
echo.
echo.

echo ========================================
echo Verification Complete
echo ========================================
echo.
echo If you see JSON data above (not "Not Found"):
echo   ✅ Backend routes are loaded correctly!
echo   ✅ Admin page should work now!
echo.
echo If you see "Not Found" errors:
echo   ❌ Backend needs to be restarted
echo   ❌ Run: restart-backend.bat
echo.
echo Next steps:
echo   1. Open: http://localhost:3000/admin/config
echo   2. Try adding a category
echo   3. Should work without errors!
echo.
pause
