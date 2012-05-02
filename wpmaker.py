#!/usr/bin/env python
# TODO, before I release:
#
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
#       Was fixed with installing osx version specific pygames installation
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
import time
import pygame

from docopt import docopt
from config import Config
from compatibility import get_screen_resolution, set_wallpaper
from images import ImageQueue
from wallpaper import wallpaper_split


class Application:
    def __init__(self, config):
        self.config = config
        self.wallpapers = ImageQueue(self.config['path'], self.config['extensions'], verbose=self.config['verbose'])
        self.resolution = (0,0)
        self._stop = False
        self._no_file_check_interval = self.config['file_check_period']

    # Use only one update period, for now
    def run(self):
        while not self._stop:
            # Check files
            if self._no_file_check_interval == self.config['file_check_period']:
                self.wallpapers.walk_path()
                self._no_file_check_interval = 0
            else:
                self._no_file_check_interval += 1

            if self.wallpapers.count():
                self.resolution = self._get_resolution()

                # Create wallpaper
                wp_name = self._make_wallpaper(self.resolution)
                self.wallpapers.shuffle_check()
                # Change wallpaper
                self._set_wallpaper(wp_name)
            else:
                raise ValueError('No wallpapers found')

            if self.config['single_run']:
                if self.config['verbose']:
                    print 'Single run, now exiting'

                try:
                    return os.EX_OK # Exit without errors
                except AttributeError:
                    return 0

            if self.config['verbose']:
                print 'sleep %ds' % self.config['update_period']
            try:
                time.sleep(self.config['update_period'])
            except KeyboardInterrupt:
                try:
                    return os.EX_OK
                except AttributeError:
                    return 0 # On windows just exit, windwos doesnt care about results

    def stop(self):
        self._stop = True

    def stopped(self):
        return self._stop

    # 'private' wallpaper manipulation functions
    def _make_wallpaper(self, size):
        """ Creates a wallpaper and saves it """
        img = wallpaper_split(size,
                              self.wallpapers.pop_image,
                              recursion_depth=self.config['recursion_depth'] - 1)

        wp_name = self.config['generated_wallpaper']
        if self.config['add_date']:
            from datetime import datetime
            now = datetime.now()
            period = wp_name.rindex('.')
            wp_name = ''.join([
                wp_name[:period],
                now.strftime('_%Y-%m-%d_%H-%M'),
                wp_name[period:]
                ])

        pygame.image.save(img, wp_name)

        return wp_name

    def _set_wallpaper(self, wp_name):
        """ Sets the wallpaper to latest generated wallpaper """
        set_wallpaper(wp_name, self.config['desktop_environment'])
        if self.config['verbose']:
            print 'wp set to ' + wp_name

    def _get_resolution(self):
        resolution = self.resolution
        if self.config['resolution']:
            resolution = self.config['resolution']
        else:
            resolution = get_screen_resolution()
            if not resolution == self.resolution and self.config['verbose']:
                print 'resolution changed to %sx%s' % (resolution[0], resolution[1])

        if max(*resolution) < 1:
            raise ValueError('Resolution incorrect: %sx%s' % (resolution[0], resolution[1]))

        return resolution

if __name__ == '__main__':
    # Append configuration file help
    from config import appname, appauthor, config_file_name
    from appdirs import AppDirs
    appdirs = AppDirs(appname, appauthor)
    dir_splitter = '/'
    if '\\' in  appdirs.user_data_dir:
        dir_splitter = '\\'
    __doc__ += """Configuration:

    Files
    %s
    %s

    See sample.config.py for information on options and examples
""" % (appdirs.user_data_dir + dir_splitter + config_file_name,
       appdirs.site_data_dir + dir_splitter + config_file_name)

    # get input options and arguments
    ioptions, iarguments = docopt(__doc__)
    # parse options
    cfg = Config(ioptions)

    app = Application(cfg)
    sys.exit(app.run())

