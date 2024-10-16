import sys
from PyQt6.QtGui import QFont, QPixmap, QImage
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QLabel,
    QVBoxLayout, QHBoxLayout, QStackedWidget, QSizePolicy, QGridLayout,
    QScrollArea, QLineEdit, QComboBox, QDialog, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal, QObject, QTimer
from ..TrainController.TrainControllerIntegratedCommunicateSignals import IntegratedCommunicate


'''
Inputs from Track Model:
Commanded Speed
Variable in Code: self.commanded_speed (converted from self.commanded_speed_tc)
Authority
Variable in Code: self.authority
Beacon Info
Variable in Code: self.beacon_station, self.beacon
Light Level Status
Variable in Code: Not explicitly defined in the code; may need to be added.
Passengers Boarding at Next Station
Variable in Code: self.passenger_boarding


Inputs from Train Controller:
Driver Emergency Brake
Variable in Code: self.emergency_brake
Driver Service Brake
Variable in Code: self.service_brake
Power Command
Variable in Code: self.commanded_power
Left Doors Open/Close
Variable in Code: self.train_left_door
Right Doors Open/Close
Variable in Code: self.train_right_door
Outside Lights On/Off
Variable in Code: self.exterior_light
Interior Lights On/Off
Variable in Code: self.interior_light
Any Announcement
Variable in Code: self.announcement
Desired Train Temperature
Variable in Code: self.desired_temperature


Outputs to Train Controller:
Commanded Speed
Variable in Code: self.commanded_speed
Authority
Variable in Code: self.authority
Beacon
Variable in Code: self.beacon
Current Velocity
Variable in Code: self.current_speed
Trigger for Failure Modes
Variable in Code: self.auto_service_brake, self.emergency_brake
Passenger Brake Status
Variable in Code: self.passenger_emergency_brake
Actual Train Temperature
Variable in Code: self.cabin_temperature


Output to Track Model:
Number of Available Seats Inside Train
Variable in Code: self.available_seats
'''





