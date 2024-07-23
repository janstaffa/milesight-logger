import requests

from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import (
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QTableView
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from widgets.chart import Chart
from constants import API_ENDPOINT_URL


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Milesight logger app")
        self.setWindowIcon(QIcon("assets/logo.ico"))
        layout = QVBoxLayout()

        button = QPushButton("Refresh")
        button.clicked.connect(self.refresh_btn_click)

        self.temp_display = QLabel(
            "Temperature: n/a° C", alignment=Qt.AlignmentFlag.AlignTop
        )
        self.hum_display = QLabel(
            "Humidity: n/a %", alignment=Qt.AlignmentFlag.AlignTop
        )
        self.bat_display = QLabel("Battery: n/a %", alignment=Qt.AlignmentFlag.AlignTop)

        layout.addWidget(button)
        layout.addWidget(self.temp_display)
        layout.addWidget(self.hum_display)
        layout.addWidget(self.bat_display)

        self.chart_view = Chart()
        layout.addWidget(self.chart_view)

        widget = QWidget()
        widget.setLayout(layout)

        # Set the central widget of the Window. Widget will expand
        # to take up all the space in the window by default.
        self.setCentralWidget(widget)
        self.fetch_latest_data(fetch_week=True)

    @Slot()
    def refresh_btn_click(self):
        self.fetch_latest_data()

    def fetch_latest_data(self, fetch_week=False):
        latest_response = requests.get(API_ENDPOINT_URL + "/latest")

        latest_response_json = latest_response.json()
        
        self.last_temp = latest_response_json["temp"]
        self.last_hum = latest_response_json["hum"]
        self.last_bat = latest_response_json["bat"]

        self.temp_display.setText("Temperature: " + str(self.last_temp) + " °C")
        self.hum_display.setText("Humidity: " + str(self.last_hum) + " %")
        self.bat_display.setText(
            "Battery: " + str(round(self.last_bat / 255 * 100, 1)) + " %"
        )

        if fetch_week:
            week_response = requests.get(API_ENDPOINT_URL + "/week")
            week_response_json = week_response.json()

            keys = ["temperature", "humidity", "battery"]
            self.chart_view.render_data(week_response_json["data"], keys)
