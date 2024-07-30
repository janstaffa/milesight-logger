from PySide6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QPushButton,
    QFrame,
    QComboBox,
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QCursor


TEXT_STYLE = "font-weight: bold"


class DisplaySection(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # Device select box
        self.device_select = QComboBox(self)
        self.device_select.addItems(["One", "Two", "Three"])
        cb_layout = QHBoxLayout()
        device_text = QLabel("EUI -")
        device_text.setStyleSheet(TEXT_STYLE)
        cb_layout.addWidget(device_text)
        cb_layout.addWidget(self.device_select)
        cb_layout.addStretch()


        # Last updated + refresh btn
        l1 = QHBoxLayout()
        last_update_text = QLabel("Last update:")
        last_update_text.setStyleSheet(TEXT_STYLE)
        l1.addWidget(last_update_text, stretch=0)
        self.last_update_display = QLabel("n/a")
        l1.addWidget(self.last_update_display, stretch=1)

        # Divider
        div = QFrame()
        div.setFrameShape(QFrame.HLine)

        # Refresh btn
        self.refresh_btn = QPushButton("\u27f3")
        self.refresh_btn.setMaximumSize(QSize(30, 30))
        self.refresh_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        font = QFont()
        font.setPointSize(10)
        self.refresh_btn.setFont(font)
        l1.addWidget(self.refresh_btn, stretch=0)

        # Temperature
        l2 = QHBoxLayout()
        temperature_text = QLabel("Temperature:")
        temperature_text.setStyleSheet(TEXT_STYLE)
        l2.addWidget(temperature_text)
        self.temp_display = QLabel("n/a °C")
        l2.addWidget(self.temp_display, stretch=1)

        # Humidity
        l3 = QHBoxLayout()
        humidity_text = QLabel("Humidity:")
        humidity_text.setStyleSheet(TEXT_STYLE)
        l3.addWidget(humidity_text)
        self.hum_display = QLabel("n/a %")
        l3.addWidget(self.hum_display, stretch=1)

        # Battery
        l4 = QHBoxLayout()
        battery_text = QLabel("Battery:")
        battery_text.setStyleSheet(TEXT_STYLE)
        l4.addWidget(battery_text)
        self.bat_display = QLabel("n/a %")
        l4.addWidget(self.bat_display, stretch=1)

        layout.addLayout(cb_layout)
        layout.addLayout(l1)
        layout.addWidget(div)
        layout.addLayout(l2)
        layout.addLayout(l3)
        layout.addLayout(l4)

        self.setLayout(layout)

    def set_devices(self, devices: list[str] = []):
        self.device_select.clear()
        self.device_select.addItems(devices)