class TrainData(QObject):
    data_changed = pyqtSignal()

    def __init__(self, communicator: IntegratedCommunicate):
        super().__init__()
        
        # For for pyqtsignals file
        self.communicator = communicator
        
        # Output to Train Controller from Track Model (Must emit signal to update the Train Controller)
        self.communicator.current_velocity_signal.connect(self.send_current_velocity)
        self.communicator.commanded_speed_signal.connect(self.send_commanded_speed)
        self.communicator.commanded_authority_signal.connect(self.send_commanded_authority)
        self.communicator.engine_failure_signal.connect(self.send_engine_failure)
        self.communicator.brake_failure_signal.connect(self.send_brake_failure)
        self.communicator.signal_failure_signal.connect(self.send_signal_failure)
        self.communicator.passenger_brake_command_signal.connect(self.send_passenger_brake_command)
        self.communicator.actual_temperature_signal.connect(self.send_actual_temperature)
        self.communicator.blocks_between_stations_signal.connect(self.send_blocks_between_stations)
        self.communicator.enable_switch_status_signal.connect(self.send_enable_switch_status)
        self.communicator.switch_status_signal.connect(self.send_switch_status)
        
        
        # Input from Train Controller
        self.communicator.power_command_signal.connect(self.handle_power_command)
        self.communicator.service_brake_command_signal.connect(self.handle_service_brake_command)
        self.communicator.emergency_brake_command_signal.connect(self.handle_emergency_brake_command)
        self.communicator.desired_temperature_signal.connect(self.handle_desired_temperature)
        self.communicator.exterior_lights_signal.connect(self.handle_exterior_lights)
        self.communicator.interior_lights_signal.connect(self.handle_interior_lights)
        self.communicator.left_door_signal.connect(self.handle_left_door)
        self.communicator.right_door_signal.connect(self.handle_right_door)
        self.communicator.announcement_signal.connect(self.handle_announcement)
        self.communicator.station_name_signal.connect(self.handle_station_name)
        
        
        # # Outputs to the Train Model
        # power_command_signal = pyqtSignal(float)
        # service_brake_command_signal = pyqtSignal(bool)
        # emergency_brake_command_signal = pyqtSignal(bool)
        # desired_temperature_signal = pyqtSignal(float)
        # exterior_lights_signal = pyqtSignal(bool)
        # interior_lights_signal = pyqtSignal(bool)
        # left_door_signal = pyqtSignal(bool) # 1 = Open, 0 = Closed
        # right_door_signal = pyqtSignal(bool)    # 1 = Open, 0 = Closed
        # announcement_signal = pyqtSignal(str)
        # station_name_signal = pyqtSignal(str)
        
        # # Inputs from the Train Model
        # current_velocity_signal = pyqtSignal(float)
        # commanded_speed_signal = pyqtSignal(float)
        # commanded_authority_signal = pyqtSignal(float)
        # engine_failure_signal = pyqtSignal(bool)
        # brake_failure_signal = pyqtSignal(bool)
        # signal_failure_signal = pyqtSignal(bool)
        # passenger_brake_command_signal = pyqtSignal(bool)
        # actual_temperature_signal = pyqtSignal(float)   # NEW
        # blocks_between_stations_signal = pyqtSignal(list)   # NEW
        # enable_switch_status_signal = pyqtSignal(bool)   # NEW -> 1 = check for next switch status, 0 = ignore next switch status
        # switch_status_signal = pyqtSignal(bool)   # NEW -> 1 = switch is right/down, 0 = switch is left/up
        
        
        # Variables for the data values
        self.cabin_temperature = 78  # degrees Fahrenheit (Actual Temperature)
        self.maximum_capacity = 222  # passengers
        self.passenger_count = 100
        self.crew_count = 2
        self.maximum_speed = 50  # mph
        self.current_speed = 40  # mph
        self.total_car_weight = 40.9  # tons (empty train weight)

        self.train_length_m = 32.2  # meters
        self.train_height_m = 3.42  # meters
        self.train_width_m = 2.65  # meters
        self.train_length = self.train_length_m * 3.28084  # feet (converted)
        self.train_height = self.train_height_m * 3.28084  # feet (converted)
        self.train_width = self.train_width_m * 3.28084  # feet (converted)
        self.number_of_cars = 1  # variable
        self.single_car_tare_weight = 40.9  # tons

        self.announcement = "RED ALERT"

        # Train Control Input Variables
        self.commanded_power = 90  # kw
        self.commanded_speed_tc = 80  # km/h
        self.commanded_speed = self.commanded_speed_tc * 0.621371  # mph (converted)
        self.authority = 400  # m
        self.commanded_authority = self.authority * 3.28084  # ft (converted)
        self.service_brake = False  # Changed to boolean
        self.exterior_light = True
        self.interior_light = True
        self.emergency_brake = False
        self.beacon_station = "Station Alpha"  # Default station

        # Cabin Control Variables
        self.desired_temperature = 76  # °F
        self.cabin_temperature = self.desired_temperature  # °F (Actual Temperature)
        self.train_left_door = False
        self.train_right_door = False
        self.advertisement = "Picture1"
        self.passenger_boarding = 0  # Number of passengers boarding at next station (default 0)

        # Variables for the buttons
        self.interior_light_on = self.interior_light
        self.exterior_light_on = self.exterior_light
        self.left_door_open = self.train_left_door
        self.right_door_open = self.train_right_door
        self.passenger_emergency_brake = False

        # Added variables for dynamic information
        self.current_acceleration = 0.3  # ft/s²
        self.available_seats = self.maximum_capacity - self.passenger_count
        self.current_train_weight = 40.9  # t (will be updated based on passengers)

        # Variables for static information
        self.static_cars = self.number_of_cars
        self.static_length = self.train_length  # ft
        self.static_width = self.train_width  # ft
        self.static_height = self.train_height  # ft
        self.static_empty_train_weight = self.single_car_tare_weight  # t

        # Update train weight based on initial passenger count
        self.update_train_weight()

        # Added variable for automatic service brake
        self.auto_service_brake = False

        # Timer for updating train state every second
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_train_state)

    # Method to update train weight based on passenger count
    def update_train_weight(self):
        empty_train_weight_kg = 40.9 * 1000  # Empty train weight in kg
        passenger_weight_kg = self.passenger_count * 68.0388  # Each passenger weighs 150 lbs (68.0388 kg)
        total_weight_kg = empty_train_weight_kg + passenger_weight_kg
        self.current_train_weight = total_weight_kg / 1000  # Convert back to tonnes
        self.total_car_weight = self.current_train_weight  # Update total car weight
        self.available_seats = self.maximum_capacity - self.passenger_count  # Update available seats
        self.data_changed.emit()

    # Add setter methods to emit signal on data change
    def set_value(self, var_name, value):
        setattr(self, var_name, value)
        # Update dependent variables
        if var_name == 'desired_temperature':
            self.cabin_temperature = value
        if var_name == 'exterior_light':
            self.exterior_light_on = value
        if var_name == 'interior_light':
            self.interior_light_on = value
        if var_name == 'train_left_door':
            self.left_door_open = value
        if var_name == 'train_right_door':
            self.right_door_open = value
        if var_name == 'number_of_cars':
            self.static_cars = value
        if var_name == 'commanded_speed_tc':
            # Convert km/h to mph
            self.commanded_speed = value * 0.621371
        if var_name == 'passenger_count':
            self.update_train_weight()
        if var_name in ['service_brake', 'emergency_brake', 'passenger_emergency_brake']:
            # Start the timer when brakes are pressed
            self.start_timer()
        if var_name == 'commanded_power':
            # Start the timer when commanded power changes
            self.start_timer()
        self.data_changed.emit()

    def start_timer(self):
        if not self.timer.isActive():
            self.timer.start(1000)  # Update every 1000 ms (1 second)

    def stop_timer(self):
        if self.timer.isActive():
            self.timer.stop()

    def update_train_state(self, delta_t=1.0):
        mass = self.current_train_weight * 1000  # Convert to kg

        current_velocity = self.current_speed * 0.44704  # Convert mph to m/s

        power_command_kw = self.commanded_power
        max_power_kw = 120

        # Use a local variable for effective power command
        effective_power_command_kw = power_command_kw

        # Limit effective commanded power
        if effective_power_command_kw > max_power_kw:
            effective_power_command_kw = max_power_kw
        elif effective_power_command_kw < 0:
            effective_power_command_kw = 0

        effective_power_command = effective_power_command_kw * 1000  # Convert kW to W

        # Calculate speed limit
        speed_limit_mps = min(self.commanded_speed, self.maximum_speed) * 0.44704  # Convert mph to m/s

        # Check if current speed exceeds speed limit
        if current_velocity > speed_limit_mps:
            self.auto_service_brake = True
        else:
            self.auto_service_brake = False

        # If emergency brake is engaged, turn off service brake
        if self.emergency_brake or self.passenger_emergency_brake:
            self.service_brake = False
            self.auto_service_brake = False

        # Check for brakes
        if self.emergency_brake or self.passenger_emergency_brake:
            acceleration = -2.73  # m/s²
            effective_power_command = 0
        elif self.service_brake or self.auto_service_brake:
            acceleration = -1.2  # m/s²
            effective_power_command = 0
        else:
            # Calculate force
            if current_velocity == 0:
                force = effective_power_command / 0.1  # Prevent division by zero
            else:
                force = effective_power_command / current_velocity

            frictional_force = 0.002 * mass * 9.8

            if force < frictional_force:
                force = 0
            else:
                force -= frictional_force

            acceleration = force / mass

            if acceleration > 0.5:
                acceleration = 0.5  # Cap positive acceleration to +0.5 m/s²

        new_velocity = current_velocity + acceleration * delta_t

        if new_velocity < 0:
            new_velocity = 0
            if acceleration < 0:
                acceleration = 0  # If speed is zero, acceleration cannot be negative

        # Convert units back for display
        self.current_speed = new_velocity * 2.23694  # m/s to mph
        self.current_acceleration = acceleration * 3.28084  # m/s² to ft/s²

        self.data_changed.emit()

        # Stop the timer if the train has stopped and no power is commanded
        if self.current_speed == 0 and (effective_power_command == 0 or self.current_acceleration == 0):
            self.stop_timer()


