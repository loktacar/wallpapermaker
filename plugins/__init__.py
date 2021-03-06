import os
import inspect
import logging

from plugin import Plugin

# Base plugin classes need to be imported so that Plugin.__subclasses__() returns correct results
from collage import Collage
from get_resolution import GetResolution
from set_wallpaper import SetWallpaper
from option import Option
from ui import UI
from source import Source
from keep import Keep

class PluginManager:
    """
        Stores all plugins for each base plugin

    """

    def __init__(self):
        logging.debug('Plugin manager initializing')

        # This will be set later, unable to activate plugins untill set
        self.config = None

        self.plugins = {}
        self.plugin_bases = {}
        for plugin_base in Plugin.__subclasses__():
            plugin_name = plugin_base.__name__
            self.plugin_bases[plugin_name] = plugin_base
            self.plugins[plugin_name] = []

        logging.debug('Searching for plugins')

        plugins_found = self.find_plugins(Plugin.__subclasses__())

        for i, plugin_base in enumerate(Plugin.__subclasses__()):
            plugin_type = plugin_base.__name__

            for plugin in plugins_found[i]:
                self.plugins[plugin_type].append(plugin)

        # list of active plugins
        self.active = {}
        for key in self.plugins:
            self.active[key] = []
        # implemented like this, instead of
        # self.active = self.plugins,
        # to circumvent problems with setting
        # self.active[key] would override self.plugins[key]

    def __getitem__(self, key):
        if len(self.active[key]):
            return self.active[key]
        else:
            return self.plugins[key]

    def plugin_hook(self, hook_name, *args, **kwargs):
        calls = 0

        # Go through each plugin type
        for plugin_type in self.plugin_bases:
            # Find each active plugin of type plugin_type
            for plugin in self.active[plugin_type]:
                # Check if plugin has a hook_name method
                if hasattr(plugin, hook_name):
                    # Call that method with *args and **kwargs arguments
                    getattr(plugin, hook_name)(*args, **kwargs)
                    calls += 1

        if calls:
            calls_str = ' in %s plugins' % calls
            logging.debug('Plugin hook %s called%s.' % (hook_name, calls_str if calls > 1 else ''))
        else:
            logging.debug('Plugin hook %s not found in any plugins.' % hook_name)

    def activate_plugins(self, config, base_plugin_type=None):
        logging.debug('Activating plugins.')

        if config:
            self.config = config
        elif not self.config: # if there is no configuration
            raise RuntimeError("No plugins can be activated before configuration is set.")

        for plugin_type in self.plugin_bases:
            if base_plugin_type and not plugin_type == base_plugin_type:
                continue

            if len(self.active[plugin_type]):
                continue

            plugin_type_class = self.plugin_bases[plugin_type]
            plugins = self.plugins[plugin_type]

            if 'get_instances' not in plugin_type_class.__dict__:
                continue

            instances = plugin_type_class.get_instances(plugins, self.config)

            if type(instances) is not list:
                instances = [instances]

            while instances:
                try:
                    instances.remove(None)
                except ValueError:
                    break

            self.active[plugin_type] += instances
            logging.debug("%d instances of plugin type %s activated" % (len(instances), plugin_type))

    def activate_plugin(self, plugin_type, plugin_name, config=None):
        # plugin_type and plugin_name are strings

        if config:
            self.config = config
        elif not self.config: # if there is no configuration
            raise RuntimeError("No plugins can be activated before configuration is set.")

        if plugin_type not in self.plugin_bases:
            raise ValueError("Plugin type %s not found." % plugin_type)

        # Find the plugin class
        plugin = None
        for p in self.plugins[plugin_type]:
            if p.__name__ == plugin_name:
                plugin = p

        if not plugin:
            raise ValueError("Plugin %s of type %s not found." % (plugin_name, plugin_type))

        # Get instance of plugin
        instance = plugin(self.config)

        # Make sure it's a list of instances
        if not instance is type(list):
            instance = [instance]

        # Activate the plugin... nothing stands in your way!
        self.active[plugin_type] += instance
        logging.debug("%d instances of %s plugin of type %s activated" % (len(instance), plugin_name, plugin_type))

        return True

    def deactivate_plugin(self, plugin_instance=None, plugin_type=None, plugin_name=None):
        # Check if arguments are correct
        if plugin_instance is None and (plugin_type is None or plugin_name is None):
            raise ValueError("Either plugin_instance, or both plugin_type and plugin_name must be set")

        # Remove specific instance
        if plugin_instance:
            plugin_name = plugin_instance.__class__.__name__
            plugin_type = plugin_instance.__class__.__bases__[0].__name__

            try:
                self.active[plugin_type].remove(plugin_instance)
            except ValueError:
                logging.debug("The instance of %s plugin of type %s not found." % (plugin_name, plugin_type))
                return False

            return True
        # Remove all instances of plugin
        else:
            plugin_instances = []
            for prospect in self.active[plugin_type]:
                if prospect.__class__.__name__ == plugin_name:
                    plugin_instances.append(prospect)

            if not plugin_instances:
                logging.debug("No instances of %s plugin of type %s active." % (plugin_name, plugin_type))
                return False

            for instance in plugin_instances:
                self.active[plugin_type].remove(instance)

            logging.debug("All %d instances of %s plugin of type %s deactivated." % (len(plugin_instances), plugin_name, plugin_type))
            return True

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
                if name.endswith(".py") and \
                        not (name.startswith("__") or name.startswith(".")):
                    curr_path = os.path.join(root, name).replace(root_dir, '')
                    modulename = curr_path.rsplit('.', 1)[0]\
                            .replace('/', '.')\
                            .replace('\\', '.')

                    # This is a python module, import it
                    try:
                        module = __import__(modulename, level=-1, fromlist=['*'])
                    except Exception, e:
                        logging.exception('plugin failed - {}'.format(modulename))
                        pass

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
