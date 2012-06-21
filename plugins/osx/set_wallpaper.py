import sys

from .. import SetWallpaper

class DarwinSetWallpaper(SetWallpaper):
    @staticmethod
    def platform_check(config):
        return sys.platform == 'darwin'

    @staticmethod
    def set(config):
        import subprocess

        DARWIN_SCRIPT = """/usr/bin/osascript << END
tell application "Finder"
set desktop picture to POSIX file "%s"
end tell
END
"""

        subprocess.Popen(DARWIN_SCRIPT % config['wallpaper'], shell=True)

