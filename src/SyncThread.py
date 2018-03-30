import time
import zlib
import csv
import json
from datetime import datetime
from threading import Thread
from os import path
from MainWindow import MainWindow
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QWidget
from GuiTools import MessageType, StatusPanel
from Settings import Settings
from RequestsHandler import RequestsHandler, RequestsHandlerException, GeneralConnectionError

class SyncThread(QObject, Thread):

    log_signal = pyqtSignal(str)
    changed_sync_state_signal = pyqtSignal(str, MessageType, StatusPanel)
    runThread = True

    sync_messages = {
        "disable_sync": "La sincronización se encuentra deshabilitada. \
                        <br>Habilitar en <strong>Ajustes</strong>.",
        "file_not_found": "No se encuentra el archivo.",
        "invalid_file_integrity": "Fallo en la integridad del archivo.",
        "connection_error": "Error en la conexión.",
        "request_error": "Error en el envio de información.",
        "all_ok": "Todo funciona correctamente."
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
                MessageType.WARNING,
                self.window.socios_panel
            )
        if not Settings.prestamos_file["enabled"]:
            self.log_signal.emit("La sincronización de 'Préstamos' está desactivada.")
            self.changed_sync_state_signal.emit(
                self.sync_messages["disable_sync"],
                MessageType.WARNING,
                self.window.prestamos_panel
            )
        self.__change_last_sync(Settings.socios_file, self.window.socios_panel)
        self.__change_last_sync(Settings.prestamos_file, self.window.prestamos_panel)
        while self.runThread:
            flag1 = self.__sync_file(Settings.socios_file, self.window.socios_panel)
            flag2 = False
            #self.__sync_file(Settings.prestamos_file, self.window.prestamos_panel)
            if flag1 or flag2:
                Settings.save_files_hash()

            time.sleep(20)

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
                    MessageType.ERROR,
                    panel
                )
                self.flag[file_info["name"]] = True
            return False

        if file_info["hash"] == self.get_file_hash(file_info["file_path"]):
            return False

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
                        MessageType.ERROR,
                        panel
                    )
                    self.flag[file_info["name"]] = True
                return False

        data_http = {
            "data": json.dumps(data)
        }
        try:
            RequestsHandler.send_data_to_api(data_http, file_info["resource_path"])
        except GeneralConnectionError as exception:
            self.log_signal.emit("No se pudo acceder al servidor.")
            self.changed_sync_state_signal(
                self.sync_messages["connection_error"],
                MessageType.ERROR,
                panel
            )
            self.flag[file_info["name"]] = True
            return
        except RequestsHandlerException as exception:
            self.log_signal.emit("Ocurrió un error en el envio de información.")
            self.log_signal.emit(exception.message)
            self.changed_sync_state_signal(
                self.sync_messages["request_error"],
                MessageType.ERROR,
                panel
            )
            self.flag[file_info["name"]] = True
            return

        self.flag[file_info["name"]] = False
        file_info["hash"] = self.get_file_hash(file_info["file_path"])
        self.log_signal.emit(
            "Archivo<strong> {} </strong>sincronizado correctamente.".format(file_info["name"])
        )
        self.changed_sync_state_signal.emit(
            self.sync_messages["all_ok"],
            MessageType.SUCCESS,
            panel
        )
        file_info["last_sync"] = datetime.now().strftime("%H:%M %d-%m-%Y")
        self.__change_last_sync(file_info, panel)
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

    def __change_last_sync(self, file_info: dict, panel: QWidget):
        self.changed_sync_state_signal.emit(
            file_info["last_sync"],
            MessageType.DATE,
            panel
        )

    def stop_sync(self):
        self.runThread = False

    def write_json(self, data, json_file):
        with open(json_file, "w") as f:
            f.write(json.dumps(
                data,
                sort_keys=False,
                indent=4,
                separators=(',', ': ')
            ))
