from sys import platform
from cx_Freeze import setup, Executable

base = None
if platform == 'win32':
    base = 'Win32GUI'

options = {
    'build_exe': {
        'includes': ['atexit'],
        "packages": ["multiprocessing", "idna", "cffi"],
        "include_files": [
            "LICENSE"
        ]
    }
}

executables = [
    Executable(
        'src/main.py',
        base=base,
        icon="res/icons/app_icon.ico",
        targetName="capounet_sync.exe"
    )
]

setup(
    name='CAPOUNET Sync',
    version='0.1',
    description='CAPOUNET Sync',
    options=options,
    executables=executables
)
