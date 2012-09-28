from .. import Option

class RecursionDepthOption(Option):
    def __init__(self):
        super(RecursionDepthOption, self).__init__()

        self.default = 3
        self.option = 'recursion-depth'
        self.cmd_argument = 'INT'
        self.description = 'Each split can be split INT times'
        self.conf_description = ['# This options is specifically for RecursiveSplit plugin\n',
                                 '# recursion_depth: maximum number of times each split can be\n',
                                 '#   split\n']

    def parse(self, value):
        return int(value)

