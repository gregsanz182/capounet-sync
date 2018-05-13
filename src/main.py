# -*- coding: utf-8 -*-
# This file is part of CAPOUNET Sync.
#
# CAPOUNET Sync
# Copyright (C) 2018  Gregory Sánchez and Anny Chacón
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import qdarkstyle
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
