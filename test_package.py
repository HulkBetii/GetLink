#!/usr/bin/env python3
"""
Test script to verify package data integrity
"""

import sys
import os
from pathlib import Path

def test_data_loading():
    """Test if the package can load data correctly"""
    print("🔍 Testing package data loading...")
    
    # Add the course_link_getter directory to Python path
    app_dir = Path(__file__).parent
    course_dir = app_dir / "course_link_getter"
    if course_dir.exists():
        sys.path.insert(0, str(course_dir))
        print(f"📁 Added to path: {course_dir}")
    else:
        sys.path.insert(0, str(app_dir))
        print(f"📁 Added to path: {app_dir}")
    
    try:
        from core.store import CatalogStore
        from core.models import Course
        
        print("✅ Core modules imported successfully")
        
        # Test store initialization
        store = CatalogStore()
        print("✅ CatalogStore initialized")
        
        # Test data loading
        legacy_path = Path(__file__).parent / "course_link_getter" / "assets" / "catalog.sample.json"
        print(f"📁 Looking for catalog at: {legacy_path}")
        print(f"📁 Catalog exists: {legacy_path.exists()}")
        
        if legacy_path.exists():
            if store.load_from_json(str(legacy_path)):
                courses = store.list_all()
                print(f"✅ Loaded {len(courses)} courses from catalog")
                
                if courses:
                    print("📋 Sample courses:")
                    for i, course in enumerate(courses[:3]):
                        print(f"  {i+1}. {course.title} ({course.category})")
                    return True
                else:
                    print("❌ No courses found in catalog")
                    return False
            else:
                print("❌ Failed to load catalog data")
                return False
        else:
            print("❌ Catalog file not found")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_package_structure():
    """Test package structure"""
    print("📦 Testing package structure...")
    
    # Check if we're in the right directory
    current_dir = Path.cwd()
    print(f"📁 Current directory: {current_dir}")
    
    # Look for course_link_getter directory
    course_dir = current_dir / "course_link_getter"
    if not course_dir.exists():
        course_dir = current_dir
        print("📁 Using current directory as course_link_getter")
    
    required_files = [
        "assets/catalog.sample.json",
        "core/__init__.py",
        "core/models.py", 
        "core/store.py",
        "ui_pyqt5/main_window.py",
        "ui_pyqt5/widgets/results_view.py",
        "launch_pyqt5.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        full_path = course_dir / file_path
        if not full_path.exists():
            missing_files.append(file_path)
        else:
            print(f"✅ {file_path}")
    
    if missing_files:
        print("❌ Missing files:")
        for file_path in missing_files:
            print(f"  - {file_path}")
        return False
    else:
        print("✅ All required files present")
        return True

def main():
    """Main test function"""
    print("🧪 Course Link Getter Package Test")
    print("=" * 50)
    
    # Test package structure
    structure_ok = test_package_structure()
    print()
    
    # Test data loading
    data_ok = test_data_loading()
    print()
    
    if structure_ok and data_ok:
        print("🎉 Package test PASSED!")
        return True
    else:
        print("❌ Package test FAILED!")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
