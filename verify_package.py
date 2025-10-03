#!/usr/bin/env python3
"""
Verify that the packaged application contains all necessary data
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def check_dmg_contents():
    """Check if DMG contains all necessary files"""
    print("🔍 Checking DMG contents...")
    
    dmg_path = "Course_Link_Getter_macOS.dmg"
    if not os.path.exists(dmg_path):
        print(f"❌ DMG file not found: {dmg_path}")
        return False
    
    # Mount DMG
    result = subprocess.run(['hdiutil', 'attach', dmg_path], 
                          capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Failed to mount DMG: {result.stderr}")
        return False
    
    # Find mounted volume
    volume_path = None
    for line in result.stdout.split('\n'):
        if 'Course Link Getter' in line and '/Volumes/' in line:
            parts = line.split()
            for part in parts:
                if '/Volumes/' in part:
                    volume_path = part
                    break
            break
    
    if not volume_path:
        print("❌ Could not find mounted volume")
        return False
    
    print(f"📁 DMG mounted at: {volume_path}")
    
    # Check app bundle
    app_path = f"{volume_path}/Course Link Getter.app"
    if not os.path.exists(app_path):
        print(f"❌ App bundle not found: {app_path}")
        return False
    
    print(f"✅ App bundle found: {app_path}")
    
    # Check for catalog file in app bundle
    catalog_path = f"{app_path}/Contents/Resources/courses_link_getter/assets/catalog.sample.json"
    if os.path.exists(catalog_path):
        print(f"✅ Catalog file found: {catalog_path}")
        
        # Check catalog content
        with open(catalog_path, 'r') as f:
            content = f.read()
            if '"courses"' in content and len(content) > 1000:
                print(f"✅ Catalog contains data ({len(content)} characters)")
                return True
            else:
                print(f"❌ Catalog appears empty or corrupted")
                return False
    else:
        print(f"❌ Catalog file not found: {catalog_path}")
        return False

def test_app_launch():
    """Test if the app can launch successfully"""
    print("🚀 Testing app launch...")
    
    # Find mounted volume
    result = subprocess.run(['mount'], capture_output=True, text=True)
    volume_path = None
    for line in result.stdout.split('\n'):
        if 'Course Link Getter' in line and '/Volumes/' in line:
            volume_path = line.split()[-1]
            break
    
    if not volume_path:
        print("❌ Could not find mounted volume")
        return False
    
    app_path = f"{volume_path}/Course Link Getter.app"
    executable_path = f"{app_path}/Contents/MacOS/Course Link Getter"
    
    if not os.path.exists(executable_path):
        print(f"❌ Executable not found: {executable_path}")
        return False
    
    print(f"✅ Executable found: {executable_path}")
    
    # Test launch (non-blocking)
    try:
        process = subprocess.Popen([executable_path], 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE)
        
        # Wait a bit for app to start
        time.sleep(2)
        
        # Check if process is still running
        if process.poll() is None:
            print("✅ App launched successfully")
            process.terminate()
            return True
        else:
            stdout, stderr = process.communicate()
            print(f"❌ App failed to launch")
            print(f"STDOUT: {stdout.decode()}")
            print(f"STDERR: {stderr.decode()}")
            return False
            
    except Exception as e:
        print(f"❌ Error launching app: {e}")
        return False

def main():
    """Main verification function"""
    print("🔍 Course Link Getter Package Verification")
    print("=" * 50)
    
    # Check DMG contents
    dmg_ok = check_dmg_contents()
    print()
    
    if dmg_ok:
        # Test app launch
        launch_ok = test_app_launch()
        print()
        
        if launch_ok:
            print("🎉 Package verification PASSED!")
            print("✅ DMG contains all necessary files")
            print("✅ App can launch successfully")
            print("✅ Catalog data is present and valid")
            return True
        else:
            print("❌ Package verification FAILED!")
            print("❌ App failed to launch")
            return False
    else:
        print("❌ Package verification FAILED!")
        print("❌ DMG missing required files")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