class BasePage(QWidget):
    def __init__(self, title, train_id_callback):
        super().__init__()

        # Set background color to very light gray
        self.setStyleSheet("background-color: #F5F5F5;")  # Very light gray

        # Main vertical layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header
        header_widget = QWidget()
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 10, 0)  # Add margin to the right
        header_layout.setSpacing(0)

        header_widget.setLayout(header_layout)
        header_widget.setStyleSheet("""
            background-color: rgb(43,120,228);  /* Blue */
            padding: 5px 0;
        """)
        header_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        # Title label
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the title
        title_label.setFont(QFont('Arial', 32, QFont.Weight.Bold))

        # Dropdown menu
        dropdown_layout = QHBoxLayout()
        dropdown_layout.setSpacing(5)
        dropdown_layout.setContentsMargins(0, 0, 0, 0)
        train_id_label = QLabel("Train ID:")
        train_id_label.setFont(QFont('Arial', 14))
        self.train_id_combo = QComboBox()
        self.train_id_combo.addItems(["1", "2", "3"])
        self.train_id_combo.setCurrentText("1")
        self.train_id_combo.setFixedWidth(60)
        self.train_id_combo.setStyleSheet("""
            QComboBox {
                color: black;
                border: 2px solid black;
                font-weight: bold;
            }
        """)
        # Prevent action on Train ID change
        # self.train_id_combo.currentTextChanged.connect(train_id_callback)

        # Add to dropdown_layout
        dropdown_layout.addWidget(train_id_label)
        dropdown_layout.addWidget(self.train_id_combo)
        dropdown_widget = QWidget()
        dropdown_widget.setLayout(dropdown_layout)

        # Add to header_layout
        header_layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignCenter)
        header_layout.addStretch()
        header_layout.addWidget(dropdown_widget, alignment=Qt.AlignmentFlag.AlignRight)

        # Add header_widget to main_layout
        main_layout.addWidget(header_widget)

        # Content area
        self.content_layout = QVBoxLayout()
        self.content_layout.setContentsMargins(10, 10, 10, 10)  # Added margins to prevent hugging edges
        self.content_layout.setSpacing(0)
        main_layout.addLayout(self.content_layout)

        self.setLayout(main_layout)

    def set_train_id_combo(self, train_id):
        self.train_id_combo.blockSignals(True)
        self.train_id_combo.setCurrentText(train_id)
        self.train_id_combo.blockSignals(False)


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
            button.clicked.connect(lambda checked, btn=button: self.toggle_button(btn))

            failure_layout.addWidget(label)
            failure_layout.addWidget(button)
            failure_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center each row

            failures_layout.addLayout(failure_layout)

        failures_container.setLayout(failures_layout)
        main_content_layout.addWidget(failures_container)

        # Add main content layout to content_layout
        self.content_layout.addLayout(main_content_layout)

    def set_train_data(self, train_data):
        # Disconnect previous train_data signal
        try:
            self.train_data.data_changed.disconnect(self.update_display)
        except:
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


