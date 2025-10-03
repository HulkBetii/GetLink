#!/usr/bin/env python3
"""
Create Windows Distribution Package
Creates a complete distribution package for Windows users
"""

import os
import sys
import shutil
import zipfile
from pathlib import Path
import subprocess

def create_distribution():
    """Create complete Windows distribution package"""
    
    print("🚀 Creating Windows Distribution Package...")
    
    # Configuration
    package_name = "Course_Link_Getter_Windows_Distribution"
    package_dir = Path(package_name)
    
    # Clean previous package
    if package_dir.exists():
        shutil.rmtree(package_dir)
    
    package_dir.mkdir()
    
    # Copy essential files
    files_to_copy = [
        "build_windows.py",
        "build_windows.bat", 
        "README_BUILD.md",
        "test_windows_build.ps1",
        "smoketest.ps1"
    ]
    
    print("📁 Copying build files...")
    for file in files_to_copy:
        if Path(file).exists():
            shutil.copy2(file, package_dir / file)
            print(f"✅ {file}")
        else:
            print(f"⚠️  {file} not found")
    
    # Copy source code
    print("📁 Copying source code...")
    source_dir = package_dir / "course_link_getter"
    shutil.copytree("course_link_getter", source_dir)
    print("✅ course_link_getter/")
    
    # Create Windows-specific README
    windows_readme = package_dir / "README_WINDOWS.txt"
    with open(windows_readme, "w", encoding="utf-8") as f:
        f.write("""Course Link Getter - Windows Distribution Package
================================================

This package contains everything needed to build Course Link Getter for Windows.

QUICK START:
-----------
1. Double-click: build_windows.bat
2. Wait for build to complete
3. Find your files in: release/

WHAT YOU GET:
------------
- Course_Link_Getter-Portable.exe (35-50 MB)
  → Run directly, no installation needed
  
- Course_Link_Getter-Setup-x64.exe (40-60 MB)  
  → Windows installer with shortcuts

REQUIREMENTS:
------------
- Windows 10/11 x64
- Python 3.8+ (will be installed automatically if missing)
- Internet connection (for downloading build tools)

BUILD PROCESS:
-------------
The build script will automatically:
✓ Check Python installation
✓ Download PyInstaller, NSIS, UPX
✓ Create isolated build environment
✓ Build portable executable
✓ Create Windows installer
✓ Generate checksums
✓ Run automated tests

TESTING:
--------
After build, run:
powershell -ExecutionPolicy Bypass -File test_windows_build.ps1

This will test both executables to ensure they work correctly.

TROUBLESHOOTING:
---------------
- If Python not found: Install from https://python.org
- If build fails: Check internet connection
- If app won't run: Check Windows Defender settings
- If installer fails: Run as Administrator

SUPPORT:
--------
- Build Guide: README_BUILD.md
- Test Script: test_windows_build.ps1
- Source Code: course_link_getter/

The build process is fully automated and handles all dependencies.
""")
    
    print("✅ README_WINDOWS.txt")
    
    # Create batch file for easy execution
    easy_build = package_dir / "EASY_BUILD.bat"
    with open(easy_build, "w", encoding="utf-8") as f:
        f.write("""@echo off
title Course Link Getter - Easy Build
color 0A

echo.
echo ========================================
echo   Course Link Getter - Easy Build
echo ========================================
echo.
echo This will build Course Link Getter for Windows
echo and create both portable and installer versions.
echo.
echo Requirements:
echo - Windows 10/11 x64
echo - Internet connection
echo - About 5-10 minutes
echo.
pause

echo.
echo Starting build process...
echo.

call build_windows.bat

echo.
echo ========================================
echo Build completed! Check the 'release' folder.
echo ========================================
echo.
pause
""")
    
    print("✅ EASY_BUILD.bat")
    
    # Create PowerShell test script
    easy_test = package_dir / "EASY_TEST.ps1"
    with open(easy_test, "w", encoding="utf-8") as f:
        f.write("""# Course Link Getter - Easy Test
Write-Host "🧪 Course Link Getter - Easy Test" -ForegroundColor Green
Write-Host "=" * 40 -ForegroundColor Green

if (Test-Path "release/Course_Link_Getter-Portable.exe") {
    Write-Host "✅ Portable executable found" -ForegroundColor Green
    Write-Host "🚀 Testing portable version..." -ForegroundColor Yellow
    
    try {
        $process = Start-Process -FilePath "release/Course_Link_Getter-Portable.exe" -PassThru
        Start-Sleep -Seconds 3
        
        if (-not $process.HasExited) {
            Write-Host "✅ Application started successfully!" -ForegroundColor Green
            Write-Host "🔄 Closing application..." -ForegroundColor Yellow
            $process.CloseMainWindow()
            Start-Sleep -Seconds 2
            if (-not $process.HasExited) {
                $process.Kill()
            }
            Write-Host "✅ Test completed successfully!" -ForegroundColor Green
        } else {
            Write-Host "❌ Application exited unexpectedly" -ForegroundColor Red
        }
    } catch {
        Write-Host "❌ Test failed: $($_.Exception.Message)" -ForegroundColor Red
    }
} else {
    Write-Host "❌ Portable executable not found" -ForegroundColor Red
    Write-Host "Please run EASY_BUILD.bat first" -ForegroundColor Yellow
}

Write-Host "`nPress any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
""")
    
    print("✅ EASY_TEST.ps1")
    
    # Create zip package
    print("📦 Creating distribution package...")
    zip_path = f"{package_name}.zip"
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(package_dir):
            for file in files:
                file_path = Path(root) / file
                arc_path = file_path.relative_to(package_dir.parent)
                zipf.write(file_path, arc_path)
    
    # Get package size
    package_size = Path(zip_path).stat().st_size / (1024 * 1024)
    
    print(f"✅ Distribution package created: {zip_path} ({package_size:.1f} MB)")
    
    # Cleanup
    shutil.rmtree(package_dir)
    
    print("\n" + "=" * 60)
    print("🎉 WINDOWS DISTRIBUTION PACKAGE READY!")
    print("=" * 60)
    print(f"📦 Package: {zip_path}")
    print(f"📏 Size: {package_size:.1f} MB")
    print("\n📋 Contents:")
    print("  • build_windows.py - Main build script")
    print("  • build_windows.bat - Easy batch launcher")
    print("  • EASY_BUILD.bat - One-click build")
    print("  • EASY_TEST.ps1 - One-click test")
    print("  • README_WINDOWS.txt - User instructions")
    print("  • README_BUILD.md - Technical guide")
    print("  • course_link_getter/ - Source code")
    print("\n🚀 For end users:")
    print("  1. Extract the zip file")
    print("  2. Double-click EASY_BUILD.bat")
    print("  3. Wait for build to complete")
    print("  4. Find executables in release/ folder")
    print("\n✅ Ready for distribution!")

if __name__ == "__main__":
    create_distribution()
