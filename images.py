import random

import Image

# Used in MakeWallpaper Thread by way of ImageThread
class ImageQueue:
    def __init__(self, images=[], index=-1, verbose=False):
        # Set index to 0 for no shuffle first
        self.images = images
        self.index = index
        self.verbose = verbose

    def pop(self, count=1):
        """ Pops images off the list, returns list of filenames """

        # Shuffle before pop
        if self.index == -1:
            self.shuffle()

        # Yield images
        for i in range(count):
            if self.verbose:
                print 'pop %d ' % self.index

            image = None
            if self.index < len(self.images):
                image = self.images[self.index]
            else:
                image = self.images[self.index % len(self.images)]

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
            return Image.open(image)
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

        return False

    def shuffle(self):
        """ Shuffles the image list """
        if self.verbose:
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
