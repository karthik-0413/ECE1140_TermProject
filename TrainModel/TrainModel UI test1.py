import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QLabel,
    QVBoxLayout, QHBoxLayout, QStackedWidget, QSizePolicy, QSpacerItem, QGridLayout, QScrollArea, QLineEdit, QComboBox, QDialog, QDialogButtonBox
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, pyqtSignal, QObject

class TrainData(QObject):
    data_changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        # Variables for the data values
        self.cabin_temperature = 78  # degrees Fahrenheit
        self.maximum_capacity = 222  # passengers
        self.passenger_count = 100
        self.crew_count = 2
        self.maximum_speed = 50  # mph
        self.current_speed = 40  # mph
        self.total_car_weight = 226.8  # tons

        self.train_length = 32.2  # meters
        self.train_height = 3.42  # meters
        self.train_width = 2.65  # meters
        self.number_of_cars = 4  # variable
        self.single_car_tare_weight = 40.9  # tons

        self.announcement = "RED ALERT"

        # Train Control Input Variables
        self.commanded_power = 90  # kw
        self.commanded_speed_tc = 60  # km/h
        self.authority = 400  # m
        self.service_brake = False  # Changed to boolean
        self.train_light = True
        self.train_horn = False
        self.emergency_brake = False
        self.direction_control = "Forward"
        self.beacon = "We are approaching to station Alpha"

        # Cabin Control Variables
        self.temperature_commanded = 76  # °F
        self.cabin_light = True
        self.train_left_door = False
        self.train_right_door = False
        self.advertisement = "Picture1"
        self.passenger_brake = False

        # Variables for the buttons
        self.interior_light_on = self.cabin_light
        self.exterior_light_on = self.train_light
        self.left_door_open = self.train_left_door
        self.right_door_open = self.train_right_door
        self.passenger_emergency_brake = self.passenger_brake

        # Added variables for dynamic information
        self.current_acceleration = 2.3  # ft/s²
        self.commanded_speed = 40  # mph
        self.commanded_authority = 500  # ft
        self.available_seats = 122
        self.current_train_weight = 48.4  # t

        # Variables for static information
        self.static_cars = 1
        self.static_length = 105  # ft
        self.static_width = 9  # ft
        self.static_height = 11  # ft
        self.static_empty_train_weight = 40.9  # t

    # Add setter methods to emit signal on data change
    def set_value(self, var_name, value):
        setattr(self, var_name, value)
        self.data_changed.emit()

class BasePage(QWidget):
    def __init__(self, title):
        super().__init__()

        # Set background color to very light gray
        self.setStyleSheet("background-color: #F5F5F5;")  # Very light gray

        # Main vertical layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header
        header = QLabel(title)
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setFont(QFont('Arial', 32, QFont.Weight.Bold))
        header.setStyleSheet("""
            background-color: lightblue;
            padding: 5px 0;
        """)
        header.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        main_layout.addWidget(header)

        # Content area
        self.content_layout = QVBoxLayout()
        self.content_layout.setContentsMargins(10, 10, 10, 10)  # Added margins to prevent hugging edges
        self.content_layout.setSpacing(0)
        main_layout.addLayout(self.content_layout)

        self.setLayout(main_layout)

class MurphyPage(BasePage):
    def __init__(self, train_data):
        super().__init__("Murphy")
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

        # Define failure types with ":" appended
        failure_types = ["Signal Pickup Failure:", "Train Engine Failure:", "Brake Failure:"]

        for failure in failure_types:
            failure_layout = QHBoxLayout()
            failure_layout.setContentsMargins(0, 0, 0, 0)
            failure_layout.setSpacing(10)  # Adjusted spacing

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
            button.clicked.connect(lambda checked, btn=button: self.toggle_button(btn))

            failure_layout.addWidget(label)
            failure_layout.addWidget(button)

            failures_layout.addLayout(failure_layout)

        failures_container.setLayout(failures_layout)
        main_content_layout.addWidget(failures_container)

        # Add main content layout to content_layout
        self.content_layout.addLayout(main_content_layout)

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

