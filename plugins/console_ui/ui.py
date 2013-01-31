from .. import UI

class Console(UI):

    def __init__(self, config):
        super(Console, self).__init__(config)
        self.config = config

    def app_started(self):
        print 'Application Started.'
        print

    def app_initialized(self, app):
        super(Console, self).app_initialized(app)
        print 'Application initialized.'
        print 

    def app_quitting(self):
        print 'Application Quitting.'

    def wallpaper_search_starting(self):
        print 'Searching for wallpapers... ',

    def wallpaper_search_finished(self):
        print 'Search complete. Wallpaper count now at %d.' % self.app.wps.count()

    def generate_starting(self):
        print 'Generating wallpaper... '

    def generate_finished(self):
        print 'Generation complete.'

