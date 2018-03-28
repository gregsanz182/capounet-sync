from PyQt5.QtCore import QSettings
from cryptography.fernet import Fernet

class Settings():
    token_path = "/oauth/token"
    api_path = "/api"
    socios_update_path = "/socios/update"
    secret = b'AvA6jPWRxrZAdQV0RSHAWtZOLrofSOG693XbjSwD6MA='
    access_token = None
    refresh_token = None
    qsettings = None
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
        ]
    }
    prestamos_file = {
        "enabled": True,
        "file_path": "",
        "name": "Socios y Ahorros",
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
        ]
    }
    client_id = None
    client_secret = None
    domain = None
    access_token_expire = None
    refresh_options = [
        "1 Hora",
        "3 Horas",
        "6 Horas",
        "12 Horas"
    ]
    refresh_rate = 0
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
        fernet = Fernet(cls.secret)
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
        cls.qsettings.setValue("others/refresh_rate", cls.refresh_rate)
        cls.qsettings.sync()

    @classmethod
    def load_settings(cls, client_id, client_secret):
        cls.client_id = client_id
        cls.client_secret = client_secret
        cls.qsettings = QSettings("settings.ini", QSettings.IniFormat)
        fernet = Fernet(cls.secret)
        if cls.qsettings.value("tokens/access_token"):
            cls.access_token = cls.get_setting(
                bytes.decode(fernet.decrypt(cls.qsettings.value("tokens/access_token"))))
        if cls.qsettings.value("tokens/refresh_token"):
            cls.refresh_token = cls.get_setting(
                bytes.decode(fernet.decrypt(cls.qsettings.value("tokens/refresh_token"))))
        cls.access_token_expire = cls.qsettings.value("tokens/access_token_expire")
        aux_file = cls.qsettings.value("paths/socios_file_path")
        if aux_file:
            cls.socios_file = aux_file
        aux_file = cls.qsettings.value("paths/prestamos_file_path")
        if aux_file:
            cls.prestamos_file = aux_file
        cls.refresh_rate = cls.qsettings.value("others/refresh_rate")
        if not cls.refresh_rate:
            cls.refresh_rate = 0
        else:
            cls.refresh_rate = int(cls.refresh_rate)

    @classmethod
    def get_setting(cls, setting):
        parts = setting.split(" ")
        if len(parts) == 3 and parts[1] == cls.client_secret and int(parts[2]) == cls.client_id:
            return parts[0]
        return None

    @classmethod
    def is_init(cls):
        if cls.access_token and cls.refresh_token:
            return True
        return False

    @classmethod
    def get_token_url(cls):
        return cls.domain + cls.token_path

    @classmethod
    def save_files_hash(cls):
        cls.qsettings.setValue("paths/socios_file_path", cls.socios_file)
        cls.qsettings.setValue("paths/prestamos_file_path", cls.prestamos_file)
