import sys
import os
from pathlib import Path
try:
    import PyInstaller
except ImportError:
    print("PyInstaller не установлен. Установка...")
    os.system(f"{sys.executable} -m pip install PyInstaller")
APP_NAME = "SQL Browser"
MAIN_FILE = "main.py"
ICON_FILE = "icon.ico"
spec_content = f'''
# -*- mode: python ; coding: utf-8 -*-
block_cipher = None
a = Analysis(
    ['{MAIN_FILE}'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['tkinter', 'sqlite3', 'mysql.connector', 'psycopg2', 'pandas', 'openpyxl'],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludedimports=[],
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
    name='{APP_NAME}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='{ICON_FILE}',
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='{APP_NAME}',
)
'''
print(f"Установка PyInstaller...")
os.system(f"{sys.executable} -m pip install PyInstaller -q")
print(f"Создание .exe файла '{APP_NAME}' из '{MAIN_FILE}'...")
print(f"Используется иконка: {ICON_FILE}")
command = f"{sys.executable} -m PyInstaller --onefile --windowed --name \"{APP_NAME}\" --icon={ICON_FILE} {MAIN_FILE}"
print(f"Команда: {command}")
result = os.system(command)
if result == 0:
    print(f"\n✅ Успешно! .exe файл создан в папке 'dist/'")
    print(f"📦 Приложение: dist/{APP_NAME}/{APP_NAME}.exe")
else:
    print(f"\n❌ Ошибка при создании .exe файла")
    sys.exit(1)