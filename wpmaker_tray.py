#!/usr/bin/env python
from docopt import docopt
from config import Config, get_doc

# Create a new gtk+ class here
# This class calls Application in wpmaker.py
# Calls it with single run option

import gobject
import pygtk
pygtk.require('2.0')
import gtk

class HelloTray:
    def __init__(self, application):
        self.application = application

        self.statusIcon = gtk.StatusIcon()
        self.statusIcon.set_from_stock(gtk.STOCK_ABOUT)
        self.statusIcon.set_visible(True)
        self.statusIcon.set_tooltip("wpmaker")

        self.menu = gtk.Menu()
        self.menuItem = gtk.ImageMenuItem(gtk.STOCK_EXECUTE)
        self.menuItem.connect('activate', self.execute_cb, self.statusIcon)
        self.menu.append(self.menuItem)

        # Config Section selection
        self.menuItem = gtk.ImageMenuItem(gtk.STOCK_PREFERENCES)

        self.subMenu = gtk.Menu()
        self.subMenuItem = gtk.ImageMenuItem(gtk.STOCK_NEW)
        self.subMenuItem.connect('activate', self.set_config_section, 'default')
        self.subMenu.append(self.subMenuItem)
        self.subMenuItem = gtk.ImageMenuItem(gtk.STOCK_YES)
        self.subMenuItem.connect('activate', self.set_config_section, 'debug')
        self.subMenu.append(self.subMenuItem)

        self.menuItem.set_submenu(self.subMenu)
        self.menu.append(self.menuItem)

        self.menuItem = gtk.ImageMenuItem(gtk.STOCK_QUIT)
        self.menuItem.connect('activate', self.quit_cb, self.statusIcon)
        self.menu.append(self.menuItem)

        self.statusIcon.connect('popup-menu', self.popup_menu_cb, self.menu)
        self.statusIcon.set_visible(1)

    def set_config_section(self, widget, section):
        gobject.idle_add(self.application.config.set_section, section)

    def execute_cb(self, widget, event, data = None):
        gobject.idle_add(self.application.run, True)
        #window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        #window.set_border_width(10)

        #button = gtk.Button("Hello World")
        #button.connect_object("clicked", gtk.Widget.destroy, window)

        #window.add(button)
        #button.show()
        #window.show()

    def quit_cb(self, widget, data = None):
        self.statusIcon.set_visible(0)
        gtk.main_quit()

    def popup_menu_cb(self, widget, button, time, data = None):
        if button == 3:
            if data:
                data.show_all()
                data.popup(None, None, gtk.status_icon_position_menu,
                           3, time, self.statusIcon)

if __name__ == "__main__":
    __doc__ = get_doc()

    ioptions, iarguments = docopt(__doc__)
    cfg = Config(ioptions)

    gobject.threads_init()

    from wpmaker import Application
    app = Application(cfg)

    helloWord = HelloTray(app)
    gtk.main()

