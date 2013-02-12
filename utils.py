#!/usr/bin/env python
import os, os.path
if os.name == 'nt':
    import win32api, win32con

def file_hidden(handle):
    if os.name == 'nt':
        attribute = win32api.GetFileAttributes(p)
        return attribute & (win32con.FILE_ATTRIBUTE_HIDDEN | win32con.FILE_ATTRIBUTE_SYSTEM)
    else:
        return os.path.basename(handle).startswith(".")
