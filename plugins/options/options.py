import os

from .. import Option

class UpdatePeriodOption(Option):
    default = 300
    option = 'update'
    cmd_argument = 'SEC'
    description = 'SEC seconds between generating and updating wallpaper'

    @staticmethod
    def parse(value):
        return int(value)

class OutputOption(Option):
    default = os.path.expanduser('~%s.wp.bmp' % os.sep)
    option = 'wallpaper'
    cmd_argument = 'PATH'
    description = 'PATH to generated wallpaper'

    @staticmethod
    def parse(value):
        return os.path.expanduser(value)

class SingleRunOption(Option):
    default=False
    option = 'single-run'
    cmd_short = 's',
    description = 'Generate wallpaper once then exit'

    @staticmethod
    def parse(value):
        return bool(value)

class ResolutionOption(Option):
    default = [(0,0)]
    option = 'resolution'
    cmd_short = 'r'
    cmd_argument = 'RES'
    description = 'Forces resolution of generated wallpaper'

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

class UIOption(Option):
    default = 'auto'
    option = 'ui'
    cmd_argument = 'UI'
    description = 'Select which plugin, UI, should be used for ui purposes'

class KeepOption(Option):
    default = False
    option = 'keep'
    cmd_argument = 'INT'
    description = 'Keep INT files instead of replacing one file'

    @staticmethod
    def parse(value):
        return int(value)
