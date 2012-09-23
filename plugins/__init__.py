import os
import inspect
import logging

from plugin import Plugin
from collage import Collage
from get_resolution import GetResolution
from set_wallpaper import SetWallpaper
from option import Option
from ui import UI

base_plugin_classes = [
        Collage,
        GetResolution,
        SetWallpaper,
        Option,
        UI
    ]

class PluginManager:
    """
        Stores all plugins for each superclass

    """

    def __init__(self):
        self.logger = logging.getLogger('root')
        self.logger.debug('Plugin manager initializing')

        self.plugins = {}
        for plugin_base in base_plugin_classes:
            plugin_type = plugin_base.__name__
            self.plugins[plugin_type] = []

        self.logger.debug('Searching for plugins')
        plugins_found = self.find_plugins('plugins/', base_plugin_classes)

        for i, plugin_base in enumerate(base_plugin_classes):
            plugin_type = plugin_base.__name__

            for plugin in plugins_found[i]:
                self.plugins[plugin_type].append(plugin())

    def __getitem__(self, key):
        return self.plugins[key]

    def set_config(self, config):
        for plu_type in self.plugins:
            plugins = self.plugins[plu_type]
            for p in plugins:
                if issubclass(p.__class__, Plugin):
                    p.set_config(config)

    def find_plugins(self, path, base_class):
        """
            finds all classes in path which inherit from base_class
        """

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
                                    self.logger.debug('add - %s.%s' % (modulename, possible_class.__name__))
                                    subclasses[i].append(possible_class)

        return subclasses

plugin_manager = PluginManager()
