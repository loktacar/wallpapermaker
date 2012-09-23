from .. import UI

class Console(UI):

    def __init__(self):
        super(Console, self).__init__()

    def app_started(self):
        print 'Application Started.'
        print

    def app_initialized(self):
        super(Console, self).app_initialized()
        print 'Application initialized.'
        print 
        print 'Plugins loaded.'
        loaded_plugins = self.app.loaded_plugins
        using_plugins = self.app.using_plugins()
        for plugins_key in loaded_plugins:
            print plugins_key + ' plugins'
            print '\t' + ("using '%s', " % using_plugins[plugins_key] if plugins_key in using_plugins else ' ')
            print '\tloaded %s' % loaded_plugins[plugins_key]
        print

    def app_quitting(self):
        print 'Application Quitting.'

    def wallpaper_search_starting(self):
        print 'Searching for wallpapers... ',

    def wallpaper_search_finished(self):
        print 'Search complete. Wallpaper count now at %d.' % self.app.wps.count()

    def generate_starting(self, collage_name=''):
        print 'Generating wallpaper%s... ' % (' using '+collage_name if collage_name else ''),

    def generate_finished(self):
        print 'Generation complete.'

