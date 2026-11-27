@echo off
cd /d "%~dp0"

echo ==================================================
echo   MYERS502 - BASE64 CODEC SOURCE RUNNER
echo ==================================================

python "main.py"

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to run MYERS502 tool from: %~dp0
    pause
)