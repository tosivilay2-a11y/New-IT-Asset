@echo off
echo ======================================================================
echo TESTING LOGIN
echo ======================================================================
echo.
echo Opening test page in your default browser...
echo.
start test-login.html
echo.
echo The test page should open in your browser.
echo Click "Test Login" button to test the backend login.
echo.
echo You should see:
echo   1. Backend health check - OK
echo   2. Login successful - with access token
echo   3. User info retrieved - with user details
echo.
echo If all 3 steps pass, the backend is working correctly.
echo The issue would be in the frontend React app.
echo.
echo ======================================================================
pause
