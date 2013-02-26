import os
import sys

from .. import SetWallpaper

class GnomeSetWallpaper(SetWallpaper):
    def __init__(self, config):
        super(GnomeSetWallpaper, self).__init__(config)

    def platform_check(self):
        return sys.platform == 'linux2' and self.config['set-wallpaper'] == 'gnome3'

    def set(self):
        wallpaper_path = os.path.abspath(self.config['wallpaper'])
        os.system(\
                "gsettings set org.gnome.desktop.background picture-options 'spanned'")
        os.system(\
                'gsettings set org.gnome.desktop.background picture-uri "file://%s"' \
                    % wallpaper_path)

