import threading
import time
from MainWindow import MainWindow
from PyQt5.QtCore import pyqtSignal, QObject
from GuiTools import InformationLabel, StatusPanel

class SyncThread(QObject, threading.Thread):

    logSignal = pyqtSignal(str)
    changedSyncStateSignal = pyqtSignal(str, int, StatusPanel)

    def __init__(self, mainWindow: MainWindow):
        super(SyncThread, self).__init__()
        self.mw = mainWindow
        self.makeConnections()

    def makeConnections(self):
        self.logSignal.connect(self.mw.printLog)
        self.changedSyncStateSignal.connect(self.mw.setSyncState)

    def run(self):
        cont = 1
        while True:
            self.logSignal.emit("hola {}".format(cont))
            if cont%2 == 0:
                self.changedSyncStateSignal.emit("Todo correcto", InformationLabel.SUCCESS, self.mw.sociosPanel)
                self.changedSyncStateSignal.emit("El archivo es incorrecto", InformationLabel.WARNING, self.mw.prestamosPanel)
            else:
                self.changedSyncStateSignal.emit("No se pudo sincronizar", InformationLabel.ERROR, self.mw.prestamosPanel)
                self.changedSyncStateSignal.emit("No hay conexion a internet", InformationLabel.WARNING, self.mw.sociosPanel)
            cont += 1
            time.sleep(4)

