# train_model.py

from PyQt6.QtGui import QFont, QPixmap, QImage
from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout,
    QScrollArea, QSizePolicy, QFrame, QPushButton
)
from PyQt6.QtCore import Qt

from base_page import BasePage


class TrainModelPage(BasePage):
    """Page representing the Train Model."""

    def __init__(self, train_data, train_id_callback):
        super().__init__("Train Model", train_id_callback)
        self.train_data = train_data  # Store the train data

        # Create a scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        # Main content widget and vertical layout inside scroll area
        content_widget = QWidget()
        content_widget.setStyleSheet("background-color: #F5F5F5;")  # Very light gray

        # Create a vertical layout for the content_widget
        content_vbox = QVBoxLayout()
        content_vbox.setContentsMargins(0, 0, 0, 0)
        content_vbox.setSpacing(0)

        # Main layout for the content
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(20, 10, 20, 10)  # Adjusted margins
        main_layout.setSpacing(10)

        # Left side: Data table
        data_layout = QVBoxLayout()
        data_layout.setSpacing(0)  # Reduced line spacing
        data_layout.setContentsMargins(1, 1, 1, 1)

        # Dynamic Information Table
        dynamic_info_layout = QGridLayout()
        dynamic_info_layout.setVerticalSpacing(0)  # Reduced line spacing
        dynamic_info_layout.setHorizontalSpacing(50)  # Increase spacing between labels and values
        dynamic_info_layout.setContentsMargins(0, 0, 0, 0)

        data_items = [
            ("Actual Temperature", "cabin_temperature", "°F"),
            ("Maximum Capacity", "maximum_capacity", "passengers"),
            ("Passenger Count", "passenger_count", ""),
            ("Crew Count", "crew_count", ""),
            ("Maximum Speed", "maximum_speed", "mph"),
            ("Current Speed", "current_speed", "mph"),
            ("Total Car Weight", "total_car_weight", "t"),
            # Removed 'Train Length', 'Train Height', 'Train Width' from Dynamic Information
            ("Number of Cars", "number_of_cars", ""),
            ("Single Car Tare Weight", "single_car_tare_weight", "t"),
            ("Current Acceleration", "current_acceleration", "ft/s²"),
            ("Commanded Speed", "commanded_speed", "mph"),
            ("Commanded Authority", "commanded_authority", "ft"),
            ("Available Seats", "available_seats", ""),
            ("Current Train Wt.", "current_train_weight", "t"),
        ]

        # Font settings
        font_label = QFont('Arial', 12)
        font_label.setBold(True)
        font_value = QFont('Arial', 12)

        self.value_labels = {}

        # Populate dynamic information layout
        for i, (label_text, var_name, unit) in enumerate(data_items):
            label = QLabel(label_text)
            label.setFont(font_label)
            label.setStyleSheet("color: black;")
            label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)  # Allow label to expand
            value_label = QLabel()
            value_label.setFont(font_value)
            value_label.setStyleSheet("color: black;")
            dynamic_info_layout.addWidget(label, i, 0, alignment=Qt.AlignmentFlag.AlignRight)
            dynamic_info_layout.addWidget(value_label, i, 1, alignment=Qt.AlignmentFlag.AlignLeft)
            self.value_labels[var_name] = value_label
            self.value_labels[var_name].setMaximumHeight(30)
            label.setMaximumHeight(30)

        # Add dynamic information label
        dynamic_info_label = QLabel("Dynamic Information")
        dynamic_info_label.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        dynamic_info_label.setStyleSheet("color: black;")
        dynamic_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        data_layout.addWidget(dynamic_info_label)
        data_layout.addLayout(dynamic_info_layout)

        # Reduce the vertical spacing between the tables
        data_layout.addSpacing(20)  # Reduced from 80 to 20

        # Static Information Table
        static_info_layout = QGridLayout()
        static_info_layout.setVerticalSpacing(0)  # Reduced line spacing
        static_info_layout.setHorizontalSpacing(50)  # Increase spacing between labels and values
        static_info_layout.setContentsMargins(1, 1, 1, 1)

        static_data_items = [
            ("Cars", "static_cars", ""),
            ("Length", "static_length", "ft"),
            ("Width", "static_width", "ft"),
            ("Height", "static_height", "ft"),
            ("Empty Train Wt.", "static_empty_train_weight", "t"),
        ]

        self.static_value_labels = {}

        # Populate static information layout
        for i, (label_text, var_name, unit) in enumerate(static_data_items):
            label = QLabel(label_text)
            label.setFont(font_label)
            label.setStyleSheet("color: black;")
            label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)  # Allow label to expand
            value_label = QLabel()
            value_label.setFont(font_value)
            value_label.setStyleSheet("color: black;")
            static_info_layout.addWidget(label, i, 0, alignment=Qt.AlignmentFlag.AlignRight)
            static_info_layout.addWidget(value_label, i, 1, alignment=Qt.AlignmentFlag.AlignLeft)
            self.static_value_labels[var_name] = value_label
            self.static_value_labels[var_name].setMaximumHeight(30)
            label.setMaximumHeight(30)

        # Add static information label
        static_info_label = QLabel("Static Information")
        static_info_label.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        static_info_label.setStyleSheet("color: black; padding-top: 20px;")  # Added padding-top
        static_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        data_layout.addWidget(static_info_label)
        data_layout.addLayout(static_info_layout)

        # Wrap the data_layout in a QFrame with a black border
        data_widget = QFrame()
        data_widget.setLayout(data_layout)
        data_widget.setFrameShape(QFrame.Shape.Panel)
        data_widget.setFrameShadow(QFrame.Shadow.Plain)
        data_widget.setLineWidth(2)
        data_widget.setMidLineWidth(0)
        data_widget.setStyleSheet("""
            QFrame {
                padding: 5px;
                max-width: 400px;  /* Increased width to allow for longer labels */
                border: 2px solid black;  /* Set border to black */
            }
            QLabel {
                border: none;
            }
        """)

        main_layout.addWidget(data_widget)

        # Right side: Buttons and announcements
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(10, 10, 10, 10)
        right_layout.setSpacing(10)

        # Announcement
        announcement_label = QLabel("ANNOUNCEMENTS:")
        announcement_label.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        announcement_label.setStyleSheet("color: black;")
        announcement_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Centered above the text box

        self.announcement_text = QLabel(self.train_data.announcement)
        self.announcement_text.setFont(QFont('Arial', 14))
        self.announcement_text.setWordWrap(True)
        self.announcement_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.announcement_text.setStyleSheet("""
            border: 1px solid black;
            padding: 5px;
            color: black;
        """)
        # Reduced the height by one-third
        self.announcement_text.setFixedHeight(100)
        self.announcement_text.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Add announcement label and text box
        announcement_layout = QVBoxLayout()
        announcement_layout.setSpacing(2)  # Reduced spacing
        announcement_layout.addWidget(announcement_label)
        announcement_layout.addWidget(self.announcement_text)

        right_layout.addLayout(announcement_layout)

        # Passenger Emergency Brake button (blood red background)
        self.passenger_emergency_brake_button = QPushButton("Passenger\nEmergency\nBrake")
        self.passenger_emergency_brake_button.setFont(QFont('Arial', 14, QFont.Weight.Bold))
        self.passenger_emergency_brake_button.setCheckable(True)
        self.passenger_emergency_brake_button.setStyleSheet("""
            QPushButton {
                background-color: #8B0000;
                color: black;
                font-weight: bold;
            }
        """)
        self.passenger_emergency_brake_button.setFixedSize(500, 130)  # Made the panic button bigger
        self.passenger_emergency_brake_button.setEnabled(True)
        self.passenger_emergency_brake_button.clicked.connect(self.passenger_emergency_brake_pressed)

        right_layout.addWidget(self.passenger_emergency_brake_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Buttons
        buttons_layout = QGridLayout()
        buttons_layout.setSpacing(20)  # Increased spacing between buttons
        buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.interior_light_button = QPushButton("Interior Light: Off")
        self.exterior_light_button = QPushButton("Exterior Light: Off")
        self.left_door_button = QPushButton("Left Door: Closed")
        self.right_door_button = QPushButton("Right Door: Closed")

        # Increased font size of buttons
        button_font = QFont('Arial', 14, QFont.Weight.Bold)

        # Increase button sizes
        button_size = (440, 80)

        # Set button styles according to the variables
        self.set_light_button_style(self.interior_light_button, self.train_data.interior_light_on, "Interior Light", button_font, button_size)
        self.set_light_button_style(self.exterior_light_button, self.train_data.exterior_light_on, "Exterior Light", button_font, button_size)
        self.set_door_button_style(self.left_door_button, self.train_data.left_door_open, "Left Door", button_font, button_size)
        self.set_door_button_style(self.right_door_button, self.train_data.right_door_open, "Right Door", button_font, button_size)

        # Add buttons to grid layout (2x2)
        buttons_layout.addWidget(self.interior_light_button, 0, 0)
        buttons_layout.addWidget(self.exterior_light_button, 0, 1)
        buttons_layout.addWidget(self.left_door_button, 1, 0)
        buttons_layout.addWidget(self.right_door_button, 1, 1)

        right_layout.addLayout(buttons_layout)

        # Load and display image (advertisement)
        image_label = QLabel()
        image_label.setFixedSize(500, 200)  # Set desired size
        image = QImage('images/train_image.jpg')  # Replace with the actual image path
        pixmap = QPixmap.fromImage(image)
        pixmap = pixmap.scaled(image_label.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        right_layout.addWidget(image_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Add right_layout to main_layout
        main_layout.addLayout(right_layout)

        # Add main_layout to content_vbox
        content_vbox.addLayout(main_layout)

        # Set content_widget's layout
        content_widget.setLayout(content_vbox)
        scroll_area.setWidget(content_widget)

        # Add scroll area to content_layout
        self.content_layout.addWidget(scroll_area)

        # Connect data changed signal
        self.train_data.data_changed.connect(self.update_display)

        # Initial display update
        self.update_display()

    def set_train_data(self, train_data):
        """Set the current train data and update connections."""
        # Disconnect previous train_data signal
        try:
            self.train_data.data_changed.disconnect(self.update_display)
        except TypeError:
            pass
        self.train_data = train_data
        self.train_data.data_changed.connect(self.update_display)
        self.update_display()

    def set_light_button_style(self, button, is_on, label, font, size):
        """Set the style of a light control button."""
        button.setText(f"{label}: {'On' if is_on else 'Off'}")
        button.setFont(font)
        button.setFixedSize(*size)
        if is_on:
            button.setStyleSheet("background-color: yellow; color: black; font-weight: bold;")
        else:
            button.setStyleSheet("background-color: gray; color: black; font-weight: bold;")

    def set_door_button_style(self, button, is_open, label, font, size):
        """Set the style of a door control button."""
        button.setText(f"{label}: {'Open' if is_open else 'Closed'}")
        button.setFont(font)
        button.setFixedSize(*size)
        if is_open:
            button.setStyleSheet("background-color: green; color: black; font-weight: bold;")
        else:
            button.setStyleSheet("background-color: red; color: black; font-weight: bold;")

    def get_unit(self, var_name):
        """Get the unit associated with a variable."""
        units = {
            'cabin_temperature': '°F',
            'maximum_capacity': 'passengers',
            'passenger_count': '',
            'crew_count': '',
            'maximum_speed': 'mph',
            'current_speed': 'mph',
            'total_car_weight': 't',
            'train_length': 'ft',
            'train_height': 'ft',
            'train_width': 'ft',
            'number_of_cars': '',
            'single_car_tare_weight': 't',
            'current_acceleration': 'ft/s²',
            'commanded_speed': 'mph',
            'commanded_authority': 'ft',
            'available_seats': '',
            'current_train_weight': 't',
            # Static units
            'static_cars': '',
            'static_length': 'ft',
            'static_width': 'ft',
            'static_height': 'ft',
            'static_empty_train_weight': 't',
        }
        return units.get(var_name, '')

    def update_display(self):
        """Update the display based on the current train data."""
        # Update the data labels
        for var_name, label in self.value_labels.items():
            value = getattr(self.train_data, var_name)
            unit = self.get_unit(var_name)
            if isinstance(value, int):
                value_text = f"{value} {unit}".strip()
            else:
                value_text = f"{value:.2f} {unit}".strip()
            label.setText(value_text)

        # Update static information
        for var_name, label in self.static_value_labels.items():
            value = getattr(self.train_data, var_name)
            unit = self.get_unit(var_name)
            if isinstance(value, int):
                value_text = f"{value} {unit}".strip()
            else:
                value_text = f"{value:.2f} {unit}".strip()
            label.setText(value_text)

        # Update the announcement text
        self.announcement_text.setText(self.train_data.announcement)

        # Update the buttons
        button_font = QFont('Arial', 16, QFont.Weight.Bold)
        button_size = (240, 80)
        self.set_light_button_style(self.interior_light_button, self.train_data.interior_light_on, "Interior Light", button_font, button_size)
        self.set_light_button_style(self.exterior_light_button, self.train_data.exterior_light_on, "Exterior Light", button_font, button_size)
        self.set_door_button_style(self.left_door_button, self.train_data.left_door_open, "Left Door", button_font, button_size)
        self.set_door_button_style(self.right_door_button, self.train_data.right_door_open, "Right Door", button_font, button_size)

        # Update the Passenger Emergency Brake button
        is_on = self.train_data.passenger_emergency_brake
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

    def passenger_emergency_brake_pressed(self):
        """Handle the passenger emergency brake being pressed."""
        is_on = self.passenger_emergency_brake_button.isChecked()
        self.train_data.set_value('passenger_emergency_brake', is_on)
        # Update button style based on state
        self.passenger_emergency_brake_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {'#550000' if is_on else '#8B0000'};
                color: black;
                font-weight: bold;
            }}
        """)
