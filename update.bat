@echo off
echo ==========================================
echo  Git Auto-Sync Script
echo ==========================================
echo.

:: Configure git user
git config user.name "njspeeder"
git config user.email "nerochristianjr2020@gmail.com"

:: Add all changes
echo Adding all changes...
git add -A

:: Get commit message
set /p message="Enter commit message (or press Enter for default): "
if "%message%"=="" set message=Update %date% %time%

:: Commit changes
echo Committing...
git commit -m "%message%"

:: Push to remote
echo Pushing to GitHub...
git push origin main

echo.
echo ==========================================
echo  Done!
echo ==========================================
pause
