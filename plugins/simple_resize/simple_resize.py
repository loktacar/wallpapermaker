import pygame

from .. import Collage

class SimpleResize(Collage):
    """
        Example class for collage plugins
            - Takes a single image and resizes it
    """
    def __init__(self):
        super(SimpleResize, self).__init__()

        self.name = 'simple resize'

    def generate(self, size):
        wallpapers = self._get_wallpapers()

        self.logger.debug('Generating...')

        collage = pygame.Surface(size)

        wp_offset, wp = self._resize_wallpaper(wallpapers[0], size)

        for x1, x2 in enumerate(range(size[0]), wp_offset[0]):
            for y1, y2 in enumerate(range(size[1]), wp_offset[1]):
                collage.set_at((x2, y2), wp.get_at((x1, y1)))

        self.logger.debug('Generation complete')

        return collage

    def _get_wallpapers(self):
        return self.wallpaper_source.pop()

