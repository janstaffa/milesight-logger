import sys
import os

from PySide6.QtWidgets import QApplication, QStyleFactory
from PySide6.QtGui import QPalette, QColor

import datetime

from constants import DEFAULT_API_ENDPOINT_URL
from widgets.main_window import MainWindow

import argparse

parser = argparse.ArgumentParser(prog="Milesight logger client", epilog="by janstaffa")
parser.add_argument("-s", "--server")

args = parser.parse_args()

if args.server == None:
    os.environ["SERVER_URL"] = DEFAULT_API_ENDPOINT_URL
else:
    os.environ["SERVER_URL"] = args.server

app = QApplication(sys.argv)


def setup_theme(app, default_colors=False):
    app.setStyle(QStyleFactory.create("Fusion"))

    if not default_colors:
        light_palette = QPalette()
        light_palette.setColor(QPalette.Window, QColor(255, 255, 255))
        light_palette.setColor(QPalette.WindowText, QColor(0, 0, 0))
        light_palette.setColor(QPalette.Base, QColor(245, 245, 245))
        light_palette.setColor(QPalette.AlternateBase, QColor(255, 255, 255))
        light_palette.setColor(QPalette.ToolTipBase, QColor(0, 0, 0))
        light_palette.setColor(QPalette.ToolTipText, QColor(0, 0, 0))
        light_palette.setColor(QPalette.Text, QColor(0, 0, 0))
        light_palette.setColor(QPalette.Button, QColor(255, 255, 255))
        light_palette.setColor(QPalette.ButtonText, QColor(0, 0, 0))
        light_palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
        light_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        light_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        light_palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))

        app.setPalette(light_palette)


setup_theme(app)


window = MainWindow()
window.resize(800, 600)
window.setMinimumSize(800, 600)
window.show()
app.exec()
