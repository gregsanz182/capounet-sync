from threading import Thread
from os import path
from MainWindow import MainWindow
from PyQt5.QtCore import pyqtSignal, QObject
from GuiTools import InformationLabel, StatusPanel
from Settings import Settings

class SyncThread(QObject, Thread):

    logSignal = pyqtSignal(str)
    changedSyncStateSignal = pyqtSignal(str, int, StatusPanel)

    syncMessages = {
        "disable_sync": "La sincronización se encuentra deshabilitada. \
                        <br>Habilitar en <strong>Ajustes</strong>."
    }

    def __init__(self, mainWindow: MainWindow):
        super(SyncThread, self).__init__()
        self.mw = mainWindow
        self.makeConnections()

    def makeConnections(self):
        self.logSignal.connect(self.mw.printLog)
        self.changedSyncStateSignal.connect(self.mw.setSyncState)

    def run(self):
        self.logSignal.emit("Inicializando...")
        self.logSignal.emit("Leyendo configuracion...")
        if not Settings.sociosFilePath[0]:
            self.logSignal.emit("La sincronización de 'Socios y Ahorros' está desactivada.")
            self.changedSyncStateSignal.emit(
                self.syncMessages["disable_sync"], 
                InformationLabel.WARNING, 
                self.mw.sociosPanel
            )
        if not Settings.prestamosFilePath[0]:
            self.logSignal.emit("La sincronización de 'Préstamos' está desactivada.")
            self.changedSyncStateSignal.emit(
                self.syncMessages["disable_sync"],
                InformationLabel.WARNING, 
                self.mw.prestamosPanel
            )
        while True:
            self.syncFile(Settings.sociosFilePath)

    def syncFile(filePath: tuple):
        if not filePath[0]:
            return
        if not path.isfile(filePath[1]):
            self.logSignal.emit("El archivo {} no es una ruta válida. Por favor, verificar en ajustes.")
            self.logSignal.emit("La sincronización de 'Socios y Ahorros' se deshabilitará.")
            self.changedSyncStateSignal.emit(
                self.syncMessages["disable_sync"], 
                InformationLabel.WARNING, 
                self.mw.sociosPanel
            )


