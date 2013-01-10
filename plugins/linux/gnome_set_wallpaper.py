import sys

from .. import SetWallpaper

class GnomeSetWallpaper(SetWallpaper):
    def __init__(self):
        super(GnomeSetWallpaper, self).__init__()

    def platform_check(self):
        return sys.platform == 'linux2' and self.config['linux.desktop-environment'] == 'gnome'

    def set(self):
        import os

        os.system(\
                'gsettings set org.gnome.desktop.background picture-uri "file://%s"' \
                    % self.config['wallpaper'])

