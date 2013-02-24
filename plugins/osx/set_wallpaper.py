import logging
import os
import sys

from .. import SetWallpaper

DARWIN_SCRIPT = """/usr/bin/osascript << END
tell application "Finder"
set desktop picture to POSIX file "%s"
end tell
END
"""

class DarwinSetWallpaper(SetWallpaper):
    def __init__(self, config):
        super(DarwinSetWallpaper, self).__init__(config)
        self.config = config

    def platform_check(self):
        return sys.platform == 'darwin' and self.config['set-wallpaper'] == 'auto'

    def set(self):
        import subprocess
        wallpaper_path = os.path.abspath(self.config['wallpaper'])
        subprocess.Popen(DARWIN_SCRIPT % wallpaper_path, shell=True)
        if not self.config['keep']:
            logging.warning("DarwinSetWallpaper works better if you configure "
                            "the Keep plugin (e.g. --keep=2)")
