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
        try:
            r = requests.post(Settings.getTokenUrl(), data=data)
            if r.status_code == 200:
                return r.json()
            if r.status_code == 404:
                raise RequestsHandlerException("La URL del dominio no es válida.")
            if r.status_code == 401:
                raise RequestsHandlerException("Credenciales incorrectas")
            if r.status_code == 500:
                raise RequestsHandlerException("Error interno del servidor (500)")
            raise RequestsHandlerException("Ocurrió un error en la petición.\nCódigo HTTP: {}".format(r.status_code))
        except requests.exceptions.InvalidURL as e:
            raise RequestsHandlerException("La URL del dominio no es válida.", e)
        except requests.exceptions.MissingSchema as e:
            raise RequestsHandlerException("El dominio no es valido.\nVerifica que incluya 'http://' o 'https://'", e)
        except requests.exceptions.ConnectionError as e:
            raise RequestsHandlerException("Error en la conexión.\nVerifica que exista conexión a internet y vuelve a intentarlo.", e)
        except requests.exceptions.ConnectTimeout as e:
            raise RequestsHandlerException("Error en la conexión.\nVerifica que exista conexión a internet y vuelve a intentarlo.", e)

class RequestsHandlerException(ValueError):

    def __init__(self, message, original_exception=None):
        super().__init__(message)
        self.message = message
        self.original_exception = original_exception
