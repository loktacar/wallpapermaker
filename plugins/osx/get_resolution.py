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
        from AppKit import NSScreen
        frame = NSScreen.mainScreen().frame()
        return (int(frame.size.width), int(frame.size.height))
