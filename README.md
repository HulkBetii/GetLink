# Course Link Getter

Lightweight PyQt5 desktop app to search a course catalog with modern UI and clipboard integration.

## Features
- **Smart Filtering**: Category, Subcategory, and Text filtering with instant updates
- **Clipboard Integration**: Copy single/bulk links with animated success notification
- **Modern UI**: Proportional table layout (Title 50%; Category 20%; Subcategory 20%; Actions 10%)
- **Export Functionality**: Export filtered results to CSV format
- **Responsive Design**: Minimal transparent scrollbars with modern light theme
- **Cross-platform**: Works on macOS, Windows, and Linux

## Quick start
```bash
git clone https://github.com/HulkBetii/GetLink.git
cd GetLink/course_link_getter
pip install -r requirements.txt
python launch_pyqt5.py
```


## Project layout
```
course_link_getter/
├── assets/
│   └── catalog.sample.json
├── core/
│   ├── models.py
│   └── store.py
├── ui_pyqt5/
│   ├── main_window.py
│   └── widgets/
│       └── results_view.py
├── launch_pyqt5.py
├── requirements.txt
└── README.md
```

## Recent Updates
- ✅ Fixed table header display issues (proper column titles)
- ✅ Resolved missing import errors
- ✅ Improved translation system
- ✅ Enhanced UI responsiveness

## Requirements
- Python 3.8+ (recommended 3.11+)
- PyQt5 5.15+
- Cross-platform compatibility

## Development
- Minimal project structure for easy maintenance
- Single-language desktop app
- Clean separation of concerns (UI, Core, Models)

## License
MIT License