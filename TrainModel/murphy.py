# murphy.py

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QSizePolicy
)
from PyQt6.QtCore import Qt

from TrainModel.base_page import BasePage

class MurphyPage(BasePage):
    def __init__(self, train_data, tc_communicate, tm_communicate):
        super().__init__("                                    Murphy", self.train_id_changed)
        self.train_data = train_data
        self.tc_communicate = tc_communicate
        self.tm_communicate = tm_communicate

        self.current_train_index = 0  # Default to first train

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

        self.failure_buttons = {}


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
            button.clicked.connect(lambda checked, btn=button, failure=failure: self.toggle_button(btn, failure))

            failure_layout.addWidget(label)
            failure_layout.addWidget(button)
            failure_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center each row

            failures_layout.addLayout(failure_layout)

            self.failure_buttons[failure] = button

        failures_container.setLayout(failures_layout)
        main_content_layout.addWidget(failures_container)

        # Add main content layout to content_layout
        self.content_layout.addLayout(main_content_layout)

        # Connect data changed signal
        self.train_data.data_changed.connect(self.update_display)

        # Initial display update
        self.update_display()

    def toggle_button(self, button, failure):
        index = self.current_train_index
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
            # Implement failure activation logic here
            if failure == "Signal Pickup Failure:":
                self.train_data.signal_failure[index] = True
            elif failure == "Train Engine Failure:":
                self.train_data.engine_failure[index] = True
            elif failure == "Brake Failure:":
                self.train_data.brake_failure[index] = True
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
            # Implement failure deactivation logic here
            if failure == "Signal Pickup Failure:":
                self.train_data.signal_failure[index] = False
            elif failure == "Train Engine Failure:":
                self.train_data.engine_failure[index] = False
            elif failure == "Brake Failure:":
                self.train_data.brake_failure[index] = False
        # Emit data_changed signal
        self.train_data.data_changed.emit()

    def train_id_changed(self, new_train_id):
        """Handle Train ID change."""
        if new_train_id:
            self.current_train_index = int(new_train_id) - 1
            self.update_display()

    def update_train_id_list(self, train_ids):
        """Update the train ID combo box."""
        self.train_id_combo.blockSignals(True)
        self.train_id_combo.clear()
        self.train_id_combo.addItems(train_ids)
        self.train_id_combo.setCurrentIndex(0)
        self.train_id_combo.blockSignals(False)
        # Update current train index
        self.current_train_index = 0
        self.update_display()

    def update_display(self):
        # Update the state of the failure buttons
        index = self.current_train_index
        if len(self.train_data.signal_failure) > 0:
            self.failure_buttons["Signal Pickup Failure:"].setChecked(self.train_data.signal_failure[index])
            self.failure_buttons["Signal Pickup Failure:"].setText("Active" if self.train_data.signal_failure[index] else "Inactive")
            self.failure_buttons["Train Engine Failure:"].setChecked(self.train_data.engine_failure[index])
            self.failure_buttons["Train Engine Failure:"].setText("Active" if self.train_data.engine_failure[index] else "Inactive")
            self.failure_buttons["Brake Failure:"].setChecked(self.train_data.brake_failure[index])
            self.failure_buttons["Brake Failure:"].setText("Active" if self.train_data.brake_failure[index] else "Inactive")
