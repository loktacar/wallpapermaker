import logging

class Plugin(object):
    def __init__(self):
        self.logger = logging.getLogger('root')
        self.config = None
        self.name = self.__class__.__name__

    def set_config(self, config):
        self.config = config
