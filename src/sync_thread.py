# -*- coding: utf-8 -*-
# This file is part of CAPOUNET Sync.
#
# CAPOUNET Sync
# Copyright (C) 2018  Gregory Sánchez and Anny Chacón
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
""" Este módulo contiene la clase SyncThread encargada del manejo del hilo de sincronización."""
import time
import zlib
import csv
import json
from datetime import datetime
from threading import Thread
from os import path
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QWidget

from main_window import MainWindow
from gui_tools import MessageType, StatusPanel
from settings import Settings
from request_handler import RequestsHandler, RequestsHandlerException

class SyncThread(QObject, Thread):
    """Clase encargada del manejo del hilo de sincronización

    Note:
        La configuración de la aplicación debe haber sido cargada previamente. Para esto llamar
        a Settings.load_settings().

    Attributes:
        log_signal (pyqtSignal): Señal a llamar cuando se desea registrar un evento en el log
        gráfico.
        sync_state_signal (pyqtSignal): Señal a llamar cuando se desea mostrar un cambio en los
        paneles de status.
        run_thread (bool): True si el hilo debe correr. False si se debe detener.
        window (MainWindow): Ventana principal de la aplicación.
        flag (QLineEdit): Banderas de estado de ejecución del hilo. Usadas para informar cuando ya
        ocurrió un error y no se desea volver a mostrarlo.
        sync_messages (dict): Diccionario con los mensajes predefinidos para cada estado de sincro-
        nización.
    """

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
        """Constructor de la clase. Construye e inicializa una instancia de SyncThread.

        Note:
            Antes de instanciar un objeto de esta clase, la configuración del programa debe haber
            sido cargada. Para esto llamar a Settings.load_settings().

        Args:
            mainWindow (QWidget): Ventana principal de la aplicación.
        """
        super(SyncThread, self).__init__()
        self.window = mainWindow
        self.flag = {}
        self.log_signal.connect(self.window.print_log)
        self.sync_state_signal.connect(self.set_sync_state)

    def run(self):
        """Método a ejecutar cuando por el hilo.

        Se encarga de realizar toda la tarea de sincronización de los archivos y de mostrar los
        debidos mensajes en la interfaz gráfica (Ventana Pricipal).
        """
        self.log_signal.emit("Inicializando...")
        self.log_signal.emit("Leyendo configuracion...")
        self.__change_last_sync(Settings.socios_file, self.window.socios_panel)
        self.__change_last_sync(Settings.prestamos_file, self.window.prestamos_panel)
        self.log_signal.emit("Iniciado correctamente.")
        self.log_signal.emit("Listo.")
        while self.run_thread:
            self.__sync_file(Settings.socios_file, self.window.socios_panel)
            self.__sync_file(Settings.prestamos_file, self.window.prestamos_panel)
            Settings.save_files_hash()
            if self.flag \
            and any(flag_value != self.ALL_OK for flag_key, flag_value in self.flag.items()):
                self.window.tray_icon.setIcon(Settings.sync_error_icon)
            else:
                self.window.tray_icon.setIcon(Settings.sync_icon)

            time.sleep(5)

    def __sync_file(self, file_info: dict, panel: QWidget):
        """Sincroniza el archivo especificado en file_info.

        Se encarga de revisar si existen cambios en el archivo a sincronizar. Luego verifica que
        la información contenida sea válida y por último intenta enviar la información al servidor
        por medio de la API.

        Args:
            file_info (dict): Información del archivo a sincronizar.
            panel (QWidget): Panel de estado del archivo a sincronizar. Utilizado para mostrar los
            cambios y mensajes de estado.

        Note:
            Esta función no debe ser llamada desde el exterior, puesto que su uso es interno en la
            clase.
        """
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
            file_info["hash"] = ""
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
            file_info["hash"] = ""
            return False

        if file_info["hash"] == self.get_file_checksum(file_info["file_path"]):
            return False

        csvfile = open(file_info["file_path"], newline='')
        try:
            data = list(csv.DictReader(csvfile))
        except UnicodeDecodeError:
            csvfile = open(file_info["file_path"], newline='', encoding='cp1252')
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
            file_info["hash"] = ""
            csvfile.close()
            return False
        csvfile.close()

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
            file_info["hash"] = ""
            return

        self.flag[file_info["name"]] = self.ALL_OK
        file_info["hash"] = self.get_file_checksum(file_info["file_path"])
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
    def get_file_checksum(file_path: str) -> str:
        """Devuelve el checksum CRC32 del archivo especificado.

        Args:
            file_path (str): Ruta del fichero.

        Returns:
            str: Checksum crc32 del fichero analizado.
        """
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
        """Válida la integridad del fichero CSV.

        Verifica que la información contenida en data sea válidad utilizando los campos pasados en
        fields.

        Args:
            data (list): Listado con la data extraida del CSV.
            fields (list): Listado con los campos a verificar.

        Returns:
            bool: True si la data analizada es válida. False en caso contrario.
        """
        for row in data:
            for field in fields:
                if field[1] and not row.get(field[0]):
                    return False
        return True

    def __change_last_sync(self, file_info: dict, panel: QWidget):
        """Cambia la fecha de la última sincronización correcta.

        Args:
            file_info (dict): Información del fichero.
            panel (QWidget): Panel de estado a modificar.
        """
        self.sync_state_signal.emit(
            file_info["last_sync"],
            MessageType.DATE,
            panel
        )

    def stop_sync(self):
        """Detiene la sincronización. En otras palabras, detiene el hilo cuando se haya terminado la
        operación actual.
        """
        self.run_thread = False

    @staticmethod
    def write_json(data, json_file):
        """Permite escribir un archivo .json con la data pasada por parámetro.

        Args:
            data: Información a escribir.
            json_file: Ruta del fichero a escribir.

        Note:
            Este método fue creado para ser utilizado en la depuración de errores.
        """
        with open(json_file, "w") as jfile:
            jfile.write(json.dumps(
                data,
                sort_keys=False,
                indent=4,
                separators=(',', ': ')
            ))

    @staticmethod
    def write_html(data, html_file):
        """Permite escribir un archivo .html con la data pasada por parámetro. Útil para mostrar las
        respuestas del servidor API.

        Args:
            data: Información a escribir.
            html_file: Ruta del fichero a escribir.

        Note:
            Este método fue creado para ser utilizado en la depuración de errores.
        """
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
