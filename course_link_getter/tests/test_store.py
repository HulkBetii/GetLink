"""
Comprehensive pytest tests for CatalogStore functionality.

Tests cover all store operations with fixtures and CI-friendly execution.
"""

import pytest
import tempfile
import json
from pathlib import Path
from core.store import CatalogStore
from core.models import Course, Category


@pytest.fixture
def sample_catalog_path():
    """Fixture providing path to sample catalog JSON."""
    return "assets/catalog.sample.json"


@pytest.fixture
def loaded_store(sample_catalog_path):
    """Fixture providing a loaded CatalogStore with sample data."""
    store = CatalogStore()
    success = store.load_from_json(sample_catalog_path)
    assert success, "Failed to load sample catalog"
    return store


class TestCatalogStore:
    """Test suite for CatalogStore functionality."""
    
    def test_load_catalog_from_file(self, sample_catalog_path):
        """Test loading catalog from JSON file."""
        store = CatalogStore()
        success = store.load_from_json(sample_catalog_path)
        assert success
        assert len(store.list_all()) > 0
    
    def test_load_catalog_file_not_found(self):
        """Test loading catalog from non-existent file."""
        store = CatalogStore()
        success = store.load_from_json("non_existent.json")
        assert not success
    
    def test_list_all_count_ge_20(self, loaded_store):
        """Assert list_all() count >= 20."""
        all_courses = loaded_store.list_all()
        assert len(all_courses) >= 20, f"Expected >= 20 courses, got {len(all_courses)}"
        assert all(isinstance(course, Course) for course in all_courses)
    
    def test_list_categories(self, loaded_store):
        """Test listing categories."""
        categories = loaded_store.list_categories()
        assert len(categories) > 0
        assert all(isinstance(category, Category) for category in categories)
        
        # Verify category structure
        for category in categories:
            assert hasattr(category, 'name')
            assert hasattr(category, 'subcategories')
            assert isinstance(category.subcategories, list)
    
    def test_filter_category_only(self, loaded_store):
        """Test filtering by category only."""
        # Test English category
        english_courses = loaded_store.filter(category="English")
        assert len(english_courses) > 0
        assert all(course.category == "English" for course in english_courses)
        
        # Test Programming category
        programming_courses = loaded_store.filter(category="Programming")
        assert len(programming_courses) > 0
        assert all(course.category == "Programming" for course in programming_courses)
        
        # Test Design category
        design_courses = loaded_store.filter(category="Design")
        assert len(design_courses) > 0
        assert all(course.category == "Design" for course in design_courses)
    
    def test_filter_category_and_subcategory(self, loaded_store):
        """Test filtering by category and subcategory."""
        # Test English + IELTS
        ielts_courses = loaded_store.filter(category="English", subcategory="IELTS")
        assert len(ielts_courses) > 0
        assert all(course.category == "English" for course in ielts_courses)
        assert all(course.subcategory == "IELTS" for course in ielts_courses)
        
        # Test Programming + Python
        python_courses = loaded_store.filter(category="Programming", subcategory="Python")
        assert len(python_courses) > 0
        assert all(course.category == "Programming" for course in python_courses)
        assert all(course.subcategory == "Python" for course in python_courses)
        
        # Test Design + UI/UX
        ui_courses = loaded_store.filter(category="Design", subcategory="UI/UX")
        assert len(ui_courses) > 0
        assert all(course.category == "Design" for course in ui_courses)
        assert all(course.subcategory == "UI/UX" for course in ui_courses)
    
    def test_filter_text_search_title(self, loaded_store):
        """Test text search on course titles."""
        # Search for "Python" in titles
        python_courses = loaded_store.filter(text="Python")
        assert len(python_courses) > 0
        assert any("Python" in course.title for course in python_courses)
        
        # Search for "IELTS" in titles
        ielts_courses = loaded_store.filter(text="IELTS")
        assert len(ielts_courses) > 0
        assert any("IELTS" in course.title for course in ielts_courses)
        
        # Search for "Design" in titles
        design_courses = loaded_store.filter(text="Design")
        assert len(design_courses) > 0
        assert any("Design" in course.title for course in design_courses)
    
    def test_filter_text_search_tags(self, loaded_store):
        """Test text search on course tags."""
        # Search for tags (case-insensitive)
        all_courses = loaded_store.list_all()
        
        # Find courses with tags
        courses_with_tags = [c for c in all_courses if c.tags]
        if courses_with_tags:
            # Search for a tag from the first course with tags
            sample_tag = courses_with_tags[0].tags[0]
            tag_courses = loaded_store.filter(text=sample_tag)
            assert len(tag_courses) > 0
            assert any(sample_tag in course.tags for course in tag_courses)
    
    def test_filter_text_search_case_insensitive(self, loaded_store):
        """Test text search is case-insensitive."""
        # Test lowercase search
        python_lower = loaded_store.filter(text="python")
        python_upper = loaded_store.filter(text="PYTHON")
        python_title = loaded_store.filter(text="Python")
        
        # All should return the same results
        assert len(python_lower) == len(python_upper) == len(python_title)
        assert python_lower == python_upper == python_title
    
    def test_filter_no_matches_returns_empty(self, loaded_store):
        """Test that no matches returns empty list."""
        # Non-existent category
        empty_courses = loaded_store.filter(category="NonExistentCategory")
        assert empty_courses == []
        
        # Non-existent subcategory
        empty_courses = loaded_store.filter(category="English", subcategory="NonExistentSubcategory")
        assert empty_courses == []
        
        # Non-existent text search
        empty_courses = loaded_store.filter(text="NonExistentSearchTerm")
        assert empty_courses == []
    
    def test_filter_combined_filters(self, loaded_store):
        """Test combining multiple filters."""
        # Category + text search
        english_python = loaded_store.filter(category="English", text="IELTS")
        assert len(english_python) > 0
        assert all(course.category == "English" for course in english_python)
        assert any("IELTS" in course.title for course in english_python)
        
        # All three filters
        specific_courses = loaded_store.filter(
            category="Programming", 
            subcategory="Python", 
            text="Python"
        )
        assert len(specific_courses) > 0
        assert all(course.category == "Programming" for course in specific_courses)
        assert all(course.subcategory == "Python" for course in specific_courses)
        assert any("Python" in course.title for course in specific_courses)
    
    def test_save_to_json(self, loaded_store):
        """Test saving catalog to JSON file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
            temp_path = temp_file.name
        
        try:
            success = loaded_store.save_to_json(temp_path)
            assert success
            
            # Verify the file was created and has content
            with open(temp_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                assert 'courses' in data
                assert 'categories' in data
                assert len(data['courses']) >= 20
                assert len(data['categories']) > 0
                
                # Verify course structure
                for course_data in data['courses']:
                    assert 'id' in course_data
                    assert 'title' in course_data
                    assert 'category' in course_data
                    assert 'subcategory' in course_data
                    assert 'provider' in course_data
                    assert 'link' in course_data
                    assert 'tags' in course_data
        finally:
            Path(temp_path).unlink(missing_ok=True)
    
    def test_performance_under_2s(self, loaded_store):
        """Test that operations complete under 2 seconds."""
        import time
        
        start_time = time.time()
        
        # Run multiple operations
        for _ in range(100):
            loaded_store.list_all()
            loaded_store.filter(category="English")
            loaded_store.filter(category="Programming", subcategory="Python")
            loaded_store.filter(text="Python")
            loaded_store.filter(category="Design", text="UI")
        
        elapsed_time = time.time() - start_time
        assert elapsed_time < 2.0, f"Operations took {elapsed_time:.2f}s, expected < 2s"
    
    def test_course_model_validation(self, loaded_store):
        """Test that all courses have valid model structure."""
        all_courses = loaded_store.list_all()
        
        for course in all_courses:
            # Test required fields
            assert isinstance(course.id, str)
            assert isinstance(course.title, str)
            assert isinstance(course.category, str)
            assert isinstance(course.subcategory, str)
            assert isinstance(course.provider, str)
            assert isinstance(course.link, str)
            assert isinstance(course.tags, list)
            
            # Test non-empty required fields
            assert len(course.id) > 0
            assert len(course.title) > 0
            assert len(course.category) > 0
            assert len(course.subcategory) > 0
            assert len(course.provider) > 0
            assert len(course.link) > 0
            
            # Test link format
            assert course.link.startswith("http")
    
    def test_category_model_validation(self, loaded_store):
        """Test that all categories have valid model structure."""
        categories = loaded_store.list_categories()
        
        for category in categories:
            # Test required fields
            assert isinstance(category.name, str)
            assert isinstance(category.subcategories, list)
            
            # Test non-empty required fields
            assert len(category.name) > 0
            assert len(category.subcategories) > 0
            
            # Test subcategory structure
            for subcategory in category.subcategories:
                assert isinstance(subcategory, str)
                assert len(subcategory) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])