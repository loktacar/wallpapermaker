import time
import random
import logging

import pygame

class Application:
    def __init__(self, config, ui=None):
        # Check if path is set in config
        if config['sources'] == None:
            raise ValueError('Sources is not set in configuration')

        # Load plugins
        from plugins import plugin_manager
        self.plugin_manager = plugin_manager

        # Call ui hooks
        self.ui = ui
        if self.ui is not None:
            self.ui.app = self

        self.plugin_manager.plugin_hook('app_started')

        # Set config
        self.config = config
        # Tell the plugins we've got a configuration
        self.plugin_manager.plugin_hook('set_config', self.config)

        # Initialize wallpaper class
        logging.debug('Initialize wallpapers')
        from wallpapers import Wallpapers
        self.wallpaper_source = Wallpapers(self.config)
        # Tell the plugins we've got a wallpaper source
        self.plugin_manager.plugin_hook('set_source', self.wallpaper_source)

        self.resolution = (0,0)

        # Variables for counting, timing, etc. in main loop
        self.next_generation = time.time()
        self.sleep_increment = 0.10 # in milliseconds
        self.is_paused = False
        self.running = True

        # Variables relating to ui changes
        self.next_collage_plugin = None

        self.plugin_manager.plugin_hook('app_initialized')

    def pause(self, paused_value=None):
        if paused_value is None:
            self.is_paused = not self.is_paused
        else:
            self.is_paused = paused_value

        logging.debug('app is %spaused' % ('' if self.is_paused else 'un'))

    def toggle_collage(self, collage_name, activate=True):
        if activate:
            if self.plugin_manager.activate_plugin('Collage', collage_name):
                self.plugin_manager.plugin_hook('collage_toggled', collage_name, activated=True)
        else:
            if self.plugin_manager.deactivate_plugin('Collage', collage_name):
                self.plugin_manager.plugin_hook('collage_toggled', collage_name, activated=False)

                # dectivation complete, check if there are any other active collages
                if not len(self.plugin_manager.active('Collage')):
                    # if not then activate ALL OF THEM
                    for c in self.plugin_manager.plugins['Collage']:
                        self.toggle_collage(c.__name__, True)

    def main(self):
        while(self.running):
            if time.time() >= self.next_generation and not self.is_paused:
                logging.debug('Loop start')

                # Get resolution
                # (width, height, x-offset, y-offset)
                res_log_message = ''
                if self.config['resolution'] == [(0,0)]:
                    self.resolutions = self.plugin_manager['GetResolution'][0].get()
                    res_log_message = 'Resolution plugin returned %s' % self.resolutions
                else:
                    self.resolution = self.config['resolution']
                    res_log_message = 'Resolution set to %s by config' % self.resolutions
                logging.debug(res_log_message)

                if self.resolution == None or self.resolution == []:
                    raise ValueError('Resolution invalid')

                wps = []
                total_width = 0
                total_height = 0

                self.plugin_manager.plugin_hook('generate_starting')

                # Find the maximum width + x-offset and height + y-offset
                # Also create a wallpaper collage for each resolution
                for i, resolution in enumerate(self.resolutions):
                    if resolution[0] + resolution[2] > total_width:
                        total_width = resolution[0] + resolution[2]

                    if resolution[1] + resolution[3] > total_height:
                        total_height = resolution[1] + resolution[3]

                    # Create new collage
                    collage_index = random.randint(0, len(self.plugin_manager['Collage']) - 1)
                    collage_plugin = self.plugin_manager['Collage'][collage_index]

                    logging.debug('Generating collage, using plugin %s' % collage_plugin.__class__.__name__)


                    # Generate collage
                    wps.append(collage_plugin.generate(resolution[:2]))

                # Merge collages
                wallpaper = pygame.Surface((total_width, total_height))
                wallpaper.lock()

                for i, resolution in enumerate(self.resolutions):
                    for x1, x2 in enumerate(range(resolution[2], resolution[2] + resolution[0])):
                        for y1, y2 in enumerate(range(resolution[3], resolution[3] + resolution[1])):
                            wallpaper.set_at((x2, y2), wps[i].get_at((x1, y1)))

                wallpaper.unlock()
                pygame.image.save(wallpaper, self.config['wallpaper'])

                if len(self.plugin_manager['SetWallpaper']):
                    self.plugin_manager['SetWallpaper'][0].set()

                self.plugin_manager.plugin_hook('generate_finished')

                if self.config['single-run']:
                    logging.debug('Single run, exiting')
                    break

                # Shuffle wallpapers
                self.wallpaper_source.wallpaper_complete()

                self.next_generation = time.time() + self.config['update']
                logging.debug('Loop end, waiting untill %s' %
                        time.strftime('%X', time.localtime(self.next_generation)))

            time.sleep(self.sleep_increment)

        self.plugin_manager.plugin_hook('app_quitting')

