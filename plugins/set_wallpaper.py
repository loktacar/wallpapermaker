from plugin import Plugin

class SetWallpaper(Plugin):
    """
        Base class for the set_wallpaper plugins
    """

    def __init__(self):
        super(SetWallpaper, self).__init__()

    def platform_check(self):
        raise NotImplementedError

    def set(self):
        raise NotImplementedError

