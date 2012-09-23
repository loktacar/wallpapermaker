import logging

class UI(object):
    """
        Base class of ui plugins
    """
    def __init__(self):
        self.app = None

        self.logger = logging.getLogger('root')

        self.logger.debug('UI plugin %s started' % self.__class__.__name__)

    # ui control functions

    def start_app(self):
        self.app.main()

    def exit_app(self):
        raise NotImplementedError()

    # ui hooks

    def app_initialized(self):
        """ Run after app initialization

            config and plugin information available now
        """

    def app_started(self):
        """ Run before app initialization """
        pass

    def app_quitting(self):
        """  """
        pass

    def generate_finished(self):
        """ Run after generating a collage """
        pass

    def generate_started(self):
        """ Run right before generating a new collage """
        pass

    def wallpaper_search_finished(self):
        """ Run after wallpaper search plugin is finished """
        pass

    def wallpaper_search_sterted(self):
        """ Run right before using wallpaper search plugins """
        pass

    # app control functions

    def start_generating(self, *args, **kwargs):
        """ Starts generation of new wallpaper """
        self.app.time_since_generation = self.app.config['update']

