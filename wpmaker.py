import sys
import time
import random

# Check if verbose
verbose = False
for arg in sys.argv:
    if arg == '--verbose' or arg == '-v':
        verbose = True

# Start logger
import log
import logging
logger = log.setup_custom_logger('root', logging.DEBUG if verbose else logging.ERROR)

# Load plugins
logger.debug('Loading plugins')
from plugins import collage_plugins, get_resolution_plugins, set_wallpaper_plugins

# Read options and arguments
logger.debug('Reading config file and parsing options')
from config import get_config
config = get_config()
print 'config: ', config

# Find wallpapers
logger.debug('Initialize wallpapers')
from wallpapers import Wallpapers
wps = Wallpapers(config)

# Instantiate collages
collages = [c(config) for c in collage_plugins]

# Get resolution function
def get_res():
    for g in get_resolution_plugins:
        if g.platform_check():
            return g.get()

    return (0,0)

# Set wallpaper
def set_wp():
    for s in set_wallpaper_plugins:
        if s.platform_check(config):
            return s.set(config)


def main():
    # File check interval counter
    file_check_counter = config['fs-interval']

    i = 0
    # Wallpaper generation loop
    while(True):
        logger.debug('Loop start')

        config['resolution'] = get_res()
        logger.info('Resolution set to %sx%s' % (config['resolution'][0], config['resolution'][1]))

        if config['resolution'] == (0,0):
            raise ValueError('Resolution not set')

        if file_check_counter == config['fs-interval']:
            logger.debug('Find wallpapers')
            wps.find_wallpapers()
            file_check_counter = 1
        else:
            file_check_counter += 1

        if not wps.count():
            raise ValueError('No wallpapers found')

        logger.debug('Make collage')
        if config['collage-plugin'] == 'all':
            collage_index = random.randint(0, len(collages) - 1)
            c = collages[collage_index].generate(config['resolution'], wps)
            collages[collage_index].save(c, config['wallpaper'])
            set_wp()
        else:
            for collage in collages:
                if collage.__class__.__name__ == config['collage-plugin']:
                    c = collage.generate(config['resolution'], wps)
                    collage.save(c, config['wallpaper'])
                    set_wp()

        # Check if wps needs shuffling
        wps.shuffle_if_needed()

        if config['single-run']:
            break

        i += 1
        logger.debug('Loop end, sleep %ds' % config['update'])
        time.sleep(config['update'])


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        # Do nothing
        pass
