# Set wallpaper code, get resolution is below

def set_win32_wallpaper(filename):
    import ctypes

    ctypes.windll.user32.SystemParametersInfoA(20, 0, filename, 0)

def set_gnome_wallpaper(filename):
    import os

    os.system(\
                "gsettings set org.gnome.desktop.background picture-uri \"file://%s\"" \
                    % filename)

def set_darwin_wallpaper(filename):
    import subprocess
    DARWIN_SCRIPT = """/usr/bin/osascript << END
tell application "Finder"
set desktop picture to POSIX file "%s"
end tell
END
"""

    subprocess.Popen(DARWIN_SCRIPT % filename, shell=True)

# Keys are matched against sys.platform and when applicable sys.platform/desktop_environment
set_wallpaper_dict = {'win32': set_win32_wallpaper, # Windows platform
                      'linux2/gnome': set_gnome_wallpaper,
                      'darwin': set_darwin_wallpaper } # Mac platform

# Get resolution code

def get_win32_resolution():
    import ctypes

    return (ctypes.windll.user32.GetSystemMetrics(0),
                  ctypes.windll.user32.GetSystemMetrics(1))

def get_xlib_resolution():
    import Xlib
    import Xlib.display

    display = Xlib.display.Display()
    root = display.screen().root
    geom = root.get_geometry()
    return (geom.width, geom.height)

def get_darwin_resolution():
    from AppKit import NSScreen
    fram = NSSceen.mainScreen().frame()
    return (int(fram.size.width), int(frame.size.height))

# Keys are matched against sys.platform
get_resolution_dict = {'win32': get_win32_resolution,
                       'linux2': get_xlib_resolution, # Linux platform w/ xlib
                       'darwin': get_darwin_resolution } # Mac platform

# Do not alter below code when adding support, dict keys will be matched again sys.platform and then desktop_environment setting
import sys

def set_wallpaper(filename, desktop_environment):
    return call_dict_function(set_wallpaper_dict, desktop_environment, filename)

def get_screen_resolution():
    return call_dict_function(get_resolution_dict, '')

def call_dict_function(dict, support, *args, **kwargs):
    for pf in dict.keys():
        if '/' in pf and len(support):
            if '%s/%s' % (sys.platform, support) == pf:
                return dict[pf](*args, **kwargs)
        else:
            if sys.platform == pf:
                return dict[pf](*args, **kwargs)

    raise NotImplementedError("Unrecognized platform: " + sys.platform)
