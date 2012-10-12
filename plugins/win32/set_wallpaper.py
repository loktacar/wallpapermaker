import sys

from .. import SetWallpaper

class Win32SetWallpaper(SetWallpaper):
    def __init__(self):
        super(Win32SetWallpaper, self).__init__()

    def platform_check(self):
        return sys.platform == 'win32'

    def set(self):
        from win32com.shell import shell, shellcon
        import pythoncom


        pythoncom.CoInitialize()
        iad = pythoncom.CoCreateInstance(shell.CLSID_ActiveDesktop, None,
                pythoncom.CLSCTX_INPROC_SERVER, shell.IID_IActiveDesktop)
        print self.config['wallpaper']
        iad.SetWallpaper(self.config['wallpaper'], 0)
        iad.SetWallpaperOptions(1, 0)
        iad.ApplyChanges(shellcon.AD_APPLY_ALL)

