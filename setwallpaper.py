import sys
import os
import subprocess

DARWIN_SCRIPT = """/usr/bin/osascript << END
tell application "Finder"
set desktop picture to POSIX file "%s"
end tell
END
"""

def set_wallpaper(filename, desktop_environment):
    # Check if windows, linux or mac
    if sys.platform == 'win32':
        set_win32_wallpaper(filename)
    elif sys.platform == 'linux2':
        if desktop_environment == 'gnome':
            set_gnome_wallpaper(filename)
    elif sys.platform == 'darwin':
        subprocess.Popen(DARWIN_SCRIPT%filename, shell=True)
    else:
        raise NotImplementedError("Unrecognized platform: "+sys.platform)

def set_win32_wallpaper(filename):
    import ctypes

    ctypes.windll.user32.SystemParametersInfoA(20, 0, filename, 0)

def set_gnome_wallpaper(filename):
        os.system(\
                "gsettings set org.gnome.desktop.background picture-uri \"file://%s\"" \
                    % filename)

