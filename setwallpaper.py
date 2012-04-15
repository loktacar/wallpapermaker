import sys
import os
from config import desktop_environment

def set_wallpaper(filename):
    # Check if windows, linux or mac

    if sys.platform == 'win32':
        set_win32_wallpaper(filename)
    elif sys.platform == 'linux2':
        if desktop_environment == 'gnome':
            set_gnome_wallpaper(filename)

def set_win32_wallpaper(filename):
    import ctypes

    ctypes.windll.user32.SystemParametersInfoA(20, 0, filename, 0)

def set_gnome_wallpaper(filename):
        os.system(\
                "gsettings set org.gnome.desktop.background picture-uri \"file://%s\"" \
                    % filename)

