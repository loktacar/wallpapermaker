import threading

class StoppableThread(threading.Thread):
    def __init__(self):
        super(StoppableThread, self).__init__()
        self.daemon = True
        self._stop = False

    def stop(self):
        self._stop = True

    def stopped(self):
        return self._stop
