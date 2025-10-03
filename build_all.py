#!/usr/bin/env python3
"""
Universal build script for Course Link Getter
Supports both macOS and Windows builds
"""

import os
import sys
import platform
import subprocess
import shutil
from pathlib import Path

def run_command(cmd, shell=False):
    """Run a command and return success status"""
    try:
        result = subprocess.run(cmd, shell=shell, check=True, capture_output=True, text=True)
        print(f"✅ {cmd}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running {cmd}: {e}")
        print(f"Error output: {e.stderr}")
        return False

def clean_build():
    """Clean previous build artifacts"""
    print("🧹 Cleaning previous builds...")
    dirs_to_clean = ['dist', 'build', '__pycache__']
    files_to_clean = ['*.spec']
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"  Removed {dir_name}/")
    
    # Clean .pyc files
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.pyc'):
                os.remove(os.path.join(root, file))

def build_macos():
    """Build for macOS"""
    print("🍎 Building for macOS...")
    
    cmd = [
        'pyinstaller',
        '--name=Course Link Getter',
        '--windowed',
        '--onedir',
        '--icon=course_link_getter/assets/icon.icns',
        '--add-data=course_link_getter/assets:courses_link_getter/assets',
        '--add-data=course_link_getter/core:courses_link_getter/core', 
        '--add-data=course_link_getter/ui_pyqt5:courses_link_getter/ui_pyqt5',
        '--hidden-import=PyQt5.QtCore',
        '--hidden-import=PyQt5.QtGui',
        '--hidden-import=PyQt5.QtWidgets',
        '--hidden-import=PyQt5.sip',
        '--clean',
        'course_link_getter/launch_pyqt5.py'
    ]
    
    if run_command(cmd):
        if os.path.exists('dist/Course Link Getter.app'):
            print("✅ macOS app created successfully!")
            
            # Create DMG
            print("📦 Creating DMG installer...")
            dmg_cmd = [
                'hdiutil', 'create', 
                '-volname', 'Course Link Getter',
                '-srcfolder', 'dist/Course Link Getter.app',
                '-ov', '-format', 'UDZO',
                'Course_Link_Getter_macOS.dmg'
            ]
            if run_command(dmg_cmd):
                print("✅ DMG created: Course_Link_Getter_macOS.dmg")
            return True
        else:
            print("❌ macOS app not found after build")
            return False
    return False

def build_windows():
    """Build for Windows (when running on Windows)"""
    print("🪟 Building for Windows...")
    
    cmd = [
        'pyinstaller',
        '--name=Course Link Getter',
        '--windowed',
        '--onedir',
        '--icon=course_link_getter/assets/icon.ico',
        '--add-data=course_link_getter/assets;courses_link_getter/assets',
        '--add-data=course_link_getter/core;courses_link_getter/core',
        '--add-data=course_link_getter/ui_pyqt5;courses_link_getter/ui_pyqt5',
        '--hidden-import=PyQt5.QtCore',
        '--hidden-import=PyQt5.QtGui',
        '--hidden-import=PyQt5.QtWidgets',
        '--hidden-import=PyQt5.sip',
        '--clean',
        'course_link_getter/launch_pyqt5.py'
    ]
    
    if run_command(cmd):
        if os.path.exists('dist/Course Link Getter'):
            print("✅ Windows executable created successfully!")
            
            # Create ZIP archive
            print("📦 Creating ZIP archive...")
            if shutil.which('powershell'):
                zip_cmd = [
                    'powershell', 'Compress-Archive',
                    '-Path', 'dist/Course Link Getter/*',
                    '-DestinationPath', 'Course_Link_Getter_Windows.zip',
                    '-Force'
                ]
            else:
                # Fallback to Python zip
                import zipfile
                with zipfile.ZipFile('Course_Link_Getter_Windows.zip', 'w') as zipf:
                    for root, dirs, files in os.walk('dist/Course Link Getter'):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, 'dist/Course Link Getter')
                            zipf.write(file_path, arcname)
            
            if run_command(zip_cmd) if 'zip_cmd' in locals() else True:
                print("✅ ZIP created: Course_Link_Getter_Windows.zip")
            return True
        else:
            print("❌ Windows executable not found after build")
            return False
    return False

def main():
    """Main build function"""
    print("🚀 Course Link Getter Build Script")
    print(f"Platform: {platform.system()} {platform.release()}")
    print("=" * 50)
    
    # Clean previous builds
    clean_build()
    
    # Check if PyInstaller is installed
    if not shutil.which('pyinstaller'):
        print("❌ PyInstaller not found. Installing...")
        if not run_command([sys.executable, '-m', 'pip', 'install', 'pyinstaller']):
            print("❌ Failed to install PyInstaller")
            return False
    
    success = False
    
    # Build based on current platform
    if platform.system() == 'Darwin':  # macOS
        success = build_macos()
    elif platform.system() == 'Windows':  # Windows
        success = build_windows()
    else:
        print(f"❌ Unsupported platform: {platform.system()}")
        print("💡 Please run this script on macOS or Windows")
        return False
    
    if success:
        print("\n🎉 Build completed successfully!")
        print("📁 Check the 'dist' folder for your application")
    else:
        print("\n❌ Build failed!")
        return False
    
    return True

if __name__ == "__main__":
    main()
