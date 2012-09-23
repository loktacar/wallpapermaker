import sys

from .. import GetResolution

class XlibGetResolution(GetResolution):
    def __init__(self):
        super(XlibGetResolution, self).__init__()

    def platform_check(self):
        try:
            import Xlib
            import Xlib.display
            return True
        except:
            return False

    def get(self):
        import Xlib
        import Xlib.display

        display = Xlib.display.Display()
        root = display.screen().root
        geom = root.get_geometry()
        return (geom.width, geom.height)

