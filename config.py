"""Usage %s [options]

Options:
    --section=SECTION           section of config file to be used
    --path=PATH                 path of wallpaper folder
    --extensions=LIST           comma seperated list of acceptable extensions
    --update=TIME               time seperating each wallpaper update in seconds
    --generated-wallpaper=PATH  path of the output wallpaper
    --resolution=WIDTHxHEIGHT   sets a static value for resolution, instead of automatic
    --recursion-depth=INT       maximum number of times each split can be split
    -s --single-run             create and set a single wallpaper then exit
    -h --help                   shows this help message and exits
    -v --verbose                prints status messages as the program runs

Configuration Files:
    %s
    %s

    See sample.config for information on options and examples

"""
# Add no-set option which doesn't set wallpaper only generates and saves it

import copy
import imp
import sys
import os

import ConfigParser

from appdirs import AppDirs

appname = 'wpmaker'
appauthor = 'viktor'
config_file_name = '%s.conf' % appname

# Determine whether script is .py or .exe
def main_is_frozen():
    return (hasattr(sys, "frozen") or    # new py2exe
            hasattr(sys, "importers") or # old py2exe
            imp.is_frozen("__main__"))   # tools/freeze

def get_doc():
    # TODO:
    #   Make __doc__ string from a dict describing each option
    appdirs = AppDirs(appname, appauthor)
    dir_splitter = '/'
    if '\\' in appdirs.user_data_dir:
        dir_splitter = '\\'

    return __doc__ % ('wpmaker.exe' if main_is_frozen() else 'wpmaker.py',
                      appdirs.user_data_dir + dir_splitter + config_file_name,
                      appdirs.site_data_dir + dir_splitter + config_file_name)

class ConfigOption:
    def __init__(self,
            default=None,
            required=False,
            parse_func=None,
            cmd_opt=False,
            cmd_short=False,
            cmd_arg=False,
            cmd_console=True,
            cmd_gui=True,
            config_file=True,
            description=''):
        self.default = default
        self.required = required
        self.parse_func = parse_func
        self.cmd_opt = cmd_opt
        self.cmd_short = cmd_short
        self.cmd_arg = cmd_arg
        self.cmd_console = cmd_console
        self.cmd_gui = cmd_gui
        self.config_file = config_file
        self.description = description

    def get(self, value):
        if not value:
            return False

        if not self.parse_func is None:
            return self.parse_func(value)
        else:
            return value

def resolution_parse(value):
    res = value.split('x')
    if type(res) == str:
        res = value.split('X')

    return [int(i) for i in res]

