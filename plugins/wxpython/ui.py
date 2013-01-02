import os
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
        icon = wx.Icon("monitor-wallpaper-icon.png", wx.BITMAP_TYPE_PNG)
        icon.SetHeight(32)
        icon.SetWidth(32)

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

        self.sel_dir_item = self.menu.Append(wx.ID_ANY, '&Select Folder', 'Select a new wallpaper folder')

        # TODO: Need to implement a better way to store and use the collage submenu
        submenu_item_index_start = 4000
        submenu_item_index = submenu_item_index_start
        self.collage_submenu = wx.Menu()
        csi_all = self.collage_submenu.Append(submenu_item_index, 'all', 'all', kind=wx.ITEM_RADIO)
        self.collage_submenu_items = {submenu_item_index: 'all'}

        for cp in self.app.plugin_manager['Collage']:
            cp_name = cp.__class__.__name__
            submenu_item_index += 1
            self.collage_submenu_items[submenu_item_index] = cp_name
            self.collage_submenu.Append(submenu_item_index,
                                        cp_name,
                                        cp_name,
                                        kind=wx.ITEM_RADIO)

        self.ui_app.Bind(wx.EVT_MENU_RANGE, self.OnCollage, id=submenu_item_index_start, id2=submenu_item_index)

        self.menu.AppendMenu(wx.ID_ANY, '&Collage', self.collage_submenu)
        self.menu.Append(wx.ID_SEPARATOR)

        self.qitem = self.menu.Append(wx.ID_EXIT, '&Quit', 'Quit application')

        wx.EVT_MENU(self.tbicon, self.sel_dir_item.GetId(), self.OnFolderSelect)
        wx.EVT_MENU(self.tbicon, self.gitem.GetId(), self.start_generating)
        wx.EVT_MENU(self.tbicon, self.pitem.GetId(), self.OnPauseSelected)
        wx.EVT_MENU(self.tbicon, self.qitem.GetId(), self.exit_app)

        #gui update timer
        self.timer = wx.Timer()
        self.ui_app.Bind(wx.EVT_TIMER, self.OnUpdateTick, self.timer)
        self.timer.Start(1000.0/24)

    # App Control functions

    def start_app(self):
        self.logger.debug('Application and UI starting')
        self.thread = threading.Thread(target=self.app.main)
        self.thread.setDaemon(True)
        self.thread.start()

        self.ui_app.MainLoop()

    def exit_app(self, *args, **kwargs):
        self.tbicon.RemoveIcon()
        self.ui_app.ExitMainLoop()
        self.ui_app.Exit()

        self.logger.debug('Application exited, goodbye!')

    # wxEvents

    def OnTaskBarRight(self, event):
        self.tbicon.PopupMenu(self.menu)

    def OnPauseSelected(self, event):
        self.app.pause()

    def OnUpdateTick(self, event):
        self.menu.Check(self.pitem.GetId(), self.app.is_paused)

        for csi in self.collage_submenu_items:
            plugins = self.app.config['collage-plugins'].split(',')
            if self.collage_submenu_items[csi] in plugins:
                self.collage_submenu.Check(csi, True)

    def OnCollage(self, event):
        self.app.switch_collage_plugin(self.collage_submenu_items[event.GetId()])
        self.logger.debug('Changing collage to %s' % collage)

    def OnFolderSelect(self, event):
        dialog = wx.DirDialog(None, message='Pick a directory', defaultPath=os.path.expanduser('~'))

        if dialog.ShowModal() == wx.ID_OK:
            path = dialog.GetPath()
            for source in self.app.plugin_manager['Source']:
                if source.__class__.handles_path(path):
                    source.set_path(path)

        dialog.Destroy()

    # Following methods are called from the application, via ui hooks

    def app_quitting(self):
        # Using CallAfter because app_quitting is called from another thread, and that's bad
        wx.CallAfter(self.exit_app)

    def app_initialized(self):
        self.initialize_gui()

