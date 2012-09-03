import sys

from .. import SetWallpaper

class GnomeSetWallpaper(SetWallpaper):
    @staticmethod
    def platform_check(config):
        return sys.platform == 'linux2' and config['desktop-environment'] == 'gnome'

    @staticmethod
    def set(config):
        import os

        os.system(\
                'gsettings set org.gnome.desktop.background picture-uri "file://%s"' \
                    % config['wallpaper'])

