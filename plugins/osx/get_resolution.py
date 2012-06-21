import sys

from .. import GetResolution

class DarwinGetResolution(GetResolution):
    @staticmethod
    def platform_check():
        return sys.platform == 'darwin'

    @staticmethod
    def get():
        from AppKit import NSScreen
        frame = NSScreen.mainScreen().frame()
        return (int(frame.size.width), int(frame.size.height))
