# Course Link Getter

Lightweight PyQt5 desktop app to search a course catalog.

## Features
- Category, Subcategory, and Text filtering with instant updates
- Copy single/bulk links with animated success notification
- Proportional table layout (Title 1/2; Category 2/5; Subcategory 2/5; Actions 1/5)
- Minimal transparent scrollbars; modern light theme

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

## Notes
- Recommended Python 3.11+
- Single-language desktop app only
- Minimal project structure for easy maintenance

MIT License