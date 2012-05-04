import os
import random

import pygame

# Used in MakeWallpaper Thread by way of ImageThread
class ImageQueue:
    def __init__(self, config, images=[], index=-1):
        self.images = images

        # Set index to 0 for no shuffle first
        self.index = index

        self.config = config

    def pop(self, count=1):
        """ Pops images off the list, returns list of filenames """

        # Shuffle before pop
        if self.index == -1:
            self.shuffle()

        # Yield images
        for i in range(count):
            image = None
            if self.index < len(self.images):
                image = self.images[self.index]
            else:
                image = self.images[self.index % len(self.images)]

            if self.config['verbose']:
                print 'pop %d - %s' % (self.index, image)

            self.index += 1

            yield image

    def pop_images(self, count=1):
        """ Pops images off the list, returns list of Image objects """
        for i in self.pop(count):
            yield self.pop_image()

    def pop_image(self):
        """ Pops a single image from list, returns Image object """
        images = self.pop()
        image = images.next()
        try:
            pyimg = pygame.image.load(image)
            if pyimg.get_width() == 0 or pyimg.get_height() == 0:
                raise IOError
            return pyimg
        except IOError:
            print 'Failed to find image %s' % image
            self.images.remove(image)
            return self.pop_image()

    def push(self, images):
        """ Pushes images onto the list, returns number of images pushed (not including duplicates) """

        if not type(images) is list:
            return 1 if self.push_image(images) else 0

        c = 0
        for image in images:
            c += 1 if self.push_image(image) else 0

        return c

    def push_image(self, image):
        """ Pushes a single image to the list, returns true if pushed (doesn't push duplicates) """
        if not image in self.images:
            self.images.append(image)
            return True

    def shuffle(self):
        """ Shuffles the image list """
        if self.config['verbose']:
            print 'Shuffling image-queue'

        random.shuffle(self.images)
        self.index = 0

    def shuffle_check(self):
        """ Shuffles images if neccesary """
        if self.index > len(self.images):
            self.shuffle()

    def count(self):
        """ Returns the number of images in the list """
        return len(self.images)

    def walk_path(self):
        os.path.walk(self.config['path'], self._callback, [])

        if self.config['verbose']:
            print '%d images in queue' % self.count()

    def _callback(self, arg, dirname, fnames):
        """ Gets a list of files from each directory in 'path', including 'path' directory iteself """
        filtered_filenames = ['%s/%s' % (dirname, i) for i in fnames if self._check_extension(i.lower())]
        pushed_count = self.push(filtered_filenames)

        if self.config['verbose'] and pushed_count:
            print 'pushed %d images from %s' % (pushed_count, dirname)

    def _check_extension(self, fname):
        """ Checks if file has extension found in extensions, from configuration """
        for extension in self.config['extensions']:
            try:
                if fname.index(extension) == len(fname) - len(extension):
                    return True
            except:
                pass

