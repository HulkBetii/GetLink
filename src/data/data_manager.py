import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from ..models import Course, Category


class DataManager:
    """Manages course and category data loading and filtering."""
    
    def __init__(self, data_file_path: str = "src/data/mock_courses.json"):
        self.data_file_path = Path(data_file_path)
        self.courses: List[Course] = []
        self.categories: List[Category] = []
        self._load_data()
    
    def _load_data(self) -> None:
        """Load course and category data from JSON file."""
        try:
            with open(self.data_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Load categories
            self.categories = [Category(**cat_data) for cat_data in data.get('categories', [])]
            
            # Load courses
            self.courses = [Course(**course_data) for course_data in data.get('courses', [])]
            
        except FileNotFoundError:
            print(f"Data file not found: {self.data_file_path}")
            self.categories = []
            self.courses = []
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON data: {e}")
            self.categories = []
            self.courses = []
        except Exception as e:
            print(f"Error loading data: {e}")
            self.categories = []
            self.courses = []
    
    def get_all_courses(self) -> List[Course]:
        """Get all available courses."""
        return self.courses.copy()
    
    def get_courses_by_category(self, category: str, subcategory: Optional[str] = None) -> List[Course]:
        """Get courses filtered by category and optionally subcategory."""
        filtered_courses = []
        
        for course in self.courses:
            if course.category == category:
                if subcategory is None or course.subcategory == subcategory:
                    filtered_courses.append(course)
        
        return filtered_courses
    
    def get_all_categories(self) -> List[Category]:
        """Get all available categories."""
        return self.categories.copy()
    
    def get_subcategories(self, category_name: str) -> List[str]:
        """Get subcategories for a specific category."""
        for category in self.categories:
            if category.name == category_name:
                return category.subcategories.copy()
        return []
    
    def search_courses(self, query: str) -> List[Course]:
        """Search courses by title, description, or instructor."""
        query_lower = query.lower()
        matching_courses = []
        
        for course in self.courses:
            if (query_lower in course.title.lower() or 
                query_lower in course.description.lower() or 
                (course.instructor and query_lower in course.instructor.lower())):
                matching_courses.append(course)
        
        return matching_courses
    
    def get_course_by_id(self, course_id: str) -> Optional[Course]:
        """Get a specific course by its ID."""
        for course in self.courses:
            if course.id == course_id:
                return course
        return None
    
    def get_courses_by_level(self, level: str) -> List[Course]:
        """Get courses filtered by difficulty level."""
        return [course for course in self.courses if course.level == level]
    
    def get_courses_by_rating(self, min_rating: float) -> List[Course]:
        """Get courses with rating >= min_rating."""
        return [course for course in self.courses 
                if course.rating is not None and course.rating >= min_rating]
