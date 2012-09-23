*Tired of having a folder full of wallpapers and only seeing one at a time?*

`wpmaker` has the ability to create collages of randomly selected images from
that folder. It can also do the standard one-at-a-time thing, keeping the aspect
ratio and cropping instead of stretching.

# Here are some examples
[![Example](http://i.imgur.com/XLNHpl.jpg)](http://i.imgur.com/XLNHp.jpg)
[![Example](http://i.imgur.com/YHrL4l.jpg)](http://i.imgur.com/YHrL4.jpg)

[A few more examples](http://imgur.com/a/9MFjX#0)

Why is this a better solution than those from other *leading brands*?

`wpmaker` is currently cross-compatible, it works on:
- Windows XP/Vista/7
- Mac OS/X (untested)
- Linux, but only Gnome (untested)

`wpmaker` can be configured either by command line options or configuration file, 
see usage directions in the `How do I use this thing anyways?` section. 

`wpmaker` also has plugins, I know *amazing* right?:
- No problem making `wpmaker` work on other systems, just add plugins
- Easy to create new collages, just add plugins
- Do you want a completely new type of plugin? Well `wpmaker` is completely 
open source and you can just write it yourself.

What about these plugins, how do I create one? For now though you
have to rely on the ones I've created for documentation.

## Installation
Follow the platform specific instructions and then download and extract the project. 
Then read the `How do I use this thing anyways?` section. 

### Windows
- Install python 2.7 ([download link](http://python.org/download/releases/2.7.3/))
- Install pygame ([download link](http://www.pygame.org/download.shtml))
- Install wxPython ([download link](http://wxpython.org/download.php), get the windows binaries for python 2.7 )

### Linux
- Install python 2.7
- Install pygame (`python-pygame` package in most repositories)
- Install `python-xlib`, for the get resolution plugin
- Install wxPython ([info](http://wiki.wxpython.org/How%20to%20install%20wxPython#Linux_-_Redhat))

#### Fedora 17 (F17)
- You should already have python 2.7 installed
- Run `yum install pygame`
- Run `yum install wxPython`
- If you get a warning about `Gtk-Message: Failed to load module "pk-gtk-module"`,
you also need to run `yum update PackageKit-gtk3-module`

## How do I use this thing anyways?
You can run `wpmaker` in the console by running `python wpmaker.py [options]`.
You can also run `wpmaker` without the console by running `python wpmaker.pyw
[options]`.

Note: You'll need to be in `wpmaker`s installation path in the console.  
Also note: On many systems you can double click the `wpmaker.py` and `wpmaker.pyw`
files to run them. They will only run if you've set the wp folder path in the
configuration file.

### Help message
```
Usage: wpmaker.py [options]

Options:
    --collage-plugin=COLLAGE  Which collage plugin should be used
    --desktop-environment=DE  Linux Desktop Environment
    --fs-interval=INT         Check wallpaper folder every INT updates
    --path=PATH               PATH to the wallpaper folder
    --recursion-depth=INT     Each split can be split INT times
    -r --resolution=RES       Forces resolution of generated wallpaper
    --section=SECTION         SECTION of configuration file to be used
    -s --single-run           Generate wallpaper once then exit
    --ui=UI                   Select which plugin, UI, should be used for ui purposes
    --update=SEC              SEC seconds between generating and updating wallpaper
    -v --verbose              Debugging output
    --wallpaper=PATH          PATH to generated wallpaper
    -h --help                 Displays this help message

Configuration files:
    (0) /home/loktacar/.config/wpmaker/wpmaker.conf
    (1) /etc/xdg/wpmaker/wpmaker.conf
```

## Configuration
To configure `wpmaker`, run `python wpmaker.py --help` for a list of
configuration files. Then create either or both of them, (0) is user-specific, (1) is
installation-specific. The options in the configuration files are the same as
the longer name of options described in the help message.

### Sample configuration
```
#############################################################
#           This is a sample configuration file             #
#############################################################

[default]
# The 'default' section is read unless another is specified
#   as a command line option (ex. wpmaker --section=debug)

# This must be set in either a configuration file or in
#   command-line
path=~\Pictures\wp

# Time between wallpaper switching, in seconds
update=180
# personal preference

# Set which ui plugin to useui=wxPython
[debug]
path=~\Pictures\wp
update=30
verbose=True

#############################################################
# Below are descriptions and default values for each option #
#            This section should not be included            #
#############################################################

[default_values]

# This options is specifically for RecursiveSplit plugin
# recursion_depth: maximum number of times each split can be
#   split
recursion-depth=3

# This option specifies which desktop environment should be manhandled into displaying the output wallpaper
desktop-environment=none

# how many wallpapers will be generated between checking of
#   wallpaper folder
fs-interval=5

# create and set a single wallpaper then exit
single-run=False

# Debugging info displayed in the command line
verbose=False

# path to the wallpaper folder. Not set by default
#   a tilde, ~, in paths is replaced with user directory path
path=None

# which collage plugin should be used, acceptable values are:
#     - 'SimpleResize'
#     - 'RecursiveSplit'
#     - 'all', plugin chosen at random
collage-plugin=all

# forces resolution of generated wallpaper
# i.e. desktop resolution is not queried, useful if
#   get_resolution plugins fail
# e.x. setting:
#   resolution=1680x1050
resolution=(0, 0)

# time between wallpaper switching
update=300

# path and filename of generated wallpaper image
wallpaper=~/.wp.bmp

# Which ui plugin should be used, acceptable values are:
#     - 'Console'
#     - 'wxPython'
ui=Console

```
``
