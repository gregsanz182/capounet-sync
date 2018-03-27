import threading
import time
from MainWindow import MainWindow

class SyncThread(threading.Thread):

    def __init__(self, mainWindow: MainWindow):
        super().__init__()
        self.mw = mainWindow

    def run(self):
        while True:
            self.mw.printLogSignal.emit("hola")
            time.sleep(1)

