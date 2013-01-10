import copy
import imp
import sys
import os
import logging

from appdirs import AppDirs
from docopt import docopt
import ConfigParser

appname = 'wpmaker'
appauthor = 'viktor'
config_file_name = '%s.conf' % appname

def get_appdirs_paths():
    appdirs = AppDirs(appname, appauthor)
    dirs = (appdirs.user_data_dir, appdirs.site_data_dir)
    return [os.path.join(dir, config_file_name) for dir in dirs]

def get_doc(options):
    doc = """Usage: wpmaker.py [options]

Options:
"""
    for op in sorted(options, key=lambda op: op.option):
        doc += """%s
""" % op.get_doc_line()

    doc += """    -h --help                 Displays this help message

Configuration files:
"""
    for i, dir in enumerate(get_appdirs_paths()):
        doc += """    (%s) %s
""" % (i, dir)

    return doc

def get_config(options):
    logging.debug('Reading config file and parsing options')

    # keys are "plugin_module.option_name"
    config = {}
    # options in each plugin
    module_options = {}

    # Set config to defaults
    for op in options:
        op_module = op.__module__.split('.')[1]

        # fill config dict
        if op_module == 'options':
            config[op.option] = op.default
        else:
            config['%s.%s' % (op_module, op.option)] = op.default

        # fill module_options dict
        if op_module in module_options:
            module_options[op_module].append(op)
        else:
            module_options[op_module] = [op]

    files = get_appdirs_paths()
    cfg = ConfigParser.SafeConfigParser()
    cfg_files = cfg.read(files)

    for section in cfg.sections():
        module_pref = '' if section == 'options' else '%s.' % section

        for op in module_options[section]:
            if cfg.has_option(section, op.option):
                config[module_pref + op.option] = op.parse(cfg.get(section, op.option))

    # Parse command line options
    from docopt import docopt
    doc_options = docopt(get_doc(options))
    for key in doc_options:
        if key[:2] == '--' and doc_options[key] is not None:
            for op in module_options['options']:
                if op.option == key[2:]:
                    config[key[2:]] = op.parse(doc_options[key])

    return config
