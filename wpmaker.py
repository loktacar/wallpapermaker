#!/usr/bin/env python
# TODO, before I release:
#   Compatibility
#       - Make mac compatible
#       - Make xmonad compatible
#       - Make kde compatible
#
#   Installation
#       - Create .dmg thingie for mac
#       - Create yum and apt packages
#       - Create installer for windows
#
# IDEAS, to be done after release:
#   - Make each split occupy a seperate folder
#   - Multiple instances of the thread running at once? With seperate configurations from config.py
#       * Option to only create image, don't set as wallpaper
#
# Optimization
#   - Multiple threads for resize and make_split functions so that it can be done on multiple cores?
#     Try to lower cpu usage, even though it's running for a while
#   - Use OpenGL or similar to create images, might save A LOT of time. However might be harder to implement.
#     Although a 3d image collage might be cool
#
# Possible installation problems
#   - MAC
#       SLD_Image is problematic, check pygame.image.get_extended()
#       http://pygame.org/download.shtml - install macintosh stuffs
#
"""Usage main.py [options]

Options:
    --section=SECTION           section of config file to be used
    --path=PATH                 path of wallpaper folder
    --extensions=LIST           comma seperated list of acceptable extensions
    --update=TIME               time seperating each wallpaper update in seconds
    --generated-wallpaper=PATH  path of the output wallpaper
    --resolution=WIDTHxHEIGHT   sets a static value for resolution, instead of automatic
    --add-date                  adds date to generated wallpaper filename
    --recursion-depth=INT       maximum number of times each split can be split
    -s --single-run             create and set a single wallpaper then exit
    -h --help                   shows this help message and exits
    -v --verbose                prints status messages as the program runs

"""

import os
import sys

import threading
import time

import pygame

from docopt import docopt

from config import parse_options
from resolution import get_screen_resolution
from setwallpaper import set_wallpaper
from images import ImageQueue
from wallpaper import wallpaper_split

class MainThread(threading.Thread):
    def __init__(self, options):
        super(MainThread, self).__init__()
        self.daemon = True
        self._stop = False

        self.options = options

        self.wallpapers = ImageQueue(self.options['path'], self.options['extensions'], verbose=self.options['verbose'])
        if self.options['resolution']:
            self.resolution = self.options['resolution']
        else:
            self.resolution = get_screen_resolution()

    # Use only one update period, for now
    def run(self):
        while not self._stop:
            # Check files
            self.wallpapers.walk_path()

            if self.wallpapers.count():
                # If not set, check resolution
                if not self.options['resolution']:
                    self.resolution = get_screen_resolution()

                # Create wallpaper
                wp_name = self._make_wallpaper(self.resolution)
                self.wallpapers.shuffle_check()
                # Change wallpaper
                self._set_wallpaper(wp_name)

            if self.options['single_run']:
                if self.options['verbose']:
                    print 'Single run, now exiting'

                os._exit(os.EX_OK) # Exit without errors

            if self.options['verbose']:
                print 'sleep %ds' % self.options['update_period']
            time.sleep(self.options['update_period'])

    def stop(self):
        self._stop = True

    def stopped(self):
        return self._stop

    # 'private' wallpaper manipulation functions
    def _make_wallpaper(self, size):
        """ Creates a wallpaper and saves it """
        img = wallpaper_split(size,
                              self.wallpapers.pop_image,
                              recursion_depth=self.options['recursion_depth'] - 1)

        wp_name = self.options['generated_wallpaper']
        if self.options['add_date']:
            from datetime import datetime
            last_period_index = 0
            try:
                last_period_index = len(wp_name) - 1 - wp_name[::-1].index('.')
            except ValueError:
                last_period_index = len(wp_name) - 1

            now = datetime.now()
            wp_name = wp_name[:last_period_index] + now.strftime('_%Y-%m-%d_%H-%M') + wp_name[last_period_index:]

        pygame.image.save(img, wp_name)

        return wp_name

    def _set_wallpaper(self, wp_name):
        """ Sets the wallpaper to latest generated wallpaper """
        set_wallpaper(wp_name, self.options['desktop_environment'])
        if self.options['verbose']:
            print 'wp set'


if __name__ == '__main__':
    # get input options and arguments
    ioptions, iarguments = docopt(__doc__)

    # parse options into dictionary
    options = parse_options(ioptions)

    # create main thread
    main_thread = MainThread(options)

    try:
        main_thread.start()
        # wait for keyboard input to kill threads
        # time seems to have no effect
        while (True):
            time.sleep(10)
    except (KeyboardInterrupt, SystemExit):
        main_thread.stop()
