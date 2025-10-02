# Course Link Getter

A desktop application for managing and searching course catalogs with advanced filtering, clipboard integration, and export capabilities.

## 🎓 Features

### Core Functionality
- **Course Management**: Browse 26+ courses across 3 categories (English, Programming, Design)
- **Advanced Filtering**: Filter by category, subcategory, and text search
- **Real-time Search**: Instant filtering with debounced text search
- **Link Management**: Copy individual or bulk course links to clipboard
- **Export Capabilities**: Export filtered results to CSV

### User Interface
- **Desktop App**: PyQt5-based native desktop application
- **Web Interface**: Browser-based alternative using Python HTTP server
- **Interactive CLI**: Command-line interface for quick access
- **Settings Persistence**: Automatic saving and restoration of user preferences

### Technical Features
- **Cross-platform**: Works on macOS, Windows, and Linux
- **Performance**: Optimized for 1000+ items with <100ms search
- **Testing**: Comprehensive pytest test suite (15 tests, <2s runtime)
- **CI/CD**: GitHub Actions workflows for continuous integration

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- pip package manager

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/HulkBetii/GetLink.git
   cd GetLink/course_link_getter
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   # Desktop app (PyQt5)
   python app_pyqt5.py
   
   # Web interface
   python web_app.py
   
   # Interactive CLI
   python simple_ui.py
   ```

## 📱 User Interfaces

### 1. Desktop Application (PyQt5)
- Native desktop experience
- Advanced filtering panel
- Sortable table view
- Context menus and keyboard shortcuts
- Settings persistence

### 2. Web Interface
- Browser-based interface
- Access at `http://localhost:8081`
- Mobile-friendly responsive design
- Real-time filtering

### 3. Command Line Interface
- Interactive menu system
- Quick course browsing
- Clipboard integration
- CSV export functionality

## 🔧 Development

### Project Structure
```
course_link_getter/
├── core/                    # Core business logic
│   ├── models.py           # Pydantic data models
│   ├── store.py            # CatalogStore for data management
│   └── settings.py         # Settings persistence
├── ui_pyqt5/               # PyQt5 desktop UI
│   ├── main_window.py      # Main application window
│   └── widgets/           # UI components
├── tests/                  # Test suite
│   └── test_store.py       # Comprehensive pytest tests
├── assets/                 # Sample data
│   └── catalog.sample.json # Course catalog
└── requirements.txt        # Dependencies
```

### Running Tests
```bash
# Quick tests (CI-friendly)
make test-quick

# Verbose tests
make test

# With coverage
python -m pytest tests/test_store.py --cov=core --cov-report=term-missing
```

### CI/CD
The project includes GitHub Actions workflows:
- **`.github/workflows/ci.yml`** - Simple CI workflow
- **`.github/workflows/test.yml`** - Comprehensive testing with coverage

## 📊 Course Data

### Categories
- **English**: IELTS, TOEIC, Speaking
- **Programming**: Python, Web, Data
- **Design**: UI/UX, Graphic

### Sample Data
- 26 courses with diverse providers
- Valid HTTP links for all courses
- Comprehensive tags and metadata
- Real-world course examples

## 🛠️ Configuration

### Settings Persistence
- User preferences saved automatically
- Cross-platform data directory using `platformdirs`
- Filter states restored on startup
- Window size and position remembered

### Export Options
- **CSV Export**: title, category, subcategory, provider, link
- **Clipboard**: Individual or bulk link copying
- **Formats**: Newline-separated links for easy pasting

## 🧪 Testing

### Test Coverage
- **15 comprehensive test cases**
- **Runtime**: <2 seconds (CI-friendly)
- **Coverage**: 83% for core functionality
- **Performance**: Validated for 1000+ items

### Test Categories
- Data loading and validation
- Filter functionality (all combinations)
- Model validation
- Performance benchmarks
- Error handling

## 📈 Performance

### Benchmarks
- **Search Performance**: <100ms for 1000+ items
- **Filter Operations**: <1ms for category filtering
- **Memory Usage**: Optimized for large datasets
- **Startup Time**: <2 seconds with data loading

### Optimization
- Efficient filtering algorithms
- Debounced search (100ms delay)
- Lazy loading for large datasets
- Memory-efficient data structures

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `make test`
5. Submit a pull request

### Code Standards
- Follow PEP 8 style guidelines
- Add tests for new functionality
- Update documentation
- Ensure CI tests pass

## 📄 License

This project is open source and available under the MIT License.

## 🔗 Links

- **Repository**: [https://github.com/HulkBetii/GetLink.git](https://github.com/HulkBetii/GetLink.git)
- **Issues**: [GitHub Issues](https://github.com/HulkBetii/GetLink/issues)
- **Actions**: [GitHub Actions](https://github.com/HulkBetii/GetLink/actions)

## 🎯 Roadmap

### Planned Features
- [ ] Database backend support
- [ ] Advanced search operators
- [ ] Course rating and reviews
- [ ] Bulk import/export
- [ ] Plugin system
- [ ] Mobile app version

### Recent Updates
- ✅ Settings persistence implementation
- ✅ Comprehensive test suite
- ✅ CI/CD pipeline setup
- ✅ Performance optimizations
- ✅ Cross-platform compatibility

---

**Course Link Getter** - Your comprehensive solution for course catalog management! 🎓✨