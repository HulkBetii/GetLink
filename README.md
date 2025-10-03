# Course Link Getter

Lightweight PyQt5 desktop app to search a course catalog with modern UI and clipboard integration.

## Features
- **Smart Filtering**: Category, Subcategory, and Text filtering with instant updates
- **Clipboard Integration**: Copy single/bulk links with animated success notification
- **Modern UI**: Proportional table layout with beautiful interface
- **Export Functionality**: Export filtered results to CSV format
- **26 Courses**: Pre-loaded course catalog
- **macOS Ready**: Includes DMG installer and single executable

## Quick Start

### Option 1: Use Pre-built Package (Recommended)
1. **Download**: `Course_Link_Getter_macOS.dmg` (35MB)
2. **Install**: Open DMG and drag to Applications
3. **Run**: Launch from Applications or Launchpad

### Option 2: Use Single Executable
1. **Download**: `Course_Link_Getter_Darwin_Distribution.zip` (30.6MB)
2. **Extract**: Unzip the file
3. **Run**: Double-click `Course_Link_Getter`

### Option 3: Run from Source
```bash
git clone https://github.com/HulkBetii/GetLink.git
cd GetLink/course_link_getter
pip install -r requirements.txt
python launch_pyqt5.py
```

## Project Structure
```
GetLink/
├── course_link_getter/           # Main application
│   ├── assets/                   # Course data and icons
│   ├── core/                     # Business logic
│   ├── ui_pyqt5/                 # User interface
│   └── launch_pyqt5.py          # Application launcher
├── Course_Link_Getter_macOS.dmg  # macOS installer
├── Course_Link_Getter_Darwin_Distribution.zip  # Single executable
└── README.md                     # This file
```

## System Requirements
- **macOS**: 10.14+ (for pre-built packages)
- **Python**: 3.8+ (for source code)
- **Dependencies**: PyQt5, pydantic

## How to Use
1. **Launch** the application
2. **Search** for courses using the search bar
3. **Filter** by category or subcategory
4. **Click "Get Link"** to copy course links
5. **Use "Copy Visible Links"** for bulk copy
6. **Export to CSV** for data backup

## License
MIT License