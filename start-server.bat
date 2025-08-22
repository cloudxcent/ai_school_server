@echo off
title AI School Backend Server
echo.
echo ================================================================
echo                    AI School Backend Server
echo ================================================================
echo.
echo This script will start the AI School backend server.
echo Make sure you have configured your .env file with Azure credentials.
echo.

cd /d "%~dp0backend"

if not exist ".env" (
    echo WARNING: .env file not found!
    echo Please copy .env.example to .env and update with your Azure credentials.
    echo.
    pause
    exit /b 1
)

echo Starting server...
echo.
python app.py

echo.
echo Server stopped.
pause
