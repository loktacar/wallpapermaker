import random

import Image

from resolution import get_ratio

def resize(img, size):
    """ Resizes image to set size, conserves aspect ration by cropping """

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

def wallpaper_split(size, get_image, iteration=0):
    """ Splits wallpaper in four with a chance of each piece being recursively generated """

    aspect_ratio = get_ratio(*size)

    wp = Image.new('RGB', size, (0,0,0))

    new_size = (size[0]/2, size[1]/2)

    # Constants for the loop
    placement = ((0,0,1,1), (1,0,2,1), (0,1,1,2), (1,1,2,2))
    chances = (4, 4, 4, 8)
    for i in range(4):
        # Check that the random calculations make sense, i.e. print them out and spekk it
        if iteration < 4 and random.randint(0,chances[iteration]) == 0:
            img = wallpaper_split(size, get_image, iteration+1)
        else:
            img = get_image()
        img = resize(img, new_size)
        pos = [new_size[j%2]*placement[i][j] for j in range(4)]
        wp.paste(img, pos)

    return wp
