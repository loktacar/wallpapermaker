wpmaker
===============================================================================

Tired of having a folder full of wallpapers and only seeing one at a time?

`wpmaker` has the ability to create collages of randomly selected images from
that folder. Also it can do the standard one-at-a-time thing, keeping the aspect
ratio and cropping instead of stretching.

[Here are some examples](http://imgur.com/a/9MFjX#0)

Why is this a better solution than other *leading brands*?

`wpmaker` is cross-compatible, it works on:
- Windows XP/Vista/7
- Mac OS/X
- Gnome Linux

`wpmaker` also has plugins, I know *amazing* right?:
- No problem making `wpmaker` work on other systems, just add plugins
- Easy to create new collages, just add plugins
- Do you want a completely new type of plugin? Well `wpmaker` is completely 
open source and you can just write it yourself.

Well, this sounds way too good to be true, there must be something missing.
You're in luck, `wpmaker` is still missing a GUI.

What about these plugins, can I create one? Sure! For now though you're gonna have
to rely on the ones I've created for information on how.

Requirements
===============================================================================
For `wpmaker` to work you need the following:

- Python version 2.5 to 2.7
- pygame
- For linux you'll need `python-xlib`, or another `get_resolution` plugin

Configuration
===============================================================================

To configure `wpmaker`, run `python wpmaker.py --help` for a list of
configuration files. Then create either or both of them, (0) is user-specific, (1) is
installation-specific. The options in the configuration files are the same as
the longer named options used in the command line.

```
#############################################################
#           This is a sample configuration file             #
#############################################################

[default]
# The 'default' section is read unless another is specified
# as a command line option (ex. wpmaker --section=debug)
path=~\Pictures\wp

# Time between wallpaper switching
update=180
# personal preference

[debug]
path=~\Pictures\wp
update_period=30

#############################################################
# Below are descriptions and default values for each option #
#            This section should not be included            #
#############################################################

[default_options]

# path to the wallpaper folder. Not set by default
# a tilde, ~, in paths is replaced with user directory path
path=Notset

# time between wallpaper switching
update=300

# path and filename of generated wallpaper image
wallpaper=~/.wp.bmp

# create and set a single wallpaper then exit
single-run=False

# forces resolution of generated wallpaper
# i.e. desktop resolution is not queried, useful if get_resolution plugins fail
resolution=None
# e.x. setting:
# resolution=1680x1050

# how many wallpapers will be generated between checking of wallpaper folder
fs-interval=5

# which collage plugin should be used, 'all' will make wpmaker choose one
# For now acceptable values are: 'SimpleResize', 'RecursiveSplit', and 'all'
collage-plugin=all

# This options is specifically for RecursiveSplit plugin
# recursion_depth: maximum number of times each split can be split
recursion-depth=3

```

How do I use this thing anyways?
===============================================================================

You can run `wpmaker` in the console by running `python wpmaker.py [options]`.
You can also run `wpmaker` without the console by running `python wpmaker.pyw
[options]`, but the `--verbose` option won't work.

Note: On many systems you can double click the wpmaker.py and wpmaker.pyw files
to run them.

The default help message(on Windows 7) goes something like this:

```
Usage wpmaker.py [options]

Options:
    --collage-plugin=COLLAGE  Which collage plugin should be used
    --fs-interval=INT         Check wallpaper folder every INT updates
    --path=PATH               PATH to the wallpaper folder
    --recursion-depth=INT     Split can be split INT times
    -r --resolution=RES       Forces resolution of generated wallpaper
    --section=SECTION         SECTION of configuration file to be used
    -s --single-run           Generate wallpaper once then exit
    --update=SEC              Time in seconds between generating and updating wallpaper
    --wallpaper=PATH          PATH to generated wallpaper
    -v --verbose              Debugging output
    -h --help                 Displays this help message

Configuration files:
    (0) D:\Users\viktor\AppData\Local\viktor\wpmaker\wpmaker.conf
    (1) C:\ProgramData\viktor\wpmaker\wpmaker.conf
```

Installation
===============================================================================
There is no standard installation yet. For not you'll need to start by
installing python, and pygame.

Then you'll need to go to the downloads tab the github page for the project,
[https://github.com/loktacar/wallpapermaker](https://github.com/loktacar/wallpapermaker)
and download the project in either zip or tar.gz format.

Uncompress the project and then you can follow the 'How do I use this thing
anyways?' section of this readme.
