import math
import random
import pygame

from resolution import get_ratio

def resize(img, size):
    """ Resizes image to set size, conserves aspect ration by cropping """

    # resize image to fit height, width, or both
    width_ratio = 1.0*size[0]/img.get_width()
    height_ratio = 1.0*size[1]/img.get_height()
    if width_ratio > height_ratio:
        new_size = (size[0], int(math.ceil(img.get_height()*width_ratio)))
    else:
        new_size = (int(math.ceil(img.get_width()*height_ratio)), size[1])

    # smoothscale
    try:
        img = pygame.transform.smoothscale(img, new_size)
    except ValueError:
        print 'bit-depth error, using crappy scaling'
        img = pygame.transform.scale(img, new_size)

    # Either width or height might be too large, LET'S CROP!
    box = (0,0,0,0)
    if img.get_width() > size[0]+1:# != size[0]:
        overflow = img.get_width() - size[0]
        margin = int(overflow / 2)
        box = (margin, 0, margin+size[0], size[1])
    if img.get_height() > size[1]+1:# != size[1]:
        overflow = img.get_height() - size[1]
        margin = int(overflow / 2)
        box = (0, margin, size[0], margin+size[1])

    if max(*box) > 0:
            img = img.subsurface(box)

    return img

def wallpaper_split(size, get_image, recursion_depth=3, iteration=0):
    """ Splits wallpaper in four with a chance of each piece being recursively generated """

    aspect_ratio = get_ratio(*size)

    wp = pygame.Surface(size)

    new_size = (int(math.ceil(size[0]/2.0)), int(math.ceil(size[1]/2.0)))

    # Constants for the loop
    placement = ((0,0,1,1), (1,0,2,1), (0,1,1,2), (1,1,2,2))
    chances = (4, 4, 4, 8)
    for i in range(4):
        if iteration < recursion_depth and random.randint(0, 4 + iteration*2) == 0:
            img = wallpaper_split(new_size, get_image, iteration=iteration + 1)
        else:
            img = get_image()
            img = resize(img, new_size)

        pos = [new_size[j%2]*placement[i][j] for j in range(4)]

        for x1, x2 in enumerate(range(pos[0], pos[2])):
            for y1, y2 in enumerate(range(pos[1], pos[3])):
                wp.set_at((x2, y2), img.get_at((x1, y1)))


    return wp
