from .. import Option

class RecursionDepthOption(Option):
    def __init__(self):
        super(RecursionDepthOption, self).__init__()

        default = 3
        self.option = 'recursion-depth'
        self.cmd_argument = 'INT'
        self.description = 'Each split can be split INT times'

    def parse(self, value):
        return int(value)

