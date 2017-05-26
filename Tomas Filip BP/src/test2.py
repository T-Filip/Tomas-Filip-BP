'''
Created on 9. 5. 2017

@author: T.Filip
'''

import sys
from cx_Freeze import setup, Executable
import os

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["pygame"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "Hra",
        version = "1.0",
        description = "Bakalarska praca",
        options = {"build_exe": build_exe_options},
        executables = [Executable("BP.py", base=base)])