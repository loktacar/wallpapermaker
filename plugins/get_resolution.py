from plugin import Plugin

class GetResolution(Plugin):
    """
        Base class for get_resolution plugins
    """

    def __init__(self):
        super(GetResolution, self).__init__()

    @staticmethod
    def get_instances(plugins, config):
        instances = []

        for plugin in plugins:
            i = plugin()
            if i.platform_check():
                instances.append(i)

        if not instances:
            logger.warning("No resolution plugin applicable, hope you set the resolution in config.")
            return None

        return instances[0]

    def platform_check(self):
        raise NotImplementedError

    def get(self):
        raise NotImplementedError

