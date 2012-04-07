#!/usr/bin/env python
from resolution import get_screen_resolution
from wallpaper import make_wallpaper, set_wallpaper

# Create a thread and update periodically, period set in config.py
#
# Create a nother thread maintaining the file list,
#   even in Image form if it cuts down on the creation time
#
# Create other forms of wallpaper collages

if __name__ == '__main__':
    resolution = get_screen_resolution()
    make_wallpaper(resolution)
    set_wallpaper()
