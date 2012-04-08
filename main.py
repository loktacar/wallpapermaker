#!/usr/bin/env python
import time

from files import ImageThread
from wallpaper import MakeWallpapers

# TODO:
#   - make each split occupy a seperate folder
#   - Randomize the file list and make it a queue, pop images as needed and push them again.
#     Randomize order upon completing a wallpaper and completing the queue.
#   - Change files.py name to images.py
#   - Multiple threads for resize and make_split functions so that it can be done on multiple cores?

image_thread = ImageThread()
update_thread = MakeWallpapers(image_thread)

def start_threads():
    image_thread.start()
    update_thread.start()

def kill_threads():
    image_thread.stop()
    update_thread.stop()

if __name__ == '__main__':
    try:
        start_threads()
        while (True):
            time.sleep(10)
    except (KeyboardInterrupt, SystemExit):
        kill_threads()
