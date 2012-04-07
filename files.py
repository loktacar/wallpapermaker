import os
import Image
import random

from config import *

def check_extension(fname):
    for extension in extensions:
        try:
            if fname.index(extension):
                return True
        except:
            pass

    return False


def callback(arg, dirname, fnames):
    # Check where fname element ends with an element in extensions list
    filtered_filenames = [i for i in fnames if check_extension(i)]
    for f in filtered_filenames:
        wallpapers.append('%s/%s' % (dirname, f))

gotten_images = []
def get_images(count):
    for i in range(count):
        f = wallpapers[random.randint(0,len(wallpapers)-1)]
        if len(wallpapers)-len(gotten_images) > count:
            while f in gotten_images:
                f = wallpapers[random.randint(0,len(wallpapers)-1)]

        gotten_images.append(f)
        yield Image.open(f)

wallpapers = []
# Populate filenames
arglist = []
os.path.walk(path, callback, arglist)
