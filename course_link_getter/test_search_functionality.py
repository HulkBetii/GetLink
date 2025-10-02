#!/usr/bin/env python3
"""
Test Search Functionality - Course Link Getter
Verify that search and filtering is working correctly
"""

import sys
from pathlib import Path

# Add the course_link_getter directory to Python path
app_dir = Path(__file__).parent
sys.path.insert(0, str(app_dir))

def test_search_functionality():
    """Test search and filtering functionality"""
    try:
        print("🔍 Testing Course Link Getter Search Functionality...")
        
        from core.store import CatalogStore
        from core.settings import SettingsManager
        
        # Initialize store and load data
        store = CatalogStore()
        settings_manager = SettingsManager()
        
        json_path = Path(__file__).parent / "assets" / "catalog.sample.json"
        if not store.load_from_json(str(json_path)):
            print("❌ Failed to load catalog data")
            return False
        
        print(f"✅ Loaded {len(store.list_all())} courses")
        
        # Test category filtering
        print("\n📂 Testing Category Filtering:")
        english_courses = store.filter(category="English")
        print(f"   English courses: {len(english_courses)}")
        for course in english_courses[:3]:  # Show first 3
            print(f"   - {course.title} ({course.subcategory})")
        
        programming_courses = store.filter(category="Programming")
        print(f"   Programming courses: {len(programming_courses)}")
        for course in programming_courses[:3]:  # Show first 3
            print(f"   - {course.title} ({course.subcategory})")
        
        # Test subcategory filtering
        print("\n🏷️ Testing Subcategory Filtering:")
        ielts_courses = store.filter(category="English", subcategory="IELTS")
        print(f"   IELTS courses: {len(ielts_courses)}")
        for course in ielts_courses:
            print(f"   - {course.title}")
        
        python_courses = store.filter(category="Programming", subcategory="Python")
        print(f"   Python courses: {len(python_courses)}")
        for course in python_courses:
            print(f"   - {course.title}")
        
        # Test text search
        print("\n🔍 Testing Text Search:")
        search_terms = ["python", "ielts", "design", "web", "data"]
        for term in search_terms:
            results = store.filter(text=term)
            print(f"   '{term}': {len(results)} results")
            if results:
                print(f"     - {results[0].title}")
        
        # Test combined filtering
        print("\n🔗 Testing Combined Filtering:")
        python_search = store.filter(category="Programming", text="python")
        print(f"   Programming + 'python': {len(python_search)} results")
        
        english_search = store.filter(category="English", text="speaking")
        print(f"   English + 'speaking': {len(english_search)} results")
        
        print("\n✅ Search functionality test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Search functionality test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_search_functionality()
