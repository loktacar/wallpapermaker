from .. import Option

class SourceOption(Option):
    default = None
    option = 'source'
    cmd_argument = 'PATH'
    description = 'Folder path of wallpapers'
    conf_description = ['# Path to wallpaper folder. \n',
                        '#   a tilde, ~, in paths is replaced with user directory path\n']

    @staticmethod
    def parse(value):
        return value

