# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['course_link_getter/launch_pyqt5.py'],
    pathex=[],
    binaries=[],
    datas=[('course_link_getter/assets', 'courses_link_getter/assets'), ('course_link_getter/core', 'courses_link_getter/core'), ('course_link_getter/ui_pyqt5', 'courses_link_getter/ui_pyqt5')],
    hiddenimports=['PyQt5.QtCore', 'PyQt5.QtGui', 'PyQt5.QtWidgets', 'PyQt5.sip'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Course_Link_Getter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['course_link_getter/assets/icon.icns'],
)
app = BUNDLE(
    exe,
    name='Course_Link_Getter.app',
    icon='course_link_getter/assets/icon.icns',
    bundle_identifier=None,
)
