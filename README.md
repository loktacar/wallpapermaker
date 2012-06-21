`wpmaker` creates wallpaper collages
===============================================================================

Tired of having a folder full of wallpapers and only seeing one at a time?

`wpmaker` has the ability to create collages from randomly selected images from
a folder. Also it can do the standard one-at-a-time thing, keeping the aspect
ratio and cropping instead of stretching.

Here is an [example](http://i.imgur.com/BnZTn.jpg)

Why is this a better solution than other *leading brands*?

`wpmaker` is cross-compatible, it works on:
- Windows XP/Vista/7
- Mac OS/X
- Gnome Linux

`wpmaker` also has plugins, I know *amazing* right?:
- No problem making `wpmaker` compatible with other systems, just add plugins
- Easy to create new collages, just add plugins
- Do you want a completely new type of plugin? Well `wpmaker` is completely 
open source and you can just add it yourself.

Well, this sounds way too good to be true, there must be something missing.
You're in luck, `wpmaker` is still missing a GUI.

What about these plugins, can I create one? Sure! For now though you're gonna have
to rely on the ones I've created for information on how. But, if you create
a plugin you can submit a pull request on github.com.

Configuration
===============================================================================

Configuring `wpmaker` is easy, run `python wpmaker.py --help` for a list of
configuration files. Then create one of them. The options are the same as the
longer named option used in the command line. See example.conf for more info.

How do I use this thing anyways?
===============================================================================

You can run `wpmaker` in the console by running `python wpmaker.py [options]`.
You can also run `wpmaker` without the console by running `wpmaker.pyw`.

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
    D:\Users\viktor\AppData\Local\viktor\wpmaker\wpmaker.conf
    C:\ProgramData\viktor\wpmaker\wpmaker.conf

See sample.conf for information on options and examples
```

