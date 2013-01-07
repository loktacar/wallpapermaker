import sys

from .. import SetWallpaper

class GnomeSetWallpaper(SetWallpaper):
    def __init__(self, config):
        super(GnomeSetWallpaper, self).__init__(config)

    def platform_check(self):
        return sys.platform == 'linux2' and self.config['desktop-environment'] == 'gnome'

    def set(self):
        import os

        os.system(\
                'gsettings set org.gnome.desktop.background picture-uri "file://%s"' \
                    % self.config['wallpaper'])

