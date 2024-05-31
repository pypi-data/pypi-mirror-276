import os
import sys
import platform

current_folder = os.path.dirname(os.path.realpath(__file__))

if current_folder not in sys.path:
    sys.path.append(current_folder)

if platform.system() == 'Darwin':  # macOS
    lib_path = os.path.join(current_folder, 'libdescriptor.dylib')
    if os.path.exists(lib_path):
        # Adjust the dynamic library search path
        from ctypes import cdll
        cdll.LoadLibrary(lib_path)

from .libdescriptor import *
