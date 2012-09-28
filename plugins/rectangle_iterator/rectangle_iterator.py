import random
import math

import pygame

from .. import Collage

class RectangleIterator(Collage):

    def __init__(self):
        super(RectangleIterator, self).__init__()

        self.generated_count = 0
        self.last_collage = None
        self.wallpapers = []

        # constants
        self.resplit_interval = 10

    def generate(self, size):

        self.logger.debug('Generating...')

        # Change a few cells if a collage has been created, and the resolution is the same
        if self.last_collage is not None and size == self.last_collage.get_size():
            collage = self._change_some_cells(size, self.wallpapers)
        # Create a completely new collage
        else:
            self.wallpapers = self._get_new_wallpapers()
            self.print_recursive_list(self.wallpapers)
            collage = self._generate_splits(size, self.wallpapers)

        self.logger.debug('Generation complete')

        # Create a new split collage if it's time, else remember the last image
        if self.generated_count >= self.resplit_interval:
            self.last_collage = None
        else:
            self.last_collage = collage

        return collage

    def print_recursive_list(self, list, c=0):
        print
        for i, e in enumerate(list):
            if type(e) is pygame.Surface:
                print '%s%s' % (c*'\t', e)
            else:
                self.print_recursive_list(e, c+1)

    def _generate_splits(self, split_size, wallpapers):
        split = pygame.Surface(split_size)

        # get cell size
        size = (int(math.ceil(split_size[0]/2.0)),
                int(math.ceil(split_size[1]/2.0)))

        # bounding boxes of each cell (as multiples of cell size).
        # top left, top right, bottom left, bottom right
        placement = ((0,0,1,1), (1,0,2,1), (0,1,1,2), (1,1,2,2))

        for i in range(4):
            offset = [0, 0]

            # recursive call, on lists of wallpapers
            if type(wallpapers[i]) is list:
                wp = self._generate_splits(size, wallpapers[i])
            # resize wallpaper
            else:
                offset, wp = self._resize_wallpaper(wallpapers[i], size)

            # calculate position (bounding box of same type as placement)
            pos = [size[j%2] * placement[i][j] for j in range(4)]

            # Add image to split
            for x1, x2 in enumerate(range(pos[0], pos[2]), offset[0]):
                for y1, y2 in enumerate(range(pos[1], pos[3]), offset[1]):
                    split.set_at((x2, y2), wp.get_at((x1, y1)))

        return split

    def _change_some_cells(size, wallpapers, i=0):
        return self.last_collage

    def _get_new_wallpapers(self, i=0):
        i_wallpapers = []

        print i, self.config['recursion-depth']
        if i < self.config['recursion-depth']:
            i_split_count = random.randint(0, 4 + i*4)
            i_split_count = 4 if i_split_count > 4 else i_split_count

            for x in range(i_split_count):
                i_wallpapers.append(self._get_new_wallpapers(i+1))

        i_wp_count = 4 - len(self.wallpapers)
        new_wps = self.wallpaper_queue.pop(i_wp_count)
        for wp in new_wps:
            insert_index = random.randint(0, 3)
            i_wallpapers.insert(insert_index, wp)

        return i_wallpapers
