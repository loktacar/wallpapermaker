import os
import sys

from .. import SetWallpaper

class Win32SetWallpaper(SetWallpaper):
    def __init__(self, config):
        super(Win32SetWallpaper, self).__init__(config)

    def platform_check(self):
        return sys.platform == 'win32' and self.config['set-wallpaper'] == 'auto' or self.config['set-wallpaper'] == 'win32'

    def set(self):
        from win32com.shell import shell, shellcon
        import pythoncom

        pythoncom.CoInitialize()
        iad = pythoncom.CoCreateInstance(shell.CLSID_ActiveDesktop, None,
                pythoncom.CLSCTX_INPROC_SERVER, shell.IID_IActiveDesktop)

        wallpaper_path = os.path.abspath(self.config['wallpaper'])
        iad.SetWallpaper(wallpaper_path, 0)
        iad.SetWallpaperOptions(1, 0)
        iad.ApplyChanges(shellcon.AD_APPLY_ALL)

