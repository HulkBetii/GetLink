# 🪟 Hướng dẫn tạo file .exe cho Windows

## 📋 Yêu cầu hệ thống

- **Windows 10** hoặc mới hơn
- **Python 3.8+** (khuyến nghị 3.11+)
- **Git** (để clone repository)

## 🚀 Cách 1: Build tự động (Khuyến nghị)

### Bước 1: Chuẩn bị môi trường
```bash
# Clone repository
git clone https://github.com/HulkBetii/GetLink.git
cd GetLink

# Cài đặt dependencies
pip install -r requirements.txt
pip install pyinstaller
```

### Bước 2: Chạy build script
```bash
# Cách 1: Sử dụng Python script
python build_windows_exe.py

# Cách 2: Sử dụng batch file
build_windows_exe.bat
```

### Bước 3: Kết quả
Sau khi build thành công, bạn sẽ có:
- `dist/Course_Link_Getter.exe` - File executable duy nhất
- `Course_Link_Getter_Windows_Installer.zip` - Package cài đặt
- `install.bat` - Script cài đặt
- `README_Windows.txt` - Hướng dẫn sử dụng

## 🔧 Cách 2: Build thủ công

### Bước 1: Cài đặt PyInstaller
```bash
pip install pyinstaller
```

### Bước 2: Chạy lệnh build
```bash
pyinstaller --name=Course_Link_Getter --windowed --onefile --icon=course_link_getter/assets/icon.ico --add-data="course_link_getter/assets;courses_link_getter/assets" --add-data="course_link_getter/core;courses_link_getter/core" --add-data="course_link_getter/ui_pyqt5;courses_link_getter/ui_pyqt5" --hidden-import=PyQt5.QtCore --hidden-import=PyQt5.QtGui --hidden-import=PyQt5.QtWidgets --hidden-import=PyQt5.sip --clean course_link_getter/launch_pyqt5.py
```

### Bước 3: Kiểm tra kết quả
```bash
# File executable sẽ được tạo tại:
dist/Course_Link_Getter.exe
```

## 📦 Phân phối ứng dụng

### Option 1: File .exe duy nhất
- Chỉ cần chia sẻ file `Course_Link_Getter.exe`
- Người dùng chỉ cần double-click để chạy
- Không cần cài đặt gì thêm

### Option 2: Package cài đặt
- Chia sẻ file `Course_Link_Getter_Windows_Installer.zip`
- Người dùng giải nén và chạy `install.bat`
- Ứng dụng sẽ được copy vào Desktop

## 🎯 Đặc điểm của file .exe

### ✅ **Ưu điểm:**
- **Single file**: Chỉ 1 file .exe duy nhất
- **Portable**: Không cần cài đặt
- **Self-contained**: Chứa tất cả dependencies
- **Cross-platform**: Chạy trên mọi Windows 10+

### 📊 **Thông tin kỹ thuật:**
- **Size**: ~40-50MB (bao gồm Python runtime + PyQt5)
- **Startup time**: 3-5 giây lần đầu
- **Memory usage**: ~50-100MB khi chạy
- **Dependencies**: Tất cả đã được đóng gói

## 🔍 Troubleshooting

### Lỗi thường gặp:

#### 1. **"PyInstaller not found"**
```bash
pip install pyinstaller
```

#### 2. **"Missing DLL"**
- Cài đặt Visual C++ Redistributable
- Download từ Microsoft website

#### 3. **"App won't start"**
- Kiểm tra Windows version (cần Windows 10+)
- Chạy với quyền Administrator
- Kiểm tra antivirus settings

#### 4. **"Antivirus warning"**
- Đây là bình thường với file .exe mới
- Thêm exception trong antivirus
- Hoặc tạm thời tắt real-time protection

### Kiểm tra build:
```bash
# Test file .exe
dist/Course_Link_Getter.exe

# Kiểm tra file size
dir dist\Course_Link_Getter.exe
```

## 📁 Cấu trúc file sau khi build

```
GetLink/
├── dist/
│   └── Course_Link_Getter.exe          # File executable chính
├── Course_Link_Getter_Windows_Installer.zip  # Package cài đặt
├── install.bat                         # Script cài đặt
├── README_Windows.txt                  # Hướng dẫn người dùng
└── build_windows_exe.py               # Script build
```

## 🚀 Deployment

### Chia sẻ với người khác:

#### **Cách 1: File .exe duy nhất**
1. Copy file `dist/Course_Link_Getter.exe`
2. Gửi cho người dùng
3. Họ chỉ cần double-click để chạy

#### **Cách 2: Package cài đặt**
1. Copy file `Course_Link_Getter_Windows_Installer.zip`
2. Gửi cho người dùng
3. Họ giải nén và chạy `install.bat`

## 📈 Performance

### **Startup time:**
- Lần đầu: 3-5 giây (extract dependencies)
- Lần sau: 1-2 giây (dependencies cached)

### **Memory usage:**
- Idle: ~50MB
- Active: ~100MB
- Peak: ~150MB

### **File size:**
- Executable: ~40-50MB
- Total package: ~45-55MB

## 🎉 Kết luận

Với hướng dẫn này, bạn có thể tạo file .exe duy nhất cho Windows với đầy đủ tính năng:

- ✅ **Single file**: Chỉ 1 file .exe
- ✅ **No installation**: Không cần cài đặt
- ✅ **All features**: Đầy đủ tính năng
- ✅ **26 courses**: Dữ liệu đầy đủ
- ✅ **Modern UI**: Giao diện đẹp
- ✅ **Cross-platform**: Windows 10+

**Repository**: [https://github.com/HulkBetii/GetLink.git](https://github.com/HulkBetii/GetLink.git)
