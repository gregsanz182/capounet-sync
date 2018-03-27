from threading import Thread
from os import path
from MainWindow import MainWindow
from PyQt5.QtCore import pyqtSignal, QObject
from GuiTools import InformationLabel, StatusPanel
from Settings import Settings

class SyncThread(QObject, Thread):

    log_signal = pyqtSignal(str)
    changed_sync_state_signal = pyqtSignal(str, int, StatusPanel)

    sync_messages = {
        "disable_sync": "La sincronización se encuentra deshabilitada. \
                        <br>Habilitar en <strong>Ajustes</strong>."
    }

    def __init__(self, mainWindow: MainWindow):
        super(SyncThread, self).__init__()
        self.window = mainWindow
        self.make_connections()

    def make_connections(self):
        self.log_signal.connect(self.window.print_log)
        self.changed_sync_state_signal.connect(self.window.set_sync_state)

    def run(self):
        self.log_signal.emit("Inicializando...")
        self.log_signal.emit("Leyendo configuracion...")
        if not Settings.socios_file["enabled"]:
            self.log_signal.emit("La sincronización de 'Socios y Ahorros' está desactivada.")
            self.changed_sync_state_signal.emit(
                self.sync_messages["disable_sync"], 
                InformationLabel.WARNING, 
                self.window.sociosPanel
            )
        if not Settings.prestamos_file["enabled"]:
            self.log_signal.emit("La sincronización de 'Préstamos' está desactivada.")
            self.changed_sync_state_signal.emit(
                self.sync_messages["disable_sync"],
                InformationLabel.WARNING, 
                self.window.prestamosPanel
            )
        while True:
            """self.syncFile(Settings.socios_file)

    def syncFile(filePath: tuple):
        if not filePath[0]:
            return
        if not path.isfile(filePath[1]):
            self.log_signal.emit("El archivo {} no es una ruta válida. Por favor, verificar en ajustes.")
            self.log_signal.emit("La sincronización de 'Socios y Ahorros' se deshabilitará.")
            self.changed_sync_state_signal.emit(
                self.sync_messages["disable_sync"], 
                InformationLabel.WARNING, 
                self.window.sociosPanel
            )"""


