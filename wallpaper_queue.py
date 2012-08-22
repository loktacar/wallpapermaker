import random
import logging

import pygame

class WallpaperQueue:
    def __init__(self, config):
        self.config = config

        self.wallpapers = []
        self.index = -1

        self.logger = logging.getLogger('root')

    def pop(self, count=1):
        """ Pops wallpapers off the list, returns a generator of pygame wallpapers """

        if self.index == -1:
            self.shuffle()

        i = 0
        while i < count:
            if self.index < len(self.wallpapers):
                wallpaper_path = self.wallpapers[self.index]
            else:
                wallpaper_path = self.wallpapers[self.index % len(self.wallpapers)]

            self.logger.debug('%d - %s' % (self.index, wallpaper_path[len(self.config['path']):]))

            # Create pygame image
            try:
                wallpaper = pygame.image.load(wallpaper_path)
                if wallpaper.get_width() == 0 or wallpaper.get_height() == 0:
                    raise IOError
            except IOError:
                self.logger.debug('Failed to find wallpaper %s' % wallpaper)
                self.wallpapers.remove(wallpaper)
                continue

            self.index += 1
            i += 1

            yield wallpaper

    def push(self, wallpaper_paths):
        """ Push wallpaper paths on to the list, wallpaper_paths can be a single filepath or a list of paths """

        if not type(wallpaper_paths) is list:
            wallpaper_paths = [wallpaper_paths, ]

        c = 0
        for wp in wallpaper_paths:
            # Push it, if it isn't already on the list and has appropriate extension
            if not wp in self.wallpapers and self._check_extension(wp):
                c += 1
                self.wallpapers.append(wp)

        return c

    def _check_extension(self, filepath):
        """ Checks if the file has an extension found in config['extensions'] """
        extensions = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'pcx', 'tga', 'tiff', 'tif', 'iff', 'xpm']
        for extension in extensions:
            try:
                if filepath.index(extension) == len(filepath) - len(extension):
                    return True
            except:
                pass

        return False

    def count(self):
        """ Returns the number of wallpapers on queue """
        return len(self.wallpapers)

    def shuffle(self):
        """ Shuffles the wallpaper queue """
        self.logger.debug('Shuffling wallpaper queue')

        random.shuffle(self.wallpapers)
        self.index = 0

    def shuffle_if_needed(self):
        """ Check if it's time for another shuffle of the wallpapers, if so shuffle 'em """
        if self.index >= len(self.wallpapers):
            self.shuffle()
            return True
        else:
            return False

