import random
import math
import logging

import pygame

from .. import Collage

class RecursiveSplit(Collage):
    name = 'recursive split'

    def __init__(self):
        super(RecursiveSplit, self).__init__()

    def generate(self, size):
        wallpapers = self._get_wallpapers()

        logging.debug('Generating...')
        collage = self.generate_split(size, wallpapers)
        logging.debug('Generation complete')

        return collage

    def generate_split(self, split_size, wallpapers, i=0):
        split = pygame.Surface(split_size)

        split.lock()

        # get cell size
        size = (int(math.ceil(split_size[0]/2.0)),
                int(math.ceil(split_size[1]/2.0)))

        # a bounding box of each cell
        placement = ((0,0,1,1), (1,0,2,1), (0,1,1,2), (1,1,2,2))
        for i in range(4):
            offset = [0,0]
            if type(wallpapers[i]) is list:
                wp = self.generate_split(size, wallpapers[i], i+1)
            else:
                offset, wp = self._resize_wallpaper(wallpapers[i], size)

            pos = [size[j%2]*placement[i][j] for j in range(4)]

            for x1, x2 in enumerate(range(pos[0], pos[2]), offset[0]):
                for y1, y2 in enumerate(range(pos[1], pos[3]), offset[1]):
                    split.set_at((x2, y2), wp.get_at((x1, y1)))

        split.unlock()
        return split

    def _get_wallpapers(self, i=1):
        # Get wallpaper for each split, breadth-first
        wallpapers = self.wallpaper_source.pop(4)

        if i < self.config['recursive_split.recursion-depth']:
            for n in range(4):
                if not random.randint(0, i*(3)):
                    wallpapers[n] = self._get_wallpapers(i+1)

        return wallpapers
