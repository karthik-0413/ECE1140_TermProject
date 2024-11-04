# murphy.py

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy
)
from PyQt6.QtCore import Qt

from base_page import BasePage


class MurphyPage(BasePage):
    """Page representing Murphy's interface for simulating failures."""

    def __init__(self, train_data, tc_communicate, tm_communicate):
        super().__init__("                                    Murphy", self.train_id_changed)
        self.train_data = train_data
        self.tc_communicate = tc_communicate
        self.tm_communicate = tm_communicate

        self.current_train_index = 0  # Default to first train

        # Adjust margins to make the page as big as other pages
        main_content_layout = QVBoxLayout()
        main_content_layout.setContentsMargins(10, 10, 10, 10)  # Adjusted margins
        main_content_layout.setSpacing(20)  # Increased spacing for better layout

        # Container for failure sections
        failures_container = QWidget()
        failures_layout = QVBoxLayout()
        failures_layout.setContentsMargins(20, 20, 20, 20)  # Adjusted margins
        failures_layout.setSpacing(30)  # Increased spacing between failure types
        failures_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the elements

        # Define failure types with ":" appended
        failure_types = ["Signal Pickup Failure:", "Train Engine Failure:", "Brake Failure:"]
        self.failure_buttons = {}

        for failure in failure_types:
            failure_layout = QHBoxLayout()
            failure_layout.setContentsMargins(0, 0, 0, 0)
            failure_layout.setSpacing(10)  # Adjusted spacing for closer elements

            label = QLabel(failure)
            label.setFont(QFont('Arial', 24, QFont.Weight.Bold))  # Increased font size
            label.setStyleSheet("color: black;")
            label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

            button = QPushButton("Inactive")
            button.setCheckable(True)
            button.setFont(QFont('Arial', 20, QFont.Weight.Bold))  # Increased font size
            button.setFixedSize(220, 80)  # Enlarged button size
            button.setStyleSheet("""
                QPushButton {
                    background-color: green;
                    color: black;
                    border-radius: 10px;
                    font-weight: bold;
                }
                QPushButton:checked {
                    background-color: #8B0000;
                    color: black;
                }
            """)
            # Map the button to its corresponding failure
            if failure.startswith("Signal"):
                button.clicked.connect(self.toggle_signal_failure)
            elif failure.startswith("Train Engine"):
                button.clicked.connect(self.toggle_engine_failure)
            elif failure.startswith("Brake"):
                button.clicked.connect(self.toggle_brake_failure)
            self.failure_buttons[failure] = button

            failure_layout.addWidget(label)
            failure_layout.addWidget(button)
            failure_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center each row

            failures_layout.addLayout(failure_layout)

        failures_container.setLayout(failures_layout)
        main_content_layout.addWidget(failures_container)

        # Add main content layout to content_layout
        self.content_layout.addLayout(main_content_layout)

        # Connect data changed signal
        self.train_data.data_changed.connect(self.update_display)

        # Initial display update
        self.update_display()

    def train_id_changed(self, new_train_id):
        """Handle Train ID change."""
        if new_train_id:
            self.current_train_index = int(new_train_id) - 1
            self.update_display()

    def toggle_signal_failure(self):
        """Toggle the Signal Pickup Failure state for the current train."""
        index = self.current_train_index
        current_state = self.train_data.signal_failure[index]
        new_state = not current_state
        self.train_data.signal_failure[index] = new_state
        self.update_failure_button("Signal Pickup Failure:", new_state)
        # Emit signal with the updated list
        self.tc_communicate.signal_failure_signal.emit(self.train_data.signal_failure)
        self.train_data.data_changed.emit()

    def toggle_engine_failure(self):
        """Toggle the Train Engine Failure state for the current train."""
        index = self.current_train_index
        current_state = self.train_data.engine_failure[index]
        new_state = not current_state
        self.train_data.engine_failure[index] = new_state
        self.update_failure_button("Train Engine Failure:", new_state)
        # Emit signal with the updated list
        self.tc_communicate.engine_failure_signal.emit(self.train_data.engine_failure)
        self.train_data.data_changed.emit()

    def toggle_brake_failure(self):
        """Toggle the Brake Failure state for the current train."""
        index = self.current_train_index
        current_state = self.train_data.brake_failure[index]
        new_state = not current_state
        self.train_data.brake_failure[index] = new_state
        self.update_failure_button("Brake Failure:", new_state)
        # Emit signal with the updated list
        self.tc_communicate.brake_failure_signal.emit(self.train_data.brake_failure)
        self.train_data.data_changed.emit()

    def update_failure_button(self, failure_name, is_active):
        """Update the appearance and text of a failure button based on its state."""
        button = self.failure_buttons[failure_name]
        if is_active:
            button.setText("Active")
            # Set bloody red color
            button.setStyleSheet("""
                QPushButton {
                    background-color: #8B0000;
                    color: black;
                    border-radius: 10px;
                    font-weight: bold;
                }
            """)
        else:
            button.setText("Inactive")
            button.setStyleSheet("""
                QPushButton {
                    background-color: green;
                    color: black;
                    border-radius: 10px;
                    font-weight: bold;
                }
            """)

    def update_display(self):
        """Update the display of failure buttons based on the current train's failure states."""
        index = self.current_train_index

        # Check if the current_train_index is within the valid range
        if index < 0 or index >= self.train_data.train_count:
            # If no trains are present, disable all failure buttons
            for failure_name, button in self.failure_buttons.items():
                button.setEnabled(False)
                button.setText("Inactive")
                button.setStyleSheet("""
                    QPushButton {
                        background-color: green;
                        color: black;
                        border-radius: 10px;
                        font-weight: bold;
                    }
                """)
            return
        else:
            # Enable all failure buttons
            for failure_name, button in self.failure_buttons.items():
                button.setEnabled(True)

        # Update each failure button based on the current train's state
        self.update_failure_button("Signal Pickup Failure:", self.train_data.signal_failure[index+1])
        self.update_failure_button("Train Engine Failure:", self.train_data.engine_failure[index+1])
        self.update_failure_button("Brake Failure:", self.train_data.brake_failure[index+1])
        print(f"In MurphyPage: Updated display for Train {index+1}")