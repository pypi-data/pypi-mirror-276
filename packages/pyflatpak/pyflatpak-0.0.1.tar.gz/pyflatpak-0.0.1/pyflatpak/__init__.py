from ctypes import cdll

__version__ = '0.0.1'

libflatpak = cdll.LoadLibrary("libflatpak.so.0")
