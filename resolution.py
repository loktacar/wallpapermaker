def get_screen_resolution():
    # TODO: Make platform independant
    import Xlib
    import Xlib.display
    display = Xlib.display.Display()
    root = display.screen().root
    geom = root.get_geometry()
    return (geom.width, geom.height)

def get_gcd(a, b):
    """ Returns greatest common divisor """
    if b == 0:
        return a
    return get_gcd(b, a % b)

def get_ratio(a, b):
    """ Returns a and b divided by the greatest common divisor """
    gcd = get_gcd(a, b)
    return (a/gcd, b/gcd)
