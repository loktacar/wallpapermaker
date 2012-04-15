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

# Recursion depth, must be greater than one
recursion_depth = 4

# Add date 'n time to generated wallpaper, will be added before last period
# ex. generated_wallpaper = '~/.wp.bmp' results in '~/.wp_2012-04-15_21-51.bmp'
add_date = False

# For linux systems only, desktop environment (gnome, kde, xmonad, xfce, etc.)
desktop_environment = 'gnome'

# Do not change the following
import os

def parse_options(cmd_opts):
    """ Generates option dictionary from defaults (above) and command line options """
    options = {}

    options['path'] = os.path.expanduser(cmd_opts.path if cmd_opts.path else path)
    options['extensions'] = cmd_opts.extensions if cmd_opts.extensions else extensions
    options['update_period'] = cmd_opts.update if cmd_opts.update else update_period
    options['generated_wallpaper'] = os.path.expanduser(\
                                        cmd_opts.generated_wallpaper if cmd_opts.generated_wallpaper else\
                                        generated_wallpaper)
    options['recursion_depth'] = cmd_opts.recursion_depth if cmd_opts.recursion_depth else recursion_depth
    options['add_date'] = cmd_opts.add_date if cmd_opts.add_date else add_date
    options['verbose'] = cmd_opts.verbose

    # Parse resolution input
    options['resolution'] = cmd_opts.resolution
    if options['resolution']:
        res = options['resolution'].split('x')
        if type(res) == str:
            res = options['resolution'].split('X')

        if type(res) == str:
            options['resolution'] == False
        else:
            try:
                options['resolution'] = [int(i) for i in res]
            except:
                options['resolution'] = False

    return options
