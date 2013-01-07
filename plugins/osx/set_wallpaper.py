import sys

from .. import SetWallpaper

class DarwinSetWallpaper(SetWallpaper):
    def __init__(self, config):
        super(DarwinSetWallpaper, self).__init__(config)

    def platform_check(self):
        return sys.platform == 'darwin'

    def set(self):
        import subprocess

        DARWIN_SCRIPT = """/usr/bin/osascript << END
tell application "Finder"
set desktop picture to POSIX file "%s"
end tell
END
"""

        subprocess.Popen(DARWIN_SCRIPT % config['wallpaper'], shell=True)

