import os
import inspect
import logging

from plugin import Plugin
from collage import Collage
from get_resolution import GetResolution
from set_wallpaper import SetWallpaper
from option import Option
from ui import UI
from source import Source

base_plugin_classes = [
        Collage,
        GetResolution,
        SetWallpaper,
        Option,
        UI,
        Source
    ]

class PluginManager:
    """
        Stores all plugins for each superclass

    """

    def __init__(self):
        logging.debug('Plugin manager initializing')

        self.plugins = {}
        for plugin_base in base_plugin_classes:
            plugin_type = plugin_base.__name__
            self.plugins[plugin_type] = []

        logging.debug('Searching for plugins')

        plugins_found = self.find_plugins(base_plugin_classes)

        for i, plugin_base in enumerate(base_plugin_classes):
            plugin_type = plugin_base.__name__

            for plugin in plugins_found[i]:
                # I will create multiple instances of the Source plugins
                if plugin_type == 'Source':
                    self.plugins[plugin_type].append(plugin)
                else:
                    self.plugins[plugin_type].append(plugin())

        # list of active plugins
        self.active = {}
        for key in self.plugins:
            self.active[key] = self.plugins[key]
        # implemented like this, instead of
        # self.active = self.plugins,
        # to circumvent problems with setting
        # self.active[key] would override self.plugins[key]

    def __getitem__(self, key):
        return self.active[key]

    def set_config(self, config):
        # Set the configuration
        for plu_type in self.plugins:
            plugins = self.plugins[plu_type]
            for p in plugins:
                if issubclass(p.__class__, Plugin):
                    p.set_config(config)

        # Activate the plugins selected in config

        # Collage plugins
        if not config['collage-plugins'] == 'all':
            collages = config['collage-plugins'].lower().split(',')
            self.active['Collage'] = []

            for p in self.plugins['Collage']:
                if p.name in collages:
                    self.active['Collage'].append(p)

            if not len(self.active['Collage']):
                raise ValueError('No collage plugins found.')

        # Source plugins
        sources = config['sources'].split(',')
        self.active['Source'] = []

        for s in sources:
            for c in self.plugins['Source']:
                if c.handles_path(s):
                    self.active['Source'].append(c(s))

    def toggle_collage(self, collage_name, activate=True):
        # Find the collage
        collage = None
        for c in self.plugins['Collage']:
            if c.name == collage_name:
                collage = c

        if not collage:
            raise ValueError("Collage, named '%s', not found" % collage_name)

        # Check if (de)activation is redundant
        if activate and collage in self.active['Collage']:
            logging.debug('Failed to activate %s, %s is active' % (collage_name, collage_name))
            return False
        if not activate and not collage in self.active['Collage']:
            logging.debug('Failed to deactivate %s, %s is inactive' % (collage_name, collage_name))
            return False

        # (De)activate
        if activate:
            self.active['Collage'].append(collage)
            logging.debug('Activating %s' % collage_name)
        else:
            self.active['Collage'].remove(collage)
            logging.debug('Deactivating %s' % collage_name)

        # If none of the collages are active, activate all
        if not len(self.active['Collage']):
            logging.debug('No active collages, activating all of them')
            self.active['Collage'] = self.plugins['Collage']
            c_names = [c.name for c in self.active['Collage']]
            activated = {}
            for c in c_names:
                activated[c] = True
            return activated

        return {collage_name: activate}

    def find_plugins(self, base_class):
        """
            finds all classes in path which inherit from base_class
        """

        if type(base_class) is not list:
            base_class = [base_class]

        subclasses = [[] for x in base_class]

        path = os.path.dirname(os.path.realpath(__file__))

        root_dir = path
        if root_dir.rindex(os.sep) == len(root_dir) - 1:
            root_dir = path[:path[:-1].rindex(os.sep) + 1]
        else:
            root_dir = path[:path.rindex(os.sep) + 1]


        # walk through files within path
        for root, dirs, files in os.walk(path):
            # Go through files
            for name in files:
                if name.endswith(".py") and not name.startswith("__"):
                    curr_path = os.path.join(root, name).replace(root_dir, '')
                    modulename = curr_path.rsplit('.', 1)[0]\
                            .replace('/', '.')\
                            .replace('\\', '.')

                    # This is a python module, import it
                    module = __import__(modulename, level=-1, fromlist=['*'])

                    # Go through each item in the list and check if they inherit from the base_classes
                    for key in module.__dict__:
                        possible_class = module.__dict__[key]
                        if inspect.isclass(possible_class):
                            for i, b_class in enumerate(base_class):
                                if issubclass(possible_class, b_class) and \
                                        not possible_class.__name__ == b_class.__name__:
                                    logging.debug('add - %s.%s' % (modulename, possible_class.__name__))
                                    subclasses[i].append(possible_class)

        return subclasses

plugin_manager = PluginManager()
