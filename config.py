import os

import ConfigParser

from appdirs import AppDirs

class Config:
    def __init__(self, cmd_opts):
        self.appname = 'wpmaker'
        self.appauthor = 'viktor'
        self.config_file_name = '%s.conf' % self.appname

        self.dirs = AppDirs(self.appname, self.appauthor)

        self.cmd_opts = cmd_opts

        self.required_option_keys = ['path']

        # Options, and also default options
        self.options = {
                'path': None,                                       # Path to wallpaper folder

                'extensions': ['jpg','png','jpeg','gif','bmp'],     # Extensions to search for

                'update_period': 300,                               # Update period, aka time to wait between
                                                                    # setting wp's

                'generated_wallpaper':
                    os.path.expanduser('~/.wp.bmp'),                # Name of generated wallpaper

                'recursion_depth': 3,                               # Recursion depth, ie how deep the splits
                                                                    # should go

                'add_date': False,                                  # Add date and time to generated wallpaper
                                                                    # file name, before last period '.'

                'single_run': False,                                # Run once and die

                'verbose': False,                                   # Print debuggin information

                'desktop_environment': 'gnome',                     # Desktop environment run in linux

                'resolution': None,                                 # Resolution of generated wallpaper

                'file_check_period': 5,                             # How often we should check the files for
                                                                    # updates

                'config_section': 'default'}                        # Section of config file to be used

        self.parse_options()

    def __setitem__(self, key, value):
        if not key in self.options:
            raise ValueError('Config.__setitem__(): key %s not found' % key)

        if key in ['add_date', 'single_run', 'verbose']:
            self.options[key] = bool(value)
        elif key in ['recursion_depth', 'update_period']:
            self.options[key] = int(value)
        elif key in ['path', 'generated_wallpaper']:
            self.options[key] = os.path.expanduser(value)
        elif key in ['extensions']:
            self.options[key] = value.split(',')
        elif key in ['resolution']:
            res = value.split('x')
            if type(res) == str:
                res = value.split('X')

            if type(res) == str:
                value = False
            else:
                try:
                    value = [int(i) for i in res]
                except:
                    value = False

            self.options[key] = value
        else:
            self.options[key] = value

    def __getitem__(self, key):
        return self.options[key]

    def parse_options(self):
        # Get config file section from command line options
        self.options['config_section'] = \
            self.cmd_opts.section \
            if self.cmd_opts.section \
            else self.options['config_section']

        # Read config files
        self._parse_config_files()

        # Read command line options
        self._parse_cmd_options()

        # Check if required options are set, e.x. 'path'
        for key in self.required_option_keys:
            if self.options[key] is None:
                raise ValueError('Required option %s not set' % key)

    def _parse_config_files(self):
        appdirs = AppDirs(self.appname, self.appauthor)
        dirs = (appdirs.user_data_dir, appdirs.site_data_dir)
        files = ['%s/%s' % (dir, self.config_file_name) for dir in dirs]

        cfg = ConfigParser.SafeConfigParser()
        read_files = cfg.read(files)

        section = self.options['config_section']

        if len(read_files):
            if not cfg.has_section(section):
                raise ValueError('Section %s not found' % section)

            for key in self.options.keys():
                if cfg.has_option(section, key):
                    self[key] = cfg.get(section, key)

    def _parse_cmd_options(self):
        #print self.cmd_opts.__dict__
        translation_dict = {'update': 'update_period'}

        # help is irrelevant
        # section has already been parsed
        ignore_keys = ['help', 'section']

        for cmd_key in self.cmd_opts.__dict__.keys():
            if cmd_key in ignore_keys:
                continue

            value = self.cmd_opts.__dict__[cmd_key]
            key = translation_dict[cmd_key] if cmd_key in translation_dict.keys() else cmd_key

            if value:
                self[key] = value
