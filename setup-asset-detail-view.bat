@echo off
echo ========================================
echo Asset Detail View Setup
echo ========================================
echo.

echo Installing QR Code package...
cd frontend
call npm install qrcode
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo The Asset Detail View is now ready to use.
echo.
echo To test:
echo 1. Make sure backend is running on port 8000
echo 2. Make sure frontend is running on port 3000
echo 3. Go to http://localhost:3000/assets
echo 4. Click the eye icon on any asset
echo.
echo Press any key to exit...
pause > nul
