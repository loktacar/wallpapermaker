import os

from .. import Option

class PathOption(Option):
    def __init__(self):
        super(PathOption, self).__init__()

        self.default = None
        self.option = 'path'
        self.cmd_argument = 'PATH'
        self.description = 'PATH to the wallpaper folder'
        self.conf_description = ['# path to the wallpaper folder. Not set by default\n',
                                 '#   a tilde, ~, in paths is replaced with user directory path\n']

    def parse(self, value):
        return os.path.expanduser(value)

class UpdatePeriodOption(Option):
    def __init__(self):
        super(UpdatePeriodOption, self).__init__()

        self.default = 300
        self.option = 'update'
        self.cmd_argument = 'SEC'
        self.description = 'SEC seconds between generating and updating wallpaper'
        self.conf_description = ['# time between wallpaper switching\n']

    def parse(self, value):
        return int(value)

class OutputOption(Option):
    def __init__(self):
        super(OutputOption, self).__init__()

        self.default = self.parse('~/.wp.bmp')
        self.option = 'wallpaper'
        self.cmd_argument = 'PATH'
        self.description = 'PATH to generated wallpaper'
        self.conf_description = ['# path and filename of generated wallpaper image\n']
        self.conf_default = '~/.wp.bmp'

    def parse(self, value):
        return os.path.expanduser(value)

class SingleRunOption(Option):
    def __init__(self):
        super(SingleRunOption, self).__init__()

        self.default=False
        self.option = 'single-run'
        self.cmd_short = 's',
        self.description = 'Generate wallpaper once then exit'
        self.conf_description = ['# create and set a single wallpaper then exit\n']

    def parse(self, value):
        return bool(value)

class ResolutionOption(Option):
    def __init__(self):
        super(ResolutionOption, self).__init__()

        self.default = self.parse("0x0")
        self.option = 'resolution'
        self.cmd_short = 'r'
        self.cmd_argument = 'RES'
        self.description = 'Forces resolution of generated wallpaper'
        self.conf_description = ['# forces resolution of generated wallpaper\n',
                                 '# i.e. desktop resolution is not queried, useful if\n',
                                 '#   get_resolution plugins fail\n',
                                 '# e.x. setting:\n',
                                 '#   resolution=1680x1050\n']

    def parse(self, value):
        res = value.split('x')

        if type(res) == str:
            res = value.split('X')

        return tuple([int(i) for i in res])

class FileCheckOption(Option):
    def __init__(self):
        super(FileCheckOption, self).__init__()

        self.default = 5
        self.option = 'fs-interval'
        self.cmd_argument = 'INT'
        self.description = 'Check wallpaper folder every INT updates'
        self.conf_description = ['# how many wallpapers will be generated between checking of\n',
                                 '#   wallpaper folder\n']

    def parse(self, value):
        return int(value)

class ConfigSectionOption(Option):
    def __init__(self):
        super(ConfigSectionOption, self).__init__()

        self.default = 'default'
        self.option = 'section'
        self.cmd_argument = 'SECTION'
        self.description = 'SECTION of configuration file to be used'

class CollageSelectionOption(Option):
    def __init__(self):
        super(CollageSelectionOption, self).__init__()

        self.default = 'all'
        self.option = 'collage-plugin'
        self.cmd_argument = 'COLLAGE'
        self.description = 'Which collage plugin should be used'
        self.conf_description = ['# which collage plugin should be used, acceptable values are:\n',
                                 "#     - 'SimpleResize'\n",
                                 "#     - 'RecursiveSplit'\n",
                                 "#     - 'all', plugin chosen at random\n"]

class VerboseOption(Option):
    def __init__(self):
        super(VerboseOption, self).__init__()

        self.default = 'False'
        self.option = 'verbose'
        self.cmd_short = 'v'
        self.description = 'Debugging output'
        self.conf_description = ['# Debugging info displayed in the command line\n']

class UIOption(Option):
    def __init__(self):
        super(UIOption, self).__init__()

        self.default = 'Console'
        self.option = 'ui'
        self.cmd_argument = 'UI'
        self.description = 'Select which plugin, UI, should be used for ui purposes'
        self.conf_description = ['# Which ui plugin should be used, acceptable values are:\n',
                                 "#     - 'Console'\n",
                                 "#     - 'wxPython'\n"]

