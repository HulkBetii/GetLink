# Python Installation Script for Windows (PowerShell)
# Automatically downloads and installs Python if not found

param(
    [switch]$Force,
    [string]$PythonVersion = "3.12.6"
)

Write-Host "🚀 Course Link Getter - Python Installer (PowerShell)" -ForegroundColor Green
Write-Host "=" * 50 -ForegroundColor Green

# Check if running as administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")

if (-not $isAdmin) {
    Write-Host "⚠️  Not running as administrator" -ForegroundColor Yellow
    Write-Host "Some features may not work properly." -ForegroundColor Yellow
    Write-Host ""
}

# Check if Python is already installed
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Python is already installed!" -ForegroundColor Green
        Write-Host "Version: $pythonVersion" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "You can now run: build_windows.bat" -ForegroundColor Green
        return
    }
} catch {
    # Python not found, continue with installation
}

Write-Host "❌ Python not found on this system." -ForegroundColor Red
Write-Host ""

if (-not $Force) {
    $response = Read-Host "Would you like to install Python automatically? (Y/N)"
    if ($response -notmatch "^[Yy]") {
        Write-Host "Installation cancelled." -ForegroundColor Yellow
        Write-Host "Please install Python manually from: https://python.org" -ForegroundColor Cyan
        return
    }
}

# Check internet connection
Write-Host "🔍 Checking internet connection..." -ForegroundColor Yellow
try {
    $ping = Test-Connection -ComputerName "google.com" -Count 1 -Quiet
    if (-not $ping) {
        throw "No internet connection"
    }
    Write-Host "✅ Internet connection available." -ForegroundColor Green
} catch {
    Write-Host "❌ No internet connection found." -ForegroundColor Red
    Write-Host "Please connect to internet and try again." -ForegroundColor Yellow
    return
}

Write-Host ""

# Create temp directory
$tempDir = Join-Path $env:TEMP "CourseLinkGetter"
if (-not (Test-Path $tempDir)) {
    New-Item -ItemType Directory -Path $tempDir -Force | Out-Null
}

# Download Python installer
$pythonUrl = "https://www.python.org/ftp/python/$PythonVersion/python-$PythonVersion-amd64.exe"
$pythonInstaller = Join-Path $tempDir "python-installer.exe"

Write-Host "📥 Downloading Python installer..." -ForegroundColor Yellow
Write-Host "URL: $pythonUrl" -ForegroundColor Cyan
Write-Host "Saving to: $pythonInstaller" -ForegroundColor Cyan
Write-Host ""

try {
    # Set security protocol for older PowerShell versions
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
    
    # Download with progress
    $webClient = New-Object System.Net.WebClient
    $webClient.DownloadFile($pythonUrl, $pythonInstaller)
    
    Write-Host "✅ Python installer downloaded successfully!" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to download Python installer." -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Please download manually from: https://python.org" -ForegroundColor Cyan
    return
}

Write-Host ""

# Verify download
if (-not (Test-Path $pythonInstaller)) {
    Write-Host "❌ Downloaded file not found." -ForegroundColor Red
    return
}

$fileSize = (Get-Item $pythonInstaller).Length / 1MB
Write-Host "📦 Downloaded file size: $([math]::Round($fileSize, 2)) MB" -ForegroundColor Cyan

Write-Host ""
Write-Host "🚀 Starting Python installation..." -ForegroundColor Yellow
Write-Host ""
Write-Host "IMPORTANT: During installation, make sure to:" -ForegroundColor Yellow
Write-Host "1. ✅ Check 'Add Python to PATH'" -ForegroundColor Green
Write-Host "2. ✅ Check 'Install for all users' (if you have admin rights)" -ForegroundColor Green
Write-Host "3. ✅ Click 'Install Now'" -ForegroundColor Green
Write-Host ""

# Run the installer
try {
    Start-Process -FilePath $pythonInstaller -Wait
    Write-Host "✅ Python installation completed!" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to run Python installer." -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    return
}

Write-Host ""
Write-Host "🔍 Verifying Python installation..." -ForegroundColor Yellow

# Wait for PATH to update
Start-Sleep -Seconds 3

# Refresh environment variables
$env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")

# Check if Python is now available
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Python installed successfully!" -ForegroundColor Green
        Write-Host "Version: $pythonVersion" -ForegroundColor Cyan
    } else {
        throw "Python not found in PATH"
    }
} catch {
    Write-Host "❌ Python installation may have failed or PATH not updated." -ForegroundColor Red
    Write-Host ""
    Write-Host "Please try one of these solutions:" -ForegroundColor Yellow
    Write-Host "1. Restart Command Prompt and try again" -ForegroundColor Cyan
    Write-Host "2. Restart your computer" -ForegroundColor Cyan
    Write-Host "3. Manually add Python to PATH" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Manual installation: https://python.org/downloads/" -ForegroundColor Cyan
    return
}

# Clean up
Write-Host ""
Write-Host "🧹 Cleaning up temporary files..." -ForegroundColor Yellow
try {
    if (Test-Path $pythonInstaller) {
        Remove-Item $pythonInstaller -Force
    }
    if (Test-Path $tempDir) {
        Remove-Item $tempDir -Force -Recurse
    }
    Write-Host "✅ Cleanup completed." -ForegroundColor Green
} catch {
    Write-Host "⚠️  Could not clean up temporary files." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🎉 Python is ready!" -ForegroundColor Green
Write-Host ""
Write-Host "You can now run: build_windows.bat" -ForegroundColor Green
Write-Host ""

# Ask if user wants to run build immediately
$runBuild = Read-Host "Would you like to run the build script now? (Y/N)"
if ($runBuild -match "^[Yy]") {
    Write-Host ""
    Write-Host "🚀 Starting build process..." -ForegroundColor Green
    try {
        & ".\build_windows.bat"
    } catch {
        Write-Host "❌ Failed to run build script." -ForegroundColor Red
        Write-Host "Please run build_windows.bat manually." -ForegroundColor Yellow
    }
}
