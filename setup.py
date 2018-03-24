import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

options = {
    'build_exe': {
        'includes': 'atexit'
    }
}

executables = [
    Executable('main.py', base=base)
]

setup(name='CAPOUNET Sync',
      version='0.1',
      description='CAPOUNET Sync',
      options=options,
      executables=executables
)
