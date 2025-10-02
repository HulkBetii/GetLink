# Course Link Getter

A desktop application for browsing and accessing course links through hierarchical category navigation with clipboard integration and export capabilities.

## Features

- **Hierarchical Navigation**: Browse courses by Category → Subcategory
- **Search & Filter**: Filter courses by category/subcategory combinations
- **Link Management**: Copy individual course links or all visible links to clipboard
- **Export Capabilities**: Export selected or all courses to CSV
- **Persistent Filters**: Remember last applied filters between sessions
- **Browser Integration**: Optional "Open in browser" functionality

## Requirements

- Python 3.11+
- PyQt6
- pydantic

## Installation

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the application:
```bash
python src/main.py
```

## Project Structure

```
GetLink/
├── src/
│   ├── models/          # Data models (Course, Category)
│   ├── ui/             # User interface components
│   ├── data/           # Data management and mock data
│   ├── utils/          # Utility functions (clipboard, export)
│   └── main.py         # Application entry point
├── requirements.txt    # Python dependencies
├── PROJECT_BRIEF.md    # Detailed project documentation
└── README.md          # This file
```

## Data

The application uses mock course data stored in `src/data/mock_courses.json`. This includes:
- 5 main categories (English, Programming, Design, Business, Data Science)
- Multiple subcategories per main category
- 12 sample courses with complete metadata

## Development

This project follows a modular architecture:
- **Models**: Pydantic data models for type safety
- **UI**: PyQt6-based user interface
- **Data**: JSON-based data storage with filtering capabilities
- **Utils**: Reusable utility functions for clipboard and export operations

## License

This project is for educational/demonstration purposes.
