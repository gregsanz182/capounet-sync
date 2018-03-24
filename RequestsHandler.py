import requests
from Settings import Settings

class RequestsHandler():

    @staticmethod
    def getAccessToken(username, password, domain):
        Settings.domain = domain
        data = {
            "grant_type": "password",
            "client_id": Settings.clientID,
            "client_secret": Settings.clientSecret,
            "username": username,
            "password": password,
            "scope": "*"
        }
        print(data)
        r = requests.post(Settings.getTokenUrl(), data=data)
        print(r)
