import time
import zlib
import csv
import json
from threading import Thread
from os import path
from MainWindow import MainWindow
from PyQt5.QtCore import pyqtSignal, QObject
from GuiTools import InformationLabel, StatusPanel
from PyQt5.QtWidgets import QWidget
from Settings import Settings

class SyncThread(QObject, Thread):

    log_signal = pyqtSignal(str)
    changed_sync_state_signal = pyqtSignal(str, int, StatusPanel)

    sync_messages = {
        "disable_sync": "La sincronización se encuentra deshabilitada. \
                        <br>Habilitar en <strong>Ajustes</strong>.",
        "file_not_found": "No se encuentra el archivo.",
        "invalid_file_integrity": "Fallo en la integridad del archivo."
    }

    def __init__(self, mainWindow: MainWindow):
        super(SyncThread, self).__init__()
        self.window = mainWindow
        self.flag = {}
        self.__make_connections()

    def __make_connections(self):
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
                self.window.socios_panel
            )
        if not Settings.prestamos_file["enabled"]:
            self.log_signal.emit("La sincronización de 'Préstamos' está desactivada.")
            self.changed_sync_state_signal.emit(
                self.sync_messages["disable_sync"],
                InformationLabel.WARNING,
                self.window.prestamos_panel
            )
        while True:
            flag1 = self.__sync_file(Settings.socios_file, self.window.socios_panel)
            flag2 = self.__sync_file(Settings.prestamos_file, self.window.prestamos_panel)
            if flag1 or flag2:
                Settings.save_files_hash()

            time.sleep(4)

    def __sync_file(self, file_info: dict, panel: QWidget):
        if not file_info["enabled"]:
            return False

        if not path.isfile(file_info["file_path"]) \
            or not path.exists(file_info["file_path"]) \
            or not file_info["file_path"].lower().endswith(".csv"):
            if not self.flag.get(file_info["name"]):
                self.log_signal.emit(
                    'El archivo "{}" no es una ruta válida. \
                    Por favor, verificar en <strong>Ajustes.</strong>'.format(
                        file_info["file_path"]
                    )
                )
                self.changed_sync_state_signal.emit(
                    self.sync_messages["file_not_found"],
                    InformationLabel.ERROR,
                    panel
                )
                self.flag[file_info["name"]] = True
            return False

        if file_info["hash"] == self.get_file_hash(file_info["file_path"]):
            return False
        file_info["hash"] = self.get_file_hash(file_info["file_path"])

        with open(file_info["file_path"], newline='') as csvfile:
            data = list(csv.DictReader(csvfile))
            if not self.check_csv_integrity(data, file_info["fields"]):
                if not self.flag.get(file_info["name"]):
                    self.log_signal.emit(
                        'La integridad del CSV <strong>"{}"</strong> es inválida. \
                        Pueden faltar campos o valores. Por favor verificar \
                        el contenido de este.'.format(file_info["name"])
                    )
                    self.changed_sync_state_signal.emit(
                        self.sync_messages["invalid_file_integrity"],
                        InformationLabel.ERROR,
                        panel
                    )
                    self.flag[file_info["name"]] = True
                return False
        self.write_json(data, file_info["file_path"]+".json")

        self.flag[file_info["name"]] = False
        return True

    def get_file_hash(self, file_path: str) -> str:
        buffersize = 65536

        with open(file_path, 'rb') as afile:
            buffr = afile.read(buffersize)
            crcvalue = 0
            while buffr:
                crcvalue = zlib.crc32(buffr, crcvalue)
                buffr = afile.read(buffersize)

        return hex(crcvalue)

    def check_csv_integrity(self, data: list, fields: list):
        for row in data:
            for field in fields:
                if field[1] and not row.get(field[0]):
                    return False
        return True

    def write_json(self, data, json_file):
        with open(json_file, "w") as f:
            f.write(json.dumps(
                data,
                sort_keys=False,
                indent=4,
                separators=(',', ': ')
            ))
