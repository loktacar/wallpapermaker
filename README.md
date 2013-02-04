*Tired of having a folder full of wallpapers and only seeing one at a time?*

`wpmaker` has the ability to create collages of randomly selected images from
a folder. It can also do the standard one-at-a-time thing, keeping the aspect
ratio and cropping instead of stretching.

# Here are some examples
[![Example](http://i.imgur.com/XLNHpl.jpg)](http://i.imgur.com/XLNHp.jpg)
[![Example](http://i.imgur.com/YHrL4l.jpg)](http://i.imgur.com/YHrL4.jpg)

[A few more examples](http://imgur.com/a/9MFjX#0)

Why is this a better solution than those from other *leading brands*?

`wpmaker` is cross-compatible, it works on:
- Windows XP/Vista/7
- Mac OS/X
- Linux: GNOME and LXDE

`wpmaker` can be configured either by command line options or configuration file, 
see usage directions in the **How do I use this thing anyways?** section. 

`wpmaker` also has plugins, I know *amazing* right?:
- No problem making `wpmaker` work on other systems, just add plugins
- Easy to create new collages, just add a plugin
- Do you want a completely new type of plugin? Well `wpmaker` is 
open source and you can just write it yourself.

What about these plugins, how do I create one? Check the wiki, I might add some info.

## Installation
### Requirements
- Python 2.7 ([download link](http://python.org/download/releases/2.7.3/))
- Pygame ([download link](http://www.pygame.org/download.shtml))
- wxPython ([download link](http://wxpython.org/download.php)) (optional)
- [docopt](https://github.com/docopt/docopt) (easy_install docopt)
- [appdirs](https://github.com/ActiveState/appdirs) (easy_install appdirs)

Follow the platform specific instructions and then download and extract the project.
Then read the **How do I use this thing anyways?** section.

### Windows
- Install python 2.7
- Install pygame
- Install wxPython (get the windows binaries for python 2.7) (optional)

### Linux
- Install python 2.7
- Install pygame (`python-pygame` package in most repositories)
- Install `python-xlib`, for the get resolution plugin
- Install wxPython ([info](http://wiki.wxpython.org/How%20to%20install%20wxPython#Linux_-_Redhat)) (optional)

#### Fedora 17 (F17)
- You should already have python 2.7 installed
- Run `yum install pygame`
- Run `yum install wxPython` (optional)
- If you get a warning about `Gtk-Message: Failed to load module "pk-gtk-module"`,
you also need to run `yum update PackageKit-gtk3-module`

## How do I use this thing anyways?
On **Windows** you can run `wpmaker` by double clicking wpmaker.pyw. On **linux** you can also run `wpmaker` by double clicking wpmaker.py or wpmaker.pyw.

You can also run `wpmaker` from the terminal by running `wpmaker.py`(on windows), `./wpmaker.py` on linux. See the help message below on how to run `wpmaker` from the terminal.

### Help message (on Fedora 17)
```
Usage: wpmaker.py [options]

Options:
    --collage-plugins=COLLAGE Which collage plugin should be used
    --linux.desktop-environment=DE
                              Linux Desktop Environment
    --recursive_split.recursion-depth=INT
                              Each split can be split INT times
    -r --resolution=RES       Forces resolution of generated wallpaper
    -s --single-run           Generate wallpaper once then exit
    --folder.source=PATH      Folder path of wallpapers
    --ui=UI                   Select which plugin, UI, should be used for ui purposes
    --update=SEC              SEC seconds between generating and updating wallpaper
    --wallpaper=PATH          PATH to generated wallpaper
    -h --help                 Displays this help message

Configuration files:
    (0) /home/user/.config/wpmaker/wpmaker.conf
    (1) /etc/xdg/wpmaker/wpmaker.conf
```

## Configuration
To configure `wpmaker`, run `python wpmaker.py --help` for a list of
configuration files. Then create either or both of them, (0) is user-specific, (1) is
installation-specific. The options in the configuration files are the same as
the longer name of options described in the help message.

### Sample configuration
The following configures `wpmaker` to the default values, with comments on how each is configured.
```
[options]
collage-plugin=recursive split,simple resize
# Which collage plugins are active on startup
# Comma seperated list of names

resolution=0x0
# Hard code the resolution of the output wallpaper image
# widthXheight
# This can be used if no GetResolution plugin works on your system

single-run=False
# Set to true if wpmaker is to create only one image then exit

ui=wxPython
# The ui to be used, currently only 'Console', and 'wxPython' available

wallpaper=~/.wp.bmp
# The filename of the output wallpaper image

[linux]
desktop-environment=gnome
# The desktop environment used on linux, currently only 'gnome', and 'lxde' supported

[recursive_split]
recursion-depth=3
# The number of splits within splits
```