class Config:
    OPTIONS = {
            'path': ConfigOption(default=None, required=True, cmd_opt='path', cmd_short='p', cmd_arg='PATH',
                                 parse_func=os.path.expanduser,
                                 description='path to wallpaper folder'),

            'extensions': ConfigOption(default=['jpg','png','jpeg','gif','bmp'],
                                       parse_func=lambda x: x.split(','),
                                       cmd_opt='extensions', cmd_arg='LIST',
                                       description='comma seperated list of acceptable extensions'),

            'update_period': ConfigOption(default=300, cmd_opt='update', cmd_short='u', cmd_arg='SEC',
                                          parse_func=int,
                                          description='time between generating and updating wallpaper'),

            'generated_wallpaper': ConfigOption(default=os.path.expanduser('~/.wp.bmp'),
                                                parse_func=os.path.expanduser,
                                                cmd_opt='wallpaper', cmd_short='w', cmd_arg='PATH',
                                                description='path to generated wallpaper'),

            'recursion_depth': ConfigOption(default=2, cmd_opt='recursion-depth', cmd_arg='INT',
                                            parse_func=int,
                                            description='maximum number of times each split can be split'),

            'single_run': ConfigOption(default=False, cmd_opt='single-run', cmd_short='s',
                                       parse_func=bool,
                                       description='create and set a single wallpaper then exit'),

            'verbose': ConfigOption(default=False, cmd_opt='verbose', cmd_short='v',
                                    parse_func=bool,
                                    description='prints out debugging information as it runs'),

            'desktop_environment': ConfigOption(default='gnome', cmd_console=False, cmd_gui=False, config_file=False),

            'resolution': ConfigOption(default=None, cmd_opt='resolution', cmd_short='r', cmd_arg='RES',
                                       parse_func=resolution_parse,
                                       description='forces resolution of generated wallpaper'),

            'file_check_interval': ConfigOption(default=5, cmd_opt='fs-interval', cmd_arg='INT',
                                                parse_func=int,
                                                description='check wallpaper folder every INT updated'),

            'config_section': ConfigOption(default='default', cmd_opt='section', cmd_arg='SECTION',
                                           config_file=False, description='section of configuration file to be used')
}


    def __init__(self, cmd_opts):
        self.cmd_opts = cmd_opts
        self.options = {}
        self.cfg = ConfigParser.SafeConfigParser()

        # Find out the full path to configuration files
        appdirs = AppDirs(appname, appauthor)
        dirs = (appdirs.user_data_dir, appdirs.site_data_dir)
        self.files = ['%s/%s' % (dir, config_file_name) for dir in dirs]

        self.cfg = ConfigParser.SafeConfigParser()
        self.cfg_files = self.cfg.read(self.files)

        # Get config file section from command line options
        self.file_section = \
            self.cmd_opts.section \
            if self.cmd_opts.section \
            else Config.OPTIONS['config_section'].default

        self.set_defaults()
        self.parse_options()

        # Check if required options are set
        for key in Config.OPTIONS.keys():
            opt = Config.OPTIONS[key]

            if self.options[key] is None and opt.required:
                raise ValueError("Config setting '%s' not set" % key)

    def parse_options(self):
        """ Read and parse options from configuration file and command line """

        # read config file options
        cfg = ConfigParser.SafeConfigParser()
        read_files = cfg.read(self.files) # read in past tense

        if len(read_files):
            if not cfg.has_section(self.file_section):
                raise ValueError('Section %s not found' % self.file_section)

            config_dict = {}
            for key in Config.OPTIONS.keys():
                if cfg.has_option(self.file_section, key):
                    config_dict[key] = cfg.get(self.file_section, key)

            self.parse_dict(config_dict, 'file')

        # read command line options
        cmd_dict = {}
        for key in Config.OPTIONS.keys():
            opt = Config.OPTIONS[key]

            if opt.cmd_opt:
                cmd_opt_ = opt.cmd_opt.replace('-','_')
                if cmd_opt_ in self.cmd_opts.__dict__.keys():
                    if self.cmd_opts.__dict__[cmd_opt_]:
                        cmd_dict[key] = self.cmd_opts.__dict__[cmd_opt_]

        self.parse_dict(cmd_dict, 'cmd')

    def set_defaults(self):
        """ Set all options to default values """
        for key in Config.OPTIONS.keys():
            opt = Config.OPTIONS[key]
            self[key] = opt.default

    def parse_dict(self, dict, dict_source=''):
        """ Set all options in dict.keys() to the values in dict[key] """

        for key in Config.OPTIONS.keys():
            opt = Config.OPTIONS[key]

            # if config option is not applicable and option is from file, continue on to the next option
            #   or config option is not applicable and option is from command line, continue
            if not opt.config_file and dict_source == 'file' or \
                    not self.cmd_opts and dict_source == 'cmd':
                continue

            # set appropriate option to the appropriate value
            if key in dict:
                self.__setitem__(key, dict[key])
            elif opt.cmd_opt in dict:
                self.__setitem__(key, dict[opt.cmd_opt])

    def read_config_files(self, parse=True):
        self.cfg = ConfigParser.SafeConfigParser()
        self.cfg_files = self.cfg.read(self.files)

        if parse:
            self._parse_config_files()

    def config_sections(self):
        return self.cfg.sections()

    def set_section(self, section):
        self.set_defaults()
        self.file_section = section
        self.parse_options()

    def __setitem__(self, key, value):
        if not key in Config.OPTIONS:
            raise ValueError('Config.__setitem__(): key %s not found' % key)

        if isinstance(value, str):
            opt = Config.OPTIONS[key]
            self.options[key] = opt.get(value)
        else:
            self.options[key] = value

    def __getitem__(self, key):
        return self.options[key]

    def get_option_list(self):
        for key in Config.OPTIONS:
            if key == 'config_section':
                continue

            opt = Config.OPTIONS[key]

            if self[key] == opt.default:
                continue

            if opt.cmd_opt and not opt.cmd_arg:
                yield '--%s' % opt.cmd_opt
            if opt.cmd_opt and opt.cmd_arg:
                yield '--%s=%s' % (opt.cmd_opt, self[key])

