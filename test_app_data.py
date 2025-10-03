#!/usr/bin/env python3
"""
Test script to verify app data loading in packaged application
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def test_packaged_app():
    """Test the packaged application data loading"""
    print("🧪 Testing packaged application data loading...")
    
    # Find mounted DMG
    result = subprocess.run(['mount'], capture_output=True, text=True)
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
        print("❌ Could not find mounted DMG")
        return False
    
    print(f"📁 Found DMG at: {volume_path}")
    
    # Check app bundle
    app_path = f"{volume_path}/Course Link Getter.app"
    executable_path = f"{app_path}/Contents/MacOS/Course Link Getter"
    
    if not os.path.exists(executable_path):
        print(f"❌ Executable not found: {executable_path}")
        return False
    
    print(f"✅ Executable found: {executable_path}")
    
    # Check catalog file in app bundle
    catalog_path = f"{app_path}/Contents/Resources/courses_link_getter/assets/catalog.sample.json"
    if not os.path.exists(catalog_path):
        print(f"❌ Catalog file not found: {catalog_path}")
        return False
    
    print(f"✅ Catalog file found: {catalog_path}")
    
    # Check catalog content
    with open(catalog_path, 'r') as f:
        content = f.read()
        if '"courses"' in content and len(content) > 1000:
            print(f"✅ Catalog contains data ({len(content)} characters)")
        else:
            print(f"❌ Catalog appears empty or corrupted")
            return False
    
    # Test app launch with output capture
    print("🚀 Testing app launch...")
    try:
        # Launch app and capture output
        process = subprocess.Popen(
            [executable_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait for app to start and capture initial output
        time.sleep(3)
        
        # Check if process is still running
        if process.poll() is None:
            print("✅ App launched successfully")
            
            # Try to get some output
            try:
                stdout, stderr = process.communicate(timeout=2)
                if stdout:
                    print(f"📝 App output: {stdout}")
                if stderr:
                    print(f"⚠️ App errors: {stderr}")
            except subprocess.TimeoutExpired:
                print("⏰ App is running (timeout waiting for output)")
            
            # Terminate the process
            process.terminate()
            return True
        else:
            stdout, stderr = process.communicate()
            print(f"❌ App failed to launch")
            print(f"STDOUT: {stdout}")
            print(f"STDERR: {stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing app: {e}")
        return False

def main():
    """Main test function"""
    print("🔍 Course Link Getter Packaged App Test")
    print("=" * 50)
    
    success = test_packaged_app()
    
    if success:
        print("\n🎉 Packaged app test PASSED!")
        print("✅ App can launch")
        print("✅ Catalog data is present")
        print("✅ App should display course data")
    else:
        print("\n❌ Packaged app test FAILED!")
        print("❌ App has issues with data loading")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
