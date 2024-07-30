from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QWidget,
    QVBoxLayout,
    QCheckBox,
    QHBoxLayout,
)
from PySide6.QtCharts import (
    QChart,
    QChartView,
    QLineSeries,
    QValueAxis,
    QDateTimeAxis,
)
from PySide6.QtCore import QPointF
from PySide6.QtGui import QPainter
from PySide6.QtGui import QCursor
from PySide6.QtCore import Qt, QPoint, QMargins
from constants import CHART_Y_RANGE_PADDING
import numpy as np


class Chart(QWidget):
    def __init__(self):
        super().__init__()

        v_layout = QVBoxLayout()

        self.temperature_check = QCheckBox("Temperature", self)
        self.temperature_check.setChecked(True)
        self.humidity_check = QCheckBox("Humidity", self)
        self.humidity_check.setChecked(True)
        self.battery_check = QCheckBox("Battery", self)

        checkboxes = [self.temperature_check, self.humidity_check, self.battery_check]

        h_layout = QHBoxLayout()

        for ch in checkboxes:
            ch.stateChanged.connect(lambda: self.update_chart())
            h_layout.addWidget(ch)

        h_layout.addStretch()
        v_layout.addLayout(h_layout, stretch=0)

        self.chart = QChart()
        self.chart.legend().setVisible(True)
        self.chart.setMargins(QMargins(0, 0, 0, 0))

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

        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        v_layout.addWidget(self.chart_view, stretch=1)

        self.tooltip = QLabel("", self.chart_view)
        self.tooltip.setStyleSheet(
            "background-color: white; border: 1px solid black; padding: 5px; font-weight: bold;"
        )
        self.tooltip.setVisible(False)

        self.setLayout(v_layout)

    def show_tooltip(self, point: QPointF, state: bool, format_str: str = "{}"):
        if state:  # If the point is hovered
            self.tooltip.setText(format_str.format(round(point.y(), 2)))
            self.tooltip.adjustSize()
            cursor_pos = self.chart_view.mapFromGlobal(QCursor.pos())
            cursor_pos += QPoint(5, 1)  # Shift the tooltip so it doesn't close itself
            self.tooltip.move(cursor_pos)

            self.tooltip.setVisible(True)
        else:
            self.tooltip.setVisible(False)

    def clear_series(self):
        self.chart.removeAllSeries()

    def add_series(self, new_series):
        self.chart.addSeries(new_series)

        new_series.attachAxis(self.x_axis)
        new_series.attachAxis(self.y_axis)

    def update_chart(self):
        for key in self.loaded_series:
            self.loaded_series[key].hide()

        checked = {
            "temperature": self.temperature_check.isChecked(),
            "humidity": self.humidity_check.isChecked(),
            "battery": self.battery_check.isChecked(),
        }
        if checked["temperature"]:
            self.loaded_series["temperature"].show()
        if checked["humidity"]:
            self.loaded_series["humidity"].show()
        if checked["battery"]:
            self.loaded_series["battery"].show()

        y_range = [1000, -1000]
        for key in self.loaded_series_ranges:
            if checked[key]:
                (y_min, y_max) = self.loaded_series_ranges[key]

                if y_min < y_range[0]:
                    y_range[0] = y_min
                if y_max > y_range[1]:
                    y_range[1] = y_max

        y_range[0] -= CHART_Y_RANGE_PADDING
        y_range[1] += CHART_Y_RANGE_PADDING

        self.y_axis.setRange(*y_range)

    def render_data(self, data):
        self.clear_series()

        self.data = data


        self.loaded_series = dict({})
        self.loaded_series_ranges = dict({})

        keys = ["temperature", "humidity", "battery"]
        for key in keys:
            d = data[key]
            y_data = np.array(d["vals"])

            if key == "battery":  # Convert to % if the key is battery
                y_data /= 255
                y_data *= 100
                y_data = np.round(y_data, 2)

            new_series = QLineSeries()

            match key:
                case "temperature":
                    new_series.hovered.connect(
                        lambda point, state: self.show_tooltip(
                            point=point, state=state, format_str="{} °C"
                        )
                    )
                    new_series.setName("Temperature (°C)")

                case "humidity":
                    new_series.hovered.connect(
                        lambda point, state: self.show_tooltip(
                            point=point, state=state, format_str="{} %"
                        )
                    )
                    new_series.setName("Humidity (%)")

                case "battery":
                    new_series.hovered.connect(
                        lambda point, state: self.show_tooltip(
                            point=point, state=state, format_str="{} %"
                        )
                    )
                    new_series.setName("Battery (%)")

                case _:
                    raise f"Invalid key: {key}"

            for i in range(len(d["timestamps"])):
                timestamp = d["timestamps"][i]
                value = y_data[i]

                new_series.append(QPointF(timestamp, value))

            self.loaded_series[key] = new_series
            self.add_series(self.loaded_series[key])

            y_min = min(y_data)
            y_max = max(y_data)

            self.loaded_series_ranges[key] = (y_min, y_max)

        self.update_chart()
