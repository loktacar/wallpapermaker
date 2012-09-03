from .. import Option

class DesktopEnvironment(Option):
    def __init__(self):
        super(DesktopEnvironment, self).__init__()

        self.default='none'
        self.option = 'desktop-environment'
        self.cmd_argument = 'DE'
        self.description = 'Linux Desktop Environment'
        self.conf_description = ['# This option specifies which desktop environment should be manhandled into displaying the output wallpaper\n']
