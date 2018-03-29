# -*- coding: utf-8 -*-
"""Este módulo contiene la clase Settings, encargada de guardar las preferencias y configuraciones
de la aplicación"""

from PyQt5.QtCore import QSettings
from cryptography.fernet import Fernet

class Settings():
    __token_path = "/oauth/token"
    __api_path = "/api"
    __secret = b'AvA6jPWRxrZAdQV0RSHAWtZOLrofSOG693XbjSwD6MA='
    access_token = None
    refresh_token = None
    qsettings = None
    qsetting_files = None
    socios_file = {
        "enabled": True,
        "file_path": "",
        "name": "Socios y Ahorros",
        "hash": "",
        "fields": [
            ("cedula", True),
            ("nombre", True),
            ("f_ingreso", False),
            ("tot_aho_acum", True),
            ("tot_ret_acum", True),
            ("dispon_ahorro", True)
        ],
        "resource_path": "/socios/update",
        "last_sync": ""
    }
    prestamos_file = {
        "enabled": True,
        "file_path": "",
        "name": "Prestamos",
        "hash": "",
        "fields": [
            ("cedula", True),
            ("concedido", True),
            ("amortizado", True),
            ("saldo", True),
            ("f_inicio", True),
            ("f_fin", True),
            ("descuento", True),
            ("cod_pres", True),
            ("nom_pres", True),
            ("cuo_a_canc", True),
            ("cuo_canc", True)
        ],
        "resource_path": "/prestamos/update",
        "last_sync": ""
    }
    client_id = None
    client_secret = None
    domain = None
    access_token_expire = None
    global_style = """
        QLabel{
            color: #BDBDBD;
        }
        QLineEdit{
            font-size: 13px; 
            height: 18px;
        }
        QPushButton#normal_button{
            height: 25px; 
            background-color: #232629;
        }
        QPushButton#accept_button{
            height: 25px; 
            background-color: #3DAEE9; 
            border-color: #515962;
        }
        QComboBox QAbstractItemView::item {
            min-height: 25px;
        }
    """

    @classmethod
    def save_settings(cls):
        fernet = Fernet(cls.__secret)
        if cls.access_token:
            cls.qsettings.setValue(
                "tokens/access_token",
                fernet.encrypt(str.encode("{} {} {}".format(
                    cls.access_token,
                    cls.client_secret,
                    cls.client_id))))
        if cls.refresh_token:
            cls.qsettings.setValue(
                "tokens/refresh_token",
                fernet.encrypt(str.encode("{} {} {}".format(
                    cls.refresh_token,
                    cls.client_secret,
                    cls.client_id))))
        if cls.access_token_expire:
            cls.qsettings.setValue("tokens/access_token_expire", cls.access_token_expire)
        cls.qsettings.setValue("paths/socios_file_path", cls.socios_file)
        cls.qsettings.setValue("paths/prestamos_file_path", cls.prestamos_file)
        cls.qsettings.setValue("urls/domain", cls.domain)
        cls.qsettings.sync()

    @classmethod
    def load_settings(cls, client_id: int, client_secret: str):
        cls.client_id = client_id
        cls.client_secret = client_secret
        cls.qsettings = QSettings("settings.ini", QSettings.IniFormat)
        cls.qsettings_files = QSettings("files_info.ini", QSettings.IniFormat)
        fernet = Fernet(cls.__secret)
        if cls.qsettings.value("tokens/access_token"):
            cls.access_token = cls.__get_setting(
                bytes.decode(fernet.decrypt(cls.qsettings.value("tokens/access_token"))))
        if cls.qsettings.value("tokens/refresh_token"):
            cls.refresh_token = cls.__get_setting(
                bytes.decode(fernet.decrypt(cls.qsettings.value("tokens/refresh_token"))))
        cls.access_token_expire = cls.qsettings.value("tokens/access_token_expire")
        aux_file = cls.qsettings.value("paths/socios_file_path")
        if aux_file:
            cls.socios_file.update(aux_file)
            cls.socios_file["hash"] = cls.qsettings_files.value("socios/hash")
            cls.socios_file["last_sync"] = cls.qsettings_files.value("socios/last_sync")
        aux_file = cls.qsettings.value("paths/prestamos_file_path")
        if aux_file:
            cls.prestamos_file.update(aux_file)
            cls.prestamos_file["hash"] = cls.qsettings_files.value("prestamos/hash")
            cls.prestamos_file["last_sync"] = cls.qsettings_files.value("prestamos/last_sync")
        cls.domain = cls.qsettings.value("urls/domain")

    @classmethod
    def __get_setting(cls, setting: str) -> str:
        parts = setting.split(" ")
        if len(parts) == 3 and parts[1] == cls.client_secret and int(parts[2]) == cls.client_id:
            return parts[0]
        return None

    @classmethod
    def is_init(cls) -> bool:
        if cls.access_token and cls.refresh_token:
            return True
        return False

    @classmethod
    def get_token_url(cls) -> str:
        return cls.domain + cls.__token_path

    @classmethod
    def get_api_resource_url(cls, resource_url: str) -> str:
        return cls.domain + cls.__api_path + resource_url

    @classmethod
    def save_files_hash(cls):
        cls.qsettings_files.setValue("socios/hash", cls.socios_file["hash"])
        cls.qsettings_files.setValue("prestamos/hash", cls.prestamos_file["hash"])
        cls.qsettings_files.setValue("socios/last_sync", cls.socios_file["last_sync"])
        cls.qsettings_files.setValue("prestamos/last_sync", cls.prestamos_file["last_sync"])
