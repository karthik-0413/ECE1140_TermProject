# murphy.py

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QScrollArea, QComboBox, QCheckBox, QPushButton
)
from PyQt6.QtCore import Qt

from base_page import BasePage

class MurphyPage(BasePage):
    """Page representing the Murphy controls (failure modes)."""

    def __init__(self, train_data, tc_communicate, tm_communicate):
        super().__init__("Murphy", self.train_id_changed)
        self.train_data = train_data  # Store the train data
        self.tc_communicate = tc_communicate
        self.tm_communicate = tm_communicate

        self.current_train_index = 0  # Default to first train

        # Create a scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        # Main content widget and vertical layout inside scroll area
        content_widget = QWidget()
        content_widget.setStyleSheet("background-color: #F5F5F5;")

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)

        # Failure Modes Label
        failure_modes_label = QLabel("Failure Modes")
        failure_modes_label.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        failure_modes_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        failure_modes_label.setStyleSheet("color: black;")

        main_layout.addWidget(failure_modes_label)

        # Failure Modes Checkboxes
        self.engine_failure_checkbox = QCheckBox("Engine Failure")
        self.brake_failure_checkbox = QCheckBox("Brake Failure")
        self.signal_pickup_failure_checkbox = QCheckBox("Signal Pickup Failure")

        # Set font and styles
        checkbox_font = QFont('Arial', 14)
        self.engine_failure_checkbox.setFont(checkbox_font)
        self.brake_failure_checkbox.setFont(checkbox_font)
        self.signal_pickup_failure_checkbox.setFont(checkbox_font)

        # Connect signals
        self.engine_failure_checkbox.stateChanged.connect(self.update_engine_failure)
        self.brake_failure_checkbox.stateChanged.connect(self.update_brake_failure)
        self.signal_pickup_failure_checkbox.stateChanged.connect(self.update_signal_pickup_failure)

        # Add checkboxes to layout
        checkboxes_layout = QVBoxLayout()
        checkboxes_layout.addWidget(self.engine_failure_checkbox)
        checkboxes_layout.addWidget(self.brake_failure_checkbox)
        checkboxes_layout.addWidget(self.signal_pickup_failure_checkbox)

        main_layout.addLayout(checkboxes_layout)

        # Spacer
        main_layout.addStretch()

        # Set content widget layout
        content_widget.setLayout(main_layout)
        scroll_area.setWidget(content_widget)

        # Add scroll area to content_layout
        self.content_layout.addWidget(scroll_area)

        # Connect data changed signal
        self.train_data.data_changed.connect(self.update_display)

        # Initial display update
        self.update_display()

    def update_train_id_list(self, train_ids):
        """Update the train ID combo box with the new list."""
        current_id = self.train_id_combo.currentText()
        self.train_id_combo.blockSignals(True)
        self.train_id_combo.clear()
        self.train_id_combo.addItems(train_ids)
        if current_id in train_ids:
            self.train_id_combo.setCurrentText(current_id)
            self.current_train_index = int(current_id) - 1
        else:
            self.train_id_combo.setCurrentIndex(0)
            self.current_train_index = 0
        self.train_id_combo.blockSignals(False)
        self.update_display()

    def train_id_changed(self, new_train_id):
        """Handle Train ID change."""
        self.current_train_index = int(new_train_id) - 1
        self.update_display()

    def update_display(self):
        """Update the display based on the current train data."""
        index = self.current_train_index

        # Update the checkboxes based on the train data
        self.engine_failure_checkbox.blockSignals(True)
        self.engine_failure_checkbox.setChecked(self.train_data.engine_failure[index])
        self.engine_failure_checkbox.blockSignals(False)

        self.brake_failure_checkbox.blockSignals(True)
        self.brake_failure_checkbox.setChecked(self.train_data.brake_failure[index])
        self.brake_failure_checkbox.blockSignals(False)

        self.signal_pickup_failure_checkbox.blockSignals(True)
        self.signal_pickup_failure_checkbox.setChecked(self.train_data.signal_failure[index])
        self.signal_pickup_failure_checkbox.blockSignals(False)

    def update_engine_failure(self, state):
        """Update engine failure status for the current train."""
        index = self.current_train_index
        is_checked = self.engine_failure_checkbox.isChecked()
        self.train_data.engine_failure[index] = is_checked
        # Emit signal to Train Controller
        self.tc_communicate.engine_failure_signal.emit(index, is_checked)
        self.train_data.data_changed.emit()

    def update_brake_failure(self, state):
        """Update brake failure status for the current train."""
        index = self.current_train_index
        is_checked = self.brake_failure_checkbox.isChecked()
        self.train_data.brake_failure[index] = is_checked
        # Emit signal to Train Controller
        self.tc_communicate.brake_failure_signal.emit(index, is_checked)
        self.train_data.data_changed.emit()

    def update_signal_pickup_failure(self, state):
        """Update signal pickup failure status for the current train."""
        index = self.current_train_index
        is_checked = self.signal_pickup_failure_checkbox.isChecked()
        self.train_data.signal_failure[index] = is_checked
        # Emit signal to Train Controller
        self.tc_communicate.signal_failure_signal.emit(index, is_checked)
        self.train_data.data_changed.emit()
