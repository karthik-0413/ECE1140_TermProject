import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QLabel,
    QVBoxLayout, QHBoxLayout, QStackedWidget, QSizePolicy, QSpacerItem, QGridLayout, QScrollArea, QLineEdit
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

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
            padding: 10px 0;
        """)
        header.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        main_layout.addWidget(header)

        # Content area
        self.content_layout = QVBoxLayout()
        self.content_layout.setContentsMargins(0, 0, 0, 0)
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
        main_content_layout = QHBoxLayout()
        main_content_layout.setContentsMargins(10, 10, 10, 10)
        main_content_layout.setSpacing(10)

        # Left side: tables
        tables_widget = QWidget()
        tables_layout = QHBoxLayout()
        tables_layout.setContentsMargins(0, 0, 0, 0)
        tables_layout.setSpacing(10)  # Reduced spacing

        # Adjust the font sizes to make tables smaller
        font_label = QFont('Arial', 12)
        font_label.setBold(True)
        font_value = QFont('Arial', 12)

        # First form
        form1_widget = QWidget()
        form1_layout = QGridLayout()
        form1_layout.setSpacing(2)  # Reduced spacing
        form1_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins to make content smaller at top and bottom

        # Data items for form1
        data_items_form1 = [
            ("Cabin Temperature", "cabin_temperature", "°F"),
            ("Maximum Capacity", "maximum_capacity", "passengers"),
            ("Passenger Count", "passenger_count", ""),
            ("Crew Count", "crew_count", ""),
            ("Maximum Speed", "maximum_speed", "mph"),
            ("Current Speed", "current_speed", "mph"),
            ("Total Car Weight", "total_car_weight", "t"),
        ]

        self.value_labels_form1 = {}

        for i, (label_text, var_name, unit) in enumerate(data_items_form1):
            label = QLabel(label_text)
            label.setFont(font_label)
            label.setStyleSheet("color: black;")
            value = getattr(self.train_data, var_name)
            value_text = f"{value} {unit}".strip()
            value_label = QLabel(value_text)
            value_label.setFont(font_value)
            value_label.setStyleSheet("color: black;")
            form1_layout.addWidget(label, i, 0, alignment=Qt.AlignmentFlag.AlignLeft)
            form1_layout.addWidget(value_label, i, 1, alignment=Qt.AlignmentFlag.AlignLeft)
            self.value_labels_form1[var_name] = value_label

        form1_widget.setLayout(form1_layout)

        # Second form
        form2_widget = QWidget()
        form2_layout = QGridLayout()
        form2_layout.setSpacing(2)  # Reduced spacing
        form2_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins

        data_items_form2 = [
            ("Train Length", "train_length", "m"),
            ("Train Height", "train_height", "m"),
            ("Train Width", "train_width", "m"),
            ("Number of Cars", "number_of_cars", ""),
            ("Single Car Tare Weight", "single_car_tare_weight", "t"),
        ]

        self.value_labels_form2 = {}

        for i, (label_text, var_name, unit) in enumerate(data_items_form2):
            label = QLabel(label_text)
            label.setFont(font_label)
            label.setStyleSheet("color: black;")
            value = getattr(self.train_data, var_name)
            value_text = f"{value} {unit}".strip()
            value_label = QLabel(value_text)
            value_label.setFont(font_value)
            value_label.setStyleSheet("color: black;")
            form2_layout.addWidget(label, i, 0, alignment=Qt.AlignmentFlag.AlignLeft)
            form2_layout.addWidget(value_label, i, 1, alignment=Qt.AlignmentFlag.AlignLeft)
            self.value_labels_form2[var_name] = value_label

        form2_widget.setLayout(form2_layout)

        # Add forms to tables layout side by side
        tables_layout.addWidget(form1_widget)
        tables_layout.addWidget(form2_widget)

        tables_widget.setLayout(tables_layout)

        # Right side: Announcements
        announcement_widget = QWidget()
        announcement_layout = QVBoxLayout()
        announcement_layout.setContentsMargins(0, 0, 0, 0)
        announcement_layout.setSpacing(5)  # Reduced spacing

        announcement_label = QLabel("ANNOUNCEMENTS:")
        announcement_label.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        announcement_label.setStyleSheet("color: black;")  # Set color to black

        self.announcement_text = QLabel(self.train_data.announcement)
        self.announcement_text.setFont(QFont('Arial', 14))
        self.announcement_text.setWordWrap(True)
        self.announcement_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.announcement_text.setStyleSheet("color: black;")  # Set color to black

        # Make announcement box have a border and bigger size
        self.announcement_text.setStyleSheet("""
            border: 1px solid black;
            padding: 5px;
            color: black;
        """)
        self.announcement_text.setFixedHeight(150)
        self.announcement_text.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        announcement_layout.addWidget(announcement_label)
        announcement_layout.addWidget(self.announcement_text)

        # Buttons under Announcement
        # Create buttons for the statuses
        self.interior_light_button = QPushButton("Interior Light: Off")
        self.exterior_light_button = QPushButton("Exterior Light: Off")
        self.left_door_button = QPushButton("Left Door: Closed")
        self.right_door_button = QPushButton("Right Door: Closed")
        self.passenger_emergency_brake_button = QPushButton("Passenger\nEmergency\nBrake")
        self.passenger_emergency_brake_button.setFont(QFont('Arial', 12, QFont.Weight.Bold))

        # Set button styles according to the variables
        self.set_light_button_style(self.interior_light_button, self.train_data.interior_light_on, "Interior Light")
        self.set_light_button_style(self.exterior_light_button, self.train_data.exterior_light_on, "Exterior Light")
        self.set_door_button_style(self.left_door_button, self.train_data.left_door_open, "Left Door")
        self.set_door_button_style(self.right_door_button, self.train_data.right_door_open, "Right Door")

        # Passenger Emergency Brake button (blood red background)
        self.passenger_emergency_brake_button.setStyleSheet("""
            background-color: #8B0000;
            color: black;
            font-weight: bold;
        """)
        self.passenger_emergency_brake_button.setFixedSize(250, 130)  # Made the panic button bigger
        self.passenger_emergency_brake_button.setEnabled(False)

        # Disable buttons in TrainModelPage
        self.interior_light_button.setEnabled(False)
        self.exterior_light_button.setEnabled(False)
        self.left_door_button.setEnabled(False)
        self.right_door_button.setEnabled(False)
        self.passenger_emergency_brake_button.setEnabled(False)

        # Create a grid layout for the buttons
        buttons_layout = QGridLayout()
        buttons_layout.setSpacing(5)  # Reduced spacing
        buttons_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins

        # Place buttons in grid
        buttons_layout.addWidget(self.interior_light_button, 0, 0)
        buttons_layout.addWidget(self.exterior_light_button, 1, 0)
        buttons_layout.addWidget(self.left_door_button, 0, 1)
        buttons_layout.addWidget(self.right_door_button, 1, 1)

        # Add buttons_layout to announcement_layout
        announcement_layout.addLayout(buttons_layout)

        # Add panic button separately
        announcement_layout.addWidget(self.passenger_emergency_brake_button, alignment=Qt.AlignmentFlag.AlignCenter)

        announcement_widget.setLayout(announcement_layout)

        # Adjust main_content_layout
        main_content_layout.addWidget(tables_widget)
        main_content_layout.addWidget(announcement_widget)

        content_widget.setLayout(main_content_layout)
        scroll_area.setWidget(content_widget)

        # Add scroll area to content_layout
        self.content_layout.addWidget(scroll_area)

    def set_light_button_style(self, button, is_on, label):
        button.setText(f"{label}: {'On' if is_on else 'Off'}")
        button.setFixedSize(160, 50)
        button.setFont(QFont('Arial', 12, QFont.Weight.Bold))
        if is_on:
            button.setStyleSheet("background-color: yellow; color: black; font-weight: bold;")
        else:
            button.setStyleSheet("background-color: gray; color: black; font-weight: bold;")

    def set_door_button_style(self, button, is_open, label):
        button.setText(f"{label}: {'Open' if is_open else 'Closed'}")
        button.setFixedSize(160, 50)
        button.setFont(QFont('Arial', 12, QFont.Weight.Bold))
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
        }
        return units.get(var_name, '')

    def update_display(self):
        # Update the data labels
        for var_name, label in self.value_labels_form1.items():
            value = getattr(self.train_data, var_name)
            unit = self.get_unit(var_name)
            value_text = f"{value} {unit}".strip()
            label.setText(value_text)

        for var_name, label in self.value_labels_form2.items():
            value = getattr(self.train_data, var_name)
            unit = self.get_unit(var_name)
            value_text = f"{value} {unit}".strip()
            label.setText(value_text)

        # Update the announcement text
        self.announcement_text.setText(self.train_data.announcement)

        # Update the buttons
        self.set_light_button_style(self.interior_light_button, self.train_data.interior_light_on, "Interior Light")
        self.set_light_button_style(self.exterior_light_button, self.train_data.exterior_light_on, "Exterior Light")
        self.set_door_button_style(self.left_door_button, self.train_data.left_door_open, "Left Door")
        self.set_door_button_style(self.right_door_button, self.train_data.right_door_open, "Right Door")

class TestBenchPage(BasePage):
    def __init__(self, train_data):
        super().__init__("Test Bench")
        self.train_data = train_data  # Store the train data

        # Create a scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        # Main content widget and layout inside scroll area
        content_widget = QWidget()
        content_widget.setStyleSheet("background-color: #F5F5F5;")  # Very light gray
        main_content_layout = QHBoxLayout()
        main_content_layout.setContentsMargins(10, 10, 10, 10)
        main_content_layout.setSpacing(10)

        self.font_label = QFont('Arial', 12)
        self.font_label.setBold(True)
        self.font_value = QFont('Arial', 12)

        self.edit_fields_form1 = {}
        self.edit_fields_form2 = {}

        # Left side: forms
        forms_widget = QWidget()
        forms_layout = QHBoxLayout()
        forms_layout.setSpacing(10)

        # First form
        form1_widget = QWidget()
        form1_layout = QGridLayout()
        form1_layout.setSpacing(2)  # Reduced spacing
        form1_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins

        # Data items for form1
        data_items_form1 = [
            ("Cabin Temperature", "cabin_temperature", "°F"),
            ("Maximum Capacity", "maximum_capacity", "passengers"),
            ("Passenger Count", "passenger_count", ""),
            ("Crew Count", "crew_count", ""),
            ("Maximum Speed", "maximum_speed", "mph"),
            ("Current Speed", "current_speed", "mph"),
            ("Total Car Weight", "total_car_weight", "t"),
        ]

        for i, (label_text, var_name, unit) in enumerate(data_items_form1):
            self.create_edit_field(label_text, var_name, unit, form1_layout, i)

        form1_widget.setLayout(form1_layout)

        # Second form
        form2_widget = QWidget()
        form2_layout = QGridLayout()
        form2_layout.setSpacing(2)  # Reduced spacing
        form2_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins

        data_items_form2 = [
            ("Train Length", "train_length", "m"),
            ("Train Height", "train_height", "m"),
            ("Train Width", "train_width", "m"),
            ("Number of Cars", "number_of_cars", ""),
            ("Single Car Tare Weight", "single_car_tare_weight", "t"),
        ]

        for i, (label_text, var_name, unit) in enumerate(data_items_form2):
            self.create_edit_field(label_text, var_name, unit, form2_layout, i)

        form2_widget.setLayout(form2_layout)

        # Add forms to forms_layout side by side
        forms_layout.addWidget(form1_widget)
        forms_layout.addWidget(form2_widget)

        forms_widget.setLayout(forms_layout)

        # Right side: Announcements and buttons
        announcement_widget = QWidget()
        announcement_layout = QVBoxLayout()
        announcement_layout.setContentsMargins(0, 0, 0, 0)
        announcement_layout.setSpacing(5)  # Reduced spacing

        announcement_label = QLabel("ANNOUNCEMENTS:")
        announcement_label.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        announcement_label.setStyleSheet("color: black;")  # Set color to black

        self.announcement_edit = QLineEdit(self.train_data.announcement)
        self.announcement_edit.setFont(QFont('Arial', 14))
        self.announcement_edit.setFixedHeight(100)  # Make it bigger
        self.announcement_edit.textChanged.connect(self.update_announcement)
        self.announcement_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.announcement_edit.setStyleSheet("color: black;")

        announcement_layout.addWidget(announcement_label)
        announcement_layout.addWidget(self.announcement_edit)

        # Buttons
        self.interior_light_button = QPushButton("Interior Light: Off")
        self.exterior_light_button = QPushButton("Exterior Light: Off")
        self.left_door_button = QPushButton("Left Door: Closed")
        self.right_door_button = QPushButton("Right Door: Closed")
        self.passenger_emergency_brake_button = QPushButton("Passenger\nEmergency\nBrake")
        self.passenger_emergency_brake_button.setFont(QFont('Arial', 12, QFont.Weight.Bold))

        # Connect buttons
        self.interior_light_button.clicked.connect(self.toggle_interior_light)
        self.exterior_light_button.clicked.connect(self.toggle_exterior_light)
        self.left_door_button.clicked.connect(self.toggle_left_door)
        self.right_door_button.clicked.connect(self.toggle_right_door)
        self.passenger_emergency_brake_button.clicked.connect(self.toggle_passenger_emergency_brake)

        # Set initial styles
        self.update_buttons()

        # Create a grid layout for the buttons
        buttons_layout = QGridLayout()
        buttons_layout.setSpacing(5)  # Reduced spacing
        buttons_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins

        # Place buttons in grid
        buttons_layout.addWidget(self.interior_light_button, 0, 0)
        buttons_layout.addWidget(self.exterior_light_button, 1, 0)
        buttons_layout.addWidget(self.left_door_button, 0, 1)
        buttons_layout.addWidget(self.right_door_button, 1, 1)

        # Add buttons_layout to announcement_layout
        announcement_layout.addLayout(buttons_layout)

        # Add panic button separately
        announcement_layout.addWidget(self.passenger_emergency_brake_button, alignment=Qt.AlignmentFlag.AlignCenter)

        announcement_widget.setLayout(announcement_layout)

        # Adjust main_content_layout
        main_content_layout.addWidget(forms_widget)
        main_content_layout.addWidget(announcement_widget)

        content_widget.setLayout(main_content_layout)
        scroll_area.setWidget(content_widget)

        # Add scroll area to content_layout
        self.content_layout.addWidget(scroll_area)

    def create_edit_field(self, label_text, var_name, unit, layout, row):
        label = QLabel(label_text)
        label.setFont(self.font_label)
        label.setStyleSheet("color: black;")
        value = getattr(self.train_data, var_name)
        value_edit = QLineEdit(str(value))
        value_edit.setFont(self.font_value)
        value_edit.setMaximumWidth(100)  # Make input boxes shorter
        value_edit.setStyleSheet("color: black;")
        value_edit.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(label, row, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(value_edit, row, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        self.edit_fields_form1[var_name] = value_edit
        # Connect the QLineEdit to update the variable
        value_edit.editingFinished.connect(lambda var=var_name, edit=value_edit: self.update_train_data(var, edit.text()))

    def update_train_data(self, var_name, value):
        # Update the variable in train_data
        try:
            # Convert to appropriate type
            current_value = getattr(self.train_data, var_name)
            if isinstance(current_value, int):
                value = int(value)
            elif isinstance(current_value, float):
                value = float(value)
            setattr(self.train_data, var_name, value)
        except ValueError:
            pass  # Handle invalid input as desired

    def update_announcement(self, text):
        self.train_data.announcement = text

    def update_buttons(self):
        # Update button styles based on train_data variables
        self.set_light_button_style(self.interior_light_button, self.train_data.interior_light_on, "Interior Light")
        self.set_light_button_style(self.exterior_light_button, self.train_data.exterior_light_on, "Exterior Light")
        self.set_door_button_style(self.left_door_button, self.train_data.left_door_open, "Left Door")
        self.set_door_button_style(self.right_door_button, self.train_data.right_door_open, "Right Door")

        # Passenger Emergency Brake button
        self.passenger_emergency_brake_button.setStyleSheet("""
            background-color: #8B0000;
            color: black;
            font-weight: bold;
        """)
        self.passenger_emergency_brake_button.setFixedSize(250, 130)  # Made the panic button bigger

    def set_light_button_style(self, button, is_on, label):
        button.setText(f"{label}: {'On' if is_on else 'Off'}")
        button.setFixedSize(160, 50)
        button.setFont(QFont('Arial', 12, QFont.Weight.Bold))
        if is_on:
            button.setStyleSheet("background-color: yellow; color: black; font-weight: bold;")
        else:
            button.setStyleSheet("background-color: gray; color: black; font-weight: bold;")

    def set_door_button_style(self, button, is_open, label):
        button.setText(f"{label}: {'Open' if is_open else 'Closed'}")
        button.setFixedSize(160, 50)
        button.setFont(QFont('Arial', 12, QFont.Weight.Bold))
        if is_open:
            button.setStyleSheet("background-color: green; color: black; font-weight: bold;")
        else:
            button.setStyleSheet("background-color: red; color: black; font-weight: bold;")

    # Button click handlers
    def toggle_interior_light(self):
        self.train_data.interior_light_on = not self.train_data.interior_light_on
        self.set_light_button_style(self.interior_light_button, self.train_data.interior_light_on, "Interior Light")

    def toggle_exterior_light(self):
        self.train_data.exterior_light_on = not self.train_data.exterior_light_on
        self.set_light_button_style(self.exterior_light_button, self.train_data.exterior_light_on, "Exterior Light")

    def toggle_left_door(self):
        self.train_data.left_door_open = not self.train_data.left_door_open
        self.set_door_button_style(self.left_door_button, self.train_data.left_door_open, "Left Door")

    def toggle_right_door(self):
        self.train_data.right_door_open = not self.train_data.right_door_open
        self.set_door_button_style(self.right_door_button, self.train_data.right_door_open, "Right Door")

    def toggle_passenger_emergency_brake(self):
        self.train_data.passenger_emergency_brake = not self.train_data.passenger_emergency_brake
        # The button is always blood red, so we don't change the color

class TrainData:
    def __init__(self):
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

        # Variables for the buttons
        self.interior_light_on = False
        self.exterior_light_on = False
        self.left_door_open = False
        self.right_door_open = False
        self.passenger_emergency_brake = False

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
