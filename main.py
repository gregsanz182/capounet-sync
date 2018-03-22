import sys
from PyQt5.QtWidgets import QApplication
from MainWindow import MainWindow

if __name__ == "__main__":
    try:
        mainApp = QApplication(sys.argv)

        mainWindow = MainWindow()
        mainWindow.show()

        mainApp.exec_()
        sys.exit(0)

    except NameError:
        print("Nombre del error:", sys.exc_info()[1])
    except SystemExit:
        print("Cerrando la ventana...")
    except Exception:
        print(sys.exc_info()[1])
    