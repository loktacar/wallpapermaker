import time

from plugin import Plugin

class UI(Plugin):
    """
        Base class of ui plugins
    """

    settings = {
            'multiple_instances': False,
            'active_required':     True,
            }

    def __init__(self, config):
        super(UI, self).__init__()

        self.app = None
        self.config = config

    @staticmethod
    def get_instances(plugins, config):
        instance = None
        if config['ui'] == 'auto':
            plugin_order = ('wxPython', 'Console')
            instance = sorted(plugins, key=lambda p: p.__name__)[0](config)
        else:
            for plugin in plugins:
                if plugin.__name__ == config['ui']:
                    instance = plugin(config)

        if not instance:
            raise RuntimeError("No UI plugin activated.")

        return instance

    # ui control functions

    def start_app(self):
        self.app.main()

    def exit_app(self):
        raise NotImplementedError()

    # ui hooks

    def app_initialized(self, app):
        """ Run after app initialization

            config and plugin information available now
        """
        self.app = app

    def app_started(self):
        """ Run before app initialization """
        pass

    def app_quitting(self):
        """ Run after app initialization """
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
        self.app.pause(False)
        self.app.next_generation = time.time()

