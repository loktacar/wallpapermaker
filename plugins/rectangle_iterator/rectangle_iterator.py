import random
import math

import pygame

from .. import Collage

class RectangleIterator(Collage):

    # bounding boxes of each cell (as multiples of cell size).
    # top left, top right, bottom left, bottom right
    placement = ((0,0,1,1), (1,0,2,1), (0,1,1,2), (1,1,2,2))

    @staticmethod
    def get_cell_size(size):
        return (int(math.ceil(size[0]/2.0)),
                int(math.ceil(size[1]/2.0)))

    # calculate position (bounding box of same type as placement)
    @staticmethod
    def get_cell_position(quadrant, size):
        return [size[j%2] * RectangleIterator.placement[quadrant][j] for j in range(4)]

    def __init__(self):
        super(RectangleIterator, self).__init__()

        self.generated_count = 0
        self.last_collage = None
        self.wallpapers = []

        # constants
        self.resplit_interval = 5

    def generate(self, size):

        # Change a few cells if a collage has been created, and the resolution is the same
        if self.last_collage is not None and size == self.last_collage.get_size():
            self.logger.debug('Generating, changing a few cells...')
            collage = self._change_some_cells(size)
        # Create a completely new collage
        else:
            self.logger.debug('Generating a whole new collage...')
            self.wallpapers = self._get_new_wallpapers()
            collage = self._generate_splits(size, self.wallpapers)

        self.logger.debug('Generation complete')

        self.generated_count += 1

        # Create a new split collage if it's time, else remember the last image
        if self.generated_count >= self.resplit_interval:
            self.last_collage = None
            self.generated_count = 0
        else:
            self.last_collage = collage

        return collage

    def _generate_splits(self, split_size, wallpapers):
        split = pygame.Surface(split_size)

        # get cell size
        size = RectangleIterator.get_cell_size(split_size)

        for i in range(4):
            offset = [0, 0]

            # recursive call, on lists of wallpapers
            if type(wallpapers[i]) is list:
                wp = self._generate_splits(size, wallpapers[i])
            # resize wallpaper
            else:
                offset, wp = self._resize_wallpaper(wallpapers[i], size)

            # calculate position (bounding box of same type as placement)
            pos = RectangleIterator.get_cell_position(i, size)

            split.lock()
            # Add image to split
            for x1, x2 in enumerate(range(pos[0], pos[2]), offset[0]):
                for y1, y2 in enumerate(range(pos[1], pos[3]), offset[1]):
                    split.set_at((x2, y2), wp.get_at((x1, y1)))
            split.unlock()

        return split

    def _change_some_cells(self, size):
        # Get one to four random images
        wp_change_count = random.randint(1, 4)
        new_wallpapers = self.wallpaper_source.pop(wp_change_count)

        wp_index_range = range(4)
        random.shuffle(wp_index_range)

        new_size = RectangleIterator.get_cell_size(size)

        # recursively run down the self.wallpaper tree
        # change one to four nodes
        for i in range(wp_change_count):
            pos = RectangleIterator.get_cell_position(wp_index_range[i], new_size)
            self._change_single_cell(new_wallpapers[i], self.wallpapers[wp_index_range[i]], new_size, pos)

        return self.last_collage

    def _change_single_cell(self, new_wallpaper, wallpaper_to_change, cell_size, cell_pos):

        # This cell contains a split
        if type(wallpaper_to_change) is list:
            random_index = random.randint(0, 3)

            new_size = RectangleIterator.get_cell_size(cell_size)
            new_pos = RectangleIterator.get_cell_position(random_index, new_size)

            abs_x_pos = new_pos[0] + cell_pos[0]
            abs_y_pos = new_pos[1] + cell_pos[1]
            absolute_pos = [abs_x_pos, abs_y_pos, abs_x_pos + new_size[0], abs_y_pos + new_size[1]]

            return self._change_single_cell(new_wallpaper, wallpaper_to_change[random_index], new_size, absolute_pos)

        # This cell is a single wallpaper, change it!
        else:
            offset, wp = self._resize_wallpaper(new_wallpaper, cell_size)

            self.last_collage.lock()
            for x1, x2 in enumerate(range(cell_pos[0], cell_pos[2]), offset[0]):
                for y1, y2 in enumerate(range(cell_pos[1], cell_pos[3]), offset[1]):
                    self.last_collage.set_at((x2, y2), wp.get_at((x1, y1)))
            self.last_collage.unlock()

            return self.last_collage

    def _get_new_wallpapers(self, i=0):
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
                wallpapers[index] = self._get_new_wallpapers(i+1)

        return wallpapers
