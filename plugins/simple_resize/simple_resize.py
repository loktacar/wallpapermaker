import logging

import pygame

from .. import Collage

class SimpleResize(Collage):
    """
        Example class for collage plugins
            - Takes a single image and resizes it
    """
    name = 'simple resize'

    def __init__(self):
        super(SimpleResize, self).__init__()

    def generate(self, size):
        wallpapers = self._get_wallpapers()

        logging.debug('Generating...')

        collage = pygame.Surface(size)
        wp_offset, wp = self._resize_wallpaper(wallpapers[0], size)
        collage.blit(wp, (0,0), pygame.Rect(wp_offset, size))

        logging.debug('Generation complete')

        return collage

    def _get_wallpapers(self):
        return self.wallpaper_source.pop()

