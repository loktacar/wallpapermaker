import os
import sys

from .. import SetWallpaper

class LXDESetWallpaper(SetWallpaper):
    def __init__(self, config):
        super(LXDESetWallpaper, self).__init__(config)

    def platform_check(self):
        return sys.platform == 'linux2' and self.config['linux.desktop-environment'] == 'lxde'

    def set(self):
        os.system('pcmanfm --set-wallpaper=%s')
        if not self.config['keep']:
            logging.warning("LXDESetWallpaper works better if you configure "
                            "the keep plugin (e.g. --keep=2)")
