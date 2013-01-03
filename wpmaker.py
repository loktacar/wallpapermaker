#!/usr/bin/env python
import sys

from application import Application

# Check if verbose
verbose = False
for arg in sys.argv:
    if arg == '--verbose' or arg == '-v':
        verbose = True

# Start logger
import logging
logging.basicConfig(format='%(levelname)s (%(threadName)s): %(message)s\n%(pathname)s:%(lineno)d @ %(asctime)s\n',
                    filename='last_run.log',
                    filemode='w',
                    level=logging.DEBUG)

# Load all plugins
from plugins import plugin_manager

# Read options and arguments
from config import get_config
config = get_config(plugin_manager['Option'])

# Set plugins' config
plugin_manager.set_config(config)

# Find and set ui
ui = None
if 'ui' in config and config['ui'] is not None:
    for plugin in plugin_manager['UI']:
        if plugin.__class__.__name__ == config['ui']:
            ui = plugin

# Check if ui is set
if ui is None and config['ui'] is not None:
    raise RuntimeError("Couldn't find ui plugin '%s'" % config['ui'])

app = Application(config, ui)

def main():
    try:
        if ui is not None:
            ui.start_app()
        else:
            app.main()
    except KeyboardInterrupt:
        pass

def lowpriority():
    """ Set the priority of the process to below-normal."""

    if sys.platform == 'win32':
        # Based on:
        #   "Recipe 496767: Set Process Priority In Windows" on ActiveState
        #   http://code.activestate.com/recipes/496767/
        import win32api,win32process,win32con

        pid = win32api.GetCurrentProcessId()
        handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, pid)
        win32process.SetPriorityClass(handle, win32process.BELOW_NORMAL_PRIORITY_CLASS)
    else:
        import os

        os.nice(1)

# ui and app should both be set, logging started and config read.
# Let's start this thing
if __name__ == '__main__':
    try:
        lowpriority()
    except:
        # TODO: Make this a logger call not a direct print
        print 'Low priority not set, exception occurred!'

    main()
