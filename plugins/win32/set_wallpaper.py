import sys

from .. import SetWallpaper

class Win32SetWallpaper(SetWallpaper):
    def __init__(self):
        super(Win32SetWallpaper, self).__init__()

    def platform_check(self):
        return sys.platform == 'win32'

    def set(self):
        import ctypes

        ctypes.windll.user32.SystemParametersInfoA(20, 0, config['wallpaper'], 0)

