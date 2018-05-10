import sys
import qdarkstyle
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QCoreApplication
from Settings import Settings
from MainWindow import MainWindow
from AccessDialog import AccessDialog
from OptionsDialog import OptionsDialog
from SyncThread import SyncThread
from QtSingleApplication import QtSingleApplication

def main():
    client_id = 2
    client_secret = "O3cKUlA2SbAaG1HG6Celyjn2UBAZoJ6s7QSm42CK"
    try:
        main_app = QtSingleApplication(client_secret, sys.argv)
        if main_app.isRunning():
            sys.exit(0)
        QCoreApplication.setApplicationName("CAPOUNET Sync")
        QCoreApplication.setOrganizationName("CAPOUNET")
        QCoreApplication.setOrganizationDomain("capounet.unet.edu.ve")

        Settings.load_settings(client_id, client_secret)
        main_app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        main_app.setWindowIcon(Settings.app_icon)

        return_code = 1
        while return_code:
            return_code = 2
            if not Settings.is_init():
                Settings.delete_settings()
                return_code = AccessDialog.obtain_configuration()
                if return_code == 1:
                    return_code = OptionsDialog.open_dialog()

            if return_code >= 1:
                main_window = MainWindow()
                sync_thread = SyncThread(main_window)
                sync_thread.start()
                if return_code == 1:
                    main_window.show()
                return_code = main_app.exec_()
                sync_thread.stop_sync()
                main_window.close()
                sync_thread.join()
                if return_code:
                    Settings.delete_settings()
                    Settings.load_settings(client_id, client_secret)

        sys.exit(0)

    except NameError:
        print("Nombre del error:", sys.exc_info()[1])
    except SystemExit:
        print("Cerrando la ventana...")

if __name__ == "__main__":
    main()
