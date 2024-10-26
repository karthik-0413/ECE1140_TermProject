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
    def __init__(self, train_data, train_id_callback):
        super().__init__("                                    Murphy", train_id_callback)
        self.train_data = train_data

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
        failure_types = ["Signal Pickup Failure:", "Train Engine Failure:", "Brake Failure:"]

        for failure in failure_types:
            failure_layout = QHBoxLayout()
            failure_layout.setContentsMargins(0, 0, 0, 0)
            failure_layout.setSpacing(5)  # Adjusted spacing for closer elements

            label = QLabel(failure)
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
            button.clicked.connect(partial(self.toggle_button, button))

            failure_layout.addWidget(label)
            failure_layout.addWidget(button)
            failure_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center each row

            failures_layout.addLayout(failure_layout)

        failures_container.setLayout(failures_layout)
        main_content_layout.addWidget(failures_container)

        # Add main content layout to content_layout
        self.content_layout.addLayout(main_content_layout)

        # Connect data_changed signal if needed
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

    def toggle_button(self, button):
        if button.isChecked():
            button.setText("Active")
            # Set bloody red color
            button.setStyleSheet("""
                QPushButton {
                    background-color: #8B0000;
                    color: black;
                    border-radius: 5px;
                    font-weight: bold;
                }
            """)
        else:
            button.setText("Inactive")
            button.setStyleSheet("""
                QPushButton {
                    background-color: green;
                    color: black;
                    border-radius: 5px;
                    font-weight: bold;
                }
            """)

    def update_display(self):
        pass  # Add any display updates if needed
