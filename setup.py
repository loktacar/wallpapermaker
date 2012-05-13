import os

from distutils.core import setup
import py2exe

#origIsSystemDLL = py2exe.build_exe.isSystemDLL # save the orginal before we edit it
#def isSystemDLL(pathname):
    ## checks if the freetype and ogg dll files are being included
    #if os.path.basename(pathname).lower() in ("libfreetype-6.dll", "libogg-0.dll", "sdl_ttf.dll"):
            #return 0
    #return origIsSystemDLL(pathname) # return the orginal function
#py2exe.build_exe.isSystemDLL = isSystemDLL # override the default function with this one

setup(
        console=['wpmaker.py'],
        windows=['wpmaker_tray.py'],
        options={
            'py2exe': {
                'optimize': 2,
                'bundle_files': 1,
                'compressed': True,
                'packages': 'encodings',
                'includes': 'cairo, pango, pangocairo, atk, gobject, gio',
                }
            },
        data_files = [#'freesansbold.ttf',
                      #'SDL.dll',
                      #'SDL_ttf.dll',
                      #'libfreetype-6.dll',
                      #'zlib1.dll'
                      ]
    )


#               TODO: download these .dll's, start by just getting freesansbold.ttf
