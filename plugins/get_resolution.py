from plugin import Plugin

class GetResolution(Plugin):
    """
        Base class for get_resolution plugins
    """

    def __init__(self):
        super(GetResolution, self).__init__()

    def platform_check(self):
        raise NotImplementedError

    def get(self):
        raise NotImplementedError

