# Course Link Getter

A desktop application for browsing and accessing course links through hierarchical category navigation with clipboard integration and export capabilities.

## Features

- **Hierarchical Navigation**: Browse courses by Category → Subcategory
- **Search & Filter**: Filter courses by category/subcategory combinations
- **Link Management**: Copy individual course links or all visible links to clipboard
- **Export Capabilities**: Export selected or all courses to CSV
- **Real-time Search**: Search courses by title, description, or instructor
- **Clean UI**: Modern PyQt6 interface with table view and filtering controls

## Requirements

- Python 3.11+
- PyQt6
- pydantic

## Installation

1. Clone or download this repository
2. Navigate to the course_link_getter directory:
   ```bash
   cd course_link_getter
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Quick Start

Run the application:
```bash
python app.py
```

### Using the Application

1. **Browse by Category**: 
   - Select a category from the left panel
   - Choose a subcategory (optional)
   - View filtered results in the table

2. **Search Courses**:
   - Use the search box to find courses by title, description, or instructor
   - Results update in real-time as you type

3. **Get Course Links**:
   - Double-click any course row to copy its link to clipboard
   - Use "Copy All Links" to copy all visible course links

4. **Export Data**:
   - Click "Export to CSV" to save all visible courses to a CSV file
   - Use File → Export to CSV menu option

5. **Show All Results**:
   - Click "Show All Results" to view all available courses

## Project Structure

```
course_link_getter/
├── app.py                    # Main application entry point
├── core/
│   ├── __init__.py
│   ├── models.py            # Pydantic data models
│   └── store.py             # Catalog data management
├── ui/
│   ├── __init__.py
│   ├── main_window.py       # Main application window
│   └── widgets/
│       ├── __init__.py
│       ├── filters_panel.py # Category/subcategory filters
│       ├── results_view.py  # Course results table
│       └── toolbar.py       # Action buttons
├── assets/
│   └── catalog.sample.json  # Sample course data
├── tests/
│   └── test_store.py        # Unit tests
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Data Format

The application uses JSON data with the following structure:

```json
{
  "categories": [
    {
      "name": "Category Name",
      "description": "Category description",
      "subcategories": [
        {
          "name": "Subcategory Name",
          "description": "Subcategory description"
        }
      ]
    }
  ],
  "courses": [
    {
      "id": "unique-id",
      "title": "Course Title",
      "description": "Course description",
      "link": "https://example.com/course",
      "category": "Category Name",
      "subcategory": "Subcategory Name",
      "duration": "8 weeks",
      "level": "Intermediate",
      "instructor": "Instructor Name",
      "price": "$199",
      "rating": 4.8
    }
  ]
}
```

## Development

### Running Tests

```bash
python -m pytest tests/
```

### Adding New Courses

Edit the `assets/catalog.sample.json` file to add new courses or categories. The application will automatically load the updated data on restart.

### Customizing the Interface

The UI is built with PyQt6 and organized into modular widgets:
- `FiltersPanel`: Category and search controls
- `ResultsView`: Course display table
- `Toolbar`: Action buttons
- `MainWindow`: Main application window

## Keyboard Shortcuts

- `Ctrl+S`: Export to CSV
- `Ctrl+Q`: Quit application
- `Enter`: Copy selected course link (when table is focused)

## Troubleshooting

### Common Issues

1. **"No module named 'PyQt6'"**: Install PyQt6 with `pip install PyQt6`
2. **Clipboard not working**: Ensure your system has clipboard utilities (pbcopy on macOS, clip on Windows, xclip on Linux)
3. **Data not loading**: Check that `assets/catalog.sample.json` exists and is valid JSON

### Platform-Specific Notes

- **macOS**: Uses `pbcopy` for clipboard operations
- **Windows**: Uses `clip` for clipboard operations  
- **Linux**: Requires `xclip` package for clipboard operations

## License

This project is for educational/demonstration purposes.
