### Base class for Collage plugins ###
import math
import logging

import pygame

class Collage(object):
    """
        Base class for collage plugins
            See simple_resize.py or recursive_split.py for example implementation of a plugin
    """
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger('root')

        self.output = None

    def generate(self, size, wallpaper_queue):
        """
            Generates the wallpaper collage
        """
        raise NotImplementedError

    def save(self, collage, filepath):
        """
            Save collage as image
        """
        pygame.image.save(collage, filepath)

    def _get_wallpapers(self, wallpapers):
        """
            Get wallpapers that will be used in generation of collage
            For recursive or multi-layered collages, return lists of lists of wallpapers
                see recursive split collage plugin
        """
        raise NotImplementedError

    def _resize_wallpaper(self, wallpaper, size):
        """
            Resizes wallpaper to set size, conserves aspect ratio
            Returns crop co-ordinates and scaled image
        """

        # find ratios
        width_ratio = 1.0*size[0]/wallpaper.get_width()
        height_ratio = 1.0*size[1]/wallpaper.get_height()

        # resize to fit width
        if width_ratio > height_ratio:
            new_size = (size[0], int(math.ceil(wallpaper.get_height()*width_ratio)))
        # resize to fit height
        else:
            new_size = (int(math.ceil(wallpaper.get_width()*height_ratio)), size[1])

        # scale wallpaper according to new_size
        try:
            wallpaper = pygame.transform.smoothscale(wallpaper, new_size)
        except ValueError:
            print 'bit-depth error, using crappy scaling'
            wallpaper = pygame.transform.scale(wallpaper, new_size)

        # Height or width might be too large
        crop = (0, 0)
        if wallpaper.get_width() > size[0]+1:
            overflow = wallpaper.get_width() - size[0]
            margin = int(overflow / 2)
            crop = (margin, 0)
        elif wallpaper.get_height() > size[1]+1:
            overflow = wallpaper.get_height() - size[1]
            margin = int(overflow / 2)
            crop = (0, margin)

        return crop, wallpaper

