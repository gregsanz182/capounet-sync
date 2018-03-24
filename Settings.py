from PyQt5.QtCore import QSettings, QCryptographicHash
from cryptography.fernet import Fernet

class Settings():
    apiPath = "/api"
    sociosUpdatePath = "/socios/update"
    secret = b'AvA6jPWRxrZAdQV0RSHAWtZOLrofSOG693XbjSwD6MA='

    def __init__(self, clientID, clientSecret, domain):
        self.accessToken = None
        self.refreshToken = None
        self.clientID = clientID
        self.clientSecret = clientSecret
        self.domain = domain
        self.ahorrosWebFile = None
        self.qsettings = QSettings("settings.ini", QSettings.IniFormat)
        self.loadSettings()

    def saveSettings(self):
        f = Fernet(self.secret)
        if self.accessToken:
            self.qsettings.setValue("tokens/access_token", f.encrypt(str.encode("{} {} {}".format(self.accessToken, self.clientSecret, self.clientID))))
        if self.refreshToken:
            self.qsettings.setValue("tokens/refresh_token", f.encrypt(str.encode("{} {} {}".format(self.refreshToken, self.clientSecret, self.clientID))))
        if self.ahorrosWebFile:
            self.qsettings.setValue("paths/ahorros_web_file")
        self.qsettings.sync()

    def loadSettings(self):
        f = Fernet(self.secret)
        if self.qsettings.value("tokens/access_token"):
            self.accessToken = self.getSetting(f.decrypt(self.qsettings.value("tokens/access_token")))
        if self.qsettings.value("tokens/refresh_token"):
            self.refreshToken = self.getSetting(f.decrypt(self.qsettings.value("tokens/refresh_token")))
        self.ahorrosWebFile = self.qsettings.value("paths/ahorros_web_file")

    def getSetting(self, setting):
        parts = setting.split(" ")
        if len(parts) == 3 and parts[1] == self.clientSecret and parts[2] == self.clientID:
            return parts[0]
        return None

    def isInit(self):
        if self.accessToken and self.refreshToken:
            return True
        return False



