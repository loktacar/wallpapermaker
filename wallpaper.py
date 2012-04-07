import os
import random
import time

import Image

from config import update_period
from files import get_images, can_get_images
from resolution import get_ratio, get_screen_resolution
from threads import StoppableThread

def resize(img, size):
    # resize image to fit height, width, or both
    width_ratio = 1.0*size[0]/img.size[0]
    height_ratio = 1.0*size[1]/img.size[1]
    if width_ratio > height_ratio:
        new_size = (size[0], int(img.size[1]*width_ratio))
    else:
        new_size = (int(img.size[0]*height_ratio), size[1])

    img = img.resize(new_size, Image.ANTIALIAS)

    # Either width or height might be too large, LET'S CROP!
    box = (0,0,0,0)
    if img.size[0] != size[0]:
        overflow = img.size[0] - size[0]
        margin = overflow / 2
        box = (margin, 0, margin+size[0], size[1])
    if img.size[1] != size[1]:
        overflow = img.size[1] - size[1]
        margin = overflow / 2
        box = (0, margin, size[0], margin+size[1])

    if max(*box) > 0:
        img = img.crop(box)

    return img

def wallpaper_split(size, iteration=0):
    aspect_ratio = get_ratio(*size)
    images = get_images(4)

    wp = Image.new('RGB', size, (0,0,0))

    new_size = (size[0]/2, size[1]/2)
    placement = ((0,0,1,1), (1,0,2,1), (0,1,1,2), (1,1,2,2))
    for i, img in enumerate(images):
        if iteration < 4 and random.randint(0,4-iteration) == 0:
            img = wallpaper_split(size, iteration+1)
        img = resize(img, new_size)
        pos = [new_size[j%2]*placement[i][j] for j in range(4)]
        wp.paste(img, pos)

    return wp

def make_wallpaper(size, filename='~/wp.png'):
    filename = os.path.expanduser(filename)
    img = wallpaper_split(size)
    img.save(filename, 'PNG', quality=100)

def set_wallpaper(filename='~/wp.png'):
    # TODO: Make platform independant
    filename = os.path.expanduser(filename)
    os.system("gsettings set org.gnome.desktop.background picture-uri \"file://%s\"" % filename)

resolution = ()

# Make wallpapers periodically
class MakeWallpapers(StoppableThread):
    def run(self):
        resolution = get_screen_resolution()
        while not self._stop and len(resolution) > 0 and can_get_images():
            print 'Make wallpaper'
            resolution = get_screen_resolution()
            make_wallpaper(resolution)
            set_wallpaper()
            print 'Sleep'
            time.sleep(update_period)
