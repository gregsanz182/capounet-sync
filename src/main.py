import sys
import qdarkstyle
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QCoreApplication
from Settings import Settings
from MainWindow import MainWindow
from AccessDialog import AccessDialog
from OptionsDialog import OptionsDialog
from SyncThread import SyncThread

def main():
    try:
        main_app = QApplication(sys.argv)
        main_app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        QCoreApplication.setApplicationName("CAPOUNET Sync")
        QCoreApplication.setOrganizationName("CAPOOUNET")
        QCoreApplication.setOrganizationDomain("capounet.unet.edu.ve")
        Settings.load_settings(2, "8jwf7A0DbakpJ7p4HKCPJXJogwGFyWPkDLsDYngx")
        main_app.setWindowIcon(Settings.app_icon)
        return_code = 1

        if not Settings.is_init():
            return_code = AccessDialog.obtain_configuration()
            if return_code == 1:
                return_code = OptionsDialog.open_dialog()

        if return_code == 1:
            main_window = MainWindow()
            main_window.show()
            sync_thread = SyncThread(main_window)
            sync_thread.start()
            main_app.exec_()
            sync_thread.stop_sync()

        sys.exit(0)

    except NameError:
        print("Nombre del error:", sys.exc_info()[1])
    except SystemExit:
        print("Cerrando la ventana...")

if __name__ == "__main__":
    main()

    

    """with open('AHORROSWEB.CSV', newline='') as csvfile:
        reader = list(csv.DictReader(csvfile))
        auth_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjgxMzRkNDlkOGQ4MGExNTBjY2U2NzE4Y2Y1OTk2NDVhZTFkNGE2NWU5NjhjZTVlYjE2MmRhMDUzNDc3OTE0MzI2ZTY0YjcxMDlkOTM2Y2I1In0.eyJhdWQiOiIyIiwianRpIjoiODEzNGQ0OWQ4ZDgwYTE1MGNjZTY3MThjZjU5OTY0NWFlMWQ0YTY1ZTk2OGNlNWViMTYyZGEwNTM0Nzc5MTQzMjZlNjRiNzEwOWQ5MzZjYjUiLCJpYXQiOjE1MjE4NTA2OTAsIm5iZiI6MTUyMTg1MDY5MCwiZXhwIjoxNTUzMzg2Njg5LCJzdWIiOiIxIiwic2NvcGVzIjpbIioiXX0.NKveH4zOhrzRIlIEQ-flktRzkVvxnCy7zplhCtALhWTC-aFFGbVMhzLfQIRQehi_7DkTeSQwG4pl7zcLKpt4k1qbnRROGlKDMFEFyfGeORlDyCiTTe3CSLxXdHmkf9fhYrERXSyZFuF91qxwSEU6SWdoSn-s0SdiLs53_O1fiaZbP-37GpIHW7HOhmQ83y26pm9WNXdKGIEjaI5WF77yf8b6Fz2yoUtRs8W51Bv9IOAwwfTd3l6VTnV9G7Bo8LVYn7PeVxqES2yMVjG9iXWNsuM4Mr5Lq7rhZDq2VIWLt8yNzAJQHyiZ1-pk0rcz4xbgijdYMtN3yvfk4kuvHNOdw1vrRLaUMbARLHGgZXpLp2aCPBpg8OXDQFBG6z-KWeL0cT7t5rbWUMv22sM5WK_p1zLA6aGY6sI5bMhxa1MK5Nbw6cdjMVo9vMKYGe4ua7isct29uY9nfhCppWSbAo2ZTFkKg0PAt53XW0v50XultvZhCmgk3YukXlcEK58-JXnsoRJ7KoXFDLh77801BPrHIvJ0eqzAKydQnnCzfzd0Dw5g2wiOc8uRukm8wmrjbdUuWhh1tb85wecYpTUZaBQXd7wElXzapoPkVNpu15cZVp6BDEcyA_wcb1xR8D_Dauj7yynOlsbnwul_MuHppZwMF2r0dkEnwKdMmUl89F903Ig"
        headers = {
            "Authorization": 'Bearer ' + auth_token
        }
        data = {
            "socios": json.dumps(reader)
        }
        r = requests.post("http://capounet.test/api/socios/update", headers=headers, data=data)
        print(r)"""
    