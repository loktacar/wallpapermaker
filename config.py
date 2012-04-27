# Configuration file for wallpapermaker

# The path to the wallpapers, the program will search through subdirectories.
path = '/media/One/Users/viktor/Pictures/wp'
#path = 'D:/Users/viktor/Pictures/wp'
#path = 'D:\\Users\\viktor\\Pictures\\Cannon'

# The name of the file that will be outputted, and used as desktop wallpaper.
# file is always saved as bitmap image, irrespective of file extension
generated_wallpaper = '~/.wp.bmp'

# Extensions the program searches for
extensions = ['jpg','png','jpeg','gif','bmp']

# The time between file searches and wallpaper changes
update_period = 300

# Number of update periods between file checks
file_check_period = 5

# Recursion depth, must be greater than one
recursion_depth = 3

# Add date 'n time to generated wallpaper, will be added before last period
# ex. generated_wallpaper = '~/.wp.bmp' results in '~/.wp_2012-04-15_21-51.bmp'
add_date = False

# Run once then die (Create wallpaper, save, set and exit)
single_run = False

# Whether or not helpful debugging messages should be printed
verbose = False

# For linux systems only, desktop environment (gnome, kde, xmonad, xfce, etc.)
desktop_environment = 'gnome'

# Do not change the following
import os

import ConfigParser

from appdirs import AppDirs

appname = 'wpmaker'
appauthor = 'viktor'
config_file_name = '%s.conf' % appname

default_config_section = 'default'

def parse_options(cmd_opts):
    options = get_defaults()

    dirs = AppDirs(appname, appauthor)

    options = parse_config_files(options,
                                 config_file_name,
                                 (dirs.user_data_dir, dirs.site_data_dir),
                                 section=cmd_opts.section if cmd_opts.section else default_config_section)

    options = parse_cmd_options(cmd_opts, options)

    return options

def parse_config_files(options, config_file_name, dirs, section=default_config_section):
    """ Checks directories for config_file_name and adds values from config file to options dictionary, last dir checked first """
    files = ['%s/%s' % (dir, config_file_name) for dir in dirs]

    cfg = ConfigParser.SafeConfigParser()
    read_files = cfg.read(files)

    if len(read_files):
        use_section = section if cfg.has_section(section) else default_config_section

        for key in options.keys():
            if cfg.has_option(use_section, key):
                options[key] = fix_config_file_values(key, cfg.get(use_section, key))

    return options

def fix_config_file_values(key, value):
    if key in ['add_date', 'single_run', 'verbose']:
        return bool(value)

    if key in ['recursion_depth', 'update_period']:
        return int(value)

    if key in ['path', 'generated_wallpaper']:
        return os.path.expanduser(value)

    if key in ['extensions']:
        return value.split(',')

    if key in ['resolution']:
        res = value.split('x')
        if type(res) == str:
            res = value.split('X')

        if type(res) == str:
            value = False
        else:
            try:
                value = [int(i) for i in res]
            except:
                value = False

        return value

    return value

def get_defaults():
    """ Generate new option dictionary from defaults (from above) """
    options = {}
    options['path'] = os.path.expanduser(path)
    options['extensions'] = extensions
    options['update_period'] = update_period
    options['generated_wallpaper'] = os.path.expanduser(generated_wallpaper)
    options['recursion_depth'] = recursion_depth
    options['add_date'] = add_date
    options['single_run'] = single_run
    options['verbose'] = verbose
    options['desktop_environment'] = desktop_environment
    options['resolution'] = False
    options['file_check_period'] = file_check_period

    return options

def parse_cmd_options(cmd_opts, options):
    """ Fills in the options dictionary with values from command line options """

    if cmd_opts.path:
        options['path'] = os.path.expanduser(cmd_opts.path)

    if cmd_opts.extensions:
        options['extensions'] = cmd_opts.extensions

    if cmd_opts.update:
        options['update_period'] = cmd_opts.update

    if cmd_opts.generated_wallpaper:
        options['generated_wallpaper'] = os.path.expanduser(cmd_opts.generated_wallpaper)

    if cmd_opts.recursion_depth:
        options['recursion_depth'] = cmd_opts.recursion_depth

    if cmd_opts.add_date:
        options['add_date'] = cmd_opts.add_date

    if cmd_opts.single_run:
        options['single_run'] = cmd_opts.single_run

    if cmd_opts.verbose:
        options['verbose'] = cmd_opts.verbose

    # Parse resolution input
    if cmd_opts.resolution:
        options['resolution'] = cmd_opts.resolution
        if options['resolution']:
            res = options['resolution'].split('x')
            if type(res) == str:
                res = options['resolution'].split('X')

            if type(res) == str:
                options['resolution'] = False
            else:
                try:
                    options['resolution'] = [int(i) for i in res]
                except:
                    options['resolution'] = False

    return options
