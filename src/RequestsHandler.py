# -*- coding: utf-8 -*-
"""Este módulo proporciona métodos para en el envio de peticiones al servidor API restful."""

import requests
from Settings import Settings

class RequestsHandler():
    """Clase encargada de manejar el envio de peticiones al servidor API.

    Define métodos necesarios para el envio de peticiones y el manejo de las respuestas.
    Puesto que la mayoría de los métodos son estáticos, no es necesario instanciar esta clase.

    Note:
        Cualquiera de los mñetodos de esta clase deben ser utilizados cuando Settings ya haya sido
        cargada a través de Settings.load_configuration()

    Note:
        Se recomienda tener un claro entendimiento del estándar OAUTH2 para poder entender los
        métodos y las peticiones realizadas.
    """

    @staticmethod
    def get_access_token(username: str, password: str, domain: str):
        """Obtiene los tokens de acceso y refresco a través de las credenciales de un cliente.

        Método estático que realiza la petición de token de acceso y refresco a la API por medio
        de OAuth2 Password Grant.

        Note:
            Para utilizar este método la configuración del programa debe haber sido previamente
            cargada a través de Settings.load_configuration().

        Args:
            username (str): Nombre se usuario.
            password (str): Contraseña del usuario.
            domain (str): URL del dominio de la API.

        Returns:
            dict: Respuesta del servidor con el token de acceso y el token de refresco.
            Opcionalmente se retorna tambien la expiración del token de acceso.

        Raises:
            InvalidURL: La URL del servidor es inválida.
            InalidAuthentication: Los datos del usuario o del cliente son invalidos.
            InternalServerError: Error interno del servidor. Puede que los datos que se estén
                pasando sean incorrectos o que la validación en el servidor es incorrecta.
            RequestError: Error en la petición. El código HTTP es devuelto junto a la excepción.
            MissingSchema: Posible ausencia de http:// o https:// en la URL del dominio.
            GeneralConnectionError: Indica un error en la conexión, ya sea porque el servidor está
                caido o porque no hay conexión a internet en la máquina donde corre el programa.
        """
        Settings.domain = domain

        #Contenido de la petición. Para comprender los parametros, se debe tener un buen
        #de OAUTH2. Cada uno de los campos están definidos en la documentacion de Laravel Passport.
        data = {
            "grant_type": "password",
            "client_id": Settings.client_id,
            "client_secret": Settings.client_secret,
            "username": username,
            "password": password,
            "scope": "*"
        }
        try:
            request = requests.post(Settings.get_token_url(), data=data)
            if request.status_code == 200:
                return request.json()
            if request.status_code == 404:
                raise InvalidURL()
            if request.status_code == 401:
                raise InvalidAuthentication()
            if request.status_code == 500:
                raise InternalServerError()
            raise RequestError(request.status_code)
        except requests.exceptions.InvalidURL as exception:
            raise InvalidURL(exception)
        except requests.exceptions.MissingSchema as exception:
            raise MissingSchema(exception)
        except requests.exceptions.ConnectionError as exception:
            raise GeneralConnectionError(exception)

    @staticmethod
    def send_data_to_api(data: dict, url: str):
        """Envia los datos extraidos de uno de los archivos.

        Método estático que realiza el envio de los datos de sincronización al servidor.
        Este método utiliza el token de acceso previamente obtenido y guardado en Settings.

        Note:
            Para utilizar este método la configuración del programa debe haber sido previamente
            cargada a través de Settings.load_configuration().

        Args:
            data (dict): Contenido a enviar como un formulario post. Ver documentación de la API.
            url (str): URL del recurso en la API.

        Returns:
            dict: Respuesta del servidor con un mensaje de éxito.

        Raises:
            InvalidURL: La URL del servidor es inválida.
            InalidAuthentication: Los datos del usuario o del cliente son invalidos.
            InternalServerError: Error interno del servidor. Puede que los datos que se estén
                pasando sean incorrectos o que la validación en el servidor es incorrecta.
            RequestError: Error en la petición. El código HTTP es devuelto junto a la excepción.
            MissingSchema: Posible ausencia de http:// o https:// en la URL del dominio.
            GeneralConnectionError: Indica un error en la conexión, ya sea porque el servidor está
                caido o porque no hay conexión a internet en la máquina donde corre el programa.
        """
        headers = {
            "Authorization": 'Bearer ' + Settings.access_token
        }
        try:
            request = requests.post(Settings.get_api_resource_url(url), headers=headers, data=data)
            if request.status_code == 200:
                return request.json()
            if request.status_code == 404:
                raise InvalidURL()
            if request.status_code == 401:
                raise InvalidAuthentication()
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
    """Define una excepción general de RequestHandler.
    """
    def __init__(self, message: str, original_exception=None):
        """
        Args:
            message (str): Mensaje a mostrar por la excepción.
            original_exception: Excepción original que causó el llamado de esta excepción.
        """
        super().__init__(message)
        self.message = message
        self.original_exception = original_exception

class InvalidURL(RequestsHandlerException):
    """Define una excepción de URL inválida.
    """

    def __init__(self, original_exception=None):
        """
        Args:
            original_exception: Excepción original que causó el llamado de esta excepción.
        """
        super().__init__("La URL del dominio no es válida.", original_exception)

class InternalServerError(RequestsHandlerException):
    """Define una excepción de Error interno del servidor.
    """

    def __init__(self, original_exception=None):
        """
        Args:
            original_exception: Excepción original que causó el llamado de esta excepción.
        """
        super().__init__("Error interno del servidor (500)", original_exception)

class RequestError(RequestsHandlerException):
    """Define una excepción de error en la petición.
    """

    def __init__(self, http_code: int, original_exception=None):
        """
        Args:
            http_code (int): Código HTTP de la respuesta.
            original_exception: Excepción original que causó el llamado de esta excepción.
        """
        super().__init__(
            "Ocurrió un error en la petición.\nCódigo HTTP: {}".format(http_code),
            original_exception)

class InvalidAuthentication(RequestsHandlerException):
    """Define una excepción de autenticación inválida.
    """

    def __init__(self, original_exception=None):
        """
        Args:
            original_exception: Excepción original que causó el llamado de esta excepción.
        """
        super().__init__("Credenciales incorrectas.", original_exception)

class MissingSchema(RequestsHandlerException):
    """Define una excepción URL sin http:// o https://.
    """

    def __init__(self, original_exception=None):
        """
        Args:
            original_exception: Excepción original que causó el llamado de esta excepción.
        """
        super().__init__(
            "El dominio no es valido.\nVerifica que incluya 'http://' o 'https://'",
            original_exception)

class GeneralConnectionError(RequestsHandlerException):
    """Define una excepción de error en la conexión.
    """

    def __init__(self, original_exception=None):
        """
        Args:
            original_exception: Excepción original que causó el llamado de esta excepción.
        """
        super().__init__(
            "Error en la conexión.\nVerifica que exista conexión a internet y vuelve a intentarlo.",
            original_exception)
