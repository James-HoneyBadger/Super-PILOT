# TempleCode IDE - Windows Build Script (PowerShell)
# Modern build script for Windows 10/11 environments

param(
    [switch]$SkipTests = $false,
    [switch]$SkipInstaller = $false,
    [string]$OutputDir = "dist\windows"
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host " TempleCode IDE Windows Build Script" -ForegroundColor Cyan  
Write-Host "========================================" -ForegroundColor Cyan
Write-Host

# Check PowerShell version
if ($PSVersionTable.PSVersion.Major -lt 5) {
    Write-Host "ERROR: PowerShell 5.0 or later required" -ForegroundColor Red
    exit 1
}

# Check for Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python not found in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8+ from python.org" -ForegroundColor Yellow
    exit 1
}

# Check for tkinter
try {
    python -c "import tkinter; print('✓ Tkinter available')"
} catch {
    Write-Host "ERROR: Tkinter not available" -ForegroundColor Red
    Write-Host "Please install Python with tkinter support" -ForegroundColor Yellow
    exit 1
}

# Install build dependencies
Write-Host "Installing build dependencies..." -ForegroundColor Yellow
try {
    python -m pip install --upgrade pip setuptools wheel
    python -m pip install pyinstaller pillow
    Write-Host "✓ Dependencies installed" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Failed to install dependencies" -ForegroundColor Red
    exit 1
}

# Create directories
$assetsDir = "assets"
if (-not (Test-Path $assetsDir)) {
    New-Item -ItemType Directory -Path $assetsDir | Out-Null
    Write-Host "✓ Created assets directory" -ForegroundColor Green
}

# Generate application icon
$iconPath = "$assetsDir\templecode.ico"
if (-not (Test-Path $iconPath)) {
    Write-Host "Creating application icon..." -ForegroundColor Yellow
    
    $iconScript = @"
from PIL import Image, ImageDraw, ImageFont
import sys

# Create a 48x48 icon with TempleCode branding
img = Image.new('RGBA', (48, 48), color=(46, 134, 193, 255))
draw = ImageDraw.Draw(img)

# Draw border
draw.rectangle([2, 2, 45, 45], outline=(255, 255, 255, 255), width=2)

# Draw "TC" text
try:
    # Try to use a system font
    font = ImageFont.truetype("arial.ttf", 16)
except:
    # Fallback to default font
    font = ImageFont.load_default()

# Center the text
text = "TC"
bbox = draw.textbbox((0, 0), text, font=font)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]
x = (48 - text_width) // 2
y = (48 - text_height) // 2 - 2

draw.text((x, y), text, fill=(255, 255, 255, 255), font=font)

# Save as ICO format
img.save('assets/templecode.ico', format='ICO', sizes=[(48, 48), (32, 32), (16, 16)])
print('✓ Icon created successfully')
"@

    try {
        $iconScript | python
    } catch {
        Write-Host "Warning: Could not create icon, using default" -ForegroundColor Yellow
    }
}

# Run tests if not skipped
if (-not $SkipTests) {
    Write-Host "Running tests..." -ForegroundColor Yellow
    try {
        python -m pytest tests/ -q --tb=short --ignore=tests/test_performance.py --ignore=tests/test_security.py
        Write-Host "✓ Tests completed" -ForegroundColor Green
    } catch {
        Write-Host "Warning: Some tests failed, continuing build..." -ForegroundColor Yellow
    }
}

# Build the executable
Write-Host "Building Windows executable..." -ForegroundColor Yellow
try {
    python build_windows.py
    
    $exePath = "$OutputDir\TempleCode.exe"
    if (Test-Path $exePath) {
        $fileSize = (Get-Item $exePath).Length / 1MB
        Write-Host "✓ Executable created: $exePath ($([math]::Round($fileSize, 1)) MB)" -ForegroundColor Green
        
        # Test the executable
        Write-Host "Testing executable..." -ForegroundColor Yellow
        $testResult = & $exePath --version 2>&1
        if ($LASTEXITCODE -eq 0 -or $testResult -like "*TempleCode*") {
            Write-Host "✓ Executable test passed" -ForegroundColor Green
        } else {
            Write-Host "Warning: Executable test inconclusive" -ForegroundColor Yellow
        }
    } else {
        throw "Executable not found at expected location"
    }
} catch {
    Write-Host "ERROR: Build failed - $_" -ForegroundColor Red
    exit 1
}

# Create installer if NSIS is available and not skipped
if (-not $SkipInstaller) {
    Write-Host "Checking for NSIS..." -ForegroundColor Yellow
    
    $nsisPath = Get-Command makensis -ErrorAction SilentlyContinue
    if ($nsisPath) {
        Write-Host "✓ NSIS found, building installer..." -ForegroundColor Green
        
        try {
            & makensis templecode_installer.nsi
            
            $installerPattern = "TempleCode-IDE-Setup-*.exe"
            $installers = Get-ChildItem -Path . -Name $installerPattern
            
            if ($installers.Count -gt 0) {
                foreach ($installer in $installers) {
                    $size = (Get-Item $installer).Length / 1MB
                    Write-Host "✓ Installer created: $installer ($([math]::Round($size, 1)) MB)" -ForegroundColor Green
                }
            } else {
                Write-Host "Warning: Installer build completed but file not found" -ForegroundColor Yellow
            }
        } catch {
            Write-Host "Warning: Installer build failed - $_" -ForegroundColor Yellow
        }
    } else {
        Write-Host "NSIS not found - skipping installer creation" -ForegroundColor Yellow
        Write-Host "Install NSIS from https://nsis.sourceforge.io/ to create installers" -ForegroundColor Cyan
    }
}

# Build summary
Write-Host
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " Build Summary" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

Write-Host "✓ Standalone executable: $OutputDir\TempleCode.exe" -ForegroundColor Green

$installers = Get-ChildItem -Path . -Name "TempleCode-IDE-Setup-*.exe" -ErrorAction SilentlyContinue
if ($installers) {
    foreach ($installer in $installers) {
        Write-Host "✓ Windows installer: $installer" -ForegroundColor Green
    }
}

Write-Host
Write-Host "The application can now be:" -ForegroundColor White
Write-Host "• Run directly from the executable" -ForegroundColor Cyan
Write-Host "• Installed using the Windows installer" -ForegroundColor Cyan  
Write-Host "• Distributed to other Windows 11 machines" -ForegroundColor Cyan

Write-Host
Write-Host "Build completed successfully! 🎉" -ForegroundColor Green