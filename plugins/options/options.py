import os

from .. import Option

class SourceOption(Option):
    default = None
    option = 'sources'
    cmd_argument = 'PATHS'
    description = 'Sources of wallpapers'
    conf_description = ['# Source of wallpapers, can be path or subreddit url. \n',
                             '# See source plugin documentation \n',
                             '#   a tilde, ~, in paths is replaced with user directory path\n']

    @staticmethod
    def parse(value):
        return value

class UpdatePeriodOption(Option):
    default = 300
    option = 'update'
    cmd_argument = 'SEC'
    description = 'SEC seconds between generating and updating wallpaper'
    conf_description = ['# time between wallpaper switching\n']

    @staticmethod
    def parse(value):
        return int(value)

class OutputOption(Option):
    default = os.path.expanduser('~%s.wp.bmp' % os.sep)
    option = 'wallpaper'
    cmd_argument = 'PATH'
    description = 'PATH to generated wallpaper'
    conf_description = ['# path and filename of generated wallpaper image\n']
    conf_default = '~/.wp.bmp'

    @staticmethod
    def parse(value):
        return os.path.expanduser(value)

class SingleRunOption(Option):
    default=False
    option = 'single-run'
    cmd_short = 's',
    description = 'Generate wallpaper once then exit'
    conf_description = ['# create and set a single wallpaper then exit\n']

    @staticmethod
    def parse(value):
        return bool(value)

class ResolutionOption(Option):
    default = [(0,0)]
    option = 'resolution'
    cmd_short = 'r'
    cmd_argument = 'RES'
    description = 'Forces resolution of generated wallpaper'
    conf_description = ['# forces resolution of generated wallpaper\n',
                             '# i.e. desktop resolution is not queried, useful if\n',
                             '#   get_resolution plugins fail\n',
                             '# e.x. setting:\n',
                             '#   resolution=1680x1050\n']

    @staticmethod
    def parse(value):
        res = value.split('x')

        if type(res) == str:
            res = value.split('X')

        return [tuple([int(i) for i in res])]

class CollageSelectionOption(Option):
    default = 'all'
    option = 'collage-plugins'
    cmd_argument = 'COLLAGE'
    description = 'Which collage plugin should be used'
    conf_description = ['# which collage plugin should be used, acceptable values are:\n',
                             "#     - 'simple resize'\n",
                             "#     - 'recursive split'\n",
                             "#     - 'all', plugin chosen at random\n"]

class VerboseOption(Option):
    default = 'False'
    option = 'verbose'
    cmd_short = 'v'
    description = 'Debugging output'
    conf_description = ['# Debugging info displayed in the command line\n']

class UIOption(Option):
    default = 'wxPython'
    option = 'ui'
    cmd_argument = 'UI'
    description = 'Select which plugin, UI, should be used for ui purposes'
    conf_description = ['# Which ui plugin should be used, acceptable values are:\n',
                             "#     - 'Console'\n",
                             "#     - 'wxPython'\n"]

