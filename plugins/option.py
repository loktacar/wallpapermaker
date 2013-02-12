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

    @staticmethod
    def parse(value):
        return value

    @classmethod
    def folder_module(cls):
        return cls.__module__.split('.')[-2]

    @classmethod
    def get_doc_line(cls):
        s = ' '*4

        if cls.cmd_short is not None:
            s += '-%s ' % cls.cmd_short

        if cls.option is not None:
            folder_module = cls.folder_module()
            if folder_module == 'options':
                s += '--%s' % cls.option
            else:
                s += '--%s.%s' % (folder_module, cls.option)

        if cls.cmd_argument is not None:
            s += '=%s' % cls.cmd_argument

        if len(s) < 30:
            s += ' ' * (30 - len(s))
        else:
            s += '\n' + ' ' * 30

        s += cls.description

        return s
