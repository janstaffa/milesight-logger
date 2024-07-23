import sys

from PySide6.QtWidgets import QApplication

import datetime

from widgets.main_window import MainWindow
import qdarktheme



app = QApplication(sys.argv)

qdarktheme.setup_theme("light")
# app.setPalette(QPalette(QColor("#ffffff")))

window = MainWindow()
window.resize(800, 600)
window.setMinimumSize(800, 600)
window.show()
app.exec()
