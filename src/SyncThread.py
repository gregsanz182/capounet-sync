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
from RequestsHandler import RequestsHandler, RequestsHandlerException

class SyncThread(QObject, Thread):

    log_signal = pyqtSignal(str)
    sync_state_signal = pyqtSignal(str, MessageType, StatusPanel)
    run_thread = True

    ALL_OK = 230
    DISABLED_SYNC = 231
    FILE_NOT_FOUND = 232
    INVALID_FILE_INTEGRITY = 233
    REQUEST_ERROR = 234

    sync_messages = {
        DISABLED_SYNC: "La sincronización se encuentra deshabilitada. \
                        <br>Habilitar en <strong>Ajustes</strong>.",
        FILE_NOT_FOUND: "No se encuentra el archivo.",
        INVALID_FILE_INTEGRITY: "Fallo en la integridad del archivo.",
        REQUEST_ERROR: "Error en el envio de información.",
        ALL_OK: "Todo funciona correctamente."
    }

    def __init__(self, mainWindow: MainWindow):
        super(SyncThread, self).__init__()
        self.window = mainWindow
        self.flag = {}
        self.__make_connections()

    def __make_connections(self):
        self.log_signal.connect(self.window.print_log)
        self.sync_state_signal.connect(self.set_sync_state)

    def run(self):
        self.log_signal.emit("Inicializando...")
        self.log_signal.emit("Leyendo configuracion...")
        self.__change_last_sync(Settings.socios_file, self.window.socios_panel)
        self.__change_last_sync(Settings.prestamos_file, self.window.prestamos_panel)
        while self.run_thread:
            flag1 = self.__sync_file(Settings.socios_file, self.window.socios_panel)
            flag2 = self.__sync_file(Settings.prestamos_file, self.window.prestamos_panel)
            if flag1 or flag2:
                Settings.save_files_hash()
            if self.flag and all(flag == self.ALL_OK for flag in self.flag):
                self.window.tray_icon.setIcon(Settings.sync_error_icon)
            else:
                self.window.tray_icon.setIcon(Settings.sync_icon)

            time.sleep(5)

    def __sync_file(self, file_info: dict, panel: QWidget):
        if not file_info["enabled"]:
            if self.flag.get(file_info["name"]) != self.DISABLED_SYNC:
                self.log_signal.emit(
                    'La sincronización de "{}" está desactivada.'.format(file_info['name'])
                )
                self.sync_state_signal.emit(
                    self.sync_messages[self.DISABLED_SYNC],
                    MessageType.WARNING,
                    panel
                )
                self.flag[file_info["name"]] = self.DISABLED_SYNC
            return False

        if not path.isfile(file_info["file_path"]) \
            or not path.exists(file_info["file_path"]) \
            or not file_info["file_path"].lower().endswith(".csv"):
            if self.flag.get(file_info["name"]) != self.FILE_NOT_FOUND:
                self.log_signal.emit(
                    'El archivo "{}" no es una ruta válida. \
                    Por favor, verificar en <strong>Ajustes.</strong>'.format(
                        file_info["file_path"]
                    )
                )
                self.sync_state_signal.emit(
                    self.sync_messages[self.FILE_NOT_FOUND],
                    MessageType.ERROR,
                    panel
                )
                self.flag[file_info["name"]] = self.FILE_NOT_FOUND
            return False

        if file_info["hash"] == self.get_file_hash(file_info["file_path"]):
            return False

        with open(file_info["file_path"], newline='') as csvfile:
            data = list(csv.DictReader(csvfile))
            if not self.check_csv_integrity(data, file_info["fields"]):
                if self.flag.get(file_info["name"]) != self.INVALID_FILE_INTEGRITY:
                    self.log_signal.emit(
                        'La integridad del CSV <strong>"{}"</strong> es inválida. \
                        Pueden faltar campos o valores. Por favor verificar \
                        el contenido de este.'.format(file_info["name"])
                    )
                    self.sync_state_signal.emit(
                        self.sync_messages[self.INVALID_FILE_INTEGRITY],
                        MessageType.ERROR,
                        panel
                    )
                    self.flag[file_info["name"]] = self.INVALID_FILE_INTEGRITY
                return False
        try:
            RequestsHandler.send_data_to_api(data, file_info["resource_path"])
        except RequestsHandlerException as exception:
            if self.flag.get(file_info["name"]) != exception.code:
                self.log_signal.emit(exception.message)
                self.sync_state_signal.emit(
                    self.sync_messages[self.REQUEST_ERROR],
                    MessageType.ERROR,
                    panel
                )
                self.flag[file_info["name"]] = exception.code
            return

        self.flag[file_info["name"]] = self.ALL_OK
        file_info["hash"] = self.get_file_hash(file_info["file_path"])
        self.log_signal.emit(
            "Archivo<strong> {} </strong>sincronizado correctamente.".format(file_info["name"])
        )
        self.sync_state_signal.emit(
            self.sync_messages[self.ALL_OK],
            MessageType.SUCCESS,
            panel
        )
        file_info["last_sync"] = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.__change_last_sync(file_info, panel)
        return True

    @staticmethod
    def get_file_hash(file_path: str) -> str:
        buffersize = 65536

        with open(file_path, 'rb') as afile:
            buffr = afile.read(buffersize)
            crcvalue = 0
            while buffr:
                crcvalue = zlib.crc32(buffr, crcvalue)
                buffr = afile.read(buffersize)

        return hex(crcvalue)

    @staticmethod
    def check_csv_integrity(data: list, fields: list):
        for row in data:
            for field in fields:
                if field[1] and not row.get(field[0]):
                    return False
        return True

    def __change_last_sync(self, file_info: dict, panel: QWidget):
        self.sync_state_signal.emit(
            file_info["last_sync"],
            MessageType.DATE,
            panel
        )

    def stop_sync(self):
        self.run_thread = False

    @staticmethod
    def write_json(data, json_file):
        with open(json_file, "w") as jfile:
            jfile.write(json.dumps(
                data,
                sort_keys=False,
                indent=4,
                separators=(',', ': ')
            ))

    @staticmethod
    def write_html(data, html_file):
        with open(html_file, "w") as jfile:
            jfile.write(data)

    @staticmethod
    def set_sync_state(string: str, message_type: MessageType, status_panel: StatusPanel):
        """Slot que cambia el estado de sincronización en el StatusPanel indicado por parámetro.

        Args:
            string (str): Mensaje a mostrar.
            message_type (MessageType): Tipo de mensaje.
            status_panel (StatusPanel): Panel al que se le asignará el mensaje.
        """
        status_panel.change_message(string, message_type)