class TrainModelPage(BasePage):
    def __init__(self, train_data, train_id_callback):
        super().__init__("                                Train Model", train_id_callback)
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
        static_info_label.setStyleSheet("color: black;")
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
            QPushButton {
                background-color: #8B0000;
                color: black;
                font-weight: bold;
            }
        """)
        self.passenger_emergency_brake_button.setFixedSize(440, 190)  # Made the panic button bigger
        self.passenger_emergency_brake_button.setEnabled(True)
        self.passenger_emergency_brake_button.clicked.connect(self.passenger_emergency_brake_pressed)

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

        # Add main_layout to content_vbox
        content_vbox.addLayout(main_layout)

        # Add a stretch to push the image to the bottom
        content_vbox.addStretch()

        # Load and display image
        image_label = QLabel()
        image = QImage('images/train_image.jpg')  # Replace with the actual image path
        pixmap = QPixmap.fromImage(image)
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add image_label to content_vbox
        content_vbox.addWidget(image_label)

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
        # Disconnect previous train_data signal
        try:
            self.train_data.data_changed.disconnect(self.update_display)
        except:
            pass
        self.train_data = train_data
        self.train_data.data_changed.connect(self.update_display)
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

    def passenger_emergency_brake_pressed(self):
        # Update the passenger emergency brake state
        self.train_data.set_value('passenger_emergency_brake', True)
        # Darken the color of the button
        self.passenger_emergency_brake_button.setStyleSheet("""
            background-color: #550000;  /* Darker red */
            color: black;
            font-weight: bold;
        """)


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

        # Current Commanded Power Display
        self.current_power_label = QLabel(f"Current Commanded Power: {self.parent().train_data.commanded_power} kW")
        self.current_power_label.setFont(QFont('Arial', 14))
        self.current_power_label.setStyleSheet("color: black;")
        layout.addWidget(self.current_power_label)

        # OK Button with white background and black text
        self.ok_button = QPushButton("OK")
        self.ok_button.setFont(QFont('Arial', 14))
        self.ok_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: black;
                border: 2px solid black;
                border-radius: 5px;
                padding: 5px 15px;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """)
        self.ok_button.clicked.connect(self.accept)
        layout.addWidget(self.ok_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    def get_announcement(self):
        return self.text_edit.text()


class SetCommandedPowerDialog(QDialog):
    def __init__(self, parent=None, current_power=0):
        super().__init__(parent)
        self.setWindowTitle("Set Commanded Power")
        self.setFixedSize(400, 200)

        layout = QVBoxLayout()

        # Current Commanded Power Display
        self.current_power_label = QLabel(f"Current Commanded Power: {current_power} kW")
        self.current_power_label.setFont(QFont('Arial', 14))
        self.current_power_label.setStyleSheet("color: black;")
        layout.addWidget(self.current_power_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Input Field
        self.label = QLabel("Enter the Commanded Power (kW):")
        self.label.setFont(QFont('Arial', 14))
        self.label.setStyleSheet("color: black;")
        layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.power_edit = QLineEdit(str(current_power))
        self.power_edit.setFont(QFont('Arial', 14))
        self.power_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.power_edit.setStyleSheet("color: black;")
        layout.addWidget(self.power_edit, alignment=Qt.AlignmentFlag.AlignCenter)

        # Buttons layout
        buttons_layout = QHBoxLayout()
        self.ok_button = QPushButton("OK")
        self.ok_button.setFont(QFont('Arial', 12, QFont.Weight.Bold))
        self.ok_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: black;
                border: 2px solid black;
                border-radius: 5px;
                padding: 5px 15px;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """)
        self.ok_button.clicked.connect(self.accept)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setFont(QFont('Arial', 12, QFont.Weight.Bold))
        self.cancel_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: black;
                border: 2px solid black;
                border-radius: 5px;
                padding: 5px 15px;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """)
        self.cancel_button.clicked.connect(self.reject)

        buttons_layout.addWidget(self.ok_button)
        buttons_layout.addWidget(self.cancel_button)

        layout.addLayout(buttons_layout)

        self.setLayout(layout)

    def get_commanded_power(self):
        try:
            power = float(self.power_edit.text())
            if power < 0:
                raise ValueError
            return power
        except ValueError:
            return None  # Invalid input


class TestBenchPage(BasePage):
    def __init__(self, train_data, train_id_callback):
        super().__init__("                                 Test Bench", train_id_callback)
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
        tc_input_layout.setHorizontalSpacing(10)  # Adjusted horizontal spacing
        tc_input_layout.setContentsMargins(0, 0, 0, 0)

        tc_data_items = [
            ("Commanded Power(kw)", "commanded_power"),
            ("Commanded Speed(km/h)", "commanded_speed_tc"),
            ("Authority(m)", "authority"),
            ("Service Brake", "service_brake"),
            ("Exterior Light", "exterior_light"),
            ("Interior Light", "interior_light"),
            ("Emergency Brake", "emergency_brake"),
            ("Beacon", "beacon"),
        ]

        for i, (label_text, var_name, *rest) in enumerate(tc_data_items):
            label = QLabel(label_text)
            label.setFont(self.font_label)
            label.setStyleSheet("color: black;")

            if var_name in ["service_brake", "exterior_light", "interior_light", "emergency_brake"]:
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
            elif var_name == "beacon":
                # Use a combo box for beacon with "We are approaching"
                station_combo = QComboBox()
                station_combo.addItems(["Station Alpha", "Station Beta", "Station Delta"])
                station_combo.setCurrentText(self.train_data.beacon_station)
                station_combo.setFont(self.font_value)
                station_combo.setStyleSheet("color: black;")
                station_combo.currentTextChanged.connect(self.update_beacon)
                tc_input_layout.addWidget(label, i, 0, alignment=Qt.AlignmentFlag.AlignLeft)

                beacon_layout = QHBoxLayout()
                prefix_label = QLabel("We are approaching")
                prefix_label.setFont(self.font_value)
                prefix_label.setStyleSheet("color: black;")
                beacon_layout.addWidget(prefix_label)
                beacon_layout.addWidget(station_combo)

                tc_input_layout.addLayout(beacon_layout, i, 1)
                unit_label = QLabel("")
                tc_input_layout.addWidget(unit_label, i, 2, alignment=Qt.AlignmentFlag.AlignLeft)
                self.tc_edit_fields["beacon_station"] = station_combo
            elif var_name == "commanded_power":
                # Replace QLineEdit and OK button with a single button to open a popup
                set_power_button = QPushButton("Set Commanded Power")
                set_power_button.setFont(self.font_value)
                set_power_button.setFixedWidth(200)
                set_power_button.setStyleSheet("""
                    QPushButton {
                        background-color: #2196F3;
                        color: white;
                        border-radius: 5px;
                        padding: 5px 10px;
                    }
                    QPushButton:hover {
                        background-color: #0b7dda;
                    }
                """)
                set_power_button.clicked.connect(self.open_set_commanded_power_dialog)
                tc_input_layout.addWidget(label, i, 0, alignment=Qt.AlignmentFlag.AlignLeft)
                tc_input_layout.addWidget(set_power_button, i, 1, alignment=Qt.AlignmentFlag.AlignLeft)
                unit_label = QLabel(rest[0] if rest else "")
                unit_label.setFont(self.font_label)
                unit_label.setStyleSheet("color: black;")
                tc_input_layout.addWidget(unit_label, i, 2, alignment=Qt.AlignmentFlag.AlignLeft)
                self.tc_edit_fields[var_name] = set_power_button
            else:
                # Numeric inputs
                value = getattr(self.train_data, var_name)
                value_edit = QLineEdit(str(value))
                value_edit.setFont(self.font_value)
                value_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Centered text
                value_edit.setMaximumWidth(80)
                value_edit.setStyleSheet("color: black;")
                value_edit.editingFinished.connect(lambda var=var_name, edit=value_edit: self.update_train_data(var, edit.text()))
                tc_input_layout.addWidget(label, i, 0, alignment=Qt.AlignmentFlag.AlignLeft)
                tc_input_layout.addWidget(value_edit, i, 1, alignment=Qt.AlignmentFlag.AlignLeft)
                unit_label = QLabel(rest[0] if rest else "")
                unit_label.setFont(self.font_label)
                unit_label.setStyleSheet("color: black;")
                # Adjust unit label position
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
        cabin_control_layout.setHorizontalSpacing(10)  # Adjusted horizontal spacing
        cabin_control_layout.setContentsMargins(0, 0, 0, 0)

        cabin_data_items = [
            ("Desired Temperature", "desired_temperature", "°F"),
            ("Train Left Door", "train_left_door"),
            ("Train Right Door", "train_right_door"),
            ("Advertisement", "advertisement", ["Picture1", "Picture2", "Picture3"]),
            ("Passenger Boarding", "passenger_boarding", ""),
        ]

        for i, (label_text, var_name, *rest) in enumerate(cabin_data_items):
            label = QLabel(label_text)
            label.setFont(self.font_label)
            label.setStyleSheet("color: black;")

            if var_name in ["train_left_door", "train_right_door"]:
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
            elif var_name == "passenger_boarding":
                # Numeric input with OK button
                value = getattr(self.train_data, var_name)
                value_edit = QLineEdit(str(value))
                value_edit.setFont(self.font_value)
                value_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Centered text
                value_edit.setMaximumWidth(80)
                value_edit.setStyleSheet("color: black;")
                # Do not connect editingFinished
                cabin_control_layout.addWidget(label, i, 0, alignment=Qt.AlignmentFlag.AlignLeft)

                # Create a horizontal layout for input field and OK button
                input_layout = QHBoxLayout()
                input_layout.setContentsMargins(0, 0, 0, 0)
                input_layout.setSpacing(5)
                input_layout.addWidget(value_edit)

                ok_button = QPushButton("OK")
                ok_button.setFont(self.font_value)
                ok_button.setFixedWidth(50)
                ok_button.setStyleSheet("""
                    QPushButton {
                        color: black;
                        border: 2px solid black;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #E0E0E0;
                    }
                """)
                ok_button.clicked.connect(lambda _, var=var_name, edit=value_edit: self.update_passenger_boarding(var, edit.text()))
                input_layout.addWidget(ok_button)

                cabin_control_layout.addLayout(input_layout, i, 1)

                unit_label = QLabel(rest[0] if rest else "")
                unit_label.setFont(self.font_label)
                unit_label.setStyleSheet("color: black;")
                cabin_control_layout.addWidget(unit_label, i, 2, alignment=Qt.AlignmentFlag.AlignLeft)
                self.cabin_edit_fields[var_name] = value_edit
            else:
                # Numeric inputs with unit label next to input field
                value = getattr(self.train_data, var_name)
                value_edit = QLineEdit(str(value))
                value_edit.setFont(self.font_value)
                value_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Centered text
                value_edit.setMaximumWidth(80)
                value_edit.setStyleSheet("color: black;")
                value_edit.editingFinished.connect(lambda var=var_name, edit=value_edit: self.update_train_data(var, edit.text()))
                cabin_control_layout.addWidget(label, i, 0, alignment=Qt.AlignmentFlag.AlignLeft)

                # Create a horizontal layout for input field and unit label
                input_layout = QHBoxLayout()
                input_layout.setContentsMargins(0, 0, 0, 0)
                input_layout.setSpacing(5)
                input_layout.addWidget(value_edit)

                unit_label = QLabel(rest[0] if rest else "")
                unit_label.setFont(self.font_label)
                unit_label.setStyleSheet("color: black;")
                input_layout.addWidget(unit_label)

                cabin_control_layout.addLayout(input_layout, i, 1)
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

        # Update the displays when data changes
        self.train_data.data_changed.connect(self.update_display)

    def set_train_data(self, train_data):
        # Disconnect previous train_data signal
        try:
            self.train_data.data_changed.disconnect(self.update_display)
        except:
            pass
        self.train_data = train_data
        self.train_data.data_changed.connect(self.update_display)
        self.update_button_states()

    def toggle_on_off(self, var_name, button):
        is_on = button.isChecked()
        button.setText("ON" if is_on else "OFF")
        # Use the same green color as in Train Model page
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {'green' if is_on else 'lightgray'};
                color: black;
                font-weight: bold;
            }}
        """)
        self.train_data.set_value(var_name, is_on)
        # Map variables with different names
        if var_name == 'interior_light':
            self.train_data.set_value('interior_light_on', is_on)
        elif var_name == 'exterior_light':
            self.train_data.set_value('exterior_light_on', is_on)
        elif var_name == 'train_left_door':
            self.train_data.set_value('left_door_open', is_on)
        elif var_name == 'train_right_door':
            self.train_data.set_value('right_door_open', is_on)
        elif var_name in ['service_brake', 'emergency_brake']:
            # Update train state when brakes are applied
            self.train_data.set_value(var_name, is_on)
            self.update_display()

    def open_set_commanded_power_dialog(self):
        dialog = SetCommandedPowerDialog(self, current_power=self.train_data.commanded_power)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_power = dialog.get_commanded_power()
            if new_power is not None:
                self.train_data.set_value('commanded_power', new_power)
            else:
                # Handle invalid input if necessary
                pass

    def update_train_data(self, var_name, value):
        # Update the variable in train_data
        try:
            # Convert to appropriate type
            if var_name in ['commanded_speed_tc', 'authority', 'desired_temperature', 'passenger_boarding']:
                current_value = getattr(self.train_data, var_name)
                if isinstance(current_value, int):
                    value = int(value)
                elif isinstance(current_value, float):
                    value = float(value)
            self.train_data.set_value(var_name, value)
            # Map variables with different names and perform unit conversions
            if var_name == 'commanded_speed_tc':
                self.train_data.set_value('commanded_speed_tc', value)
                # Commanded Speed is updated via set_value method
            elif var_name == 'authority':
                # Convert meters to feet
                value_ft = float(value) * 3.28084
                self.train_data.set_value('commanded_authority', value_ft)
            elif var_name == 'desired_temperature':
                # Update actual temperature
                self.train_data.set_value('cabin_temperature', value)
        except ValueError:
            pass  # Handle invalid input as desired

    def update_commanded_power(self, var_name, value):
        # This method is no longer needed as commanded power is set via popup
        pass

    def update_passenger_boarding(self, var_name, value):
        # Update passenger boarding and add to passenger count
        try:
            value = int(value)
            self.train_data.passenger_boarding = value
            # Add passenger_boarding to passenger_count
            self.train_data.passenger_count += self.train_data.passenger_boarding
            self.train_data.passenger_boarding = 0  # Reset passenger_boarding to 0
            self.train_data.update_train_weight()
            self.update_display()
        except ValueError:
            pass  # Handle invalid input

    def update_beacon(self, station):
        beacon_text = f"We are approaching {station}"
        self.train_data.set_value('beacon_station', station)
        self.train_data.set_value('beacon', beacon_text)

    def open_announcement_dialog(self):
        dialog = AnnouncementDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            announcement = dialog.get_announcement()
            self.train_data.set_value('announcement', announcement)

    def update_button_states(self):
        # Initialize button states based on train_data
        for var_name, button in self.tc_edit_fields.items():
            if var_name in ["service_brake", "exterior_light", "interior_light", "emergency_brake"]:
                is_on = getattr(self.train_data, var_name)
                button.setChecked(is_on)
                button.setText("ON" if is_on else "OFF")
                # Use the same green color as in Train Model page
                button.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {'green' if is_on else 'lightgray'};
                        color: black;
                        font-weight: bold;
                    }}
                """)
        for var_name, button in self.cabin_edit_fields.items():
            if var_name in ["train_left_door", "train_right_door"]:
                is_on = getattr(self.train_data, var_name)
                button.setChecked(is_on)
                button.setText("ON" if is_on else "OFF")
                # Use the same green color as in Train Model page
                button.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {'green' if is_on else 'lightgray'};
                        color: black;
                        font-weight: bold;
                    }}
                """)

    def update_display(self):
        # Update the state of the brake buttons
        for var_name in ['service_brake', 'emergency_brake']:
            button = self.tc_edit_fields.get(var_name)
            if button:
                is_on = getattr(self.train_data, var_name)
                button.setChecked(is_on)
                button.setText("ON" if is_on else "OFF")
                button.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {'green' if is_on else 'lightgray'};
                        color: black;
                        font-weight: bold;
                    }}
                """)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt6 Train Control Application")
        self.setGeometry(100, 100, 1000, 620)  # Increased window size

        # Create TrainData instances for each Train ID
        self.train_data_dict = {'1': TrainData(), '2': TrainData(), '3': TrainData()}
        self.current_train_id = '1'
        self.current_train_data = self.train_data_dict[self.current_train_id]

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
        self.train_model_page = TrainModelPage(self.current_train_data, self.train_id_changed)
        self.test_bench_page = TestBenchPage(self.current_train_data, self.train_id_changed)
        self.murphy_page = MurphyPage(self.current_train_data, self.train_id_changed)

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

    def train_id_changed(self, new_train_id):
        pass  # No action on Train ID change

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