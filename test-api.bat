@echo off
echo Testing AI School Backend API
echo ==============================
echo.

echo Testing Health Endpoint...
curl -X GET http://localhost:5000/api/health
echo.
echo.

echo Testing Registration...
curl -X POST http://localhost:5000/api/auth/register ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"test@aischool.com\",\"password\":\"password123\",\"full_name\":\"Test User\",\"phone_number\":\"+1234567890\"}"
echo.
echo.

pause
