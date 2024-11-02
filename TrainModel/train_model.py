# train_model.py

from PyQt6.QtGui import QFont, QPixmap, QImage
from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout,
    QScrollArea, QSizePolicy, QFrame, QPushButton, QComboBox
)
from PyQt6.QtCore import Qt

from base_page import BasePage


class TrainModelPage(BasePage):
    """Page representing the Train Model."""

    def __init__(self, train_data, tc_communicate, tm_communicate):
        super().__init__("Train Model", self.train_id_changed)
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

        # Train Image at the top
        train_image_label = QLabel()
        train_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        train_image = QPixmap('images/train_image.jpg')  # Replace with your image path
        train_image = train_image.scaledToHeight(200, Qt.TransformationMode.SmoothTransformation)
        train_image_label.setPixmap(train_image)
        main_layout.addWidget(train_image_label)

        # Dynamic Data Section
        dynamic_data_label = QLabel("Dynamic Data")
        dynamic_data_label.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        dynamic_data_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        dynamic_data_label.setStyleSheet("color: black;")
        main_layout.addWidget(dynamic_data_label)

        dynamic_data_layout = QGridLayout()
        dynamic_data_layout.setHorizontalSpacing(20)
        dynamic_data_layout.setVerticalSpacing(10)

        # List of dynamic data variables
        dynamic_data = [
            ("Cabin Temperature (°F):", "cabin_temperature"),
            ("Passenger Count:", "passenger_count"),
            ("Crew Count:", "crew_count"),
            ("Maximum Speed (mph):", "maximum_speed"),
            ("Current Speed (mph):", "current_speed"),
            ("Total Car Weight (tons):", "total_car_weight"),
            ("Current Acceleration (ft/s²):", "current_acceleration"),
            ("Available Seats:", "available_seats"),
            ("Current Position (ft):", "current_position"),
            ("Current Elevation (ft):", "elevation"),
            ("Current Grade (%):", "grade"),
            ("Current Train Weight (tons):", "current_train_weight"),
        ]

        self.value_labels = {}

        for i, (label_text, var_name) in enumerate(dynamic_data):
            label = QLabel(label_text)
            label.setFont(QFont('Arial', 14))
            label.setStyleSheet("color: black;")
            dynamic_data_layout.addWidget(label, i, 0, alignment=Qt.AlignmentFlag.AlignRight)

            value_label = QLabel()
            value_label.setFont(QFont('Arial', 14))
            value_label.setStyleSheet("color: black;")
            dynamic_data_layout.addWidget(value_label, i, 1, alignment=Qt.AlignmentFlag.AlignLeft)

            self.value_labels[var_name] = value_label

        main_layout.addLayout(dynamic_data_layout)

        # Static Information Section
        static_data_label = QLabel("Static Information")
        static_data_label.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        static_data_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        static_data_label.setStyleSheet("color: black;")
        main_layout.addWidget(static_data_label)

        static_data_layout = QGridLayout()
        static_data_layout.setHorizontalSpacing(20)
        static_data_layout.setVerticalSpacing(10)

        # List of static data variables
        static_data = [
            ("Number of Cars:", "static_cars"),
            ("Train Length (ft):", "static_length"),
            ("Train Width (ft):", "static_width"),
            ("Train Height (ft):", "static_height"),
            ("Empty Train Weight (tons):", "static_empty_train_weight"),
        ]

        self.static_value_labels = {}

        for i, (label_text, var_name) in enumerate(static_data):
            label = QLabel(label_text)
            label.setFont(QFont('Arial', 14))
            label.setStyleSheet("color: black;")
            static_data_layout.addWidget(label, i, 0, alignment=Qt.AlignmentFlag.AlignRight)

            value_label = QLabel()
            value_label.setFont(QFont('Arial', 14))
            value_label.setStyleSheet("color: black;")
            static_data_layout.addWidget(value_label, i, 1, alignment=Qt.AlignmentFlag.AlignLeft)

            self.static_value_labels[var_name] = value_label

        main_layout.addLayout(static_data_layout)

        # Announcement Section
        announcement_label = QLabel("Announcement")
        announcement_label.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        announcement_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        announcement_label.setStyleSheet("color: black;")
        main_layout.addWidget(announcement_label)

        self.announcement_text = QLabel()
        self.announcement_text.setFont(QFont('Arial', 14))
        self.announcement_text.setStyleSheet("color: black;")
        self.announcement_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.announcement_text.setWordWrap(True)
        main_layout.addWidget(self.announcement_text)

        # Buttons Section
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(20)

        # Interior Light Button
        self.interior_light_button = QPushButton("Interior Light")
        self.interior_light_button.setCheckable(True)
        self.interior_light_button.clicked.connect(self.toggle_interior_light)

        # Exterior Light Button
        self.exterior_light_button = QPushButton("Exterior Light")
        self.exterior_light_button.setCheckable(True)
        self.exterior_light_button.clicked.connect(self.toggle_exterior_light)

        # Left Door Button
        self.left_door_button = QPushButton("Left Door")
        self.left_door_button.setCheckable(True)
        self.left_door_button.clicked.connect(self.toggle_left_door)

        # Right Door Button
        self.right_door_button = QPushButton("Right Door")
        self.right_door_button.setCheckable(True)
        self.right_door_button.clicked.connect(self.toggle_right_door)

        # Passenger Emergency Brake Button
        self.passenger_emergency_brake_button = QPushButton("Passenger Emergency Brake")
        self.passenger_emergency_brake_button.setCheckable(True)
        self.passenger_emergency_brake_button.clicked.connect(self.passenger_emergency_brake_pressed)

        # Set styles for buttons
        button_font = QFont('Arial', 16, QFont.Weight.Bold)
        button_size = (240, 80)
        self.set_light_button_style(self.interior_light_button, False, "Interior Light", button_font, button_size)
        self.set_light_button_style(self.exterior_light_button, False, "Exterior Light", button_font, button_size)
        self.set_door_button_style(self.left_door_button, False, "Left Door", button_font, button_size)
        self.set_door_button_style(self.right_door_button, False, "Right Door", button_font, button_size)
        self.passenger_emergency_brake_button.setFont(button_font)
        self.passenger_emergency_brake_button.setFixedSize(*button_size)
        self.passenger_emergency_brake_button.setStyleSheet("""
            QPushButton {
                background-color: #8B0000;
                color: black;
                font-weight: bold;
            }
            QPushButton:checked {
                background-color: #550000;
                color: black;
            }
        """)

        # Add buttons to layout
        buttons_layout.addWidget(self.interior_light_button)
        buttons_layout.addWidget(self.exterior_light_button)
        buttons_layout.addWidget(self.left_door_button)
        buttons_layout.addWidget(self.right_door_button)
        buttons_layout.addWidget(self.passenger_emergency_brake_button)

        main_layout.addLayout(buttons_layout)

        # Spacer
        main_layout.addStretch()

        # Set content widget layout
        content_widget.setLayout(main_layout)
        scroll_area.setWidget(content_widget)

        # Add scroll area to content_layout
        self.content_layout.addWidget(scroll_area)

        # Connect data changed signal
        self.train_data.data_changed.connect(self.update_display)

        # Connect to the announcement signal
        self.train_data.announcement.connect(self.update_announcement)

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
            for label in self.value_labels.values():
                label.setText("N/A")
            for label in self.static_value_labels.values():
                label.setText("N/A")
            self.announcement_text.setText("")
            return

        # Update the data labels
        for var_name, label in self.value_labels.items():
            value_list = getattr(self.train_data, var_name)
            value = value_list[index]
            unit = self.get_unit(var_name)
            if isinstance(value, int):
                value_text = f"{value} {unit}".strip()
            else:
                value_text = f"{value:.2f} {unit}".strip()
            label.setText(value_text)

        # Update static information
        for var_name, label in self.static_value_labels.items():
            value_list = getattr(self.train_data, var_name)
            value = value_list[index]
            unit = self.get_unit(var_name)
            if isinstance(value, int):
                value_text = f"{value} {unit}".strip()
            else:
                value_text = f"{value:.2f} {unit}".strip()
            label.setText(value_text)

        # Update the announcement text
        self.announcement_text.setText(self.train_data.announcement_text[index])

        # Update the buttons
        button_font = QFont('Arial', 16, QFont.Weight.Bold)
        button_size = (240, 80)
        self.set_light_button_style(self.interior_light_button, self.train_data.interior_light_on[index], "Interior Light", button_font, button_size)
        self.set_light_button_style(self.exterior_light_button, self.train_data.exterior_light_on[index], "Exterior Light", button_font, button_size)
        self.set_door_button_style(self.left_door_button, self.train_data.left_door_open[index], "Left Door", button_font, button_size)
        self.set_door_button_style(self.right_door_button, self.train_data.right_door_open[index], "Right Door", button_font, button_size)

        # Update the Passenger Emergency Brake button
        is_on = self.train_data.passenger_emergency_brake[index]
        self.passenger_emergency_brake_button.blockSignals(True)  # Block signals to prevent recursion
        self.passenger_emergency_brake_button.setChecked(is_on)
        self.passenger_emergency_brake_button.blockSignals(False)  # Re-enable signals
        self.passenger_emergency_brake_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {'#550000' if is_on else '#8B0000'};
                color: black;
                font-weight: bold;
            }}
        """)

    def update_announcement(self, announcement_list):
        """Update the announcement text for the current train."""
        index = self.current_train_index
        if index < len(announcement_list):
            self.announcement_text.setText(announcement_list[index])

    def get_unit(self, var_name):
        """Get the unit for the given variable name."""
        units = {
            "cabin_temperature": "°F",
            "maximum_speed": "mph",
            "current_speed": "mph",
            "total_car_weight": "tons",
            "current_acceleration": "ft/s²",
            "current_position": "ft",
            "elevation": "ft",
            "grade": "%",
            "current_train_weight": "tons",
            "static_length": "ft",
            "static_width": "ft",
            "static_height": "ft",
            "static_empty_train_weight": "tons",
        }
        return units.get(var_name, "")

    def set_light_button_style(self, button, is_on, label, font, size):
        """Set the style for light buttons."""
        button.setFont(font)
        button.setFixedSize(*size)
        button.setText(f"{label}: {'On' if is_on else 'Off'}")
        button.setChecked(is_on)
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {'green' if is_on else 'red'};
                color: black;
                font-weight: bold;
            }}
        """)

    def set_door_button_style(self, button, is_open, label, font, size):
        """Set the style for door buttons."""
        button.setFont(font)
        button.setFixedSize(*size)
        button.setText(f"{label}: {'Open' if is_open else 'Closed'}")
        button.setChecked(is_open)
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {'green' if is_open else 'red'};
                color: black;
                font-weight: bold;
            }}
        """)

    def toggle_interior_light(self):
        """Toggle the interior light."""
        index = self.current_train_index
        is_on = not self.train_data.interior_light_on[index]
        self.train_data.interior_light_on[index] = is_on
        # Update the entire list and emit signal
        self.tc_communicate.interior_lights_signal.emit(self.train_data.interior_light_on)
        self.update_display()

    def toggle_exterior_light(self):
        """Toggle the exterior light."""
        index = self.current_train_index
        is_on = not self.train_data.exterior_light_on[index]
        self.train_data.exterior_light_on[index] = is_on
        # Update the entire list and emit signal
        self.tc_communicate.exterior_lights_signal.emit(self.train_data.exterior_light_on)
        self.update_display()

    def toggle_left_door(self):
        """Toggle the left door."""
        index = self.current_train_index
        is_open = not self.train_data.left_door_open[index]
        self.train_data.left_door_open[index] = is_open
        # Update the entire list and emit signal
        self.tc_communicate.left_door_signal.emit(self.train_data.left_door_open)
        self.update_display()

    def toggle_right_door(self):
        """Toggle the right door."""
        index = self.current_train_index
        is_open = not self.train_data.right_door_open[index]
        self.train_data.right_door_open[index] = is_open
        # Update the entire list and emit signal
        self.tc_communicate.right_door_signal.emit(self.train_data.right_door_open)
        self.update_display()

    def passenger_emergency_brake_pressed(self):
        """Handle the passenger emergency brake being pressed."""
        index = self.current_train_index
        is_on = self.passenger_emergency_brake_button.isChecked()
        # Update the list for all trains
        self.train_data.passenger_emergency_brake[index] = is_on
        # Emit signal with the updated list
        self.tc_communicate.passenger_brake_command_signal.emit(self.train_data.passenger_emergency_brake)
        # Update display
        self.update_display()
