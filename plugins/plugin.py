import logging

class Plugin(object):
    settings = {
            'multiple_instances': False,
            'active_required':     False,
            }

    def __init__(self):
        self.config = None

    def set_config(self, config):
        self.config = config