class TrainModelPage(BasePage):
    def __init__(self, train_data):
        super().__init__("Train Model")
        self.train_data = train_data  # Store the train data

        # Create a scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        # Main content widget and layout inside scroll area
        content_widget = QWidget()
        content_widget.setStyleSheet("background-color: #F5F5F5;")  # Very light gray

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
        #dynamic_info_layout.

        data_items = [
            ("Cabin Temperature", "cabin_temperature", "°F"),
            ("Maximum Capacity", "maximum_capacity", "passengers"),
            ("Passenger Count", "passenger_count", ""),
            ("Crew Count", "crew_count", ""),
            ("Maximum Speed", "maximum_speed", "mph"),
            ("Current Speed", "current_speed", "mph"),
            ("Total Car Weight", "total_car_weight", "t"),
            ("Train Length", "train_length", "m"),
            ("Train Height", "train_height", "m"),
            ("Train Width", "train_width", "m"),
            ("Number of Cars", "number_of_cars", ""),
            ("Single Car Tare Weight", "single_car_tare_weight", "t"),
            ("Current Acceleration", "current_acceleration", "ft/s²"),
            ("Commanded Speed", "commanded_speed", "mph"),
            ("Commanded Authority", "commanded_authority", "ft"),
            ("Available Seats", "available_seats", ""),
            ("Current Train Wt.", "current_train_weight", "t"),
        ]

        # font sizes
        font_label = QFont('Arial', 12)
        font_label.setBold(True)
        font_value = QFont('Arial', 12)

        self.value_labels = {}

        # Add column headers
        dynamic_info_layout.addWidget(QLabel("Element Name"), 0, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        dynamic_info_layout.addWidget(QLabel("Train 1"), 0, 1, alignment=Qt.AlignmentFlag.AlignCenter)

        for i, (label_text, var_name, unit) in enumerate(data_items):
            label = QLabel(label_text)
            label.setFont(font_label)
            label.setStyleSheet("color: black;")
            value_label = QLabel()
            value_label.setFont(font_value)

            value_label.setStyleSheet("color: black;")
            dynamic_info_layout.addWidget(label, i + 1, 0, alignment=Qt.AlignmentFlag.AlignRight)
            dynamic_info_layout.addWidget(value_label, i + 1, 1, alignment=Qt.AlignmentFlag.AlignLeft)
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

        # Add vertical spacer of 20 pixels
        data_layout.addSpacing(80)

        # Static Information Table (Updated to match dynamic info table)
        static_info_layout = QGridLayout()
        static_info_layout.setVerticalSpacing(0)  # Reduced line spacing
        static_info_layout.setHorizontalSpacing(50)  # Increase spacing between labels and values
        static_info_layout.setContentsMargins(1, 1, 1, 1)

        static_data_items = [
            ("Cars", "static_cars", ""),
            ("Length", "static_length", "ft."),
            ("Width", "static_width", "ft."),
            ("Height", "static_height", "ft."),
            ("Empty Train Wt.", "static_empty_train_weight", "t"),
        ]

        self.static_value_labels = {}

        # Add column headers
        static_info_layout.addWidget(QLabel("Element Name"), 0, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        static_info_layout.addWidget(QLabel("Train 1"), 0, 1, alignment=Qt.AlignmentFlag.AlignCenter)

        for i, (label_text, var_name, unit) in enumerate(static_data_items):
            label = QLabel(label_text)
            label.setFont(font_label)
            label.setStyleSheet("color: black;")
            value_label = QLabel()
            value_label.setFont(font_value)
            value_label.setStyleSheet("color: black;")
            static_info_layout.addWidget(label, i + 1, 0, alignment=Qt.AlignmentFlag.AlignRight)
            static_info_layout.addWidget(value_label, i + 1, 1, alignment=Qt.AlignmentFlag.AlignLeft)
            self.static_value_labels[var_name] = value_label
            self.static_value_labels[var_name].setMaximumHeight(30)
            label.setMaximumHeight(30)

        # Add static information label
        static_info_label = QLabel("Static Information")
        static_info_label.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        static_info_label.setStyleSheet("color: black;")
        static_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        data_layout.addWidget(static_info_label)
        data_layout.addLayout(static_info_layout)

        # Wrap the data_layout in a widget with a border
        data_widget = QWidget()
        data_widget.setLayout(data_layout)
        data_widget.setStyleSheet("""
            QWidget {
                border: 2px solid black;
                padding: 5px;
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

        # Add stretch to move buttons lower
        right_layout.addStretch(1)

        # Buttons
        buttons_layout = QVBoxLayout()
        buttons_layout.setSpacing(20)  # Increased spacing between buttons
        buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.interior_light_button = QPushButton("Interior Light: Off")
        self.exterior_light_button = QPushButton("Exterior Light: Off")
        self.left_door_button = QPushButton("Left Door: Closed")
        self.right_door_button = QPushButton("Right Door: Closed")
        self.passenger_emergency_brake_button = QPushButton("Passenger\nEmergency\nBrake")
        # Increased font size of buttons
        button_font = QFont('Arial', 14, QFont.Weight.Bold)
        self.passenger_emergency_brake_button.setFont(button_font)

        # Increase button sizes
        button_size = (440, 80)

        # Set button styles according to the variables
        self.set_light_button_style(self.interior_light_button, self.train_data.interior_light_on, "Interior Light", button_font, button_size)
        self.set_light_button_style(self.exterior_light_button, self.train_data.exterior_light_on, "Exterior Light", button_font, button_size)
        self.set_door_button_style(self.left_door_button, self.train_data.left_door_open, "Left Door", button_font, button_size)
        self.set_door_button_style(self.right_door_button, self.train_data.right_door_open, "Right Door", button_font, button_size)

        # Passenger Emergency Brake button (blood red background)
        self.passenger_emergency_brake_button.setStyleSheet("""
            background-color: #8B0000;
            color: black;
            font-weight: bold;
        """)
        self.passenger_emergency_brake_button.setFixedSize(440, 190)  # Made the panic button bigger
        self.passenger_emergency_brake_button.setEnabled(False)

        # Disable buttons in TrainModelPage
        self.interior_light_button.setEnabled(False)
        self.exterior_light_button.setEnabled(False)
        self.left_door_button.setEnabled(False)
        self.right_door_button.setEnabled(False)
        self.passenger_emergency_brake_button.setEnabled(False)

        # Add buttons to vertical layout
        buttons_layout.addWidget(self.interior_light_button)
        buttons_layout.addWidget(self.exterior_light_button)
        buttons_layout.addWidget(self.left_door_button)
        buttons_layout.addWidget(self.right_door_button)

        right_layout.addLayout(buttons_layout)

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

        # Add panic button separately
        right_layout.addWidget(self.passenger_emergency_brake_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Add right_layout to main_layout
        main_layout.addLayout(right_layout)

        content_widget.setLayout(main_layout)
        scroll_area.setWidget(content_widget)

        # Add scroll area to content_layout
        self.content_layout.addWidget(scroll_area)

        # Connect data changed signal
        self.train_data.data_changed.connect(self.update_display)

        # Initial display update
        self.update_display()

    def set_light_button_style(self, button, is_on, label, font, size):
        button.setText(f"{label}: {'On' if is_on else 'Off'}")
        button.setFont(font)
        button.setFixedSize(*size)
        if is_on:
            button.setStyleSheet("background-color: yellow; color: black; font-weight: bold;")
        else:
            button.setStyleSheet("background-color: gray; color: black; font-weight: bold;")

    def set_door_button_style(self, button, is_open, label, font, size):
        button.setText(f"{label}: {'Open' if is_open else 'Closed'}")
        button.setFont(font)
        button.setFixedSize(*size)
        if is_open:
            button.setStyleSheet("background-color: green; color: black; font-weight: bold;")
        else:
            button.setStyleSheet("background-color: red; color: black; font-weight: bold;")

    def get_unit(self, var_name):
        units = {
            'cabin_temperature': '°F',
            'maximum_capacity': 'passengers',
            'passenger_count': '',
            'crew_count': '',
            'maximum_speed': 'mph',
            'current_speed': 'mph',
            'total_car_weight': 't',
            'train_length': 'm',
            'train_height': 'm',
            'train_width': 'm',
            'number_of_cars': '',
            'single_car_tare_weight': 't',
            'current_acceleration': 'ft/s²',
            'commanded_speed': 'mph',
            'commanded_authority': 'ft',
            'available_seats': '',
            'current_train_weight': 't',
            # Static units
            'static_cars': '',
            'static_length': 'ft.',
            'static_width': 'ft.',
            'static_height': 'ft.',
            'static_empty_train_weight': 't',
        }
        return units.get(var_name, '')

    def update_display(self):
        # Update the data labels
        for var_name, label in self.value_labels.items():
            value = getattr(self.train_data, var_name)
            unit = self.get_unit(var_name)
            value_text = f"{value} {unit}".strip()
            label.setText(value_text)

        # Update static information
        for var_name, label in self.static_value_labels.items():
            value = getattr(self.train_data, var_name)
            unit = self.get_unit(var_name)
            value_text = f"{value} {unit}".strip()
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

class AnnouncementDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Enter the Announcement")
        self.setFixedSize(600, 300)

        layout = QVBoxLayout()
        self.label = QLabel("Enter the announcement you want to display:")
        self.label.setFont(QFont('Arial', 14))
        self.label.setStyleSheet("color: black;")
        layout.addWidget(self.label)

        self.text_edit = QLineEdit()
        self.text_edit.setFont(QFont('Arial', 14))
        self.text_edit.setStyleSheet("color: black;")
        layout.addWidget(self.text_edit)

        # OK Button
        self.ok_button = QPushButton("OK")
        self.ok_button.setFont(QFont('Arial', 14))
        self.ok_button.setStyleSheet("color: black;")
        self.ok_button.clicked.connect(self.accept)
        layout.addWidget(self.ok_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

class TestBenchPage(BasePage):
    def __init__(self, train_data):
        super().__init__("Test Bench")
        self.train_data = train_data  # Store the train data

        # Create a scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        # Main content widget and vertical layout inside scroll area
        content_widget = QWidget()
        content_widget.setStyleSheet("background-color: #F5F5F5;")

        main_vertical_layout = QVBoxLayout()
        main_vertical_layout.setContentsMargins(10, 0, 10, 10)
        main_vertical_layout.setSpacing(5)
        main_vertical_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.font_label = QFont('Arial', 13)  # Increased by 1
        self.font_label.setBold(True)
        self.font_value = QFont('Arial', 13)  # Increased by 1

        self.tc_edit_fields = {}
        self.cabin_edit_fields = {}

        # Main horizontal layout to place tables side by side
        main_horizontal_layout = QHBoxLayout()
        main_horizontal_layout.setSpacing(20)

        # Train Control Input Section
        tc_section_layout = QVBoxLayout()
        tc_section_layout.setSpacing(5)

        tc_title = QLabel("Train Control Input")
        tc_title.setFont(QFont('Arial', 17, QFont.Weight.Bold))  # Increased by 1
        tc_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        tc_title.setStyleSheet("color: black;")

        tc_input_layout = QGridLayout()
        tc_input_layout.setSpacing(5)
        tc_input_layout.setContentsMargins(0, 0, 0, 0)

        tc_data_items = [
            ("Commanded Power", "commanded_power", "kw"),
            ("Commanded Speed", "commanded_speed_tc", "km/h"),
            ("Authority", "authority", "m"),
            ("Service Brake", "service_brake"),
            ("Train Light", "train_light"),
            ("Train Horn", "train_horn"),
            ("Emergency Brake", "emergency_brake"),
            ("Direction Control", "direction_control", ["Forward", "Reverse"]),
            ("Beacon", "beacon"),
        ]

        for i, (label_text, var_name, *rest) in enumerate(tc_data_items):
            label = QLabel(label_text)
            label.setFont(self.font_label)
            label.setStyleSheet("color: black;")

            if var_name in ["service_brake", "train_light", "train_horn", "emergency_brake"]:
                # Use a button for ON/OFF
                button = QPushButton("OFF")
                button.setCheckable(True)
                button.setFont(self.font_value)
                button.setFixedWidth(80)
                button.clicked.connect(lambda checked, var=var_name, btn=button: self.toggle_on_off(var, btn))
                tc_input_layout.addWidget(label, i, 0, alignment=Qt.AlignmentFlag.AlignLeft)
                tc_input_layout.addWidget(button, i, 1, alignment=Qt.AlignmentFlag.AlignLeft)
                unit_label = QLabel(rest[0] if rest else "")
                unit_label.setFont(self.font_label)
                unit_label.setStyleSheet("color: black;")
                tc_input_layout.addWidget(unit_label, i, 2, alignment=Qt.AlignmentFlag.AlignLeft)
                self.tc_edit_fields[var_name] = button
            elif var_name == "direction_control":
                # Use combo box for direction
                options = rest[0]
                combo_box = QComboBox()
                combo_box.addItems(options)
                combo_box.setCurrentText(getattr(self.train_data, var_name))
                combo_box.setFont(self.font_value)
                combo_box.setStyleSheet("color: black;")
                combo_box.currentTextChanged.connect(lambda text, var=var_name: self.update_train_data(var, text))
                tc_input_layout.addWidget(label, i, 0, alignment=Qt.AlignmentFlag.AlignLeft)
                tc_input_layout.addWidget(combo_box, i, 1, alignment=Qt.AlignmentFlag.AlignLeft)
                unit_label = QLabel("")
                tc_input_layout.addWidget(unit_label, i, 2)
                self.tc_edit_fields[var_name] = combo_box
            elif var_name == "beacon":
                # Use two combo boxes for beacon
                action_combo = QComboBox()
                action_combo.addItems(["We are approaching to", "We are locating at"])
                station_combo = QComboBox()
                station_combo.addItems(["station Alpha", "station Beta", "station Delta"])
                action_combo.setFont(self.font_value)
                station_combo.setFont(self.font_value)
                action_combo.setStyleSheet("color: black;")
                station_combo.setStyleSheet("color: black;")
                action_combo.currentIndexChanged.connect(self.update_beacon)
                station_combo.currentIndexChanged.connect(self.update_beacon)
                tc_input_layout.addWidget(label, i, 0, alignment=Qt.AlignmentFlag.AlignLeft)
                beacon_layout = QHBoxLayout()
                beacon_layout.addWidget(action_combo)
                beacon_layout.addWidget(station_combo)
                tc_input_layout.addLayout(beacon_layout, i, 1)
                unit_label = QLabel("")
                tc_input_layout.addWidget(unit_label, i, 2)
                self.tc_edit_fields["beacon_action"] = action_combo
                self.tc_edit_fields["beacon_station"] = station_combo
            else:
                # Numeric inputs
                value = getattr(self.train_data, var_name)
                value_edit = QLineEdit(str(value))
                value_edit.setFont(self.font_value)
                value_edit.setMaximumWidth(80)
                value_edit.setStyleSheet("color: black;")
                value_edit.editingFinished.connect(lambda var=var_name, edit=value_edit: self.update_train_data(var, edit.text()))
                tc_input_layout.addWidget(label, i, 0, alignment=Qt.AlignmentFlag.AlignLeft)
                tc_input_layout.addWidget(value_edit, i, 1, alignment=Qt.AlignmentFlag.AlignLeft)
                unit_label = QLabel(rest[0] if rest else "")
                unit_label.setFont(self.font_label)
                unit_label.setStyleSheet("color: black;")
                tc_input_layout.addWidget(unit_label, i, 2, alignment=Qt.AlignmentFlag.AlignLeft)
                self.tc_edit_fields[var_name] = value_edit

        tc_section_layout.addWidget(tc_title)
        tc_section_layout.addLayout(tc_input_layout)

        # Train Control Input Widget
        tc_input_widget = QWidget()
        tc_input_widget.setLayout(tc_section_layout)

        # Cabin Control Section
        cabin_section_layout = QVBoxLayout()
        cabin_section_layout.setSpacing(5)

        cabin_title = QLabel("Cabin Control")
        cabin_title.setFont(QFont('Arial', 17, QFont.Weight.Bold))  # Increased by 1
        cabin_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cabin_title.setStyleSheet("color: black;")

        cabin_control_layout = QGridLayout()
        cabin_control_layout.setSpacing(5)
        cabin_control_layout.setContentsMargins(0, 0, 0, 0)

        cabin_data_items = [
            ("Temperature Commanded", "temperature_commanded", "°F"),
            ("Cabin Light", "cabin_light"),
            ("Train Left Door", "train_left_door"),
            ("Train Right Door", "train_right_door"),
            ("Passenger Brake", "passenger_brake"),
            ("Advertisement", "advertisement", ["Picture1", "Picture2", "Picture3"]),
        ]

        for i, (label_text, var_name, *rest) in enumerate(cabin_data_items):
            label = QLabel(label_text)
            label.setFont(self.font_label)
            label.setStyleSheet("color: black;")

            if var_name in ["cabin_light", "train_left_door", "train_right_door", "passenger_brake"]:
                # Use a button for ON/OFF
                button = QPushButton("OFF")
                button.setCheckable(True)
                button.setFont(self.font_value)
                button.setFixedWidth(80)
                button.clicked.connect(lambda checked, var=var_name, btn=button: self.toggle_on_off(var, btn))
                cabin_control_layout.addWidget(label, i, 0, alignment=Qt.AlignmentFlag.AlignLeft)
                cabin_control_layout.addWidget(button, i, 1, alignment=Qt.AlignmentFlag.AlignLeft)
                unit_label = QLabel("")
                cabin_control_layout.addWidget(unit_label, i, 2)
                self.cabin_edit_fields[var_name] = button
            elif var_name == "advertisement":
                # Use a combo box for advertisement
                options = rest[0]
                combo_box = QComboBox()
                combo_box.addItems(options)
                combo_box.setCurrentText(getattr(self.train_data, var_name))
                combo_box.setFont(self.font_value)
                combo_box.setStyleSheet("color: black;")
                combo_box.currentTextChanged.connect(lambda text, var=var_name: self.update_train_data(var, text))
                cabin_control_layout.addWidget(label, i, 0, alignment=Qt.AlignmentFlag.AlignLeft)
                cabin_control_layout.addWidget(combo_box, i, 1, alignment=Qt.AlignmentFlag.AlignLeft)
                unit_label = QLabel("")
                cabin_control_layout.addWidget(unit_label, i, 2)
                self.cabin_edit_fields[var_name] = combo_box
            else:
                # Numeric inputs
                value = getattr(self.train_data, var_name)
                value_edit = QLineEdit(str(value))
                value_edit.setFont(self.font_value)
                value_edit.setMaximumWidth(80)
                value_edit.setStyleSheet("color: black;")
                value_edit.editingFinished.connect(lambda var=var_name, edit=value_edit: self.update_train_data(var, edit.text()))
                cabin_control_layout.addWidget(label, i, 0, alignment=Qt.AlignmentFlag.AlignLeft)
                cabin_control_layout.addWidget(value_edit, i, 1, alignment=Qt.AlignmentFlag.AlignLeft)
                unit_label = QLabel(rest[0] if rest else "")
                unit_label.setFont(self.font_label)
                unit_label.setStyleSheet("color: black;")
                cabin_control_layout.addWidget(unit_label, i, 2, alignment=Qt.AlignmentFlag.AlignLeft)
                self.cabin_edit_fields[var_name] = value_edit

        cabin_section_layout.addWidget(cabin_title)
        cabin_section_layout.addLayout(cabin_control_layout)

        # Cabin Control Widget
        cabin_control_widget = QWidget()
        cabin_control_widget.setLayout(cabin_section_layout)

        # Add both widgets to the horizontal layout
        main_horizontal_layout.addWidget(tc_input_widget)
        main_horizontal_layout.addWidget(cabin_control_widget)

        main_vertical_layout.addLayout(main_horizontal_layout)

        # Announcement Button (moved below the tables)
        announcement_button = QPushButton("Announcement")
        announcement_button.setFont(QFont('Arial', 15, QFont.Weight.Bold))  # Increased by 1
        announcement_button.setFixedSize(200, 50)
        announcement_button.setStyleSheet("""
            QPushButton {
                border: 2px solid black;
                background-color: #F0F0F0;
                color: black;
            }
            QPushButton:hover {
                background-color: #E0E0E0;
            }
        """)
        announcement_button.clicked.connect(self.open_announcement_dialog)

        # Center the Announcement button
        announcement_layout = QHBoxLayout()
        announcement_layout.addStretch()
        announcement_layout.addWidget(announcement_button)
        announcement_layout.addStretch()

        main_vertical_layout.addLayout(announcement_layout)

        # Set content widget layout
        content_widget.setLayout(main_vertical_layout)
        scroll_area.setWidget(content_widget)

        # Add scroll area to content_layout
        self.content_layout.addWidget(scroll_area)

        # Initialize button states
        self.update_button_states()

    def toggle_on_off(self, var_name, button):
        is_on = button.isChecked()
        button.setText("ON" if is_on else "OFF")
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {'green' if is_on else 'lightgray'};
                color: black;
            }}
        """)
        self.train_data.set_value(var_name, is_on)
        # Map variables with different names
        if var_name == 'cabin_light':
            self.train_data.set_value('interior_light_on', is_on)
        elif var_name == 'train_light':
            self.train_data.set_value('exterior_light_on', is_on)
        elif var_name == 'train_left_door':
            self.train_data.set_value('left_door_open', is_on)
        elif var_name == 'train_right_door':
            self.train_data.set_value('right_door_open', is_on)
        elif var_name == 'passenger_brake':
            self.train_data.set_value('passenger_emergency_brake', is_on)

    def update_train_data(self, var_name, value):
        # Update the variable in train_data
        try:
            # Convert to appropriate type
            if var_name in ['commanded_power', 'commanded_speed_tc', 'authority', 'temperature_commanded']:
                current_value = getattr(self.train_data, var_name)
                if isinstance(current_value, int):
                    value = int(value)
                elif isinstance(current_value, float):
                    value = float(value)
            self.train_data.set_value(var_name, value)
            # Map variables with different names
            if var_name == 'commanded_speed_tc':
                self.train_data.set_value('commanded_speed', value)
            elif var_name == 'authority':
                self.train_data.set_value('commanded_authority', value)
            elif var_name == 'temperature_commanded':
                self.train_data.set_value('cabin_temperature', value)
        except ValueError:
            pass  # Handle invalid input as desired

    def update_beacon(self):
        action = self.tc_edit_fields["beacon_action"].currentText()
        station = self.tc_edit_fields["beacon_station"].currentText()
        beacon_text = f"{action} {station}"
        self.train_data.set_value('beacon', beacon_text)

    def open_announcement_dialog(self):
        dialog = AnnouncementDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            announcement = dialog.text_edit.text()
            self.train_data.set_value('announcement', announcement)

    def update_button_states(self):
        # Initialize button states based on train_data
        for var_name, button in self.tc_edit_fields.items():
            if var_name in ["service_brake", "train_light", "train_horn", "emergency_brake"]:
                is_on = getattr(self.train_data, var_name)
                button.setChecked(is_on)
                button.setText("ON" if is_on else "OFF")
                button.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {'green' if is_on else 'lightgray'};
                        color: black;
                    }}
                """)
        for var_name, button in self.cabin_edit_fields.items():
            if var_name in ["cabin_light", "train_left_door", "train_right_door", "passenger_brake"]:
                is_on = getattr(self.train_data, var_name)
                button.setChecked(is_on)
                button.setText("ON" if is_on else "OFF")
                button.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {'green' if is_on else 'lightgray'};
                        color: black;
                    }}
                """)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt6 Application Example")
        self.setGeometry(100, 100, 1000, 600)  # Increased window size

        # Create TrainData instance
        self.train_data = TrainData()

        # Central widget and main layout
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Top navigation layout
        nav_layout = QHBoxLayout()
        nav_layout.setSpacing(0)

        # Navigation buttons
        self.train_model_btn = QPushButton("Train Model")
        self.test_bench_btn = QPushButton("Test Bench")
        self.murphy_btn = QPushButton("Murphy")

        # Set fixed size and style for navigation buttons
        for btn in [self.train_model_btn, self.test_bench_btn, self.murphy_btn]:
            btn.setFixedSize(150, 50)
            btn.setFont(QFont('Arial', 12, QFont.Weight.Bold))
            btn.setStyleSheet("""
                QPushButton {
                    background-color: lightgray;
                    color: black;
                    border: 1px solid #ccc;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #d3d3d3;
                }
            """)

        # Connect buttons to methods
        self.train_model_btn.clicked.connect(self.show_train_model)
        self.test_bench_btn.clicked.connect(self.show_test_bench)
        self.murphy_btn.clicked.connect(self.show_murphy)

        # Add navigation buttons to layout without spacing
        nav_layout.addWidget(self.train_model_btn)
        nav_layout.addWidget(self.test_bench_btn)
        nav_layout.addWidget(self.murphy_btn)

        # Add navigation layout to main layout
        nav_container = QWidget()
        nav_container.setLayout(nav_layout)
        nav_container.setFixedHeight(50)
        main_layout.addWidget(nav_container, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        # Stacked widget to hold different pages
        self.stacked_widget = QStackedWidget()

        # Pages
        self.train_model_page = TrainModelPage(self.train_data)
        self.test_bench_page = TestBenchPage(self.train_data)
        self.murphy_page = MurphyPage(self.train_data)

        # Add pages to stacked widget
        self.stacked_widget.addWidget(self.train_model_page)
        self.stacked_widget.addWidget(self.test_bench_page)
        self.stacked_widget.addWidget(self.murphy_page)

        # Initially show Murphy page
        self.stacked_widget.setCurrentWidget(self.murphy_page)

        # Add stacked widget to main layout
        main_layout.addWidget(self.stacked_widget)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def show_train_model(self):
        self.train_model_page.update_display()
        self.stacked_widget.setCurrentWidget(self.train_model_page)

    def show_test_bench(self):
        self.stacked_widget.setCurrentWidget(self.test_bench_page)

    def show_murphy(self):
        self.stacked_widget.setCurrentWidget(self.murphy_page)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
