import os
import random
import time

import Image

from config import path, extensions, file_update_period
from threads import StoppableThread

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
        fullpath = '%s/%s' % (dirname, f)
        if not fullpath in wallpapers:
            wallpapers.append(fullpath)

gotten_images = []
def get_images(count):
    for i in range(count):
        f = wallpapers[random.randint(0,len(wallpapers)-1)]
        if len(wallpapers)-len(gotten_images) > count:
            while f in gotten_images:
                f = wallpapers[random.randint(0,len(wallpapers)-1)]

        gotten_images.append(f)
        yield Image.open(f)

def can_get_images():
    return len(wallpapers) > 0

# Maintain Images
class ImageThread(StoppableThread):
    def run(self):
        while not self._stop:
            print 'Updating file list'
            os.path.walk(path, callback, [])
            time.sleep(file_update_period)

wallpapers = []
# Populate filenames
#arglist = []
#os.path.walk(path, callback, arglist)
