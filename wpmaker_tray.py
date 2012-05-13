#!/usr/bin/env python
import sys
import subprocess

from docopt import docopt
from config import Config, get_doc

# Create a new gtk+ class here
# This class calls Application in wpmaker.py
# Calls it with single run option

import gobject
import pygtk
if not sys.platform == 'win32':
    pygtk.require('2.0')
import gtk

class TrayApplication:
    def __init__(self, config):
        self.config = config
        self.running = None

        self.statusIcon = gtk.StatusIcon()
        self.statusIcon.set_from_stock(gtk.STOCK_ABOUT)
        self.statusIcon.set_visible(True)
        self.statusIcon.set_tooltip("wpmaker")

        menu = gtk.Menu()

        # Config Section selection
        sections = self.config.config_sections()
        if len(sections) > 1:
            menuItem = gtk.ImageMenuItem(gtk.STOCK_PREFERENCES)
            subMenu = gtk.Menu()
            for section in sections:
                subMenuItem = gtk.MenuItem(section)
                subMenuItem.connect('activate', self.set_config_section, section)
                subMenu.append(subMenuItem)

        menuItem.set_submenu(subMenu)
        menu.append(menuItem)

        seperator = gtk.SeparatorMenuItem()
        menu.append(seperator)

        menuItem = gtk.ImageMenuItem(gtk.STOCK_QUIT)
        menuItem.connect('activate', self.quit_cb, self.statusIcon)
        menu.append(menuItem)

        self.statusIcon.connect('popup-menu', self.popup_menu_cb, menu)
        self.statusIcon.set_visible(1)

        self.run()

    def set_config_section(self, widget, section):
        self.config.set_section(section)
        self.run()

    def quit_cb(self, widget, data = None):
        self.statusIcon.set_visible(0)
        gtk.main_quit()

    def popup_menu_cb(self, widget, button, time, data = None):
        if button == 3:
            if data:
                data.show_all()
                data.popup(None, None, gtk.status_icon_position_menu,
                           3, time, self.statusIcon)

    def run(self):
        if self.running is not None:
            self.stop()

        command = ['python', 'wpmaker.py']
        options = [x for x in cfg.get_option_list()]
        self.running = subprocess.Popen(command + options)

    def stop(self):
        self.running.kill()
        self.running = None

if __name__ == "__main__":
    __doc__ = get_doc('wpmaker_tray')

    ioptions, iarguments = docopt(__doc__)
    cfg = Config(ioptions)

    tray = TrayApplication(cfg)

    try:
        gtk.main()
    except KeyboardInterrupt:
        tray.statusIcon.set_visible(0)

