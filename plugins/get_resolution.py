class GetResolution(object):
    """
        Base class for get_resolution plugins
    """

    @staticmethod
    def platform_check():
        raise NotImplementedError

    @staticmethod
    def get():
        raise NotImplementedError

