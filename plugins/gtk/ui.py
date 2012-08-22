from .. import UI

class GTK(UI):

    def __init__(self):
        super(GTK, self).__init__()

    # "events"
    def app_started(self):
        import gtk
        # Initialize gtk stuffs

    # control funcitons

    def start_app(self):
        import gtk
        import gtk.gdk

        thread = threading.Thread(target=self.app.main)
        thread.setDaemon(True)
        thread.start()
        gtk.gdk.threads_init()
        gtk.main()
