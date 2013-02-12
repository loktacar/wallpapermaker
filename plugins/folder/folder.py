import random
import os
import logging

import pygame

from .. import Source
from utils import file_hidden

class Folder(Source):
    def __init__(self, path, include_hidden=False):
        super(Folder, self).__init__(path)

        self.path = os.path.expanduser(path)
        self.include_hidden = include_hidden
        self.index = -1

    @staticmethod
    def handles_path(path):
        # Unix
        if path[0] == '/' or path[0] == '~':
            return True
        # Windows local and network
        elif path[1:3] == ':\\' or path[:2] == '\\\\':
            return True

        return False

    def set_path(self, path):
        self.wallpapers = []
        self.index = -1
        self.path = path
        logging.debug('Changing folder path to %s' % self.path)

    def pop(self, count=1):
        logging.debug('popping %d images' % count)

        # If this is the first run, find images and shuffle
        if self.index == -1:
            self._shuffle()
            self.index = 0

        i = 0
        while i < count:
            wallpaper_path = self.wallpapers[self.index % len(self.wallpapers)]

            # Create pygame image
            try:
                wallpaper = self._image_from_path(wallpaper_path)
            except:
                logging.error('Failed to find wallpaper %s' % wallpaper)
                self.wallpapers.remove(wallpaper)
                continue

            self.index += 1
            i += 1

            yield wallpaper

    def _find_wallpapers(self):
        for root, dirs, files in os.walk(self.path):
            if not self.include_hidden:
                if file_hidden(root):
                    continue # The dir we're visiting is hidden
                for f in files:
                    if file_hidden(os.path.join(root, f)):
                        files.remove(f)
                for d in dirs:
                    if file_hidden(os.path.join(root, d)):
                        # Don't traverse in to hidden directories
                        dirs.remove(d)

            self._folder_visit(root, files)

        count = self.count()
        logging.debug('%s image%s in %s' % (count, '' if count == 1 else 's', self.path))

    def _folder_visit(self, dirpath, filenames):
        wallpaper_paths = [os.path.join(dirpath, filename) for filename in filenames]
        pushed_count = self._push(wallpaper_paths)

    def _push(self, wallpaper_paths):
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
        extensions = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'pcx', 'tga', 'tiff', 'tif', 'iff', 'xpm']
        for extension in extensions:
            try:
                if filepath.index(extension) == len(filepath) - len(extension):
                    return True
            except:
                pass

        return False

    def wallpaper_complete(self):
        if self.index >= len(self.wallpapers):
            self._shuffle()

    def _shuffle(self):
        """ Shuffles the wallpaper queue """
        logging.debug('Shuffling wallpaper queue')

        self._find_wallpapers()

        random.shuffle(self.wallpapers)
        self.index = 0
