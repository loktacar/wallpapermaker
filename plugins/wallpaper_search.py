import pygame

from plugin import Plugin

class WallpaperSearch(Plugin):
    def __init__(self):
        super(WallpaperSearch, self).__init__()

        self.wallpapers = []

    def pop(self, count=1):
        raise NotImplementedError()

    def count(self):
        return len(self.wallpapers)

    def _image_from_path(self, path):
        wallpaper = pygame.image.load(path)

        if wallpaper.get_width() == 0 or wallpaper.get_height() == 0:
            raise IOError

        return wallpaper

