import sys
import requests

from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QPushButton,
)
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis, QDateTimeAxis
from PySide6.QtCore import QPointF
from PySide6.QtGui import QPainter
from PySide6.QtGui import QPalette, QColor, QIcon, QCursor
from PySide6.QtCore import Qt, QPoint

import datetime

import qdarktheme

API_ENDPOINT_URL = "http://localhost:1111/api"


# Subclass QMainWindow to customize your application's main window
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

        self.series = QLineSeries()

        self.chart = QChart()
        self.chart.legend().setVisible(True)
        self.chart.addSeries(self.series)

        self.x_axis = QDateTimeAxis()
        self.x_axis.setTickCount(7)
        self.x_axis.setFormat("dd. MM. hh:mm")
        self.x_axis.setTitleText("Date")

        self.y_axis = QValueAxis()
        self.y_axis.setRange(0, 0)
        self.y_axis.setLabelFormat("%0.2f")
        self.y_axis.setTickCount(1)
        self.y_axis.setMinorTickCount(5)
        self.y_axis.setTitleText("Value")

        self.chart.addAxis(self.x_axis, Qt.AlignmentFlag.AlignBottom)
        self.chart.addAxis(self.y_axis, Qt.AlignmentFlag.AlignLeft)

        # self.chart.setTitle("Temperature")

        self._chart_view = QChartView(self.chart)
        self._chart_view.setRenderHint(QPainter.Antialiasing)

        self.tooltip = QLabel("", self._chart_view)
        self.tooltip.setStyleSheet(
            "background-color: white; border: 1px solid black; padding: 5px; font-weight: bold;"
        )
        self.tooltip.setVisible(False)

        layout.addWidget(self._chart_view)

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

            self.chart.removeAllSeries()

            keys = ["temperature", "humidity"]

            y_range = [1000, -1000]

            for key in keys:
                data = week_response_json["data"][key]

                y_data = data["vals"]

                new_series = QLineSeries()

                if key == "temperature":
                    new_series.hovered.connect(
                        lambda point, state: self.show_tooltip(
                            point=point, state=state, format_str="{} °C"
                        )
                    )
                    new_series.setName("Temperature (°C)")
                else:
                    new_series.hovered.connect(
                        lambda point, state: self.show_tooltip(
                            point=point, state=state, format_str="{} %"
                        )
                    )
                    new_series.setName("Humidity (%)")

                for i in range(len(data["timestamps"])):
                    timestamp = data["timestamps"][i]
                    value = data["vals"][i]

                    new_series.append(QPointF(timestamp, value))

                self.chart.addSeries(new_series)

                new_series.attachAxis(self.x_axis)
                new_series.attachAxis(self.y_axis)

                y_min = min(y_data)
                y_max = max(y_data)

                if y_min < y_range[0]:
                    y_range[0] = y_min
                if y_max > y_range[1]:
                    y_range[1] = y_max

            y_range[0] -= 10
            y_range[1] += 10

            self.y_axis.setRange(*y_range)

    def show_tooltip(self, point: QPointF, state: bool, format_str: str = "{}"):
        if state:  # If the point is hovered
            self.tooltip.setText(format_str.format(round(point.y(), 2)))
            self.tooltip.adjustSize()
            cursor_pos = self._chart_view.mapFromGlobal(QCursor.pos())
            cursor_pos += QPoint(5, 1)  # Shift the tooltip so it doesn't close itself
            self.tooltip.move(cursor_pos)

            self.tooltip.setVisible(True)
        else:
            self.tooltip.setVisible(False)


app = QApplication(sys.argv)

qdarktheme.setup_theme("light")
# app.setPalette(QPalette(QColor("#ffffff")))

window = MainWindow()
window.resize(800, 600)
window.setMinimumSize(800, 600) 
window.show()
app.exec()
