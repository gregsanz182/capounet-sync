import requests
from Settings import Settings

class RequestsHandler():

    @staticmethod
    def get_access_token(username, password, domain):
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
            request = requests.post(Settings.getTokenUrl(), data=data)
            if request.status_code == 200:
                return request.json()
            if request.status_code == 404:
                raise InvalidURL()
            if request.status_code == 401:
                raise InvalidAuthetication()
            if request.status_code == 500:
                raise InternalServerError()
            raise RequestError(request.status_code)
        except requests.exceptions.InvalidURL as exception:
            raise InvalidURL(exception)
        except requests.exceptions.MissingSchema as exception:
            raise MissingSchema(exception)
        except requests.exceptions.ConnectionError as exception:
            raise GeneralConnectionError(exception)

class RequestsHandlerException(Exception):

    def __init__(self, message, original_exception=None):
        super().__init__(message)
        self.message = message
        self.original_exception = original_exception

class InvalidURL(RequestsHandlerException):

    def __init__(self, original_exception=None):
        super().__init__("La URL del dominio no es válida.", original_exception)

class InternalServerError(RequestsHandlerException):

    def __init__(self, original_exception=None):
        super().__init__("Error interno del servidor (500)", original_exception)

class RequestError(RequestsHandlerException):

    def __init__(self, http_code, original_exception=None):
        super().__init__(
            "Ocurrió un error en la petición.\nCódigo HTTP: {}".format(http_code),
            original_exception)

class InvalidAuthetication(RequestsHandlerException):

    def __init__(self, original_exception=None):
        super().__init__("Credenciales incorrectas.", original_exception)

class MissingSchema(RequestsHandlerException):

    def __init__(self, original_exception=None):
        super().__init__(
            "El dominio no es valido.\nVerifica que incluya 'http://' o 'https://'",
            original_exception)

class GeneralConnectionError(RequestsHandlerException):

    def __init__(self, original_exception=None):
        super().__init__(
            "Error en la conexión.\nVerifica que exista conexión a internet y vuelve a intentarlo.",
            original_exception)
