import threading
import logging

import wx

from .. import UI

class wxPython(UI):
    def __init__(self):
        super(wxPython, self).__init__()
        self.logger = logging.getLogger('root')

    def initialize_gui(self):
        self.logger.debug('initializing gui...')
        #setup app
        self.ui_app = wx.PySimpleApp()

        #setup icon object
        icon = wx.Icon("favico.ico", wx.BITMAP_TYPE_ICO)

        #setup taskbar icon
        self.tbicon = wx.TaskBarIcon()
        self.tbicon.SetIcon(icon, "wpmaker")

        #add taskbar icon event
        wx.EVT_TASKBAR_RIGHT_UP(self.tbicon, self.OnTaskBarRight)

        self.ui_app.MainLoop()
        self.logger.debug('ui MainLoop started')

    def create_tbicon_menu(self):
        menu = wx.Menu()
        qitem = menu.Append(wx.ID_EXIT, '&Quit', 'Quit application')
        wx.EVT_MENU(self.tbicon, wx.ID_EXIT, self.OnQuitMenuItemSelect)
        return menu

    def quit_ui(self):
        self.tbicon.RemoveIcon()
        self.ui_app.ExitMainLoop()
        self.ui_app.Exit()
        self.logger.debug('ui quit')

    # wxEvents

    def OnTaskBarRight(self, event):
        self.tbicon.PopupMenu(self.create_tbicon_menu())

    def OnQuitMenuItemSelect(self, event):
        self.quit_ui()

    # Following methods are called from the application, via ui hooks

    def app_quitting(self):
        # Using CallAfter because app_quitting is called from another thread
        wx.CallAfter(self.quit_ui)

    def start_app(self):
        self.logger.debug('starting app thread...')
        self.thread = threading.Thread(target=self.app.main)
        self.thread.setDaemon(True)
        self.thread.start()
        self.logger.debug('app thread started')

        self.initialize_gui()

