'''
Created on 20. 4. 2017

@author: T.Filip
'''


import sys
from cx_Freeze import setup, Executable
import os 
os.environ['TCL_LIBRARY'] = r'C:\Program Files\Python35-32\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Program Files\Python35-32\tcl\tk8.6'

build_exe_options = {
        #"optimize": 2,
        #"includes": [],
        #"compressed": True,
        #"copy_dependent_files": True,
        #"create_shared_zip": False,
        #"append_script_to_exe": True,
        #"include_in_shared_zip": False,

        #"include_files":[('vPlot.ui'),
        #                 ('vPlot.py'),
        #                 ('company.jpg')], 
        #"include_msvcr": True,
        "packages": ["pygame"],
        #"build_exe": {"packages":["pygame"],
        #                 "include_files": ["img"]}
    }


setup(
    name = "rpg",
    version = "3.6",
    description = "rpg",
    options = {"build_exe":{"packages": ["pygame"]}},
    executables = [Executable("BP.py", base = "Win32GUI")])