# Course Link Getter - Desktop Application

Lightweight PyQt5 desktop app for searching course catalogs with modern UI and clipboard integration.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python launch_pyqt5.py
```

## Features

- **Smart Search**: Category, subcategory, and text filtering
- **Clipboard Integration**: Copy single or bulk links
- **Export Functionality**: CSV export for filtered results
- **Modern UI**: Proportional table layout with responsive design
- **26 Courses**: Pre-loaded sample catalog
- **Cross-Platform**: macOS, Windows, Linux support

## Files

- `launch_pyqt5.py` - Application entry point
- `core/models.py` - Data models and validation
- `core/store.py` - Data management and loading
- `ui_pyqt5/main_window.py` - Main application window
- `ui_pyqt5/widgets/results_view.py` - Course table widget
- `assets/catalog.sample.json` - Sample course data
- `requirements.txt` - Python dependencies

## System Requirements

- Python 3.8+
- PyQt5 5.15+
- 50MB RAM minimum
- Any modern desktop OS

## Troubleshooting

**App won't start:**
```bash
pip install PyQt5==5.15.11 pydantic==2.5.2
```

**No data visible:**
- Check `assets/catalog.sample.json` exists
- Verify file permissions
- Look for console error messages

**UI issues:**
- Update PyQt5: `pip install --upgrade PyQt5`
- Check system DPI settings
- Restart application

See main README.md for detailed documentation.