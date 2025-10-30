@echo off
REM TempleCode IDE - Windows Build Script
REM Builds the complete Windows application package

echo ========================================
echo  TempleCode IDE Windows Build Script
echo ========================================
echo.

REM Check for Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from python.org
    pause
    exit /b 1
)

REM Check for required packages
echo Checking dependencies...
python -c "import tkinter" >nul 2>&1
if errorlevel 1 (
    echo ERROR: Tkinter is not available
    echo Please install Python with tkinter support
    pause
    exit /b 1
)

REM Install build dependencies
echo Installing build dependencies...
python -m pip install --upgrade pip
python -m pip install pyinstaller pillow

REM Create assets directory if it doesn't exist
if not exist "assets" mkdir assets

REM Generate a simple icon if none exists
if not exist "assets\templecode.ico" (
    echo Creating default application icon...
    python -c "
from PIL import Image, ImageDraw
import sys
# Create a simple 32x32 icon
img = Image.new('RGB', (32, 32), color='#2E86C1')
draw = ImageDraw.Draw(img)
draw.rectangle([4, 4, 28, 28], outline='white', width=2)
draw.text((8, 10), 'TC', fill='white')
img.save('assets/templecode.ico', format='ICO')
print('Icon created successfully')
" || (
        echo Warning: Could not create icon, continuing without it...
    )
)

REM Build the executable
echo.
echo Building Windows executable...
python build_windows.py

if errorlevel 1 (
    echo ERROR: Build failed
    pause
    exit /b 1
)

REM Check if executable was created
if exist "dist\windows\TempleCode.exe" (
    echo.
    echo SUCCESS: Windows executable created!
    echo Location: dist\windows\TempleCode.exe
    echo.
    echo You can now:
    echo 1. Run the executable directly
    echo 2. Create an installer with NSIS (if installed)
    echo 3. Distribute the executable
    echo.
    
    REM Test the executable
    echo Testing the executable...
    "dist\windows\TempleCode.exe" --help >nul 2>&1
    if errorlevel 1 (
        echo Warning: Executable test failed, but file exists
    ) else (
        echo Executable test passed!
    )
    
) else (
    echo ERROR: Executable was not created
    exit /b 1
)

REM Check for NSIS to build installer
where makensis >nul 2>&1
if not errorlevel 1 (
    echo.
    echo NSIS found! Building Windows installer...
    makensis templecode_installer.nsi
    
    if exist "TempleCode-IDE-Setup-*.exe" (
        echo.
        echo SUCCESS: Windows installer created!
        for %%f in (TempleCode-IDE-Setup-*.exe) do echo Installer: %%f
    ) else (
        echo Warning: Installer build failed
    )
) else (
    echo.
    echo NSIS not found - skipping installer creation
    echo Install NSIS from https://nsis.sourceforge.io/ to create an installer
)

echo.
echo Build process complete!
pause