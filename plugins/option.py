from plugin import Plugin

class Option(Plugin):
    """
        Base class for option plugins
    """

    # Default value, if default is None, option is required to be set to something else
    default = None

    # Option name
    option = None

    # Short command line option
    cmd_short = None
    # Command line argument name
    cmd_argument = None

    # Description, duhh
    description = ''

    # Config file description
    conf_description = """"""
    conf_default = None # if option is set to none, default is used

    @staticmethod
    def parse(value):
        return value

    @classmethod
    def get_doc_line(cls):
        s = ' '*4

        if cls.cmd_short is not None:
            s += '-%s ' % cls.cmd_short

        if cls.option is not None:
            s += '--%s' % cls.option

        if cls.cmd_argument is not None:
            s += '=%s' % cls.cmd_argument

        s += ' ' * (30 - len(s))

        s += cls.description

        return s
