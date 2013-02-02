from .. import Option

class DesktopEnvironment(Option):
    default = 'gnome'
    option = 'desktop-environment'
    cmd_argument = 'DE'
    description = 'Linux Desktop Environment'
