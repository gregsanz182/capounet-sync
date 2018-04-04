# -*- coding: utf-8 -*-
"""Este módulo proporciona una clase para el manejo de las configuraciones del programa."""

from PyQt5.QtCore import QSettings, QStandardPaths
from PyQt5.QtGui import QIcon
from cryptography.fernet import Fernet

class Settings():
    """Esta clase proporciona variables y métodos para el manejo de preferencias y configuraciones.

    Proporciona objetos, variables y métodos para la carga y el guardado de las configuraciones
    de la aplicación.
    Esta clase contiene, en su mayoria, métodos de clase, por lo que no es necesario instanciar
    la clase en un objeto.
    Se accede a los métodos y atributos por medio del nombre de la clase, y esta puede ser utilizada
    de manera global en toda el programa.

    Note:
        Antes de empezar a utilizar esta clase, se debe llamar a Settings.load_settings() y pasarle
        los argumentos requeridos.

    Attributes:
        __token_path (str): Ruta relativa para la obtención de los tokens de acceso. Para uso
            interno en la clase.
        __api_path (str): Ruta relativa para el acceso a la API. Para uso interno en la clase.
        __secret (bytes): Secreto de aplicación utilizado para encriptar cierta información.
        access_token (str): Token de acceso a la API.
        refresh_token (str): Token de refresco para obtener un nuevo token de acceso.
        qsettings (QSettings): Objeto de QSettings que permite guardar y cargar las configuraciones
            del programa.
        qsettings_files (QSettings): Objeto que permite guardar y cargar la última fecha de
            sincronización de los archivos y los hash de cada uno.
        socios_file (dict): Contiene información importante para el manejo del archivo 'Ahorros y
            socios'.
        prestamos_file (dict): Contiene información importante para el manejo del archivo
            'Prestamos'.
        client_id (int): ID del cliente en la API. Debe obtenerse cuando se llama a load_settings().
        client_secret (str): Secreto del cliente en la API. Debe obtenerse cuando se llama a
            load_settings().
        domain (str): Dirección URL del dominio de la API.
        access_token_expire (int): Contiene el tiempo de expiración del token de acceso.
        global_style (str): Contiene el estilo css que se debe utilizar en todos los componentes de
            la aplicación.
    """
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
    app_icon = None
    sync_icon = None
    sync_error_icon = None

    @classmethod
    def save_settings(cls):
        """Guarda la configuración de la aplicación en el disco duro o en memoria permanente.

        Utiliza qsettings para guardar las preferencias de la aplicación en memoria permanente.
        Dicha configuración es guardada en un archivo (settings.ini) ubicado en la carpeta del
        usuario en el sistema.

        El token de acceso y de refresco son codificados antes de ser guardados. Esto no asegura
        una encriptación segura de los datos, sino que solo sirve para ocultarlos de la mirada
        casual de intrusos.

        Note:
            Antes de utilizar este método, debe haberse cargado al menos una vez la configuración
            incial a través de load_settings()
        """
        #Se instancia un objeto Fernet con el secreto de la aplicación
        fernet = Fernet(cls.__secret)

        if cls.access_token:
            #Solo se guarda el token de acceso si este existe.
            #Para codificar el token, se guarda junto a el secreto e ID del cliente.
            cls.qsettings.setValue(
                "tokens/access_token",
                fernet.encrypt(str.encode("{} {} {}".format(
                    cls.access_token,
                    cls.client_secret,
                    cls.client_id))))

        if cls.refresh_token:
            #Solo se guarda el token de refresco si este existe.
            #Para codificar el token, se guarda junto a el secreto e ID del cliente.
            cls.qsettings.setValue(
                "tokens/refresh_token",
                fernet.encrypt(str.encode("{} {} {}".format(
                    cls.refresh_token,
                    cls.client_secret,
                    cls.client_id))))

        if cls.access_token_expire:
            #Solo se guarda tiempo de expiración si este existe.
            cls.qsettings.setValue("tokens/access_token_expire", cls.access_token_expire)

        #Aqui solo se guarda la habilitación de la sincronizacion y la ruta del archivo a
        #sincronizar.
        cls.qsettings.setValue(
            "paths/socios_file_path",
            {k: v for k, v in cls.socios_file.items() if k in ("enabled", "file_path")}
        )
        cls.qsettings.setValue(
            "paths/prestamos_file_path",
            {k: v for k, v in cls.prestamos_file.items() if k in ("enabled", "file_path")}
        )

        cls.qsettings.setValue("urls/domain", cls.domain)
        cls.qsettings.sync()

    @classmethod
    def load_settings(cls, client_id: int, client_secret: str):
        """Carga las configuraciones y preferencias de la aplicación.

        Además incializa los archivos settings.ini y files_info.ini si no han sido creados.
        Este método debe ser llamado al menos una vez en el uso de la aplicación. Se recomienda que
        sea al principio.

        Args:
            client_id (int): ID del cliente en la API.
            client_secret (str): Secreto del cliente en la API.
        """
        cls.client_id = client_id
        cls.client_secret = client_secret
        config_path = QStandardPaths.standardLocations(QStandardPaths.DataLocation)[0]
        cls.qsettings = QSettings("{}/settings.ini".format(config_path), QSettings.IniFormat)
        cls.qsettings_files = QSettings("{}/files_info.ini".format(config_path), QSettings.IniFormat)

        #Se instancia un objeto Fernet con el secreto de la aplicación
        fernet = Fernet(cls.__secret)

        #Si el token está guardado se obtiene y se decodifica
        if cls.qsettings.value("tokens/access_token"):
            cls.access_token = cls.__get_setting(
                bytes.decode(fernet.decrypt(cls.qsettings.value("tokens/access_token"))))

        #Si el token está guardado se obtiene y se decodifica
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

        cls.app_icon = QIcon("res/icons/app_icon.ico")
        cls.sync_icon = QIcon("res/icons/sync_icon.ico")
        cls.sync_error_icon = QIcon("res/icons/sync_error_icon.ico")

    @classmethod
    def __get_setting(cls, setting: str) -> str:
        """Decodifica el setting.

        Args:
            setting (str): Configuracion a decodificar

        Returns:
            str: Configuración decodificada. Devuelve None si la codificación es incorrecta.
        """
        parts = setting.split(" ")
        if len(parts) == 3 and parts[1] == cls.client_secret and int(parts[2]) == cls.client_id:
            return parts[0]
        return None

    @classmethod
    def is_init(cls) -> bool:
        """Verifica si existen los tokens de acceso y refresco en la configuración.

        Returns:
            bool: True si ambos tokens existen, False en caso contrario.
        """
        if cls.access_token and cls.refresh_token:
            return True
        return False

    @classmethod
    def get_token_url(cls) -> str:
        """Devuelve el URL para obtener los tokens de acceso.

        Returns:
            str: Ruta para obtener el token de acceso en la API.
        """
        return cls.domain + cls.__token_path

    @classmethod
    def get_api_resource_url(cls, resource_url: str) -> str:
        """Devuelve el URL para acceder a los recursos de la API.

        Returns:
            str: Ruta para acceder a los recursos de la API.
        """
        return cls.domain + cls.__api_path + resource_url

    @classmethod
    def save_files_hash(cls):
        """Guarda en disco el hash del último archivo sincronizado correctamente, asi como también
        la fecha de la última sincronización de cada archivo.
        """
        cls.qsettings_files.setValue("socios/hash", cls.socios_file["hash"])
        cls.qsettings_files.setValue("prestamos/hash", cls.prestamos_file["hash"])
        cls.qsettings_files.setValue("socios/last_sync", cls.socios_file["last_sync"])
        cls.qsettings_files.setValue("prestamos/last_sync", cls.prestamos_file["last_sync"])
        cls.qsettings_files.sync()
