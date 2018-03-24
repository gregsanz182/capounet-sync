from PyQt5.QtCore import QSettings

class Settings():
    apiPath = "/api"
    sociosUpdatePath = "/socios/update"

    def __init__(self, clientID, clientSecret, domain):
        self.accessToken = None
        self.refreshToken = None
        self.clientID = clientID
        self.clientSecret = clientSecret
        self.domain = domain
        self.ahorrosWebFile = None

    def loadSettings(self):
        settings = QSettings("settings.ini", QSettings.IniFormat)
        self.accessToken = settings.value("tokens/access_token")
        self.refreshToken = settings.value("tokens/resfresh_token")
        self.ahorrosWebFile = settings.value("paths/ahorros_web_file")
