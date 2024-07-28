import requests

from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import (
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QTableView,
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from widgets.display_section import DisplaySection
from widgets.chart import Chart
from constants import API_ENDPOINT_URL
from time import gmtime, strftime

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Milesight logger app")
        self.setWindowIcon(QIcon("assets/logo.ico"))

        main_layout = QVBoxLayout()
        self.display_section = DisplaySection()
        self.display_section.refresh_btn.clicked.connect(self.refresh_btn_click)

        main_layout.addWidget(self.display_section)

        self.chart_view = Chart()
        main_layout.addWidget(self.chart_view)

        widget = QWidget()
        widget.setLayout(main_layout)

        self.setCentralWidget(widget)
        self.fetch_latest_data(fetch_week=True)

    def refresh_btn_click(self):
        self.fetch_latest_data()

    def fetch_latest_data(self, fetch_week=False):
        latest_response = requests.get(API_ENDPOINT_URL + "/latest")
        latest_response_json = latest_response.json()
        
        now_str = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        self.display_section.last_update_display.setText(now_str)

        self.last_temp = latest_response_json["temp"]
        self.last_hum = latest_response_json["hum"]
        self.last_bat = latest_response_json["bat"]

        self.display_section.temp_display.setText(str(self.last_temp) + " °C")
        self.display_section.hum_display.setText(str(self.last_hum) + " %")
        bat_perc = round(self.last_bat / 255 * 100, 1)
        self.display_section.bat_display.setText(str(bat_perc) + " %")

        if fetch_week:
            week_response = requests.get(API_ENDPOINT_URL + "/week")
            week_response_json = week_response.json()

            keys = ["temperature", "humidity", "battery"]
            self.chart_view.render_data(week_response_json["data"], keys)
