from pydantic import BaseModel, Field
from typing import List


class Category(BaseModel):
    """Represents a category with its subcategories."""
    
    name: str = Field(..., description="Category name")
    subcategories: List[str] = Field(..., description="List of subcategory names")
    
    def get_all_categories(self) -> List[str]:
        """Get all categories including subcategories."""
        return [self.name] + self.subcategories
    
    def has_subcategory(self, subcategory: str) -> bool:
        """Check if a subcategory exists in this category."""
        return subcategory in self.subcategories
