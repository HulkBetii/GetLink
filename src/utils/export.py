import csv
from pathlib import Path
from typing import List
from ..models import Course


class ExportManager:
    """Handles export operations for course data."""
    
    @staticmethod
    def export_to_csv(courses: List[Course], file_path: str) -> bool:
        """Export courses to CSV file."""
        try:
            file_path = Path(file_path)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = [
                    'id', 'title', 'description', 'link', 'category', 'subcategory',
                    'duration', 'level', 'instructor', 'price', 'rating'
                ]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for course in courses:
                    writer.writerow({
                        'id': course.id,
                        'title': course.title,
                        'description': course.description,
                        'link': course.link,
                        'category': course.category,
                        'subcategory': course.subcategory,
                        'duration': course.duration or '',
                        'level': course.level or '',
                        'instructor': course.instructor or '',
                        'price': course.price or '',
                        'rating': course.rating or ''
                    })
            return True
        except Exception as e:
            print(f"Error exporting to CSV: {e}")
            return False
    
    @staticmethod
    def export_selected_courses(courses: List[Course], output_dir: str = "exports") -> str:
        """Export selected courses to CSV with timestamp."""
        from datetime import datetime
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"selected_courses_{timestamp}.csv"
        file_path = Path(output_dir) / filename
        
        success = ExportManager.export_to_csv(courses, str(file_path))
        return str(file_path) if success else ""
    
    @staticmethod
    def export_all_courses(courses: List[Course], output_dir: str = "exports") -> str:
        """Export all courses to CSV with timestamp."""
        from datetime import datetime
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"all_courses_{timestamp}.csv"
        file_path = Path(output_dir) / filename
        
        success = ExportManager.export_to_csv(courses, str(file_path))
        return str(file_path) if success else ""
