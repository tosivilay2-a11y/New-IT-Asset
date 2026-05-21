@echo off
echo ========================================
echo Installing QR Code Package
echo ========================================
echo.

cd /d "%~dp0frontend"
echo Current directory: %CD%
echo.

echo Installing qrcode package...
call npm install qrcode --save

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Please restart your frontend server:
echo 1. Stop the current server (Ctrl+C)
echo 2. Run: npm start
echo.
pause
