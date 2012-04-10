import os
import random
import time

import Image

from config import path, extensions, file_update_period
from threads import StoppableThread

# Used in MakeWallpaper Thread by way of ImageThread
class ImageQueue:
    def __init__(self, images=[], index=0):
        self.images = images
        self.index = index

    def pop(self, count=1):
        for i in range(count):
            print 'pop %d ' % self.index

            image = None
            if self.index < len(self.images):
                image = self.images[self.index]
            else:
                image = self.images[self.index % len(self.images)]

            self.index += 1

            yield image

        if self.index >= len(self.images):
            self.shuffle()

    def pop_image(self, count=1):
        for i in self.pop(count):
            yield Image.open(i)

    def push(self, image):
        if not image in self.images:
            self.images.append(image)

    def shuffle(self):
        random.shuffle(self.images)
        self.index = 0

# Maintain Image Queue, use in MakeWallpapers Thread
class ImageThread(StoppableThread):
    def __init__(self):
        super(ImageThread, self).__init__()
        self.wallpapers = ImageQueue()
        self._can_get_images = False

    def run(self):
        while not self._stop:
            print 'Updating file list'
            self._can_get_images = False
            os.path.walk(path, self.callback, [])
            self.wallpapers.shuffle()
            self._can_get_images = True

            time.sleep(file_update_period)

    def callback(self, arg, dirname, fnames):
        # Check where fname element ends with an element in extensions list
        filtered_filenames = [i for i in fnames if self.check_extension(i)]
        for f in filtered_filenames:
            self.wallpapers.push('%s/%s' % (dirname, f))

    def get_image(self):
        return self.wallpapers.pop_image().next() if self._can_get_images else None

    def get_images(self, count):
        return self.wallpapers.pop_image(count) if self._can_get_images else None

    def check_extension(self, fname):
        for extension in extensions:
            try:
                if fname.index(extension):
                    return True
            except:
                pass

        return False

    def can_get_images(self):
        return self._can_get_images

