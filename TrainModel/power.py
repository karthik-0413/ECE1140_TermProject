# power.py

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt


class SetCommandedPowerDialog(QDialog):
    def __init__(self, parent=None, current_power=0):
        super().__init__(parent)
        self.setWindowTitle("Set Commanded Power")
        self.setFixedSize(400, 200)

        layout = QVBoxLayout()

        # Current Commanded Power Display
        self.current_power_label = QLabel(f"Current Commanded Power: {current_power} kW")
        self.current_power_label.setFont(QFont('Arial', 14))
        self.current_power_label.setStyleSheet("color: black;")
        layout.addWidget(self.current_power_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Input Field
        self.label = QLabel("Enter the Commanded Power (kW):")
        self.label.setFont(QFont('Arial', 14))
        self.label.setStyleSheet("color: black;")
        layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.power_edit = QLineEdit(str(current_power))
        self.power_edit.setFont(QFont('Arial', 14))
        self.power_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.power_edit.setStyleSheet("color: black;")
        layout.addWidget(self.power_edit, alignment=Qt.AlignmentFlag.AlignCenter)

        # Buttons layout
        buttons_layout = QHBoxLayout()
        self.ok_button = QPushButton("OK")
        self.ok_button.setFont(QFont('Arial', 12, QFont.Weight.Bold))
        self.ok_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: black;
                border: 2px solid black;
                border-radius: 5px;
                padding: 5px 15px;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """)
        self.ok_button.clicked.connect(self.accept)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setFont(QFont('Arial', 12, QFont.Weight.Bold))
        self.cancel_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: black;
                border: 2px solid black;
                border-radius: 5px;
                padding: 5px 15px;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """)
        self.cancel_button.clicked.connect(self.reject)

        buttons_layout.addWidget(self.ok_button)
        buttons_layout.addWidget(self.cancel_button)

        layout.addLayout(buttons_layout)

        self.setLayout(layout)

    def get_commanded_power(self):
        try:
            power = float(self.power_edit.text())
            if power < 0:
                raise ValueError
            return power
        except ValueError:
            return None  # Invalid input
