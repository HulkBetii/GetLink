#!/usr/bin/env python3
"""
Windows Build Script for Course Link Getter
Creates both installer .exe and portable .exe for Windows distribution
"""

import os
import sys
import subprocess
import shutil
import platform
import hashlib
from pathlib import Path
import tempfile
import urllib.request
import zipfile

# Configuration
APP_NAME = "Course Link Getter"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Lightweight desktop app to search course catalog"
APP_AUTHOR = "CourseLinkGetter"
APP_ICON = "course_link_getter/assets/icon.ico"  # Will be adjusted per platform
APP_ENTRY = "course_link_getter/launch_pyqt5.py"

# Build directories
BUILD_DIR = Path("build")
DIST_DIR = Path("dist")
RELEASE_DIR = Path("release")

def log(message):
    """Log with timestamp"""
    print(f"[BUILD] {message}")

def run_command(cmd, cwd=None, check=True):
    """Run command with logging"""
    log(f"Running: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    try:
        result = subprocess.run(
            cmd, 
            cwd=cwd, 
            check=check, 
            capture_output=True, 
            text=True,
            shell=isinstance(cmd, str)
        )
        if result.stdout:
            log(f"STDOUT: {result.stdout}")
        if result.stderr:
            log(f"STDERR: {result.stderr}")
        return result
    except subprocess.CalledProcessError as e:
        log(f"Command failed: {e}")
        if e.stdout:
            log(f"STDOUT: {e.stdout}")
        if e.stderr:
            log(f"STDERR: {e.stderr}")
        raise

def check_requirements():
    """Check if required tools are available"""
    log("Checking requirements...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        raise RuntimeError("Python 3.8+ required")
    log(f"✅ Python {sys.version}")
    
    # Check if we're on Windows
    if platform.system() != "Windows":
        log("⚠️  Warning: Not on Windows, but building Windows package")
    
    # Check PyInstaller
    try:
        import PyInstaller
        log(f"✅ PyInstaller {PyInstaller.__version__}")
    except ImportError:
        log("❌ PyInstaller not found, installing...")
        run_command([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Check NSIS (optional, will download if needed)
    nsis_path = shutil.which("makensis")
    if nsis_path:
        log(f"✅ NSIS found: {nsis_path}")
    else:
        log("⚠️  NSIS not found, will download portable version")
    
    # Check UPX (optional)
    upx_path = shutil.which("upx")
    if upx_path:
        log(f"✅ UPX found: {upx_path}")
    else:
        log("⚠️  UPX not found, will download if needed")

def download_tools():
    """Download required tools if missing"""
    tools_dir = Path("tools")
    tools_dir.mkdir(exist_ok=True)
    
    # Download NSIS portable if needed
    nsis_path = shutil.which("makensis")
    if not nsis_path:
        nsis_dir = tools_dir / "nsis"
        if not nsis_dir.exists():
            log("Downloading NSIS portable...")
            nsis_url = "https://sourceforge.net/projects/nsis/files/NSIS%203/3.08/nsis-3.08-setup.exe/download"
            nsis_installer = tools_dir / "nsis-installer.exe"
            
            try:
                urllib.request.urlretrieve(nsis_url, nsis_installer)
                log("✅ NSIS downloaded")
                log("⚠️  Please install NSIS manually or use portable version")
            except Exception as e:
                log(f"❌ Failed to download NSIS: {e}")
                log("⚠️  Will create installer script without NSIS")
    
    # Download UPX if needed
    upx_path = shutil.which("upx")
    if not upx_path:
        upx_dir = tools_dir / "upx"
        if not upx_dir.exists():
            log("Downloading UPX...")
            upx_url = "https://github.com/upx/upx/releases/download/v4.2.1/upx-4.2.1-win64.zip"
            upx_zip = tools_dir / "upx.zip"
            
            try:
                urllib.request.urlretrieve(upx_url, upx_zip)
                with zipfile.ZipFile(upx_zip, 'r') as zip_ref:
                    zip_ref.extractall(upx_dir)
                upx_zip.unlink()
                log("✅ UPX downloaded")
            except Exception as e:
                log(f"❌ Failed to download UPX: {e}")
                log("⚠️  Will build without UPX compression")

def create_venv():
    """Create isolated virtual environment for building"""
    log("Creating build virtual environment...")
    
    venv_dir = Path("build_venv")
    if venv_dir.exists():
        shutil.rmtree(venv_dir)
    
    # Create venv
    run_command([sys.executable, "-m", "venv", str(venv_dir)])
    
    # Get venv python
    if platform.system() == "Windows":
        venv_python = venv_dir / "Scripts" / "python.exe"
    else:
        venv_python = venv_dir / "bin" / "python"
    
    # Install requirements
    requirements_file = Path("course_link_getter/requirements.txt")
    if requirements_file.exists():
        log("Installing requirements...")
        run_command([str(venv_python), "-m", "pip", "install", "-r", str(requirements_file)])
    
    # Install PyInstaller and Pillow
    run_command([str(venv_python), "-m", "pip", "install", "pyinstaller", "pillow"])
    
    return venv_python

def build_portable(venv_python):
    """Build portable .exe using PyInstaller"""
    log("Building portable executable...")
    
    # Clean previous builds
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    
    # PyInstaller command
    cmd = [
        str(venv_python), "-m", "PyInstaller",
        "--onefile",
        "--noconsole",
        "--name", APP_NAME.replace(" ", "_"),
        "--distpath", str(DIST_DIR),
        "--workpath", str(BUILD_DIR),
        "--specpath", str(BUILD_DIR),
    ]
    
    # Add icon if exists (platform-specific)
    if platform.system() == "Darwin":  # macOS
        icon_path = Path("course_link_getter/assets/icon.icns")
    else:  # Windows/Linux
        icon_path = Path("course_link_getter/assets/icon.ico")
    
    if icon_path.exists():
        cmd.extend(["--icon", str(icon_path.absolute())])
        log(f"✅ Using icon: {icon_path.absolute()}")
    else:
        log("⚠️  No icon found, using default")
    
    # Add data files
    assets_dir = Path("course_link_getter/assets")
    if assets_dir.exists():
        # Use absolute path for --add-data
        abs_assets = assets_dir.absolute()
        cmd.extend(["--add-data", f"{abs_assets}{os.pathsep}assets"])
        log(f"✅ Adding assets: {abs_assets}")
    
    # Add hidden imports for PyQt5
    hidden_imports = [
        "PyQt5.QtCore",
        "PyQt5.QtGui", 
        "PyQt5.QtWidgets",
        "pydantic",
        "json",
        "pathlib",
        "sys"
    ]
    
    for imp in hidden_imports:
        cmd.extend(["--hidden-import", imp])
    
    # Add the main script
    cmd.append(APP_ENTRY)
    
    # Run PyInstaller
    log("Running PyInstaller...")
    run_command(cmd)
    
    # Check if executable was created
    exe_name = f"{APP_NAME.replace(' ', '_')}.exe"
    exe_path = DIST_DIR / exe_name
    
    if exe_path.exists():
        log(f"✅ Portable executable created: {exe_path}")
        return exe_path
    else:
        raise RuntimeError(f"Failed to create executable: {exe_path}")

def compress_with_upx(exe_path):
    """Compress executable with UPX if available"""
    upx_path = shutil.which("upx")
    if not upx_path:
        # Try tools directory
        tools_upx = Path("tools/upx/upx.exe")
        if tools_upx.exists():
            upx_path = str(tools_upx)
    
    if upx_path:
        log("Compressing with UPX...")
        try:
            run_command([upx_path, "--best", str(exe_path)])
            log("✅ UPX compression completed")
        except Exception as e:
            log(f"⚠️  UPX compression failed: {e}")
    else:
        log("⚠️  UPX not available, skipping compression")

def create_nsis_installer(exe_path):
    """Create NSIS installer script"""
    log("Creating NSIS installer script...")
    
    nsis_script = f"""
; Course Link Getter Installer Script
!define APP_NAME "{APP_NAME}"
!define APP_VERSION "{APP_VERSION}"
!define APP_PUBLISHER "{APP_AUTHOR}"
!define APP_EXE "${{APP_NAME}}.exe"
!define APP_ICON "{APP_ICON}"

; Modern UI
!include "MUI2.nsh"

; General
Name "${{APP_NAME}}"
OutFile "release/${{APP_NAME}}-Setup-x64.exe"
InstallDir "$PROGRAMFILES64\\${{APP_NAME}}"
InstallDirRegKey HKLM "Software\\${{APP_NAME}}" "Install_Dir"
RequestExecutionLevel admin

; Interface
!define MUI_ABORTWARNING
!define MUI_ICON "${{APP_ICON}}"
!define MUI_UNICON "${{APP_ICON}}"

; Pages
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "LICENSE.txt"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

; Languages
!insertmacro MUI_LANGUAGE "English"

; Installer sections
Section "Main Application" SecMain
    SetOutPath "$INSTDIR"
    
    ; Copy executable
    File "{exe_path}"
    
    ; Create uninstaller
    WriteUninstaller "$INSTDIR\\Uninstall.exe"
    
    ; Registry entries
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APP_NAME}}" "DisplayName" "${{APP_NAME}}"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APP_NAME}}" "UninstallString" "$INSTDIR\\Uninstall.exe"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APP_NAME}}" "DisplayVersion" "${{APP_VERSION}}"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APP_NAME}}" "Publisher" "${{APP_PUBLISHER}}"
    WriteRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APP_NAME}}" "NoModify" 1
    WriteRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APP_NAME}}" "NoRepair" 1
    
    ; Start menu shortcut
    CreateDirectory "$SMPROGRAMS\\${{APP_NAME}}"
    CreateShortCut "$SMPROGRAMS\\${{APP_NAME}}\\${{APP_NAME}}.lnk" "$INSTDIR\\${{APP_EXE}}" "" "$INSTDIR\\${{APP_EXE}}" 0
    CreateShortCut "$SMPROGRAMS\\${{APP_NAME}}\\Uninstall.lnk" "$INSTDIR\\Uninstall.exe"
    
    ; Desktop shortcut
    CreateShortCut "$DESKTOP\\${{APP_NAME}}.lnk" "$INSTDIR\\${{APP_EXE}}" "" "$INSTDIR\\${{APP_EXE}}" 0
SectionEnd

; Uninstaller
Section "Uninstall"
    ; Remove files
    Delete "$INSTDIR\\${{APP_EXE}}"
    Delete "$INSTDIR\\Uninstall.exe"
    RMDir "$INSTDIR"
    
    ; Remove shortcuts
    Delete "$SMPROGRAMS\\${{APP_NAME}}\\${{APP_NAME}}.lnk"
    Delete "$SMPROGRAMS\\${{APP_NAME}}\\Uninstall.lnk"
    RMDir "$SMPROGRAMS\\${{APP_NAME}}"
    Delete "$DESKTOP\\${{APP_NAME}}.lnk"
    
    ; Remove registry entries
    DeleteRegKey HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APP_NAME}}"
    DeleteRegKey HKLM "Software\\${{APP_NAME}}"
SectionEnd
"""
    
    # Write NSIS script
    nsis_file = Path("installer.nsi")
    with open(nsis_file, "w", encoding="utf-8") as f:
        f.write(nsis_script)
    
    log(f"✅ NSIS script created: {nsis_file}")
    
    # Create LICENSE.txt if not exists
    license_file = Path("LICENSE.txt")
    if not license_file.exists():
        with open(license_file, "w", encoding="utf-8") as f:
            f.write(f"{APP_NAME} v{APP_VERSION}\n")
            f.write(f"Copyright (c) 2024 {APP_AUTHOR}\n\n")
            f.write("MIT License\n\n")
            f.write("Permission is hereby granted, free of charge, to any person obtaining a copy\n")
            f.write("of this software and associated documentation files (the \"Software\"), to deal\n")
            f.write("in the Software without restriction, including without limitation the rights\n")
            f.write("to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n")
            f.write("copies of the Software, and to permit persons to whom the Software is\n")
            f.write("furnished to do so, subject to the following conditions:\n\n")
            f.write("The above copyright notice and this permission notice shall be included in all\n")
            f.write("copies or substantial portions of the Software.\n")
    
    return nsis_file

def build_installer(nsis_file, exe_path):
    """Build NSIS installer"""
    log("Building NSIS installer...")
    
    # Ensure release directory exists
    RELEASE_DIR.mkdir(exist_ok=True)
    
    # Find NSIS
    nsis_path = shutil.which("makensis")
    if not nsis_path:
        # Try tools directory
        tools_nsis = Path("tools/nsis/makensis.exe")
        if tools_nsis.exists():
            nsis_path = str(tools_nsis)
    
    if nsis_path:
        try:
            run_command([nsis_path, str(nsis_file)])
            installer_path = RELEASE_DIR / f"{APP_NAME}-Setup-x64.exe"
            if installer_path.exists():
                log(f"✅ Installer created: {installer_path}")
                return installer_path
            else:
                log("❌ Installer not found after build")
        except Exception as e:
            log(f"❌ NSIS build failed: {e}")
    else:
        log("❌ NSIS not found, cannot create installer")
    
    return None

def create_checksums(portable_path, installer_path):
    """Create checksums for both files"""
    log("Creating checksums...")
    
    checksums = []
    
    if portable_path and portable_path.exists():
        with open(portable_path, "rb") as f:
            sha256 = hashlib.sha256(f.read()).hexdigest()
        checksums.append(f"{portable_path.name} *{portable_path.name}")
        checksums.append(f"SHA256: {sha256}")
        checksums.append("")
    
    if installer_path and installer_path.exists():
        with open(installer_path, "rb") as f:
            sha256 = hashlib.sha256(f.read()).hexdigest()
        checksums.append(f"{installer_path.name} *{installer_path.name}")
        checksums.append(f"SHA256: {sha256}")
        checksums.append("")
    
    checksums_file = RELEASE_DIR / "checksums.txt"
    with open(checksums_file, "w") as f:
        f.write("\n".join(checksums))
    
    log(f"✅ Checksums created: {checksums_file}")

def create_smoketest():
    """Create PowerShell smoketest script"""
    smoketest_script = """
# Course Link Getter Smoketest
param(
    [string]$ExePath = "dist/Course_Link_Getter.exe",
    [int]$TimeoutSeconds = 20
)

Write-Host "🧪 Starting smoketest for Course Link Getter..." -ForegroundColor Green

# Check if executable exists
if (-not (Test-Path $ExePath)) {
    Write-Host "❌ Executable not found: $ExePath" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Executable found: $ExePath" -ForegroundColor Green

# Get file size
$fileSize = (Get-Item $ExePath).Length
Write-Host "📦 File size: $([math]::Round($fileSize / 1MB, 2)) MB" -ForegroundColor Cyan

try {
    Write-Host "🚀 Starting application..." -ForegroundColor Yellow
    
    # Start the application
    $process = Start-Process -FilePath $ExePath -PassThru -WindowStyle Normal
    
    # Wait for window to appear
    $timeout = $TimeoutSeconds
    $windowFound = $false
    
    while ($timeout -gt 0 -and -not $windowFound) {
        Start-Sleep -Milliseconds 500
        $timeout -= 0.5
        
        # Check if process is still running
        if ($process.HasExited) {
            Write-Host "❌ Application exited unexpectedly" -ForegroundColor Red
            exit 1
        }
        
        # Look for window (simplified check)
        $windows = Get-Process | Where-Object { $_.MainWindowTitle -like "*Course Link Getter*" }
        if ($windows) {
            $windowFound = $true
            Write-Host "✅ Application window found!" -ForegroundColor Green
        }
    }
    
    if (-not $windowFound) {
        Write-Host "❌ Application window not found within $TimeoutSeconds seconds" -ForegroundColor Red
        $process.Kill()
        exit 1
    }
    
    # Let it run for a moment
    Start-Sleep -Seconds 2
    
    # Close the application
    Write-Host "🔄 Closing application..." -ForegroundColor Yellow
    $process.CloseMainWindow()
    
    # Wait for graceful exit
    if (-not $process.WaitForExit(5000)) {
        Write-Host "⚠️  Application didn't close gracefully, forcing..." -ForegroundColor Yellow
        $process.Kill()
    }
    
    Write-Host "✅ Smoketest completed successfully!" -ForegroundColor Green
    exit 0
    
} catch {
    Write-Host "❌ Smoketest failed: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
"""
    
    smoketest_file = Path("smoketest.ps1")
    with open(smoketest_file, "w", encoding="utf-8") as f:
        f.write(smoketest_script)
    
    log(f"✅ Smoketest script created: {smoketest_file}")
    return smoketest_file

def main():
    """Main build process"""
    log("=" * 60)
    log(f"Building {APP_NAME} v{APP_VERSION} for Windows")
    log("=" * 60)
    
    try:
        # Pre-flight checks
        check_requirements()
        download_tools()
        
        # Create build environment
        venv_python = create_venv()
        
        # Build portable executable
        portable_path = build_portable(venv_python)
        
        # Compress with UPX
        compress_with_upx(portable_path)
        
        # Create installer
        nsis_file = create_nsis_installer(portable_path)
        installer_path = build_installer(nsis_file, portable_path)
        
        # Copy portable to release
        if portable_path.exists():
            release_portable = RELEASE_DIR / f"{APP_NAME.replace(' ', '_')}-Portable.exe"
            shutil.copy2(portable_path, release_portable)
            log(f"✅ Portable copied to: {release_portable}")
        
        # Create checksums
        create_checksums(
            RELEASE_DIR / f"{APP_NAME.replace(' ', '_')}-Portable.exe" if portable_path.exists() else None,
            installer_path
        )
        
        # Create smoketest
        create_smoketest()
        
        # Summary
        log("=" * 60)
        log("BUILD COMPLETED SUCCESSFULLY!")
        log("=" * 60)
        
        if portable_path.exists():
            portable_size = portable_path.stat().st_size / (1024 * 1024)
            log(f"📦 Portable: {portable_path} ({portable_size:.1f} MB)")
        
        if installer_path and installer_path.exists():
            installer_size = installer_path.stat().st_size / (1024 * 1024)
            log(f"📦 Installer: {installer_path} ({installer_size:.1f} MB)")
        
        log(f"📁 Release directory: {RELEASE_DIR.absolute()}")
        log("🧪 Run smoketest: powershell -ExecutionPolicy Bypass -File smoketest.ps1")
        
        # Cleanup
        if Path("build_venv").exists():
            shutil.rmtree("build_venv")
            log("🧹 Cleaned up build environment")
        
    except Exception as e:
        log(f"❌ Build failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
