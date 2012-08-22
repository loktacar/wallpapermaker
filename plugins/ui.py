class UI(object):
    """
        Base class of ui plugins
    """
    def __init__(self, app=None):
        self.app = app

        self.initialized = False

    # function hooks

    def app_started(self):
        """ Run before app initialization """
        pass

    def app_initialized(self):
        """ Run after app initialization

            config and plugin information available now
        """
        self.initialized = True

    def app_quitting(self):
        """  """
        pass

    def generate_started(self):
        """ Run right before generating a new collage """
        pass

    def generate_finished(self):
        """ Run after generating a collage """
        pass

    # control functions

    def start_app(self):
        """ Starts the application main thread """
        self.app.main()

    def start_generating(self):
        self.app.time_since_generation = 100 * self.app.config['update']

    def loaded_plugins(self):
        """ Shows which plugins have been loaded """
        if not self.initialized :
            raise AttributeError("Application not initialized, cannot comply")
        return self.app.loaded_plugins()

    def using_plugins(self):
        """ Shows which plugins are going to be used """
        if not self.initialized:
            raise AttributeError("Application not initialized, cannot comply")
        return self.app.using_plugins()

