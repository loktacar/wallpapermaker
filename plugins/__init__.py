import os
import inspect
import logging

def find_plugins(path, base_class):
    """
        finds all classes in path which inherit from base_class
    """

    logger = logging.getLogger('root')

    if type(base_class) is not list:
        base_class = [base_class]

    subclasses = [[] for x in base_class]

    # walk through files within path
    for root, dirs, files in os.walk(path):
        for name in files:
            if name.endswith(".py") and not name.startswith("__"):
                path = os.path.join(root, name)
                modulename = path.rsplit('.', 1)[0].replace('/', '.').replace('\\', '.')

                module = __import__(modulename, level=-1, fromlist=['*'])

                for key in module.__dict__:
                    possible_class = module.__dict__[key]
                    if inspect.isclass(possible_class):
                        for i, b_class in enumerate(base_class):
                            if issubclass(possible_class, b_class) and \
                                    not possible_class.__name__ == b_class.__name__:
                                logger.debug('add - %s.%s' % (modulename, possible_class.__name__))
                                subclasses[i].append(possible_class)

    return subclasses

from collage import Collage
from get_resolution import GetResolution
from set_wallpaper import SetWallpaper
from option import Option
from ui import UI

collage_plugins, get_resolution_plugins, set_wallpaper_plugins, option_plugins, ui_plugins = find_plugins('plugins/', [Collage, GetResolution, SetWallpaper, Option, UI])
