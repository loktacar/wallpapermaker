#!/usr/bin/env python
import time

from files import ImageThread
from wallpaper import MakeWallpapers

update_thread = MakeWallpapers()
file_update_thread = ImageThread()

def start_threads():
    file_update_thread.start()
    update_thread.start()

def kill_threads():
    file_update_thread.stop()
    update_thread.stop()

if __name__ == '__main__':
    try:
        start_threads()
        while (True):
            time.sleep(10)
    except (KeyboardInterrupt, SystemExit):
        kill_threads()
