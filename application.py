import time
import random
import logging

import pygame

from config import save_config

class Application:
    def __init__(self, config, ui=None):
        from plugins import plugin_manager
        self.plugin_manager = plugin_manager
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

        # Important parts are all here
        self.plugin_manager.plugin_hook('app_initialized', self)

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

                # Set the wallpaper_source in the newly activated collage plugin
                self.plugin_manager.plugin_hook('set_source', self.wallpaper_source)
            else:
                logging.warning('Failed to activate %s collage' % collage_name)
        else:
            if self.plugin_manager.deactivate_plugin(plugin_type='Collage', plugin_name=collage_name):
                self.plugin_manager.plugin_hook('collage_toggled', collage_name, activated=False)
            else:
                logging.warning('Failed to deactivate %s collage' % collage_name)

            # dectivation complete, check if there are any other active collages
            if not len(self.plugin_manager.active['Collage']):
                # if not then activate ALL OF THEM
                for c in self.plugin_manager.plugins['Collage']:
                    self.toggle_collage(c.__name__, activate=True)

            # Set the wallpaper_source in the newly activated collage plugins
            self.plugin_manager.plugin_hook('set_source', self.wallpaper_source)

    def update_config_file(self, section, option, value):
        save_config(section, option, value)

    def main(self):
        while(self.running):
            self.generate()

            if self.config['single-run']:
                logging.debug('Single run, exiting')
                break

            time.sleep(self.sleep_increment)

        self.plugin_manager.plugin_hook('app_quitting')

    def get_resolution(self):
        # (width, height, x-offset, y-offset)
        res_log_message = ''
        resolutions = None
        if self.config['resolution'] == [(0,0)]:
            resolutions = self.plugin_manager['GetResolution'][0].get()
            res_log_message = 'Resolution plugin returned %s' % resolutions
        else:
            resolutions = self.config['resolution']
            res_log_message = 'Resolution set to %s by config' % resolutions
        logging.debug(res_log_message)

        for i, r in enumerate(resolutions):
            if len(r) == 2:
                # Add default x- and y-offset coordinates if missing to (0,0)
                resolutions[i] = (r[0], r[1], 0, 0)

        if not resolutions:
            raise ValueError('Resolution invalid')
        logging.debug("resolutions: {}".format(resolutions))
        self.resolutions = resolutions

    def generate(self):
        if time.time() >= self.next_generation and not self.is_paused:
            logging.debug('Loop start')

            # Get resolution
            self.get_resolution()

            wps = []
            total_width = 0
            total_height = 0
            # To fix issues with windows tiling
            min_width = 0
            min_height = 0

            self.plugin_manager.plugin_hook('generate_starting')

            # Create a wallpaper collage for each resolution
            for i, resolution in enumerate(self.resolutions):
                # Find the maximum width + x-offset and height + y-offset
                if resolution[0] + resolution[2] > total_width:
                    total_width = resolution[0] + resolution[2]
                if resolution[1] + resolution[3] > total_height:
                    total_height = resolution[1] + resolution[3]

                # Find the minimum offset of width and height
                if resolution[2] < min_width:
                    min_width = resolution[2]
                if resolution[3] < min_height:
                    min_height = resolution[3]

                # Create new collage
                collage_plugin = random.choice(self.plugin_manager['Collage'])

                logging.debug('Generating collage, using plugin %s' % collage_plugin.__class__.__name__)

                # Generate collage
                wps.append(collage_plugin.generate(resolution[:2]))

            # For windows tiling append (right/bottom) wallpapers left/ontop of main screen (those with negative offset)
            total_width -= min_width
            total_height -= min_height

            # Merge collages
            wallpaper = pygame.Surface((total_width, total_height))

            for i, resolution in enumerate(self.resolutions):
                size = resolution[:2]
                offset = resolution[2:]

                # Fix windows tiling issues
                if offset[0] < 0:
                    offset = (offset[0] + total_width, offset[1])
                if offset[1] < 0:
                    offset = (offset[0], offset[1] + total_height)

                wallpaper.blit(wps[i], offset)

                # More windows tiling issues
                neu_offset = (offset[0], offset[1])
                if offset[0] + size[0] > total_width:
                    neu_offset = (offset[0] - total_width, neu_offset[1])
                if offset[1] + size[1] > total_height:
                    neu_offset = (neu_offset[0], offset[1] - total_height)

                if not neu_offset == offset:
                    wallpaper.blit(wps[i], neu_offset)

            pygame.image.save(wallpaper, self.config['wallpaper'])

            if len(self.plugin_manager['SetWallpaper']):
                if not self.config['set-wallpaper'] == 'none':
                    try:
                        self.plugin_manager['SetWallpaper'][0].set()
                    except TypeError:
                        logging.warning('No set-wallpaper plugin active')

            self.plugin_manager.plugin_hook('generate_finished')

            # Shuffle wallpapers
            self.wallpaper_source.wallpaper_complete()

            self.next_generation = time.time() + self.config['update']
            logging.debug('Loop end, waiting untill %s' %
                    time.strftime('%X', time.localtime(self.next_generation)))
