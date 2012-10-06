import time
import random
import logging

import pygame

class Application:
    def __init__(self, config, ui=None):
        self.logger = logging.getLogger('root')

        # Load plugins
        self.logger.debug('Loading plugins')
        from plugins import plugin_manager
        self.plugin_manager = plugin_manager

        # Call ui hooks
        self.ui = ui
        if self.ui is not None:
            self.ui.app = self

        self.ui_hook('app_started')

        # Set config
        self.config = config

        # Initialize wallpaper class
        self.logger.debug('Initialize wallpapers')
        from wallpapers import Wallpapers
        self.wallpaper_source = Wallpapers(self.config)

        for collage in self.plugin_manager['Collage']:
            collage.wallpaper_source = self.wallpaper_source

        self.resolution = (0,0)

        # Variables for counting, timing, etc. in main loop
        self.next_generation = time.time()
        self.sleep_increment = 0.10 # in milliseconds
        self.is_paused = False
        self.running = True

        # Variables relating to ui changes
        self.next_collage_plugin = None

        self.ui_hook('app_initialized')

    def pause(self, paused_value=None):
        if paused_value is None:
            self.is_paused = not self.is_paused
        else:
            self.is_paused = paused_value

        self.logger.debug('app is %spaused' % ('' if self.is_paused else 'un'))

    def switch_collage_plugin(self, collage):
        self.next_collage_plugin = collage

    def ui_hook(self, hook_name, *args, **kwargs):
        if self.ui is not None:
            if hook_name in self.ui.__class__.__dict__:
                self.logger.debug('ui hook %s called' % hook_name)
                getattr(self.ui, hook_name)(*args, **kwargs)
            else:
                self.logger.debug('ui hook %s not implemented' % hook_name)

    def get_resolution(self):
        for g in self.plugin_manager['GetResolution']:
            if g.platform_check():
                return g.get()

        return None

    def set_wallpaper(self):
        for s in self.plugin_manager['SetWallpaper']:
            if s.platform_check():
                return s.set()

    def main(self):
        while(self.running):
            if time.time() >= self.next_generation and not self.is_paused:
                self.logger.debug('Loop start')

                # Get resolution
                # (width, height, x-offset, y-offset)
                res_log_message = ''
                if self.config['resolution'] == [(0,0)]:
                    self.resolutions = self.get_resolution()
                    res_log_message = 'Resolution plugin returned %s' % self.resolutions
                else:
                    self.resolution = self.config['resolution']
                    res_log_message = 'Resolution set to %s by config' % self.resolutions[0]
                self.logger.debug(res_log_message)

                if self.resolution == None:
                    raise ValueError('Resolution invalid')

                wps = []
                total_width = 0
                total_height = 0

                # Find the maximum width + x-offset and height + y-offset
                # Also create a wallpaper collage for each resolution
                for i, resolution in enumerate(self.resolutions):
                    if resolution[0] + resolution[2] > total_width:
                        total_width = resolution[0] + resolution[2]

                    if resolution[1] + resolution[3] > total_height:
                        total_height = resolution[1] + resolution[3]

                    # Create new collage
                    collage_plugin = None
                    # Find a random collage
                    if self.config['collage-plugin'] == 'all':
                        collage_index = random.randint(0, len(self.plugin_manager['Collage']) - 1)
                        collage_plugin = self.plugin_manager['Collage'][collage_index]
                    # Find configured collage
                    else:
                        for c in self.plugin_manager['Collage']:
                            if c.__class__.__name__ == self.config['collage-plugin']:
                                collage_plugin = c

                        if collage_plugin == None:
                            raise ValueError('Collage plugin not found')

                    self.logger.debug('Generating collage, using plugin %s' % collage_plugin.__class__.__name__)

                    self.ui_hook('generate_starting', collage_plugin.__class__.__name__)

                    # Generate collage
                    wps.append(collage_plugin.generate(resolution[:2]))

                # Merge collages
                wallpaper = pygame.Surface((total_width, total_height))
                wallpaper.lock()

                for i, resolution in enumerate(self.resolutions):
                    for x1, x2 in enumerate(range(resolution[2], resolution[2] + resolution[0])):
                        for y1, y2 in enumerate(range(resolution[3], resolution[3] + resolution[1])):
                            #print '(%d, %d) and (%d, %d)' % (x1, y1, x2, y2)
                            wallpaper.set_at((x2, y2), wps[i].get_at((x1, y1)))

                wallpaper.unlock()
                collage_plugin.save(wallpaper, self.config['wallpaper'])
                self.set_wallpaper()

                self.ui_hook('generate_finished')

                if self.config['single-run']:
                    self.logger.debug('Single run, exiting')
                    break

                self.next_generation = time.time() + self.config['update']
                self.logger.debug('Loop end, waiting untill %s' %
                        time.strftime('%X', time.localtime(self.next_generation)))

            time.sleep(self.sleep_increment)

            if self.next_collage_plugin is not None:
                self.config['collage-plugin'] = self.next_collage_plugin
                self.next_collage_plugin = None

        self.ui_hook('app_quitting')

