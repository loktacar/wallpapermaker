from AppKit import NSScreen

from .. import GetResolution

class DarwinGetResolution(GetResolution):
    def __init__(self):
        super(DarwinGetResolution, self).__init__()

    def platform_check(self):
        try:
            from AppKit import NSScreen
            return True
        except:
            return False

    def get(self):
        return [(int(screen.frame().size.width), int(screen.frame().size.height))
            for screen in NSScreen.screens()]

# TODO: Check AppKit documentation for NSScreen.screens().frame()'s offset from top left frame
