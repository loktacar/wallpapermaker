import sys

from .. import SetWallpaper

class Win32SetWallpaper(SetWallpaper):
    @staticmethod
    def platform_check(config):
        return sys.platform == 'win32'

    @staticmethod
    def set(config):
        import ctypes

        ctypes.windll.user32.SystemParametersInfoA(20, 0, config['wallpaper'], 0)

