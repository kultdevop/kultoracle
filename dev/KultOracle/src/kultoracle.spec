# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['kultoraclemain.py'],
    pathex=[],
    binaries=[('/lib/python3.8/site-packages/PyQt5/Qt5/plugins/wayland-shell-integration/*', 'PyQt5/Qt5/plugins/wayland-shell-integration'), ('/lib/python3.8/site-packages/PyQt5/Qt5/plugins/wayland-graphics-integration-client/*', 'PyQt5/Qt5/plugins/wayland-graphics-integration-client'), ('/lib/python3.8/site-packages/PyQt5/Qt5/plugins/wayland-decoration-client/*', 'PyQt5/Qt5/plugins/wayland-decoration-client'), ('/lib/python3.8/site-packages/fitz/*', 'fitz')],
    datas=[('sqlscripts/DDL.sql', '.')],
    hiddenimports=['json'],
    hookspath=['./__pyinstaller'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='kultoracle',
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
)
