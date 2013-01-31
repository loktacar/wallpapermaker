import pygame

from plugin import Plugin

class Source(Plugin):
    def __init__(self, path):
        super(Source, self).__init__()

        self.path = path
        self.wallpapers = []

    @staticmethod
    def get_instances(plugins, config):
        if not config['sources']:
            raise ValueError("No sources configured.")

        sources = config['sources'].split(',')

        instances = []
        for plugin in plugins:
            for i, source in enumerate(sources):
                if plugin.handles_path(source):
                    instances.append(plugin(source))
                    sources.pop(i)

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
