#!/usr/bin/env python3
"""
Test Data Loading - Course Link Getter
Verify that the catalog data is being loaded correctly
"""

import sys
from pathlib import Path

# Add the course_link_getter directory to Python path
app_dir = Path(__file__).parent
sys.path.insert(0, str(app_dir))

def test_data_loading():
    """Test if the catalog data is loading correctly"""
    try:
        print("🔍 Testing Course Link Getter Data Loading...")
        
        from core.store import CatalogStore
        from core.settings import SettingsManager
        
        # Test store initialization
        store = CatalogStore()
        settings_manager = SettingsManager()
        
        print(f"✅ Store initialized: {type(store)}")
        print(f"✅ Settings manager initialized: {type(settings_manager)}")
        
        # Test JSON loading
        json_path = Path(__file__).parent / "assets" / "catalog.sample.json"
        print(f"📁 Looking for catalog at: {json_path}")
        print(f"📁 File exists: {json_path.exists()}")
        
        if json_path.exists():
            print(f"📄 File size: {json_path.stat().st_size} bytes")
            
            # Try to load the data
            success = store.load_from_json(str(json_path))
            print(f"📊 Load success: {success}")
            
            if success:
                # Test basic operations
                all_courses = store.list_all()
                print(f"📚 Total courses loaded: {len(all_courses)}")
                
                categories = store.list_categories()
                print(f"📂 Categories loaded: {len(categories)}")
                for cat in categories:
                    print(f"   - {cat.name}: {len(cat.subcategories)} subcategories")
                
                # Test filtering
                english_courses = store.filter(category="English")
                print(f"🇬🇧 English courses: {len(english_courses)}")
                
                programming_courses = store.filter(category="Programming")
                print(f"💻 Programming courses: {len(programming_courses)}")
                
                design_courses = store.filter(category="Design")
                print(f"🎨 Design courses: {len(design_courses)}")
                
                # Test search
                search_results = store.filter(text="python")
                print(f"🔍 Search 'python': {len(search_results)} results")
                
                print("✅ Data loading test completed successfully!")
                return True
            else:
                print("❌ Failed to load catalog data")
                return False
        else:
            print("❌ Catalog file not found!")
            return False
            
    except Exception as e:
        print(f"❌ Data loading test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_data_loading()
