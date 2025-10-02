from pydantic import BaseModel, Field
from typing import List


class Category(BaseModel):
    """Represents a category with its subcategories."""
    name: str = Field(..., description="Category name")
    subcategories: List[str] = Field(default_factory=list, description="List of subcategory names")


class Course(BaseModel):
    """Represents a course with all its metadata."""
    id: str = Field(..., description="Unique identifier for the course")
    title: str = Field(..., description="Course title")
    category: str = Field(..., description="Main category name")
    subcategory: str = Field(..., description="Subcategory name")
    provider: str = Field(..., description="Course provider/platform")
    link: str = Field(..., description="Course URL")
    tags: List[str] = Field(default_factory=list, description="Course tags")