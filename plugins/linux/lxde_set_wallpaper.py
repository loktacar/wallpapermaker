import sys

from .. import SetWallpaper

class LXDESetWallpaper(SetWallpaper):
    def __init__(self, config):
        super(LXDESetWallpaper, self).__init__(config)
        self.cycle = 0

    def platform_check(self):
        return sys.platform == 'linux2' and self.config['linux.desktop-environment'] == 'lxde'

    def set(self):
        import os

        # TODO: Find a better solution than cycling
        #       - Cause: --set-wallpaper doesn't reload the file if the arguments are the same
        os.system(\
                'pcmanfm --set-wallpaper=%s --wallpaper-mode=%s' % (self.config['wallpaper'], 'fit' if self.cycle % 2 else 'center'))

        self.cycle += 1
