@echo off
echo Starting AI School Backend Tests...
echo =====================================

cd /d "d:\AI School App for TV and Mobile\ai_school\backend"

echo.
echo Running test_setup.py...
python test_setup.py

echo.
echo Running test_azure_connection.py...
python test_azure_connection.py

echo.
echo Running simple_test.py...
python simple_test.py

echo.
echo Running test_kids_profiles.py...
python test_kids_profiles.py

echo.
echo Running test_profiles.py...
python test_profiles.py

echo.
echo Running test_api.py...
python test_api.py

echo.
echo Running test_fastapi.py...
python test_fastapi.py

echo.
echo All tests completed!
pause
