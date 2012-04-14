#!/usr/bin/env python
# TODO:
#   - make each split occupy a seperate folder
#   - Change name of main.py
#   - Multiple instances of the thread running at once? With seperate configurations from config.py
#   - Remove deleted images
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
    --fupdate=TIME              time seperating each scan of the wallpaper folder in seconds
    --generated-wallpaper=PATH  path of the output wallpaper
    --resolution=WIDTHxHEIGHT   sets a static value for resolution, instead of automatic
    -h --help                   shows this help message and exits
    -v --verbose                prints status messages as the program runs

"""

import os
import threading
import time

from docopt import docopt

import config
from resolution import get_screen_resolution
from setwallpaper import set_wallpaper
from images import ImageQueue
from wallpaper import wallpaper_split

def parse_options(cmd_opts):
    """ Generates option dictionary from configuration file and command line options """
    options = {}

    options['path'] = os.path.expanduser(cmd_opts.path if cmd_opts.path else config.path)
    options['extensions'] = cmd_opts.extensions if cmd_opts.extensions else config.extensions
    options['update_period'] = cmd_opts.update if cmd_opts.update else config.update_period
    options['generated_wallpaper'] = os.path.expanduser(\
                                        cmd_opts.generated_wallpaper if cmd_opts.generated_wallpaper else\
                                        config.generated_wallpaper)
    options['verbose'] = cmd_opts.verbose

    # Parse resolution input
    options['resolution'] = cmd_opts.resolution
    if options['resolution']:
        res = options['resolution'].split('x')
        if type(res) == str:
            res = options['resolution'].split('X')

        if type(res) == str:
            options['resolution'] == False
        else:
            try:
                options['resolution'] = [int(i) for i in res]
            except:
                options['resolution'] = False

    return options

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
