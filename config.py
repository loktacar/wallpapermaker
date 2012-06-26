import copy
import imp
import sys
import os
import logging

from appdirs import AppDirs
from docopt import docopt
import ConfigParser

from plugins import option_plugins

appname = 'wpmaker'
appauthor = 'viktor'
config_file_name = '%s.conf' % appname

options = [op() for op in option_plugins]

logger = logging.getLogger('root')

def get_appdirs_paths():
    appdirs = AppDirs(appname, appauthor)
    dirs = (appdirs.user_data_dir, appdirs.site_data_dir)
    return [os.path.join(dir, config_file_name) for dir in dirs]

def get_doc():
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
""" % (i, str(dir)) # dir converted to string from unicode since docopt failes when doc string is in unicode

    return doc

def get_config():
    from docopt import docopt
    doc_options = docopt(get_doc())

    config = {}

    # Set config to defaults
    default_section = 'default'
    for op in options:
        config[op.option] = op.default

        if op.option == 'section':
            default_section = op.default

    # Get config file configuration
    files = get_appdirs_paths()
    cfg = ConfigParser.SafeConfigParser()
    cfg_files = cfg.read(files)

    # Set config file section and read files
    file_section = doc_options['--section'] if doc_options['--section'] else default_section
    files_read = cfg.read(files)

    # Parse config file
    if len(files_read):
        if not cfg.has_section(file_section):
            raise ValueError('Section %s not found' % file_section)

        for op in options:
            if cfg.has_option(file_section, op.option):
                config[op.option] = op.parse(cfg.get(file_section, op.option))

    # Parse command line options
    for key in doc_options:
        if key[:2] == '--' and doc_options[key] is not None:
            for op in options:
                if op.option == key[2:]:
                    config[key[2:]] = op.parse(doc_options[key])

    return config
