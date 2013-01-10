from .. import Option

class RecursionDepthOption(Option):
    default = 3
    option = 'recursion-depth'
    cmd_argument = 'INT'
    description = 'Each split can be split INT times'
    conf_description = ['# This options is specifically for RecursiveSplit plugin\n',
                             '# recursion_depth: maximum number of times each split can be\n',
                             '#   split\n']

    @staticmethod
    def parse(value):
        return int(value)

