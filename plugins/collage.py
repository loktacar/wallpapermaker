### Base class for Collage plugins ###
import math
import logging

import pygame

from plugin import Plugin

class Collage(Plugin):
    """
        Base class for collage plugins
            See simple_resize.py or recursive_split.py for example implementation of a plugin
    """

    def __init__(self, config):
        super(Collage, self).__init__()
        self.config = config

        self.wallpaper_source = None

    @staticmethod
    def get_instances(plugins, config):
        collages = config['collage-plugins']

        if not collages == 'all':
            collages = collages.split(',')
            collages = [c.strip() for c in collages]

        instances = []
        for plugin in plugins:
            if plugin.name in collages or collages == 'all':
                instances.append(plugin(config))
                collages.remove(plugin.name)

        for collage_exception in collages:
            logging.warning('Collage %s not found' % collage_exception)

        return instances


    def set_source(self, source):
        self.wallpaper_source = source

    def generate(self, size, wallpaper_queue):
        """
            Generates the wallpaper collage
        """
        raise NotImplementedError()

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
            logging.debug('bit-depth error, using crappy scaling')
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

