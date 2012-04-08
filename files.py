import os
import random
import time

import Image

from config import path, extensions, file_update_period
from threads import StoppableThread

# Maintain Images
class ImageThread(StoppableThread):
    def __init__(self):
        super(ImageThread, self).__init__()
        self.wallpapers = []
        self.gotten_images = []

    def run(self):
        while not self._stop:
            print 'Updating file list'
            os.path.walk(path, self.callback, [])
            time.sleep(file_update_period)

    def callback(self, arg, dirname, fnames):
        # Clear gotten images
        del self.gotten_images[:]

        # Check where fname element ends with an element in extensions list
        filtered_filenames = [i for i in fnames if self.check_extension(i)]
        for f in filtered_filenames:
            fullpath = '%s/%s' % (dirname, f)
            if not fullpath in self.wallpapers:
                self.wallpapers.append(fullpath)

    def get_image(self):
        return self.get_images(1).next()

    def get_images(self, count):
        for i in range(count):
            f = self.wallpapers[random.randint(0,len(self.wallpapers)-1)]
            if len(self.wallpapers)-len(self.gotten_images) > count:
                while f in self.gotten_images:
                    f = self.wallpapers[random.randint(0,len(self.wallpapers)-1)]

            self.gotten_images.append(f)
            yield Image.open(f)

    def check_extension(self, fname):
        for extension in extensions:
            try:
                if fname.index(extension):
                    return True
            except:
                pass

        return False

    def can_get_images(self):
        return len(self.wallpapers) > 0

