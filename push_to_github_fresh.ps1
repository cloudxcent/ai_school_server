# AI School - Fresh GitHub Push Script (PowerShell)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   AI School - Fresh GitHub Push Script" -ForegroundColor Cyan  
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Navigate to project directory
Set-Location "d:\AI School App for TV and Mobile\ai_school"
Write-Host "Current directory: $(Get-Location)" -ForegroundColor Yellow
Write-Host ""

# Step 1: Initialize git if needed
Write-Host "Step 1: Initializing Git repository..." -ForegroundColor Green
git init
Write-Host ""

# Step 2: Set Git configuration
Write-Host "Step 2: Setting up Git configuration..." -ForegroundColor Green
git config user.name "cloudxcent"
git config user.email "cloudxcent@github.com"
Write-Host ""

# Step 3: Add all files
Write-Host "Step 3: Adding all files..." -ForegroundColor Green
git add .
Write-Host ""

# Step 4: Check status
Write-Host "Step 4: Checking Git status..." -ForegroundColor Green
git status --short
Write-Host ""

# Step 5: Commit changes
Write-Host "Step 5: Committing changes..." -ForegroundColor Green
git commit -m "Complete AI School Platform - Android app with Python Flask backend and Azure integration"
Write-Host ""

# Step 6: Remove existing remote (if any)
Write-Host "Step 6: Removing existing remote (if any)..." -ForegroundColor Green
try {
    git remote remove origin
} catch {
    Write-Host "No existing remote to remove" -ForegroundColor Gray
}
Write-Host ""

# Step 7: Add GitHub remote
Write-Host "Step 7: Adding GitHub remote repository..." -ForegroundColor Green
git remote add origin https://github.com/cloudxcent/ai_school_server.git
Write-Host ""

# Step 8: Set main branch
Write-Host "Step 8: Setting main branch..." -ForegroundColor Green
git branch -M main
Write-Host ""

# Step 9: Push to GitHub
Write-Host "Step 9: Pushing to GitHub..." -ForegroundColor Green
git push -u origin main
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Push completed! Check your GitHub repository:" -ForegroundColor Green
Write-Host "https://github.com/cloudxcent/ai_school_server" -ForegroundColor Blue
Write-Host "========================================" -ForegroundColor Cyan

Read-Host "Press Enter to continue..."
