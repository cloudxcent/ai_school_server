@echo off
title AI School FastAPI Backend Server
echo.
echo ================================================================
echo                    AI School FastAPI Backend Server
echo ================================================================
echo.
echo This script will start the AI School FastAPI backend server.
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

echo Starting FastAPI server...
echo Server will be available at: http://localhost:8000
echo Interactive API docs at: http://localhost:8000/docs
echo.
python fastapi_app.py

echo.
echo Server stopped.
pause
