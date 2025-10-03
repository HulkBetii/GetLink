@echo off
REM Build Windows single .exe file
echo 🪟 Building Course Link Getter for Windows (Single EXE)...

REM Clean previous builds
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist *.spec del *.spec
if exist *.exe del *.exe
if exist *.zip del *.zip

REM Create single executable
echo 📦 Creating single .exe file...
pyinstaller ^
    --name=Course_Link_Getter ^
    --windowed ^
    --onefile ^
    --icon=course_link_getter/assets/icon.ico ^
    --add-data="course_link_getter/assets;courses_link_getter/assets" ^
    --add-data="course_link_getter/core;courses_link_getter/core" ^
    --add-data="course_link_getter/ui_pyqt5;courses_link_getter/ui_pyqt5" ^
    --hidden-import=PyQt5.QtCore ^
    --hidden-import=PyQt5.QtGui ^
    --hidden-import=PyQt5.QtWidgets ^
    --hidden-import=PyQt5.sip ^
    --clean ^
    course_link_getter/launch_pyqt5.py

REM Check if build was successful
if exist "dist\Course_Link_Getter.exe" (
    echo ✅ Windows executable created successfully!
    echo 📁 File location: dist\Course_Link_Getter.exe
    
    REM Get file size
    for %%A in ("dist\Course_Link_Getter.exe") do echo 📊 File size: %%~zA bytes
    
    REM Create installer script
    echo Creating installer script...
    echo @echo off > install.bat
    echo echo Course Link Getter - Windows Installer >> install.bat
    echo echo ===================================== >> install.bat
    echo echo. >> install.bat
    echo echo This will install Course Link Getter to your system. >> install.bat
    echo echo. >> install.bat
    echo pause >> install.bat
    echo echo. >> install.bat
    echo echo Installing... >> install.bat
    echo copy "Course_Link_Getter.exe" "%%USERPROFILE%%\Desktop\Course_Link_Getter.exe" >> install.bat
    echo echo. >> install.bat
    echo echo ✅ Installation completed! >> install.bat
    echo echo 📁 Course Link Getter.exe has been copied to your Desktop >> install.bat
    echo echo. >> install.bat
    echo echo You can now run the application from your Desktop. >> install.bat
    echo echo. >> install.bat
    echo pause >> install.bat
    
    echo ✅ Installer script created: install.bat
    
    REM Create README
    echo Creating README...
    echo # Course Link Getter - Windows > README_Windows.txt
    echo. >> README_Windows.txt
    echo ## Quick Installation >> README_Windows.txt
    echo. >> README_Windows.txt
    echo 1. **Download**: Course_Link_Getter_Windows_Installer.zip >> README_Windows.txt
    echo 2. **Extract**: Unzip the file to any folder >> README_Windows.txt
    echo 3. **Install**: Double-click install.bat to install >> README_Windows.txt
    echo 4. **Run**: Find Course_Link_Getter.exe on your Desktop >> README_Windows.txt
    echo. >> README_Windows.txt
    echo ## Manual Installation >> README_Windows.txt
    echo. >> README_Windows.txt
    echo 1. **Download**: Course_Link_Getter.exe >> README_Windows.txt
    echo 2. **Copy**: Move the file to any folder you want >> README_Windows.txt
    echo 3. **Run**: Double-click Course_Link_Getter.exe >> README_Windows.txt
    echo. >> README_Windows.txt
    echo ## Features >> README_Windows.txt
    echo. >> README_Windows.txt
    echo - ✅ 26 courses loaded automatically >> README_Windows.txt
    echo - ✅ Search and filter functionality >> README_Windows.txt
    echo - ✅ Copy links to clipboard >> README_Windows.txt
    echo - ✅ Export to CSV >> README_Windows.txt
    echo - ✅ Modern UI with dark theme >> README_Windows.txt
    echo. >> README_Windows.txt
    echo ## System Requirements >> README_Windows.txt
    echo. >> README_Windows.txt
    echo - Windows 10 or later >> README_Windows.txt
    echo - No additional software required (all dependencies included) >> README_Windows.txt
    
    echo ✅ README created: README_Windows.txt
    
    REM Create ZIP installer package
    echo 📦 Creating installer package...
    powershell Compress-Archive -Path "dist\Course_Link_Getter.exe","install.bat","README_Windows.txt" -DestinationPath "Course_Link_Getter_Windows_Installer.zip" -Force
    echo ✅ Installer package created: Course_Link_Getter_Windows_Installer.zip
    
    echo.
    echo 🎉 Windows EXE build completed successfully!
    echo 📁 Files created:
    echo   - dist\Course_Link_Getter.exe (single executable)
    echo   - Course_Link_Getter_Windows_Installer.zip (installer package)
    echo   - install.bat (installer script)
    echo   - README_Windows.txt (user guide)
    
) else (
    echo ❌ Build failed!
    echo 💡 Make sure PyInstaller is installed: pip install pyinstaller
    exit /b 1
)

echo.
echo 🚀 Ready to distribute!
pause
