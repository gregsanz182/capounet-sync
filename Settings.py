from PyQt5.QtCore import QSettings, QCryptographicHash
from cryptography.fernet import Fernet

class Settings():
    tokenPath = "/oauth/token"
    apiPath = "/api"
    sociosUpdatePath = "/socios/update"
    secret = b'AvA6jPWRxrZAdQV0RSHAWtZOLrofSOG693XbjSwD6MA='
    accessToken = None
    refreshToken = None
    QSettings = None
    sociosFilePath = (True, "")
    prestamosFilePath = (True, "")
    clientID = None
    clientSecret = None
    domain = None
    accessTokenExpire = None
    refreshOptions = [
        "1 Hora",
        "3 Horas",
        "6 Horas",
        "12 Horas"
    ]
    refreshRate = 0
    globalStyle = """
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
    def saveSettings(cls):
        f = Fernet(cls.secret)
        if cls.accessToken:
            cls.qsettings.setValue("tokens/access_token", f.encrypt(str.encode("{} {} {}".format(cls.accessToken, cls.clientSecret, cls.clientID))))
        if cls.refreshToken:
            cls.qsettings.setValue("tokens/refresh_token", f.encrypt(str.encode("{} {} {}".format(cls.refreshToken, cls.clientSecret, cls.clientID))))
        if cls.accessTokenExpire:
            cls.qsettings.setValue("tokens/access_token_expire", cls.accessTokenExpire)
        cls.qsettings.setValue("paths/socios_file_path", cls.sociosFilePath)
        cls.qsettings.setValue("paths/prestamos_file_path", cls.prestamosFilePath)
        cls.qsettings.setValue("others/refresh_rate", cls.refreshRate)
        cls.qsettings.sync()

    @classmethod
    def loadSettings(cls, client_id, client_secret):
        cls.clientID = client_id
        cls.clientSecret = client_secret
        cls.qsettings = QSettings("settings.ini", QSettings.IniFormat)
        f = Fernet(cls.secret)
        if cls.qsettings.value("tokens/access_token"):
            cls.accessToken = cls.getSetting(bytes.decode(f.decrypt(cls.qsettings.value("tokens/access_token"))))
        if cls.qsettings.value("tokens/refresh_token"):
            cls.refreshToken = cls.getSetting(bytes.decode(f.decrypt(cls.qsettings.value("tokens/refresh_token"))))
        cls.accessTokenExpire = cls.qsettings.value("tokens/access_token_expire")
        cls.sociosFilePath = cls.qsettings.value("paths/socios_file_path")
        if cls.sociosFilePath is None:
            cls.sociosFilePath = (True, "")
        cls.prestamosFilePath = cls.qsettings.value("paths/prestamos_file_path")
        if cls.prestamosFilePath is None:
            cls.prestamosFilePath = (True, "")
        cls.refreshRate = cls.qsettings.value("others/refresh_rate")
        if cls.refreshRate is None:
            cls.refreshRate = 0
        else:
            cls.refreshRate = int(cls.refreshRate)

    @classmethod
    def getSetting(cls, setting):
        parts = setting.split(" ")
        if len(parts) == 3 and parts[1] == cls.clientSecret and int(parts[2]) == cls.clientID:
            return parts[0]
        return None

    @classmethod
    def isInit(cls):
        if cls.accessToken and cls.refreshToken:
            return True
        return False

    @classmethod
    def getTokenUrl(cls):
        return cls.domain + cls.tokenPath