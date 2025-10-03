# Course Link Getter

A lightweight PyQt5 desktop application for searching and managing course catalogs with modern UI and clipboard integration.

## Features

- **🔍 Smart Search**: Real-time filtering by category, subcategory, and text content
- **📋 Clipboard Integration**: Copy individual links or bulk copy filtered results
- **📊 Data Export**: Export filtered results to CSV format
- **🎨 Modern UI**: Clean, responsive interface with proportional table layout
- **🚀 Quick Launch**: Fast startup with pre-loaded course data
- **📱 Cross-Platform**: Works on macOS, Windows, and Linux

## 📦 Quick Start

### Prerequisites
- Python 3.8 or higher
- PyQt5 library

### Installation & Run

1. **Clone the repository:**
   ```bash
   git clone https://github.com/HulkBetii/GetLink.git
   cd GetLink/course_link_getter
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch the application:**
   ```bash
   python launch_pyqt5.py
   ```

## 📁 Project Structure

```
course_link_getter/
├── assets/                    # Application data and icons
│   ├── catalog.sample.json   # Course catalog data
│   └── icon.*               # Application icons (ico, icns, png)
├── core/                     # Core business logic
│   ├── models.py            # Data models (Course, etc.)
│   └── store.py             # Data storage and management
├── ui_pyqt5/                # User interface components
│   ├── main_window.py       # Main application window
│   └── widgets/
│       └── results_view.py   # Course results table widget
├── launch_pyqt5.py          # Application entry point
├── requirements.txt          # Python dependencies
└── README.md                # Application documentation
```

## 💻 System Requirements

- **Python**: 3.8+ (recommended: 3.11+)
- **Operating System**: macOS, Windows, or Linux
- **Memory**: 50MB RAM minimum
- **Dependencies**: PyQt5, pydantic

## 🎯 How to Use

1. **Launch** the application from terminal or IDE
2. **Search** for courses using the search bar
3. **Filter** results by category or subcategory
4. **Copy links** using "Get Link" buttons or bulk "Copy Visible Links"
5. **Export** filtered data to CSV if needed

## 🛠️ Development

### Adding New Courses
Edit `assets/catalog.sample.json` to add or modify course data:

```json
{
  "title": "Course Title",
  "category": "Category Name", 
  "subcategory": "Subcategory Name",
  "link": "https://course-url.com"
}
```

### Customizing UI
- Modify `ui_pyqt5/main_window.py` for window layout
- Update `ui_pyqt5/widgets/results_view.py` for table appearance
- Add new icons to `assets/` directory

### Adding Features
- Extend `core/models.py` for new data structures
- Update `core/store.py` for data management logic
- Add new widgets in `ui_pyqt5/widgets/`

## 📊 Sample Data

The application comes with a pre-loaded catalog containing 26 sample courses across various categories:
- Technology & Programming
- Business & Management  
- Design & Creative
- And more...

## 🔧 Troubleshooting

### Common Issues

**Application won't start:**
- Ensure Python 3.8+ is installed
- Install PyQt5: `pip install PyQt5`
- Check that all files are in correct locations

**No data visible:**
- Verify `assets/catalog.sample.json` exists
- Check file permissions
- Look for console error messages

**UI looks incorrect:**
- Update PyQt5: `pip install --upgrade PyQt5`
- Check system DPI settings
- Verify Python version compatibility

## 📝 Dependencies

- **PyQt5**: Cross-platform GUI framework
- **pydantic**: Data validation and settings management

All dependencies are listed in `requirements.txt` and can be installed with:
```bash
pip install -r requirements.txt
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the source code for details.

## 🔗 Links

- **Repository**: [https://github.com/HulkBetii/GetLink](https://github.com/HulkBetii/GetLink)
- **Documentation**: See `course_link_getter/README.md` for detailed app documentation

---

**Course Link Getter** - Simple, fast, and efficient course catalog management.