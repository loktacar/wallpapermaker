import sys

from .. import GetResolution

class Win32GetResolution(GetResolution):
    @staticmethod
    def platform_check():
        return sys.platform == 'win32'

    @staticmethod
    def get():
        import ctypes

        return (ctypes.windll.user32.GetSystemMetrics(0),
                ctypes.windll.user32.GetSystemMetrics(1))
