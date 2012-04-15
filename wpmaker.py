#!/usr/bin/env python
# TODO:
#   - Remove deleted images from queue
#   - Add a recursion level option
#   - Add option to add date to generated wallpaper name, preceding the '.'
#   - Read configuration from default locations (see appdirs and Config module)
#
# Compatibility
#   - Make mac compatible
#   - Make xmonad compatible
#
# IDEAS
#   - Make each split occupy a seperate folder
#   - Multiple instances of the thread running at once? With seperate configurations from config.py
#       * Option to only create image, don't set as wallpaper
#
# Optimization
#   - Multiple threads for resize and make_split functions so that it can be done on multiple cores?
#     Try to lower cpu usage, even though it's running for a while
#
"""Usage main.py [options]

Options:
    --path=PATH                 path of wallpaper folder
    --extensions=LIST           comma seperated list of acceptable extensions
    --update=TIME               time seperating each wallpaper update in seconds
    --generated-wallpaper=PATH  path of the output wallpaper
    --resolution=WIDTHxHEIGHT   sets a static value for resolution, instead of automatic
    -h --help                   shows this help message and exits
    -v --verbose                prints status messages as the program runs

"""

import os
import sys

# Add site-packages directory to pythonpath
sys.path.append(os.path.abspath('site-packages'))

import threading
import time

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

        self.wallpapers = ImageQueue(verbose=self.options['verbose'])
        if self.options['resolution']:
            self.resolution = self.options['resolution']
        else:
            self.resolution = get_screen_resolution()


    # Use only one update period, for now
    def run(self):
        while not self._stop:
            # Check files
            os.path.walk(self.options['path'], self._callback, [])
            if self.options['verbose']:
                print '%d images in queue' % self.wallpapers.count()

            if self.wallpapers.count():
                # If not set, check resolution
                if not self.options['resolution']:
                    self.resolution = get_screen_resolution()

                # Create wallpaper
                self._make_wallpaper(self.resolution)
                self.wallpapers.shuffle_check()
                # Change wallpaper
                self._set_wallpaper()

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
        img = wallpaper_split(size, self.wallpapers.pop_image)
        img.save(self.options['generated_wallpaper'], 'BMP')

    def _set_wallpaper(self):
        """ Sets the wallpaper to latest generated wallpaper """
        set_wallpaper(self.options['generated_wallpaper'])

    # 'private' file functions
    def _callback(self, arg, dirname, fnames):
        """ Gets a list of files from each directory in 'path', including 'path' directory iteself """
        filtered_filenames = ['%s/%s' % (dirname, i) for i in fnames if self._check_extension(i.lower())]
        pushed_count = self.wallpapers.push(filtered_filenames)

        if self.options['verbose'] and pushed_count:
            print 'pushed %d images from %s' % (pushed_count, dirname)

    def _check_extension(self, fname):
        """ Checks if file has extension found in extensions, from configuration """
        for extension in self.options['extensions']:
            try:
                if fname.index(extension) == len(fname) - len(extension):
                    return True
            except:
                pass


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