from PyQt6 import QtWidgets
from .core.settings import Settings
from .ui.main_window import MainWindow

def run():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setOrganizationName("CGHMaskDesigner")
    app.setApplicationName("Main")
    st = Settings()
    w = MainWindow(st)
    w.show()
    sys.exit(app.exec())
