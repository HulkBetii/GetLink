from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Union


class Category(BaseModel):
    """Represents a category with its subcategories."""
    name: str = Field(..., description="Category name")
    subcategories: List[str] = Field(default_factory=list, description="List of subcategory names")


class Course(BaseModel):
    """Represents a course with all its metadata."""
    id: str = Field(..., description="Unique identifier for the course")
    title: Union[str, Dict[str, str]] = Field(..., description="Course title (string or multilingual dict)")
    category: str = Field(..., description="Main category name")
    subcategory: str = Field(..., description="Subcategory name")
    link: str = Field(..., description="Course URL")
    
    def get_title(self, language_code: str = "en") -> str:
        """Get course title in specified language."""
        if isinstance(self.title, dict):
            return self.title.get(language_code, self.title.get("en", "Unknown Title"))
        return self.title