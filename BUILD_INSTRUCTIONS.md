# Hướng dẫn đóng gói Course Link Getter

## 📦 Đã tạo sẵn cho macOS
- ✅ **Course_Link_Getter_macOS.dmg** (35MB) - File cài đặt cho macOS
- ✅ **Course Link Getter.app** - Ứng dụng macOS trong thư mục `dist/`

## 🪟 Build cho Windows

### Cách 1: Sử dụng script tự động
```bash
# Trên máy Windows, chạy:
python build_all.py
```

### Cách 2: Build thủ công trên Windows
```bash
# 1. Cài đặt PyInstaller
pip install pyinstaller

# 2. Chạy build script
build_windows.bat
```

### Cách 3: Build thủ công từng bước
```bash
# 1. Cài đặt dependencies
pip install -r requirements.txt
pip install pyinstaller

# 2. Build executable
pyinstaller --name="Course Link Getter" --windowed --onedir --icon=course_link_getter/assets/icon.ico --add-data="course_link_getter/assets;courses_link_getter/assets" --add-data="course_link_getter/core;courses_link_getter/core" --add-data="course_link_getter/ui_pyqt5;courses_link_getter/ui_pyqt5" --hidden-import=PyQt5.QtCore --hidden-import=PyQt5.QtGui --hidden-import=PyQt5.QtWidgets --hidden-import=PyQt5.sip --clean course_link_getter/launch_pyqt5.py

# 3. Tạo ZIP archive
powershell Compress-Archive -Path "dist\Course Link Getter\*" -DestinationPath "Course_Link_Getter_Windows.zip" -Force
```

## 📁 Cấu trúc file sau khi build

### macOS
```
Course_Link_Getter_macOS.dmg          # File cài đặt
dist/
└── Course Link Getter.app/           # Ứng dụng macOS
    ├── Contents/
    │   ├── Info.plist
    │   ├── MacOS/
    │   │   └── Course Link Getter    # Executable chính
    │   └── Resources/
    └── ...
```

### Windows
```
Course_Link_Getter_Windows.zip       # File nén chứa ứng dụng
dist/
└── Course Link Getter/               # Thư mục ứng dụng Windows
    ├── Course Link Getter.exe        # Executable chính
    ├── _internal/                    # Dependencies
    └── ...
```

## 🚀 Cách sử dụng file đóng gói

### macOS
1. Mở file `Course_Link_Getter_macOS.dmg`
2. Kéo `Course Link Getter.app` vào thư mục Applications
3. Chạy ứng dụng từ Launchpad hoặc Applications

### Windows
1. Giải nén file `Course_Link_Getter_Windows.zip`
2. Chạy file `Course Link Getter.exe` trong thư mục đã giải nén

## ⚠️ Lưu ý quan trọng

1. **Cross-platform**: File macOS chỉ chạy trên macOS, file Windows chỉ chạy trên Windows
2. **Dependencies**: Tất cả dependencies đã được đóng gói vào file executable
3. **Size**: File đóng gói khá lớn (~35MB) do chứa toàn bộ Python runtime và PyQt5
4. **Antivirus**: Một số antivirus có thể cảnh báo về file executable mới - đây là bình thường

## 🔧 Troubleshooting

### Lỗi thường gặp:
- **"App can't be opened"** (macOS): Chạy `xattr -cr "Course Link Getter.app"`
- **Missing DLL** (Windows): Cài đặt Visual C++ Redistributable
- **PyQt5 not found**: Đảm bảo đã cài đặt PyQt5 trước khi build

### Kiểm tra build:
```bash
# Test macOS app
open "dist/Course Link Getter.app"

# Test Windows (trên Windows)
"dist/Course Link Getter/Course Link Getter.exe"
```
