#!/usr/bin/env python
import sys

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

class HelloTray:
    def __init__(self, application):
        self.application = application

        self.statusIcon = gtk.StatusIcon()
        self.statusIcon.set_from_stock(gtk.STOCK_ABOUT)
        self.statusIcon.set_visible(True)
        self.statusIcon.set_tooltip("wpmaker")

        menu = gtk.Menu()

        # Config Section selection
        sections = self.application.config.config_sections()
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

        self.generate_callback()

    def set_config_section(self, widget, section):
        gobject.idle_add(self.application.config.set_section, section)

    def quit_cb(self, widget, data = None):
        self.statusIcon.set_visible(0)
        gtk.main_quit()

    def popup_menu_cb(self, widget, button, time, data = None):
        if button == 3:
            if data:
                data.show_all()
                data.popup(None, None, gtk.status_icon_position_menu,
                           3, time, self.statusIcon)

    def generate_callback(self):
        # TODO: use popen to call the application
        #       - this may take more time because of filesystem checks etc.
        #       - should however stop it from throwing segmentation faults
        #       - self.config should be a Config instance and generate the arguments for the application
        gobject.idle_add(self.application.run, True, True)

        gobject.timeout_add_seconds(self.application.config['update_period'], self.generate_callback)

if __name__ == "__main__":
    __doc__ = get_doc()

    ioptions, iarguments = docopt(__doc__)
    cfg = Config(ioptions)

    gobject.threads_init()

    from wpmaker import Application
    app = Application(cfg)

    helloWord = HelloTray(app)
    gtk.main()

