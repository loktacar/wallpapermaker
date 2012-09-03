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

logger.debug('Loading UI plugins')
from plugins import ui_plugins

# Read options and arguments
logger.debug('Reading config file and parsing options') # Move log call to get_config()
from config import get_config
config = get_config()

# Find and set ui
ui = None
if config['ui'] is not None:
    logger.debug('Setting ui to %s plugin' % config['ui'])
    for plugin in ui_plugins:
        if plugin.__name__ == config['ui']:
            ui = plugin()

# Check if ui is set
if ui is None and config['ui'] is not None:
    raise RuntimeError("Couldn't start ui '%s'" % config['ui'])

app = Application(config, ui)

# ui and app should both be set, logging started and config read.
# Let's start this thing
if __name__ == '__main__':
    try:
        if ui is not None:
            ui.start_app()
        else:
            app.main()
    except KeyboardInterrupt:
        pass
