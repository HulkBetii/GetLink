import json
from pathlib import Path
from typing import List, Optional
from .models import Course, Category


class CatalogStore:
    """Manages course catalog data loading, saving, and querying."""
    
    def __init__(self):
        self.courses: List[Course] = []
        self.categories: List[Category] = []
    
    def load_from_json(self, path: str) -> bool:
        """Load catalog data from JSON file."""
        try:
            json_path = Path(path)
            if not json_path.exists():
                print(f"Catalog file not found: {json_path}")
                return False
            
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Load categories
            self.categories = []
            for cat_data in data.get('categories', []):
                category = Category(
                    name=cat_data['name'],
                    subcategories=cat_data.get('subcategories', [])
                )
                self.categories.append(category)
            
            # Load courses
            self.courses = [Course(**course_data) for course_data in data.get('courses', [])]
            
            return True
            
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error parsing catalog data: {e}")
            return False
        except Exception as e:
            print(f"Error loading catalog: {e}")
            return False
    
    def save_to_json(self, path: str) -> bool:
        """Save current catalog data to JSON file."""
        try:
            json_path = Path(path)
            json_path.parent.mkdir(parents=True, exist_ok=True)
            
            data = {
                "categories": [
                    {
                        "name": cat.name,
                        "subcategories": cat.subcategories
                    }
                    for cat in self.categories
                ],
                "courses": [course.model_dump() for course in self.courses]
            }
            
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"Error saving catalog: {e}")
            return False
    
    def list_all(self) -> List[Course]:
        """Get all available courses."""
        return self.courses.copy()
    
    def list_categories(self) -> List[Category]:
        """Get all available categories."""
        return self.categories.copy()
    
    def filter(self, category: Optional[str] = None, subcategory: Optional[str] = None, text: Optional[str] = None) -> List[Course]:
        """Filter courses by category, subcategory, and/or text search.
        
        Optimized for performance - should handle 1k+ items in under 100ms.
        """
        filtered_courses = self.courses
        
        # Filter by category (fastest filter first)
        if category:
            filtered_courses = [course for course in filtered_courses if course.category == category]
        
        # Filter by subcategory
        if subcategory:
            filtered_courses = [course for course in filtered_courses if course.subcategory == subcategory]
        
        # Filter by text search (most expensive, do last)
        if text:
            text_lower = text.lower()
            # Pre-compile search terms for better performance
            filtered_courses = [
                course for course in filtered_courses
                if (text_lower in course.title.lower() or
                    text_lower in course.provider.lower() or
                    any(text_lower in tag.lower() for tag in course.tags))
            ]
        
        return filtered_courses