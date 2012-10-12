import sys

from .. import GetResolution

class Win32GetResolution(GetResolution):
    def __init__(self):
        super(Win32GetResolution, self).__init__()

    def platform_check(self):
        return sys.platform == 'win32'

    def get(self):
        import win32api

        resolutions = []
        for result in win32api.EnumDisplayMonitors():
            res = result[-1]
            resolutions.append((res[2] - res[0], res[3] - res[1], res[0], res[1]))

        return resolutions

