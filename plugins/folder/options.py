from .. import Option

class SourceOption(Option):
    default = None
    option = 'source'
    cmd_argument = 'PATH'
    description = 'Folder path of wallpapers'

    @staticmethod
    def parse(value):
        return value

