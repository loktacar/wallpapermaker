from .. import Option

class SourceOption(Option):
    default = None
    option = 'source'
    cmd_argument = 'PATH'
    description = 'Folder path of wallpapers'

    @staticmethod
    def parse(value):
        return value

class SourceHiddenOption(Option):
    default = False
    option = 'include_hidden'
    description = 'Include hidden files and folders'

    @staticmethod
    def parse(value):
        return bool(value)
