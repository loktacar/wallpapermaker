import logging

import pygame

from plugin import Plugin
from config import ConfigurationError

class Source(Plugin):
    def __init__(self, path):
        super(Source, self).__init__()

        self.path = path
        self.wallpapers = []

    @staticmethod
    def get_instances(plugins, config):
        # Find plugins that handle each source
        instances = []
        source_config_found = False
        for plugin in plugins:
            # module name of the plugin
            module = plugin.__module__.split('.')[1]

            # check if there is a source configured for this plugin
            try:
                source = config['%s.source' % module]
                if source is None:
                    raise
            except:
                continue
            source_config_found = True

            if plugin.handles_path(source):
                if module == 'folder':
                    instances.append(plugin(source,
                        include_hidden=config['folder.include_hidden']))
                else:
                    instances.append(plugin(source))
            else:
                logging.warning('Source in [%s] section not handled by corresponding plugin' %
                                module)

        if not source_config_found:
            raise ConfigurationError("No sources configured.")
        if not instances:
            raise ValueError("No plugins could handle your sources.")

        return instances


    @staticmethod
    def handles_path(path):
        """ Checks if this implementation of Source plugin can handle a particular path """
        raise NotImplementedError()

    def pop(self, count=1):
        raise NotImplementedError()

    def count(self):
        return len(self.wallpapers)

    def _image_from_path(self, path):
        wallpaper = pygame.image.load(path)

        if wallpaper.get_width() == 0 or wallpaper.get_height() == 0:
            raise IOError

        return wallpaper

    def wallpaper_complete(self):
        """ Called when the wallpaper is complete """
        pass
