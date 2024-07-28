from PySide6.QtWidgets import (
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QPushButton,
    QTableView,
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QColor


class DisplaySection(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()


        # Last updated + refresh btn
        l1 = QHBoxLayout()
        l1.addWidget(QLabel("Last update:"), stretch=0)
        self.last_update_display = QLabel("n/a")
        l1.addWidget(self.last_update_display, stretch=1)
        
        self.refresh_btn = QPushButton("\u27f3")
        self.refresh_btn.setMaximumSize(QSize(30, 30))
        font = QFont()
        font.setPointSize(10)
        self.refresh_btn.setFont(font)
        l1.addWidget(self.refresh_btn, stretch=0)

        

        # Temperature
        l2 = QHBoxLayout()
        l2.addWidget(QLabel("Temperature:"))
        self.temp_display = QLabel("n/a °C")
        l2.addWidget(self.temp_display, stretch=1)
        
        # Humidity
        l3 = QHBoxLayout()
        l3.addWidget(QLabel("Humidity:"))
        self.hum_display = QLabel("n/a %")
        l3.addWidget(self.hum_display, stretch=1)
        
        # Battery
        l4 = QHBoxLayout()
        l4.addWidget(QLabel("Battery:"))
        self.bat_display = QLabel("n/a %")
        l4.addWidget(self.bat_display, stretch=1)

        layout.addLayout(l1)
        layout.addLayout(l2)
        layout.addLayout(l3)
        layout.addLayout(l4)

        self.setLayout(layout)
