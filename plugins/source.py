import pygame

from plugin import Plugin

class Source(Plugin):
    def __init__(self):
        super(Source, self).__init__()

        self.wallpapers = []

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

