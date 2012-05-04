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
#   - Windows
#       If I end up using gtk+ for tray icon I will have to install it and add gtk installation path to PATH environment variable
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
import pygtk
#pygtk.require('2.0')
import gtk

import os
import sys
import threading
import time

import pygame

from docopt import docopt
from config import Config
from compatibility import get_screen_resolution, set_wallpaper
from images import ImageQueue
from wallpaper import wallpaper_split


class MainThread(threading.Thread):
    def __init__(self, config):
        super(MainThread, self).__init__()
        self.daemon = True
        self._stop = False
        self._sleeping = False

        self.config = config
        self.wallpapers = ImageQueue(self.config)
        self.resolution = (0,0)
        self._no_file_check_interval = self.config['file_check_period']

    # Use only one update period, for now
    def run(self):
        while not self._stop:
            self._sleeping = False

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

                self.stop()
            else:
                if self.config['verbose']:
                    print 'sleep %ds' % self.config['update_period']

                self._sleeping = True

                time.sleep(self.config['update_period'])

    def stop(self):
        self._stop = True

    def stopped(self):
        return self._stop

    def sleeping(self):
        return self._sleeping

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

class CmdInputThread(threading.Thread):

    def __init__(self, main_thread):
        super(CmdInputThread, self).__init__()
        self.main_thread = main_thread
        self._stop = False
        self.daemon = True

    def run(self):
        while not self._stop and not self.main_thread.stopped():
            try:
                s = raw_input()
            except (KeyboardInterrupt, EOFError):
                sys.exit()

            if s == 'v' or s == 'verbose':
                self.main_thread.config['verbose'] = not self.main_thread.config['verbose']
                print self.main_thread.config['verbose']
            if s == 'q' or s == 'quit':
                self.stop()

        print 'cmdinputthread stopped'

    def stop(self):
        self._stop = True

    def stopped(self):
        return self._stop

class ControlThread(threading.Thread):

    def __init__(self, threads):
        super(ControlThread, self).__init__()
        self.threads = threads

    def run(self):
        while self.are_threads_running():
            time.sleep(0.5)

    def are_threads_running(self):
        running = True
        for t in self.threads:
            running = running and not t.stopped()

        return running

class HelloTray(threading.Thread):
    def __init__(self):
        super(HelloTray, self).__init__()
        self.daemon = True
        self._stop = False

        self.statusIcon = gtk.StatusIcon()
        self.statusIcon.set_from_stock(gtk.STOCK_ABOUT)
        self.statusIcon.set_visible(True)
        self.statusIcon.set_tooltip("Hello World")

        self.menu = gtk.Menu()
        self.menuItem = gtk.ImageMenuItem(gtk.STOCK_EXECUTE)
        self.menuItem.connect('activate', self.execute_cb, self.statusIcon)
        self.menu.append(self.menuItem)
        self.menuItem = gtk.ImageMenuItem(gtk.STOCK_QUIT)
        self.menuItem.connect('activate', self.quit_cb, self.statusIcon)
        self.menu.append(self.menuItem)

        self.statusIcon.connect('popup-menu', self.popup_menu_cb, self.menu)
        self.statusIcon.set_visible(1)

        #gtk.main()

    def run(self):
        gtk.gdk.threads_init()
        gtk.main()

        self._stop = True

    def execute_cb(self, widget, event, data = None):
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_border_width(10)

        button = gtk.Button("Hello World")
        button.connect_object("clicked", gtk.Widget.destroy, window)

        window.add(button)
        button.show()
        window.show()

    def quit_cb(self, widget, data = None):
        self.statusIcon.set_visible(0)
        gtk.main_quit()

    def popup_menu_cb(self, widget, button, time, data = None):
        if button == 3:
            if data:
                data.show_all()
                data.popup(None, None, gtk.status_icon_position_menu,
                        3, time, self.statusIcon)

    def stopped(self):
        return self._stop

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


    #app = Application(cfg)
    #sys.exit(app.run())

    main_thread = MainThread(cfg)
    main_thread.start()

    #input_thread = CmdInputThread(main_thread)
    #input_thread.start()

    tray_thread = HelloTray()
    tray_thread.start()

    ctrl_thread = ControlThread((main_thread, tray_thread))
    ctrl_thread.start()

