from pydantic import BaseModel, Field
from typing import Optional


class Course(BaseModel):
    """Represents a course with all its metadata."""
    
    id: str = Field(..., description="Unique identifier for the course")
    title: str = Field(..., description="Course title")
    description: str = Field(..., description="Course description")
    link: str = Field(..., description="Course URL")
    category: str = Field(..., description="Main category name")
    subcategory: str = Field(..., description="Subcategory name")
    duration: Optional[str] = Field(None, description="Course duration (e.g., '2 hours', '4 weeks')")
    level: Optional[str] = Field(None, description="Difficulty level (e.g., 'Beginner', 'Intermediate', 'Advanced')")
    instructor: Optional[str] = Field(None, description="Instructor name")
    price: Optional[str] = Field(None, description="Course price")
    rating: Optional[float] = Field(None, ge=0.0, le=5.0, description="Course rating (0-5 stars)")
    
    class Config:
        json_encoders = {
            # Add any custom encoders if needed
        }
