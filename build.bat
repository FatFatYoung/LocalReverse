@echo off
echo ========================================
echo LocalReverse - Build Script
echo ========================================
echo.

echo [1/4] Cleaning old files...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist "*.spec" del /q "*.spec"
echo [OK] Cleaned
echo.

echo [2/4] Installing dependencies...
pip install pyinstaller requests >nul 2>&1
echo [OK] Dependencies installed
echo.

echo [3/4] Building...
pyinstaller --onefile --windowed ^
    --name "LocalReverse" ^
    --add-data "config.json;." ^
    --add-data "i18n.py;." ^
    --exclude-module matplotlib ^
    --exclude-module numpy ^
    --exclude-module pandas ^
    --exclude-module scipy ^
    --exclude-module PIL ^
    --exclude-module PIL.Image ^
    --exclude-module PyQt5 ^
    --exclude-module PySide2 ^
    --exclude-module PyQt6 ^
    --exclude-module PySide6 ^
    --exclude-module flask ^
    --exclude-module django ^
    --exclude-module aiohttp ^
    main.py
echo [OK] Build complete
echo.

echo [4/4] Copying config template to dist...
if exist dist\ (
    if not exist "dist\config.json" (
        echo {"rules": []} > "dist\config.json"
        echo [OK] Created config.json in dist
    ) else (
        echo [OK] Config already exists in dist
    )
)
echo.

echo ========================================
echo Build Complete!
echo ========================================
echo.
echo Executable: dist\LocalReverse.exe
echo.
echo Usage:
echo 1. Double-click LocalReverse.exe
echo 2. Add mapping rules (local port -> target URL)
echo 3. Click Start All Services
echo.

dir dist\LocalReverse.exe 2>nul
echo.
pause
