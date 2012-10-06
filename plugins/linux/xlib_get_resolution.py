import sys

from .. import GetResolution

class XlibGetResolution(GetResolution):
    def __init__(self):
        super(XlibGetResolution, self).__init__()

    def platform_check(self):
        return sys.platform == 'linux2'

    def get(self):
        import subprocess

        output = subprocess.Popen('xrandr | grep " connected" | cut -d" " -f3', shell=True, stdout=subprocess.PIPE).communicate()[0]

        resolutions = []

        displays = output.strip().split('\n')
        for display in displays:
            values = display.split('+')
            res_values = values[0].split('x')

            # create resolution tuple
            # (width, height, x-offset, y-offset)
            # offset is counted from top left screen
            res_tuple = (int(res_values[0]), int(res_values[1]), int(values[1]), int(values[2]))

            resolutions.append(res_tuple)

        return resolutions

