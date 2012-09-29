import random
import math

import pygame

from .. import Collage

class RecursiveSplit(Collage):

    def __init__(self):
        super(RecursiveSplit, self).__init__()

    def generate(self, size):
        wallpapers = self._get_wallpapers()

        self.logger.debug('Generating...')
        collage = self.generate_split(size, wallpapers)
        self.logger.debug('Generation complete')

        return collage

    def generate_split(self, split_size, wallpapers, i=0):
        split = pygame.Surface(split_size)

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

        return split

    def _get_wallpapers(self, i=1):
        # Get wallpaper for each split, breadth-first
        wallpapers = []

        # get a random amount of images
        if i >= self.config['recursion-depth']:
            i_wp_count = 4
        else:
            i_wp_count = random.randint(0, 4 + i*4)
            i_wp_count = i_wp_count if i_wp_count <= 4 else 4

        wallpapers = self.wallpaper_source.pop(i_wp_count)

        # add empty list where splits will happen, i.e. where actual images are missing
        if i_wp_count < 4:
            i_splits = 4 - i_wp_count
            for j in range(i_splits):
                wallpapers.insert(random.randint(0, len(wallpapers)), [])

        # fill the lists
        for index, wp in enumerate(wallpapers):
            if type(wp) is list:
                wallpapers[index] = self._get_wallpapers(i+1)

        return wallpapers
