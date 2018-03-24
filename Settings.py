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
    ahorrosWebFile = None
    clientID = None
    clientSecret = None
    domain = None

    @classmethod
    def saveSettings(cls):
        f = Fernet(cls.secret)
        if cls.accessToken:
            cls.qsettings.setValue("tokens/access_token", f.encrypt(str.encode("{} {} {}".format(cls.accessToken, cls.clientSecret, cls.clientID))))
        if cls.refreshToken:
            cls.qsettings.setValue("tokens/refresh_token", f.encrypt(str.encode("{} {} {}".format(cls.refreshToken, cls.clientSecret, cls.clientID))))
        if cls.ahorrosWebFile:
            cls.qsettings.setValue("paths/ahorros_web_file")
        cls.qsettings.sync()

    @classmethod
    def loadSettings(cls, client_id, client_secret):
        cls.clientID = client_id
        cls.clientSecret = client_secret
        cls.qsettings = QSettings("settings.ini", QSettings.IniFormat)
        f = Fernet(cls.secret)
        if cls.qsettings.value("tokens/access_token"):
            cls.accessToken = cls.getSetting(f.decrypt(cls.qsettings.value("tokens/access_token")))
        if cls.qsettings.value("tokens/refresh_token"):
            cls.refreshToken = cls.getSetting(f.decrypt(cls.qsettings.value("tokens/refresh_token")))
        cls.ahorrosWebFile = cls.qsettings.value("paths/ahorros_web_file")

    @classmethod
    def getSetting(cls, setting):
        parts = setting.split(" ")
        if len(parts) == 3 and parts[1] == cls.clientSecret and parts[2] == cls.clientID:
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