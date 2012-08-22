class Option(object):
    """
        Base class for option plugins
    """
    def __init__(self):
        # Default value, if default is None, option is required to be set to something else
        self.default = None

        # Option name
        self.option = None

        # Short command line option
        self.cmd_short = None
        # Command line argument name
        self.cmd_argument = None

        # Description, duhh
        self.description = ''

        # Config file description
        self.conf_description = """"""
        self.conf_default = None # if option is set to none, self.default is used

    def parse(self, value):
        return value

    def get_doc_line(self):
        s = ' '*4

        if self.cmd_short is not None:
            s += '-%s ' % self.cmd_short

        if self.option is not None:
            s += '--%s' % self.option

        if self.cmd_argument is not None:
            s += '=%s' % self.cmd_argument

        s += ' ' * (30 - len(s))

        s += self.description

        return s
