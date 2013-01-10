from .. import Option

class DesktopEnvironment(Option):
    default='none'
    option = 'desktop-environment'
    cmd_argument = 'DE'
    description = 'Linux Desktop Environment'
    conf_description = ['# This option specifies which desktop environment should be manhandled into displaying the output wallpaper\n']
