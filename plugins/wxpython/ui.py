import threading

import wx

from .. import UI

class wxPython(UI):
    def __init__(self):
        super(wxPython, self).__init__()

    def initialize_gui(self):
        self.logger.debug('initializing gui...')
        #setup app
        self.ui_app = wx.PySimpleApp()

        #setup icon object
        icon = wx.Icon("favico.ico", wx.BITMAP_TYPE_ICO)

        #setup taskbar icon
        self.tbicon = wx.TaskBarIcon()
        self.tbicon.SetIcon(icon, "wpmaker")
        wx.EVT_TASKBAR_RIGHT_UP(self.tbicon, self.OnTaskBarRight)

        #menu
        self.menu = wx.Menu()

        self.gitem = self.menu.Append(wx.ID_ANY, '&Generate', 'Generate new wallpaper')
        self.pitem = self.menu.Append(wx.ID_ANY, '&Pause', 'Pause wallpaper generation', kind=wx.ITEM_CHECK)
        self.menu.Check(self.pitem.GetId(), True)
        self.menu.Append(wx.ID_SEPARATOR)

        # TODO: Need to implement a better way to store and use the collage submenu
        submenu_item_index_start = 4000
        submenu_item_index = submenu_item_index_start
        self.collage_submenu = wx.Menu()
        csi_all = self.collage_submenu.Append(submenu_item_index, 'all', 'all', kind=wx.ITEM_RADIO)
        self.collage_submenu_items = {submenu_item_index: 'all'}

        for cp in self.app.loaded_plugins['collage']:
            submenu_item_index += 1
            self.collage_submenu_items[submenu_item_index] = cp
            self.collage_submenu.Append(submenu_item_index,
                                        cp,
                                        cp,
                                        kind=wx.ITEM_RADIO)

        self.ui_app.Bind(wx.EVT_MENU_RANGE, self.OnCollage, id=submenu_item_index_start, id2=submenu_item_index)

        self.menu.AppendMenu(wx.ID_ANY, '&Collage', self.collage_submenu)
        self.menu.Append(wx.ID_SEPARATOR)

        self.qitem = self.menu.Append(wx.ID_EXIT, '&Quit', 'Quit application')

        wx.EVT_MENU(self.tbicon, self.gitem.GetId(), self.start_generating)
        wx.EVT_MENU(self.tbicon, self.pitem.GetId(), self.OnPauseSelected)
        wx.EVT_MENU(self.tbicon, self.qitem.GetId(), self.quit_ui)

        #gui update timer
        self.timer = wx.Timer()
        self.ui_app.Bind(wx.EVT_TIMER, self.OnUpdateTick, self.timer)
        self.timer.Start(1000.0/24)

        self.ui_app.MainLoop()
        self.logger.debug('ui MainLoop started')

    def quit_ui(self, *args, **kwargs):
        self.tbicon.RemoveIcon()
        self.ui_app.ExitMainLoop()
        self.ui_app.Exit()
        self.logger.debug('ui quit')

    # wxEvents

    def OnTaskBarRight(self, event):
        self.tbicon.PopupMenu(self.menu)

    def OnPauseSelected(self, event):
        self.pause_app_toggle()

    def OnUpdateTick(self, event):
        self.menu.Check(self.pitem.GetId(), self.app.is_paused)

        #self.collage_submenu.Check(
        #        self.collage_submenu_items[self.app.config['collage-plugin']].GetId(), True)

        for csi in self.collage_submenu_items:
            if self.collage_submenu_items[csi] == self.app.config['collage-plugin']:
                self.collage_submenu.Check(csi, True)

    def OnCollage(self, event):
        self.switch_collage_plugin(self.collage_submenu_items[event.GetId()])
        #print event.GetId()
        #print event.GetText()

    # Following methods are called from the application, via ui hooks

    def app_quitting(self):
        # Using CallAfter because app_quitting is called from another thread, and that's bad
        wx.CallAfter(self.quit_ui)

    def start_app(self):
        self.thread = threading.Thread(target=self.app.main)
        self.thread.setDaemon(True)
        self.thread.start()
        self.logger.debug('app thread started')

        self.initialize_gui()
