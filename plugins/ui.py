import logging

class UI(object):
    """
        Base class of ui plugins
    """
    def __init__(self, app=None):
        self.app = app

        self.initialized = False

        self.logger = logging.getLogger('root')

    # ui control functions

    def start_app(self):
        """ Starts the application main thread """
        self.app.main()

    def pause_app_toggle(self):
        """ Pauses the application loop, starts generating upon resume """
        self.app.pause()

    def switch_collage_plugin(self, collage):
        self.app.switch_collage_plugin(collage)
        self.logger.debug(collage)

    # ui hooks

    def app_initialized(self):
        """ Run after app initialization

            config and plugin information available now
        """
        self.initialized = True

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

