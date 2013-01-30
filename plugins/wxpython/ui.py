import os
import threading
import logging
import time

import wx

from .. import UI

class wxPython(UI):
    def __init__(self, config):
        super(wxPython, self).__init__(config)

    def initialize_gui(self):
        logging.debug('initializing gui...')
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

        # action menu items
        self.gitem = self.menu.Append(wx.ID_ANY, '&Generate', 'Generate new wallpaper')
        self.pitem = self.menu.Append(wx.ID_ANY, '&Pause', 'Pause wallpaper generation', kind=wx.ITEM_CHECK)
        self.menu.Check(self.pitem.GetId(), True)
        self.menu.Append(wx.ID_SEPARATOR)

        # configuration menu items
        self.sel_dir_item = self.menu.Append(wx.ID_ANY, '&Select Folder', 'Select a new wallpaper folder')

        self._create_collage_menu()

        self.interval_submenu = wx.Menu()
        self.interval_submenu_itervals = [1, 5, 10, 30, 60]
        self.interval_submenu_items = {}
        submenu_item_index_start = 6000
        submenu_item_index = submenu_item_index_start
        for interval in self.interval_submenu_itervals:
            self.interval_submenu_items[submenu_item_index] = interval
            self.interval_submenu.Append(id=submenu_item_index,
                                         text='%d min' % interval,
                                         kind=wx.ITEM_NORMAL)
            submenu_item_index += 1
        self.ui_app.Bind(wx.EVT_MENU_RANGE, self.OnInterval, id=submenu_item_index_start, id2=submenu_item_index)
        self.menu.AppendMenu(wx.ID_ANY, '&Interval', self.interval_submenu)

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
        logging.debug('Application and UI starting')
        self.thread = threading.Thread(target=self.app.main)
        self.thread.setDaemon(True)
        self.thread.start()

        self.ui_app.MainLoop()

    def exit_app(self, *args, **kwargs):
        self.tbicon.RemoveIcon()
        self.ui_app.ExitMainLoop()
        self.ui_app.Exit()

        logging.debug('Application exited, goodbye!')

    # wxEvents

    def OnTaskBarRight(self, event):
        self.tbicon.PopupMenu(self.menu)

    def OnPauseSelected(self, event):
        self.app.pause()

    def OnUpdateTick(self, event):
        self.menu.Check(self.pitem.GetId(), self.app.is_paused)

    def OnCollage(self, event):
        collage = self.collage_submenu_class_names[event.GetId()]
        self.app.toggle_collage(collage, activate=event.IsChecked())

    def OnInterval(self, event):
        interval = self.interval_submenu_items[event.GetId()] * 60
        self.app.next_generation += interval - self.app.config['update']
        self.app.config['update'] = interval

        if self.app.next_generation > time.time():
            logging.debug('Generation interval changed, waiting until %s' %
                    time.strftime('%X', time.localtime(self.app.next_generation)))
        else:
            logging.debug('Generation interval changed, starting generation...')


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

    def collage_toggled(self, collage_name, activated):
        """ Called when collage plugin is (de)activated """

        for csi in self.collage_submenu_items:
            if self.collage_submenu_items[csi] == collage_name:
                self.collage_submenu.Check(csi, activated)


    def _create_collage_menu(self):
        # TODO: Need to implement a better way to store and use the collage submenu
        submenu_item_index_start = 4000
        submenu_item_index = submenu_item_index_start
        self.collage_submenu = wx.Menu()
        self.collage_submenu_items = {}
        self.collage_submenu_class_names = {}
        self.active_collages = [c.__class__.__name__ for c in self.app.plugin_manager['Collage']]

        for cp in self.app.plugin_manager.plugins['Collage']:
            class_name = cp.__name__
            collage_name = cp.name
            submenu_item_index += 1
            self.collage_submenu_items[submenu_item_index] = collage_name
            self.collage_submenu_class_names[submenu_item_index] = class_name
            self.collage_submenu.Append(submenu_item_index,
                                              collage_name,
                                              collage_name,
                                              kind=wx.ITEM_CHECK)

            if class_name in self.active_collages:
                self.collage_submenu.Check(submenu_item_index, True)

        self.ui_app.Bind(wx.EVT_MENU_RANGE, self.OnCollage, id=submenu_item_index_start, id2=submenu_item_index)

        self.menu.AppendMenu(wx.ID_ANY, '&Collage', self.collage_submenu)


