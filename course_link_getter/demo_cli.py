#!/usr/bin/env python3
"""
Course Link Getter - Command Line Demo

Demonstrates the core functionality without GUI dependencies.
"""

import sys
from pathlib import Path

# Add the course_link_getter directory to Python path
app_dir = Path(__file__).parent
sys.path.insert(0, str(app_dir))

from core.store import CatalogStore
from core.models import Course, Category


def print_courses(courses, title="Courses"):
    """Print courses in a formatted table."""
    if not courses:
        print(f"No {title.lower()} found.")
        return
    
    print(f"\n{title} ({len(courses)} found):")
    print("=" * 80)
    print(f"{'Title':<40} {'Category':<12} {'Subcategory':<12} {'Provider':<15}")
    print("-" * 80)
    
    for course in courses:
        title_short = course.title[:37] + "..." if len(course.title) > 40 else course.title
        print(f"{title_short:<40} {course.category:<12} {course.subcategory:<12} {course.provider:<15}")
    
    print("=" * 80)


def main():
    """Main demo function."""
    print("🎓 Course Link Getter - Command Line Demo")
    print("=" * 50)
    
    # Initialize store
    store = CatalogStore()
    
    # Load data
    print("Loading course catalog...")
    success = store.load_from_json("assets/catalog.sample.json")
    if not success:
        print("❌ Failed to load catalog data!")
        return
    
    print("✅ Catalog loaded successfully!")
    
    # Show categories
    categories = store.list_categories()
    print(f"\n📚 Available Categories ({len(categories)}):")
    for cat in categories:
        print(f"  • {cat.name}: {', '.join(cat.subcategories)}")
    
    # Show all courses
    all_courses = store.list_all()
    print_courses(all_courses, f"All Courses")
    
    # Demo filtering
    print("\n🔍 Filtering Demos:")
    
    # Filter by category
    eng_courses = store.filter(category="English")
    print_courses(eng_courses, "English Courses")
    
    # Filter by category and subcategory
    python_courses = store.filter(category="Programming", subcategory="Python")
    print_courses(python_courses, "Python Programming Courses")
    
    # Search by text
    ielts_courses = store.filter(text="IELTS")
    print_courses(ielts_courses, "IELTS Courses (Text Search)")
    
    # Search by provider
    coursera_courses = store.filter(text="Coursera")
    print_courses(coursera_courses, "Coursera Courses")
    
    # Show course details
    if all_courses:
        print(f"\n📖 Sample Course Details:")
        print("-" * 50)
        sample_course = all_courses[0]
        print(f"Title: {sample_course.title}")
        print(f"Category: {sample_course.category}")
        print(f"Subcategory: {sample_course.subcategory}")
        print(f"Provider: {sample_course.provider}")
        print(f"Link: {sample_course.link}")
        print(f"Tags: {', '.join(sample_course.tags) if sample_course.tags else 'None'}")
    
    # Export demo
    print(f"\n💾 Export Demo:")
    export_file = "demo_export.csv"
    if store.save_to_json(export_file):
        print(f"✅ Exported all courses to {export_file}")
    else:
        print("❌ Export failed")
    
    print(f"\n🎉 Demo completed! The application is fully functional.")
    print(f"📊 Summary: {len(all_courses)} courses across {len(categories)} categories")


if __name__ == "__main__":
    main()
