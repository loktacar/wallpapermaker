import sys

from .. import GetResolution

class XlibGetResolution(GetResolution):
    @staticmethod
    def platform_check():
        return sys.platform == 'linux2'

    @staticmethod
    def get():
        import Xlib
        import Xlib.display

        display = Xlib.display.Display()
        root = display.screen().root
        geom = root.get_geometry()
        return (geom.width, geom.height)

