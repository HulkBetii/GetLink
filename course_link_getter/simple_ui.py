#!/usr/bin/env python3
"""
Course Link Getter - Simple Interactive UI

A simple text-based interface that works on any system.
"""

import sys
from pathlib import Path
from core.store import CatalogStore
from core.models import Course, Category


class SimpleUI:
    """Simple interactive user interface."""
    
    def __init__(self):
        self.store = CatalogStore()
        self.current_courses = []
        self.load_data()
    
    def load_data(self):
        """Load course data."""
        print("🔄 Loading course catalog...")
        success = self.store.load_from_json("assets/catalog.sample.json")
        if not success:
            print("❌ Failed to load catalog data!")
            sys.exit(1)
        
        self.current_courses = self.store.list_all()
        print(f"✅ Loaded {len(self.current_courses)} courses from {len(self.store.list_categories())} categories")
    
    def show_menu(self):
        """Show main menu."""
        print("\n" + "="*60)
        print("🎓 Course Link Getter - Interactive Menu")
        print("="*60)
        print("1. Show all courses")
        print("2. Filter by category")
        print("3. Filter by subcategory")
        print("4. Search by text")
        print("5. Show categories")
        print("6. Copy all visible links")
        print("7. Export to CSV")
        print("8. Show course details")
        print("0. Exit")
        print("="*60)
    
    def show_courses(self, courses=None, title="Courses"):
        """Display courses in a table format."""
        if courses is None:
            courses = self.current_courses
        
        if not courses:
            print(f"No {title.lower()} found.")
            return
        
        print(f"\n{title} ({len(courses)} found):")
        print("-" * 100)
        print(f"{'#':<3} {'Title':<40} {'Category':<12} {'Subcategory':<12} {'Provider':<15}")
        print("-" * 100)
        
        for i, course in enumerate(courses, 1):
            title_short = course.title[:37] + "..." if len(course.title) > 40 else course.title
            print(f"{i:<3} {title_short:<40} {course.category:<12} {course.subcategory:<12} {course.provider:<15}")
        
        print("-" * 100)
        self.current_courses = courses
    
    def show_categories(self):
        """Show available categories and subcategories."""
        categories = self.store.list_categories()
        print(f"\n📚 Available Categories ({len(categories)}):")
        print("-" * 50)
        
        for category in categories:
            print(f"• {category.name}:")
            for sub in category.subcategories:
                print(f"  - {sub}")
            print()
    
    def filter_by_category(self):
        """Filter courses by category."""
        categories = self.store.list_categories()
        print("\nAvailable categories:")
        for i, cat in enumerate(categories, 1):
            print(f"{i}. {cat.name}")
        
        try:
            choice = int(input("\nEnter category number: ")) - 1
            if 0 <= choice < len(categories):
                category = categories[choice]
                courses = self.store.filter(category=category.name)
                self.show_courses(courses, f"{category.name} Courses")
            else:
                print("Invalid choice.")
        except ValueError:
            print("Invalid input.")
    
    def filter_by_subcategory(self):
        """Filter courses by subcategory."""
        categories = self.store.list_categories()
        print("\nAvailable categories:")
        for i, cat in enumerate(categories, 1):
            print(f"{i}. {cat.name}")
        
        try:
            cat_choice = int(input("\nEnter category number: ")) - 1
            if 0 <= cat_choice < len(categories):
                category = categories[cat_choice]
                print(f"\nAvailable subcategories for {category.name}:")
                for i, sub in enumerate(category.subcategories, 1):
                    print(f"{i}. {sub}")
                
                sub_choice = int(input("\nEnter subcategory number: ")) - 1
                if 0 <= sub_choice < len(category.subcategories):
                    subcategory = category.subcategories[sub_choice]
                    courses = self.store.filter(category=category.name, subcategory=subcategory)
                    self.show_courses(courses, f"{category.name} - {subcategory} Courses")
                else:
                    print("Invalid subcategory choice.")
            else:
                print("Invalid category choice.")
        except ValueError:
            print("Invalid input.")
    
    def search_by_text(self):
        """Search courses by text."""
        query = input("\nEnter search term: ").strip()
        if query:
            courses = self.store.filter(text=query)
            self.show_courses(courses, f"Search Results for '{query}'")
        else:
            print("No search term entered.")
    
    def copy_links(self):
        """Copy all visible course links to clipboard."""
        if not self.current_courses:
            print("No courses to copy.")
            return
        
        links = [course.link for course in self.current_courses]
        links_text = "\n".join(links)
        
        try:
            import subprocess
            if sys.platform == "darwin":  # macOS
                subprocess.run(["pbcopy"], input=links_text, text=True, check=True)
                print(f"✅ Copied {len(links)} links to clipboard!")
            elif sys.platform == "win32":  # Windows
                subprocess.run(["clip"], input=links_text, text=True, check=True)
                print(f"✅ Copied {len(links)} links to clipboard!")
            else:  # Linux
                subprocess.run(["xclip", "-selection", "clipboard"], input=links_text, text=True, check=True)
                print(f"✅ Copied {len(links)} links to clipboard!")
        except Exception as e:
            print(f"❌ Failed to copy to clipboard: {e}")
            print("\nLinks:")
            for i, link in enumerate(links, 1):
                print(f"{i}. {link}")
    
    def export_csv(self):
        """Export visible courses to CSV."""
        if not self.current_courses:
            print("No courses to export.")
            return
        
        filename = f"courses_export.csv"
        try:
            import csv
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['id', 'title', 'category', 'subcategory', 'provider', 'link', 'tags']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for course in self.current_courses:
                    writer.writerow({
                        'id': course.id,
                        'title': course.title,
                        'category': course.category,
                        'subcategory': course.subcategory,
                        'provider': course.provider,
                        'link': course.link,
                        'tags': ', '.join(course.tags) if course.tags else ''
                    })
            
            print(f"✅ Exported {len(self.current_courses)} courses to {filename}")
        except Exception as e:
            print(f"❌ Failed to export CSV: {e}")
    
    def show_course_details(self):
        """Show detailed information about a specific course."""
        if not self.current_courses:
            print("No courses to show details for.")
            return
        
        self.show_courses(self.current_courses, "Current Courses")
        
        try:
            choice = int(input("\nEnter course number to see details: ")) - 1
            if 0 <= choice < len(self.current_courses):
                course = self.current_courses[choice]
                print(f"\n📖 Course Details:")
                print("-" * 50)
                print(f"Title: {course.title}")
                print(f"Category: {course.category}")
                print(f"Subcategory: {course.subcategory}")
                print(f"Provider: {course.provider}")
                print(f"Link: {course.link}")
                print(f"Tags: {', '.join(course.tags) if course.tags else 'None'}")
                print("-" * 50)
            else:
                print("Invalid course number.")
        except ValueError:
            print("Invalid input.")
    
    def run(self):
        """Run the interactive interface."""
        print("🎓 Welcome to Course Link Getter!")
        
        while True:
            self.show_menu()
            choice = input("\nEnter your choice (0-8): ").strip()
            
            if choice == "0":
                print("👋 Goodbye!")
                break
            elif choice == "1":
                self.show_courses()
            elif choice == "2":
                self.filter_by_category()
            elif choice == "3":
                self.filter_by_subcategory()
            elif choice == "4":
                self.search_by_text()
            elif choice == "5":
                self.show_categories()
            elif choice == "6":
                self.copy_links()
            elif choice == "7":
                self.export_csv()
            elif choice == "8":
                self.show_course_details()
            else:
                print("Invalid choice. Please try again.")


def main():
    """Main function."""
    ui = SimpleUI()
    ui.run()


if __name__ == "__main__":
    main()
