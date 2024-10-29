# murphy.py

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QWidget, QPushButton, QLabel,
    QVBoxLayout, QHBoxLayout, QSizePolicy
)
from PyQt6.QtCore import Qt
from functools import partial

from base_page import BasePage


class MurphyPage(BasePage):
    def __init__(self, train_data, train_id_callback, tc_communicate, tm_communicate):
        super().__init__("                                    Murphy", train_id_callback)
        self.train_data = train_data
        self.tc_communicate = tc_communicate
        self.tm_communicate = tm_communicate

        # Adjust margins to make the page as big as other pages
        main_content_layout = QVBoxLayout()
        main_content_layout.setContentsMargins(10, 10, 10, 10)  # Adjusted margins
        main_content_layout.setSpacing(10)

        # Container for failure sections
        failures_container = QWidget()
        failures_layout = QVBoxLayout()
        failures_layout.setContentsMargins(20, 20, 20, 20)  # Adjusted margins
        failures_layout.setSpacing(20)  # Adjusted spacing
        failures_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the elements

        # Define failure types with ":" appended
        self.failure_types = {
            "engine_failure": "Engine Failure:",
            "brake_failure": "Brake Failure:",
            "signal_failure": "Signal Pickup Failure:"
        }

        self.failure_buttons = {}

        for var_name, failure_label in self.failure_types.items():
            failure_layout = QHBoxLayout()
            failure_layout.setContentsMargins(0, 0, 0, 0)
            failure_layout.setSpacing(5)  # Adjusted spacing for closer elements

            label = QLabel(failure_label)
            label.setFont(QFont('Arial', 18))
            label.setStyleSheet("color: black;")
            label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

            button = QPushButton("Inactive")
            button.setCheckable(True)
            button.setFont(QFont('Arial', 14, QFont.Weight.Bold))
            button.setFixedSize(160, 60)
            button.setStyleSheet("""
                QPushButton {
                    background-color: green;
                    color: black;
                    border-radius: 5px;
                    font-weight: bold;
                }
                QPushButton:checked {
                    background-color: #8B0000;
                    color: black;
                }
            """)
            button.clicked.connect(partial(self.toggle_failure, var_name, button))

            failure_layout.addWidget(label)
            failure_layout.addWidget(button)
            failure_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center each row

            failures_layout.addLayout(failure_layout)

            self.failure_buttons[var_name] = button

        failures_container.setLayout(failures_layout)
        main_content_layout.addWidget(failures_container)

        # Add main content layout to content_layout
        self.content_layout.addLayout(main_content_layout)

        # Connect data_changed signal
        self.train_data.data_changed.connect(self.update_display)

    def set_train_data(self, train_data):
        # Disconnect previous train_data signal
        try:
            self.train_data.data_changed.disconnect(self.update_display)
        except Exception:
            pass
        self.train_data = train_data
        self.train_data.data_changed.connect(self.update_display)
        self.update_display()

    def toggle_failure(self, var_name, button):
        is_active = button.isChecked()
        button.setText("Active" if is_active else "Inactive")
        # Set button color
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {'#8B0000' if is_active else 'green'};
                color: black;
                border-radius: 5px;
                font-weight: bold;
            }}
        """)
        # Update train data
        self.train_data.set_value(var_name, is_active)
        # Emit failure signal to Train Controller
        if var_name == "engine_failure":
            self.tc_communicate.engine_failure_signal.emit(is_active)
        elif var_name == "brake_failure":
            self.tc_communicate.brake_failure_signal.emit(is_active)
        elif var_name == "signal_failure":
            self.tc_communicate.signal_failure_signal.emit(is_active)

    def update_display(self):
        # Update the state of the failure buttons
        for var_name, button in self.failure_buttons.items():
            is_active = getattr(self.train_data, var_name)
            button.blockSignals(True)
            button.setChecked(is_active)
            button.blockSignals(False)
            button.setText("Active" if is_active else "Inactive")
            button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {'#8B0000' if is_active else 'green'};
                    color: black;
                    border-radius: 5px;
                    font-weight: bold;
                }}
            """)
