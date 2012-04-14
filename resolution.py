import sys

def get_screen_resolution():
    # Check if windows, linux or mac
    resolution = (0, 0)

    if sys.platform == 'win32':
        import ctypes
        resolution = (ctypes.windll.user32.GetSystemMetrics(0),
                      ctypes.windll.user32.GetSystemMetrics(1))
    elif sys.platform == 'linux':
        import Xlib
        import Xlib.display
        display = Xlib.display.Display()
        root = display.screen().root
        geom = root.get_geometry()
        resolution = (geom.width, geom.height)

    return resolution

def get_gcd(a, b):
    """ Returns greatest common divisor """
    if b == 0:
        return a
    return get_gcd(b, a % b)

def get_ratio(a, b):
    """ Returns a and b divided by the greatest common divisor """
    gcd = get_gcd(a, b)
    return (a/gcd, b/gcd)
