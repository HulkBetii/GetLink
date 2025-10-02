# Course Link Getter - Project Brief

## Project Overview
A desktop application for browsing and accessing course links through hierarchical category navigation with clipboard integration and export capabilities.

## Scope

### In Scope
- **Hierarchical Navigation**: Two-level category system (Category → Subcategory)
- **Search & Filter**: Filter courses by category/subcategory combinations
- **Results Display**: Table/card view in center pane with course details
- **Link Management**: 
  - "Get Link" button per course → copy to clipboard
  - Optional "Open in browser" functionality
- **Bulk Operations**:
  - "All results" view (no filters applied)
  - Export selected results to CSV
  - Copy all visible links to clipboard
- **Persistence**: Remember last applied filters between sessions
- **Local Data**: Mock course catalog stored as JSON

### Out of Scope
- User authentication/authorization
- Network connectivity or web scraping
- Real-time data updates
- Multi-user support
- Cloud synchronization

## Core Entities

### Course
```python
class Course(BaseModel):
    id: str
    title: str
    description: str
    link: str
    category: str
    subcategory: str
    duration: Optional[str] = None
    level: Optional[str] = None
    instructor: Optional[str] = None
```

### Category
```python
class Category(BaseModel):
    name: str
    subcategories: List[str]
```

## Primary User Flows

### 1. Browse by Category
1. User selects category from left panel
2. System shows subcategories for selected category
3. User selects subcategory
4. Center pane displays filtered courses
5. User can click "Get Link" to copy course URL

### 2. Search All Courses
1. User clicks "All Results" button
2. Center pane shows all available courses
3. User can still use "Get Link" on individual items

### 3. Export Data
1. User selects multiple courses (checkbox selection)
2. User clicks "Export to CSV" button
3. System generates CSV file with selected course data

### 4. Copy All Links
1. User applies any filter (or "All Results")
2. User clicks "Copy All Links" button
3. System copies all visible course links to clipboard

## Technical Stack
- **Language**: Python 3.11
- **GUI Framework**: PyQt6
- **Data Models**: Pydantic
- **Data Storage**: Local JSON files
- **Export Format**: CSV

## Success Criteria
- [ ] User can navigate categories and subcategories intuitively
- [ ] Search results display clearly with all relevant course information
- [ ] "Get Link" functionality works reliably (clipboard integration)
- [ ] Export to CSV includes all selected course data
- [ ] "Copy All Links" works for any filtered view
- [ ] Last applied filters persist between app sessions
- [ ] App responds smoothly with 1000+ course entries
- [ ] Clean, professional UI that's easy to navigate

## File Structure
```
GetLink/
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── course.py
│   │   └── category.py
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── main_window.py
│   │   ├── category_panel.py
│   │   └── results_panel.py
│   ├── data/
│   │   ├── __init__.py
│   │   ├── data_manager.py
│   │   └── mock_courses.json
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── clipboard.py
│   │   └── export.py
│   └── main.py
├── requirements.txt
├── README.md
└── PROJECT_BRIEF.md
```

## Development Phases
1. **Phase 1**: Core data models and mock data
2. **Phase 2**: Basic UI layout and navigation
3. **Phase 3**: Search/filter functionality
4. **Phase 4**: Link management and clipboard integration
5. **Phase 5**: Export and bulk operations
6. **Phase 6**: Persistence and polish
