#!/usr/bin/env python
import sys

from application import Application

# Check if verbose
verbose = False
for arg in sys.argv:
    if arg == '--verbose' or arg == '-v':
        verbose = True

# Start logger
import log
import logging
logger = log.setup_custom_logger('root', logging.DEBUG if verbose else logging.ERROR)

# Load all plugins
from plugins import plugin_manager

# Read options and arguments
from config import get_config
config = get_config()

# Set plugins' config
plugin_manager.set_config(config)

# Find and set ui
ui = None
if config['ui'] is not None:
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

# ui and app should both be set, logging started and config read.
# Let's start this thing
if __name__ == '__main__':
    main()
