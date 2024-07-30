import requests

from PySide6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QWidget,
)
from PySide6.QtGui import QIcon
from utils import *
from widgets.display_section import DisplaySection
from widgets.chart import Chart
from constants import API_ENDPOINT_URL
from time import gmtime, strftime
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.devices = []

        self.setWindowTitle("Milesight logger app")
        self.setWindowIcon(QIcon("assets/logo.ico"))

        main_layout = QVBoxLayout()

        self.display_section = DisplaySection()

        self.display_section.device_select.currentTextChanged.connect(
            lambda t: self.fetch_latest_data(t, fetch_week=True)
        )

        self.display_section.refresh_btn.clicked.connect(self.refresh_btn_click)

        main_layout.addWidget(self.display_section, stretch=0)

        self.chart_widget = Chart()
        main_layout.addWidget(self.chart_widget, stretch=1)

        widget = QWidget()
        widget.setLayout(main_layout)

        self.setCentralWidget(widget)

        self.fetch_device_list()
        if len(self.devices) == 0:
            InfoMessage("No devices logged on the server").exec()
            sys.exit()

    def refresh_btn_click(self):
        if len(self.devices) == 0:
            InfoMessage("No devices logged on the server").exec()
            sys.exit()

        self.fetch_latest_data(self.devices[0], fetch_week=True)

    def set_loading_state(self):
        self.display_section.temp_display.setText("-")
        self.display_section.hum_display.setText("-")
        self.display_section.bat_display.setText("-")
        self.display_section.last_update_display.setText("-")

        self.chart_widget.clear_series()
        self.display_section.temp_display.repaint()
        self.display_section.hum_display.repaint()
        self.display_section.bat_display.repaint()
        self.display_section.last_update_display.repaint()

    def fetch_latest_data(self, device_eui, fetch_week=False):
        if device_eui == None or len(device_eui) == "" or device_eui == "":
            return

        self.set_loading_state()
        try:
            latest_response = requests.get(
                API_ENDPOINT_URL + "/latest", params={"device": device_eui}
            )
            data = process_server_response(latest_response)

            now_str = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            self.display_section.last_update_display.setText(now_str)

            self.last_temp = data["temp"]
            self.last_hum = data["hum"]
            self.last_bat = data["bat"]

            self.display_section.temp_display.setText(str(self.last_temp) + " °C")
            self.display_section.hum_display.setText(str(self.last_hum) + " %")
            bat_perc = round(self.last_bat / 255 * 100, 1)
            self.display_section.bat_display.setText(str(bat_perc) + " %")
        except Exception as error:
            ErrorMessage(title="Request failed", msg=str(error)).exec()

        if fetch_week:
            week_response = requests.get(
                API_ENDPOINT_URL + "/week", params={"device": device_eui}
            )
            try:
                data = process_server_response(week_response)
                self.chart_widget.render_data(data["data"])

            except Exception as error:
                ErrorMessage(title="Request failed", msg=str(error)).exec()

    def fetch_device_list(self):
        try:
            response = requests.get(API_ENDPOINT_URL + "/devices")
            device_list = process_server_response(response)

            self.devices = device_list
            self.display_section.set_devices(device_list)

        except Exception as error:
            ErrorMessage(title="Request failed", msg=str(error)).exec()
