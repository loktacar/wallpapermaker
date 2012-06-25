import os
import logging

from wallpaper_queue import WallpaperQueue

class Wallpapers:
    """ Handles the wallpaper queues, reads folder contents and fills the queues """

    def __init__(self, config):
        self.config = config

        self.queues = [WallpaperQueue(config)]

        self.logger = logging.getLogger('root')

    def pop(self, count=1):
        return [wp for wp in self.queues[0].pop(count)]

    def find_wallpapers(self):
        os.path.walk(self.config['path'], self._folder_visit, [])

        self.logger.debug('%d image in queue' % self.count())

    def _folder_visit(self, arg, dirpath, filenames):
        wallpaper_paths = [os.path.join(dirpath, filename) for filename in filenames]
        pushed_count = self.queues[0].push(wallpaper_paths)

        if pushed_count:
            rel_dirpath = dirpath[len(self.config['path']):]
            self.logger.debug('%d wps pushed from %s' % (pushed_count, rel_dirpath if rel_dirpath else '\\'))

    def count(self):
        return sum([q.count() for q in self.queues])

    def shuffle_if_needed(self):
        for q in self.queues:
            q.shuffle_if_needed()
