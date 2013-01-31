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
        return sys.platform == 'darwin'

    def set(self):
        import subprocess
        subprocess.Popen(DARWIN_SCRIPT % self.config['wallpaper'], shell=True)

