import logging

class Plugin(object):
    def __init__(self):
        self.logger = logging.getLogger('root')
        self.config = None

    def set_config(self, config):
        self.config = config
