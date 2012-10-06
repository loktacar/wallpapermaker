import sys

from .. import GetResolution

class Win32GetResolution(GetResolution):
    def __init__(self):
        super(Win32GetResolution, self).__init__()

    def platform_check(self):
        return sys.platform == 'win32'

    def get(self):
        import ctypes

        return [(ctypes.windll.user32.GetSystemMetrics(0),
                ctypes.windll.user32.GetSystemMetrics(1))]

# Check EnumDisplatMonitors function in windll's for each screens offset from top-left screen
