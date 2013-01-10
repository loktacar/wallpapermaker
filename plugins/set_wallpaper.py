from plugin import Plugin

class SetWallpaper(Plugin):
    """
        Base class for the set_wallpaper plugins
    """

    def __init__(self, config):
        super(SetWallpaper, self).__init__()

        self.config = config

    @staticmethod
    def get_instances(plugins, config):
        instances = []

        for plugin in plugins:
            i = plugin(config)
            if i.platform_check():
                instances.append(i)

        if not instances:
            logger.warning("No plugin to set wallpapers, what's going on?")
            return None

        return instances[0]

    def platform_check(self):
        raise NotImplementedError

    def set(self):
        raise NotImplementedError

