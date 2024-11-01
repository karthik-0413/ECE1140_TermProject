# testbench.py

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QLabel, QVBoxLayout, QHBoxLayout, QGridLayout,
    QScrollArea, QPushButton, QLineEdit, QComboBox, QWidget
)
from PyQt6.QtCore import Qt

from base_page import BasePage
from announcement import AnnouncementDialog  # Import the updated AnnouncementDialog

class TestBenchPage(BasePage):
    """Page representing the Test Bench for Train Control Inputs."""

    def __init__(self, train_data, tc_communicate, tm_communicate):
        super().__init__("Test Bench", self.train_id_changed)
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

        # Control Inputs Label
        control_inputs_label = QLabel("Train Control Inputs")
        control_inputs_label.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        control_inputs_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        control_inputs_label.setStyleSheet("color: black;")

        main_layout.addWidget(control_inputs_label)

        # Control Inputs Grid
        control_inputs_layout = QGridLayout()
        control_inputs_layout.setHorizontalSpacing(20)
        control_inputs_layout.setVerticalSpacing(10)

        # List of control inputs
        control_inputs = [
            ("Power Command (kW):", "commanded_power", self.set_commanded_power),
            ("Service Brake:", "service_brake", self.toggle_service_brake),
            ("Emergency Brake:", "emergency_brake", self.toggle_emergency_brake),
            ("Desired Temperature (°F):", "desired_temperature", self.set_desired_temperature),
            ("Exterior Lights:", "exterior_light", self.toggle_exterior_light),
            ("Interior Lights:", "interior_light", self.toggle_interior_light),
            ("Left Door:", "train_left_door", self.toggle_left_door),
            ("Right Door:", "train_right_door", self.toggle_right_door),
            ("Announcement:", "announcement_text", self.open_announcement_dialog),
        ]

        self.input_widgets = {}

        for i, (label_text, var_name, callback) in enumerate(control_inputs):
            label = QLabel(label_text)
            label.setFont(QFont('Arial', 14))
            label.setStyleSheet("color: black;")
            control_inputs_layout.addWidget(label, i, 0, alignment=Qt.AlignmentFlag.AlignRight)

            if var_name in ["commanded_power", "desired_temperature"]:
                # Line edit for numerical inputs
                line_edit = QLineEdit()
                line_edit.setFont(QFont('Arial', 14))
                line_edit.setFixedWidth(200)
                control_inputs_layout.addWidget(line_edit, i, 1, alignment=Qt.AlignmentFlag.AlignLeft)
                self.input_widgets[var_name] = line_edit
                line_edit.returnPressed.connect(callback)
            elif var_name == "announcement_text":
                # Button to open announcement dialog
                button = QPushButton("Set Announcement")
                button.setFont(QFont('Arial', 14))
                button.setFixedWidth(200)
                control_inputs_layout.addWidget(button, i, 1, alignment=Qt.AlignmentFlag.AlignLeft)
                self.input_widgets[var_name] = button
                button.clicked.connect(callback)
            else:
                # Toggle button for booleans
                button = QPushButton()
                button.setFont(QFont('Arial', 14))
                button.setFixedWidth(200)
                control_inputs_layout.addWidget(button, i, 1, alignment=Qt.AlignmentFlag.AlignLeft)
                self.input_widgets[var_name] = button
                button.clicked.connect(callback)

        main_layout.addLayout(control_inputs_layout)

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
            if train_ids:
                self.train_id_combo.setCurrentIndex(0)
                self.current_train_index = 0
            else:
                self.current_train_index = None
        self.train_id_combo.blockSignals(False)
        self.update_display()

    def train_id_changed(self, new_train_id):
        """Handle Train ID change."""
        if new_train_id:
            self.current_train_index = int(new_train_id) - 1
            self.update_display()

    def update_display(self):
        """Update the display based on the current train data."""
        index = self.current_train_index
        if index is None or index >= self.train_data.train_count:
            # No valid train selected
            for widget in self.input_widgets.values():
                widget.setEnabled(False)
            return
        else:
            for widget in self.input_widgets.values():
                widget.setEnabled(True)

        # Update input widgets with current values
        # Update line edits
        self.input_widgets['commanded_power'].setText(str(self.train_data.commanded_power[index]))
        self.input_widgets['desired_temperature'].setText(str(self.train_data.desired_temperature[index]))

        # Update buttons
        self.update_button(self.input_widgets['service_brake'], self.train_data.service_brake[index], "Service Brake")
        self.update_button(self.input_widgets['emergency_brake'], self.train_data.emergency_brake[index], "Emergency Brake")
        self.update_button(self.input_widgets['exterior_light'], self.train_data.exterior_light[index], "Exterior Light")
        self.update_button(self.input_widgets['interior_light'], self.train_data.interior_light[index], "Interior Light")
        self.update_button(self.input_widgets['train_left_door'], self.train_data.train_left_door[index], "Left Door")
        self.update_button(self.input_widgets['train_right_door'], self.train_data.train_right_door[index], "Right Door")

    def update_button(self, button, is_on, label):
        """Update the button text and style based on state."""
        button.setText(f"{label}: {'On' if is_on else 'Off'}")
        if is_on:
            button.setStyleSheet("background-color: green; color: black; font-weight: bold;")
        else:
            button.setStyleSheet("background-color: red; color: black; font-weight: bold;")

    def set_commanded_power(self):
        """Set the commanded power."""
        index = self.current_train_index
        try:
            power = float(self.input_widgets['commanded_power'].text())
            self.train_data.commanded_power[index] = power
            # Emit signal to Train Model
            self.tc_communicate.power_command_signal.emit(index, power)
            self.train_data.data_changed.emit()
        except ValueError:
            pass  # Invalid input, ignore

    def toggle_service_brake(self):
        """Toggle the service brake."""
        index = self.current_train_index
        current_state = self.train_data.service_brake[index]
        new_state = not current_state
        self.train_data.service_brake[index] = new_state
        self.update_button(self.input_widgets['service_brake'], new_state, "Service Brake")
        # Emit signal to Train Model
        self.tc_communicate.service_brake_command_signal.emit(index, new_state)
        self.train_data.data_changed.emit()

    def toggle_emergency_brake(self):
        """Toggle the emergency brake."""
        index = self.current_train_index
        current_state = self.train_data.emergency_brake[index]
        new_state = not current_state
        self.train_data.emergency_brake[index] = new_state
        self.update_button(self.input_widgets['emergency_brake'], new_state, "Emergency Brake")
        # Emit signal to Train Model
        self.tc_communicate.emergency_brake_command_signal.emit(index, new_state)
        self.train_data.data_changed.emit()

    def set_desired_temperature(self):
        """Set the desired temperature."""
        index = self.current_train_index
        try:
            temp = float(self.input_widgets['desired_temperature'].text())
            self.train_data.desired_temperature[index] = temp
            # Emit signal to Train Model
            self.tc_communicate.desired_temperature_signal.emit(index, temp)
            self.train_data.data_changed.emit()
        except ValueError:
            pass  # Invalid input, ignore

    def toggle_exterior_light(self):
        """Toggle the exterior light."""
        index = self.current_train_index
        current_state = self.train_data.exterior_light[index]
        new_state = not current_state
        self.train_data.exterior_light[index] = new_state
        self.update_button(self.input_widgets['exterior_light'], new_state, "Exterior Light")
        # Emit signal to Train Model
        self.tc_communicate.exterior_lights_signal.emit(index, new_state)
        self.train_data.data_changed.emit()

    def toggle_interior_light(self):
        """Toggle the interior light."""
        index = self.current_train_index
        current_state = self.train_data.interior_light[index]
        new_state = not current_state
        self.train_data.interior_light[index] = new_state
        self.update_button(self.input_widgets['interior_light'], new_state, "Interior Light")
        # Emit signal to Train Model
        self.tc_communicate.interior_lights_signal.emit(index, new_state)
        self.train_data.data_changed.emit()

    def toggle_left_door(self):
        """Toggle the left door."""
        index = self.current_train_index
        current_state = self.train_data.train_left_door[index]
        new_state = not current_state
        self.train_data.train_left_door[index] = new_state
        self.update_button(self.input_widgets['train_left_door'], new_state, "Left Door")
        # Emit signal to Train Model
        self.tc_communicate.left_door_signal.emit(index, new_state)
        self.train_data.data_changed.emit()

    def toggle_right_door(self):
        """Toggle the right door."""
        index = self.current_train_index
        current_state = self.train_data.train_right_door[index]
        new_state = not current_state
        self.train_data.train_right_door[index] = new_state
        self.update_button(self.input_widgets['train_right_door'], new_state, "Right Door")
        # Emit signal to Train Model
        self.tc_communicate.right_door_signal.emit(index, new_state)
        self.train_data.data_changed.emit()

    def open_announcement_dialog(self):
        """Open the announcement dialog to set the announcement text."""
        index = self.current_train_index

        # Create and display the announcement dialog
        dialog = AnnouncementDialog(index, self)
        if dialog.exec():
            text = dialog.get_announcement()
            train_index = dialog.get_train_index()
            self.train_data.announcement_text[train_index] = text
            # Emit signal to Train Model
            self.tc_communicate.announcement_signal.emit(train_index, text)
            self.train_data.data_changed.emit()
