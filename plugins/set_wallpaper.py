class SetWallpaper(object):
    """
        Base class for the set_wallpaper plugins
    """

    @staticmethod
    def platform_check(config):
        raise NotImplementedError

    @staticmethod
    def set(config):
        raise NotImplementedError

