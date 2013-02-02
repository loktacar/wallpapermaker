from .. import Option

class RecursionDepthOption(Option):
    default = 3
    option = 'recursion-depth'
    cmd_argument = 'INT'
    description = 'Each split can be split INT times'

    @staticmethod
    def parse(value):
        return int(value)

