@echo off
echo ========================================
echo   AI School - Fresh GitHub Push Script
echo ========================================
echo.

cd /d "d:\AI School App for TV and Mobile\ai_school"

echo Current directory: %CD%
echo.

echo Step 1: Checking Git status...
git status
echo.

echo Step 2: Setting up Git configuration...
git config user.name "cloudxcent"
git config user.email "your-email@example.com"
echo.

echo Step 3: Adding all files...
git add .
echo.

echo Step 4: Committing changes...
git commit -m "Complete AI School Platform - Android app with Python Flask backend and Azure integration"
echo.

echo Step 5: Checking for existing remote...
git remote -v
echo.

echo Step 6: Removing existing remote (if any)...
git remote remove origin 2>nul
echo.

echo Step 7: Adding GitHub remote repository...
git remote add origin https://github.com/cloudxcent/ai_school_server.git
echo.

echo Step 8: Setting main branch...
git branch -M main
echo.

echo Step 9: Pushing to GitHub...
git push -u origin main
echo.

echo ========================================
echo Push completed! Check your GitHub repository:
echo https://github.com/cloudxcent/ai_school_server
echo ========================================
pause
