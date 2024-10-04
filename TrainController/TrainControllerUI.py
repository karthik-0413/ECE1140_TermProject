from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QMessageBox
)
from PyQt6.QtCore import Qt, QElapsedTimer, QTimer
# from TrainController import TrainController
from TrainControllerTestBench import TrainControllerTestBench
from TrainControllerCommunicateSignals import Communicate
import time
from PyQt6.QtCore import QCoreApplication

class TrainControllerUI(QWidget):
    def __init__(self, communicator: Communicate):
        super().__init__()
        
        # For for pyqtsignals file
        self.communicator = communicator

        # For Timer
        self.elapsed_timer = QElapsedTimer()
        self.timer = QTimer()
        
        # Train Specs
        self.mass = 56700
        self.friction_coefficient = 0.05
        self.max_power = 120000

        # For the failure modes
        self.engine_fail = False
        self.brake_fail = False
        self.signal_fail = False
        
        # For the passenger brake
        self.passenger_brake = False
        
        # Temperature Values
        self.current_temperature = 70.0
        self.desired_temperature = 0.0
        
        # For the toggling the different status lights
        self.exterior_lights = False
        self.interior_lights = False
        self.left_door = False
        self.right_door = False
        self.brake_status = False
        
        # Engineer's Values
        self.kp = 25.0
        self.ki = 0.5
        
        # Vital Variables
        self.commanded_speed = 31.07
        self.commanded_authority = 750.0
        
        # Key input and output
        self.current_velocity = 10.0
        self.power_command = 0.0
        self.next_station = 'Shadyside'
        
        # Inputs by User
        self.setpoint_speed = 0.0
        self.setpoint_speed_submit = False
        self.operation_mode = 1    # 1 for manual, 0 for automatic
        # In manual mode, the user is allowed to pick the setpoint speed
        # In automatic mode, the commanded speed is the setpoint speed
            # Disable doors open and close buttons
            # Disable interior lights
            # Disable exterior lights
            # Disable brake button
            # Disable setpoint speed input
            
        self.speed_limit = 31.07    # Speed Limit in mph (70km/hr)
        
        # Everything Interactable for the User
        self.driver_service_brake_command = False
        self.driver_emergency_brake_command = False
        
        # Deceleration for Braking
        self.service_brake_deceleration = -1.2
        self.emergency_brake_deceleration = -2.73
        
        # Variables needed for speed increase
        self.previous_acceleration = 0.0
        self.current_position = 0.0
        
        # Variables needed for power command
        self.desired_velocity = 0.0
        self.uk_current = 0.0
        self.ek_current = 0.0
        self.uk_previous = 0.0
        self.ek_previous = 0.0
        self.dt = 1.0
        
        # Variables for position
        # self.previous_position = 0.0
        # self.previous_velocity = 0.0
    
    
        # All pyqtsignals
        self.communicator.engine_failure_signal.connect(self.handle_engine_failure)
        self.communicator.brake_failure_signal.connect(self.handle_brake_failure)
        self.communicator.signal_failure_signal.connect(self.handle_signal_failure)
        self.communicator.passenger_brake_command_signal.connect(self.handle_passenger_brake_command)
        self.communicator.commanded_speed_signal.connect(self.handle_commanded_speed)
        self.communicator.commanded_authority_signal.connect(self.handle_commanded_authority)
        self.communicator.passenger_brake_command_signal.connect(self.handle_passenger_brake_command)
        self.communicator.engineer_kp_signal.connect(self.updated_set_kp)
        self.communicator.engineer_ki_signal.connect(self.updated_set_ki)
        self.communicator.station_name_signal.connect(self.handle_station_name)
        self.communicator.current_velocity_signal.connect(self.handle_current_velocity)
        
        
        # UI STARTS HERE
        self.setWindowTitle("Train Controller")
        self.setStyleSheet("background-color: lightgray;")

        # Main Layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 15, 30, 10)

        # Tabs and Main Header
        # tab_layout = QHBoxLayout()
        # tab1 = QLabel("Train Controller")
        # tab2 = QLabel("Engineer's View")
        # tab3 = QLabel("Test Bench")
        # tab_layout.addWidget(tab1)
        # tab_layout.addWidget(tab2)
        # tab_layout.addWidget(tab3)

        # Title Label
        title_banner = QHBoxLayout()
        title_banner.setSpacing(0)
        title_label = QLabel("Train Controller")
        title_label.setStyleSheet("font: Times New Roman; font-size: 30px; font-weight: bold; color: white; background-color: blue; border-radius: 10px; padding: 10px;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_banner.addWidget(title_label)

        # Create a container widget for the title banner to avoid the main layout's margin restriction
        title_container = QWidget()
        title_container.setLayout(title_banner)
        title_container.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(title_container)

        # Train ID Combo Box in the header
        # self.train_id_combo = QComboBox()
        # self.train_id_combo.addItems(["1", "2", "3"])
        # self.train_id_combo.setStyleSheet("background-color: white; color: black;")
        # self.train_id_combo.setEnabled(False)
        # title_banner.addWidget(title_label, 3)
        # title_banner.addWidget(QLabel("Train ID:"), 0)
        # title_banner.addWidget(self.train_id_combo, 0)

        # Main Grid Layout for UI Elements
        main_grid = QGridLayout()

        # LEFT SECTION (Speed Controls and Operation Mode)
        # Speed Information
        current_speed_box = QVBoxLayout()
        current_speed_label = QLabel("Current Speed:")
        current_speed_label.setStyleSheet("padding-top: 10px; font-size: 14px; font-weight: bold; color: black; margin-top: 0px; margin-right: 100px")

        self.current_speed_edit = QLineEdit(str(self.current_velocity))
        self.timer.timeout.connect(lambda: self.update_current_speed(self.current_velocity))
        self.current_speed_edit.setText(self.current_speed_edit.text() + " mph")
        self.current_speed_edit.setEnabled(False)
        self.current_speed_edit.setStyleSheet("background-color: lightgray; max-width: 100px; border-radius: 5px; color: black; border: 2px solid black; padding: 2px;")
        current_speed_box.addWidget(current_speed_label)
        current_speed_box.addWidget(self.current_speed_edit)
        current_speed_box.addSpacerItem(QSpacerItem(0, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        main_grid.addLayout(current_speed_box, 0, 0)


        commanded_speed_box = QVBoxLayout()
        commanded_speed_label = QLabel("Commanded Speed:")
        commanded_speed_label.setStyleSheet("font-size: 14px; font-weight: bold; color: black;")
        self.commanded_speed_edit = QLineEdit(str(self.commanded_speed))
        self.commanded_speed_edit.setText(self.commanded_speed_edit.text() + " mph")
        self.commanded_speed_edit.setEnabled(False)
        self.commanded_speed_edit.setStyleSheet("background-color: lightgray; max-width: 100px; border-radius: 5px; color: black; border: 2px solid black; padding: 2px;")
        commanded_speed_box.addWidget(commanded_speed_label)
        commanded_speed_box.addWidget(self.commanded_speed_edit)
        commanded_speed_box.addSpacerItem(QSpacerItem(0, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        main_grid.addLayout(commanded_speed_box, 1, 0)


        commanded_authority_box = QVBoxLayout()
        commanded_authority_label = QLabel("Commanded Authority:")
        commanded_authority_label.setStyleSheet("font-size: 14px; font-weight: bold; color: black;")
        self.commanded_authority_edit = QLineEdit(str(self.commanded_authority))
        self.timer.start(1000)  # Update every 100 ms
        self.timer.timeout.connect(lambda: self.update_commanded_authority() if not self.signal_fail else None)
        self.commanded_authority_edit.setText(self.commanded_authority_edit.text() + " feet")
        self.commanded_authority_edit.setEnabled(False)
        self.commanded_authority_edit.setStyleSheet("background-color: lightgray; max-width: 100px; border-radius: 5px; color: black; margin-bottom: 35px; border: 2px solid black; padding: 2px;")
        commanded_authority_box.addWidget(commanded_authority_label)
        commanded_authority_box.addWidget(self.commanded_authority_edit)
        
        main_grid.addLayout(commanded_authority_box, 2, 0)

        # Operational Mode
        operational_mode_label = QLabel("Operational Mode:")
        operational_mode_label.setStyleSheet("font-size: 14px; font-weight: bold; color: black; margin-bottom 30px;")
        main_grid.addWidget(operational_mode_label, 4, 0)
        
        self.manual_button = QPushButton("Manual")
        self.manual_button.clicked.connect(self.set_manual_mode)
        main_grid.addWidget(self.manual_button, 5, 0)

        self.automatic_button = QPushButton("Automatic")
        self.automatic_button.clicked.connect(self.set_automatic_mode)
        main_grid.addWidget(self.automatic_button, 6, 0)
        
        self.operation_mode_timer = QTimer(self)
        self.operation_mode_timer.timeout.connect(self.update_button_styles)
        self.operation_mode_timer.start(10)  # Check every 10 milliseconds
        

        # Service brake button
        self.brake_button = QPushButton("   SERVICE BRAKE")
        self.brake_button.setStyleSheet("margin-top: 40px; background-color: yellow; font-size: 16px; border-radius: 10px; font-weight: bold; color: black; border: 3px solid black; padding-top: 20px; max-width: 150px; padding-bottom: 20px; padding-right: 15px")
        # Add the horizontal layout to the main grid
        self.brake_button.pressed.connect(self.apply_service_brake)
        self.brake_button.pressed.connect(self.start_braking)
        self.brake_button.released.connect(self.stop_braking)
        main_grid.addWidget(self.brake_button, 8, 0)  # Ensure it spans across two columns

        # CENTER SECTION (Setpoint Speed and Power Command)
        setpoint_box = QVBoxLayout()

        # Setpoint Label
        setpoint_label = QLabel("Setpoint Speed")
        setpoint_label.setStyleSheet("padding-left: 20px; font-size: 30px; font-weight: bold; color: black;")
        setpoint_box.addWidget(setpoint_label, alignment=Qt.AlignmentFlag.AlignCenter)  # Add to setpoint_box with center alignment

        # Setpoint Layout
        setpoint_layout = QHBoxLayout()
        setpoint_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins

        self.setpoint_speed_edit = QLineEdit()
        self.setpoint_speed_edit.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.setpoint_speed_edit.editingFinished.connect(self.update_setpoint_speed_calculations)
        self.setpoint_speed_edit.setPlaceholderText("50")
        self.setpoint_speed_edit.setStyleSheet("margin-left: 50px; max-width: 100px; color: black; border: 2px solid black; border-radius: 5px; padding: 5px;")
        self.setpoint_speed_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setpoint_unit = QLabel("mph")
        self.setpoint_unit.setStyleSheet("font-size: 12px; color: black;")
        
        self.setpoint_confirm = QPushButton("OK")
        self.setpoint_confirm.setStyleSheet("background-color: green; color: white; border: 2px solid black; padding: 5px; border-radius: 5px;")
        self.setpoint_confirm.pressed.connect(self.update_setpoint_speed_calculations)
        # ONLY Call that function if the button is pressed and when editing th einput box it should wait til the butotn is pressed again to call that function

        # Add widgets to setpoint_layout
        setpoint_layout.addWidget(self.setpoint_speed_edit, alignment=Qt.AlignmentFlag.AlignCenter)
        setpoint_layout.addWidget(self.setpoint_unit, alignment=Qt.AlignmentFlag.AlignCenter)
        setpoint_layout.addWidget(self.setpoint_confirm, alignment=Qt.AlignmentFlag.AlignCenter)

        # Add setpoint_layout to setpoint_box
        setpoint_box.addLayout(setpoint_layout)

        # Finally, add setpoint_box to the main grid at the desired position
        main_grid.addLayout(setpoint_box, 1, 1, 1, 1, Qt.AlignmentFlag.AlignCenter)


        # Checkmark
        # self.setpoint_check = QPushButton()
        # self.setpoint_check.setIcon(QIcon('Eo_circle_green_checkmark.png'))
        # self.setpoint_check.setStyleSheet("background-color: white; border: none; padding: 0px;")
        # main_grid.addWidget(self.setpoint_check, 1, 3)

        # Power Command (Centered Narrower Input Box)
        power_command_label = QLabel("Power Command")
        power_command_label.setStyleSheet("font-size: 25px; font-weight: bold; color: black; padding-left: 22px;")
        main_grid.addWidget(power_command_label, 4, 1, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)

        power_command_layout = QHBoxLayout()
        self.power_command_edit = QLineEdit(str(self.power_command))
        # Connect to update function every time setpoint speed is changed
        self.setpoint_speed_edit.textChanged.connect(lambda: self.update_power_command())
        # Timer to update power command every millisecond
        # self.power_command_timer = QTimer(self)
        # self.power_command_timer.timeout.connect(lambda: self.update_power_command(self.setpoint_speed, self.current_velocity))
        # self.power_command_timer.start(1)  # Update every 1 millisecond
        self.power_command_edit.setStyleSheet("font-size: 20px; max-width: 100px; color: black; border: 2px solid black; border-radius: 5px; padding: 5px;")
        self.power_command_edit.setEnabled(False)
        self.power_command_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.power_unit = QLabel("kWatts")
        self.power_unit.setStyleSheet("font-size: 16px; color: black;")
        self.power_command_edit.setStyleSheet("margin-left: 50px; max-width: 100px; color: black; border: 2px solid black; border-radius: 5px; padding: 5px; background-color: lightgray;")
        self.power_unit.setStyleSheet("font-size: 12px; color: black; background-color: lightgray;")
        power_command_layout.addWidget(self.power_command_edit, alignment=Qt.AlignmentFlag.AlignCenter)
        power_command_layout.addWidget(self.power_unit, alignment=Qt.AlignmentFlag.AlignCenter)
        main_grid.addLayout(power_command_layout, 5, 1, 1, 1, Qt.AlignmentFlag.AlignCenter)

        # RIGHT SECTION (Train Controls)
        current_temp_box = QVBoxLayout()
        current_temp_label = QLabel("Current Train Temperature:")
        current_temp_label.setStyleSheet("font-size: 14px; font-weight: bold; color: black; padding-left: 40px;")
        self.current_temp_edit = QLineEdit(f"{self.current_temperature}")
        self.current_temp_edit.setText(f"{self.current_temperature} °F")
        # self.current_speed_edit.setText(self.current_speed_edit.text() + " mph")
        
        
        # Timer to update the current temperature display
        # self.temp_update_timer = QTimer(self)
        # self.temp_update_timer.timeout.connect(self.update_current_temp_display)
        # self.temp_update_timer.start(1000)  # Update every 1000 milliseconds (1 second)
        # self.current_temp_edit.setText(self.current_temp_edit.text() + " °F")
        self.current_temp_edit.setEnabled(False)
        self.current_temp_edit.setStyleSheet("background-color: lightgray; max-width: 100px; color: black; margin-left: 45px; border: 2px solid black; border-radius: 5px; padding: 2px;")
        current_temp_box.addWidget(current_temp_label)
        current_temp_box.addWidget(self.current_temp_edit)
        current_temp_box.addSpacerItem(QSpacerItem(0, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        main_grid.addLayout(current_temp_box, 0, 3)


        # Create the label for the desired train temperature
        desired_temp_box = QVBoxLayout()
        desired_temp_label = QLabel("Desired Train Temperature:")
        desired_temp_label.setStyleSheet("font-size: 14px; font-weight: bold; color: black; padding-left: 40px;")

        
        # Create a QLineEdit for numeric temperature input
        self.temp_input = QLineEdit()
        self.temp_input.setStyleSheet("max-width: 200px; color: black; margin-left: 40px; border: 2px solid black; border-radius: 5px; padding: 3px;")
        self.temp_input.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.temp_input.setPlaceholderText("Enter temperature (70°F to 100°F)")  # Optional placeholder text
        self.temp_input.editingFinished.connect(self.update_desired_temperature)

        # Add the label and input field to the layout
        desired_temp_box.addWidget(desired_temp_label)
        desired_temp_box.addWidget(self.temp_input)

        # Add the QLineEdit to the main grid at the desired position
        main_grid.addLayout(desired_temp_box, 1, 3)


        # Interior Lights Control
        interior_lights_layout = QHBoxLayout()
        interior_lights_label = QLabel("Interior Lights Status:")
        interior_lights_label.setStyleSheet("font-size: 14px; font-weight: bold; color: black; padding-left: 40px;")
        self.interior_lights_status = QPushButton("ON")
        self.interior_lights_status.setStyleSheet("background-color: #f5c842; max-width: 80px; border: 2px solid black; border-radius: 5px; padding: 3px;")
        self.interior_lights_status.pressed.connect(lambda: self.toggle_interior_lights(self.interior_lights))
        interior_lights_layout.addWidget(interior_lights_label)
        interior_lights_layout.addWidget(self.interior_lights_status)
        interior_lights_layout.addSpacerItem(QSpacerItem(20, 20))
        main_grid.addLayout(interior_lights_layout, 2, 3)


        # Exterior Lights Control
        exterior_lights_layout = QHBoxLayout()
        exterior_lights_label = QLabel("Exterior Lights Status:")
        exterior_lights_label.setStyleSheet("font-size: 14px; font-weight: bold; color: black; padding-left: 40px;")
        self.exterior_lights_status = QPushButton("OFF")
        self.exterior_lights_status.setStyleSheet("background-color: #888c8b; max-width: 80px; border: 2px solid black; border-radius: 5px; padding: 3px;")
        self.exterior_lights_status.pressed.connect(lambda: self.toggle_exterior_lights(self.exterior_lights))
        exterior_lights_layout.addWidget(exterior_lights_label)
        exterior_lights_layout.addWidget(self.exterior_lights_status)
        exterior_lights_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum))
        main_grid.addLayout(exterior_lights_layout, 3, 3)


        # Brake Status Control
        brake_status_layout = QHBoxLayout()
        brake_status_label = QLabel("Brake Status:")
        brake_status_label.setStyleSheet("font-size: 14px; font-weight: bold; color: black; padding-left: 40px;")
        self.brake_status = QPushButton("OFF")
        # stylesheet for off
        self.brake_status.setStyleSheet("background-color: #888c8b; max-width: 80px; border: 2px solid black; border-radius: 5px; padding: 3px;")
        brake_status_layout.addWidget(brake_status_label)
        brake_status_layout.addWidget(self.brake_status)
        brake_status_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum))
        main_grid.addLayout(brake_status_layout, 4, 3)



        # Right Door Status Control
        right_door_layout = QHBoxLayout()
        right_door_status_label = QLabel("Right Door Status:")
        right_door_status_label.setStyleSheet("font-size: 14px; font-weight: bold; color: black; padding-left: 40px;")
        self.right_door_status = QPushButton("CLOSE")
        self.right_door_status.setStyleSheet("background-color: red; max-width: 80px; border: 2px solid black; border-radius: 5px; padding: 3px;")
        right_door_layout.addWidget(right_door_status_label)
        right_door_layout.addWidget(self.right_door_status)
        right_door_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum))
        main_grid.addLayout(right_door_layout, 5, 3)



        # Left Door Status Control
        left_door_layout = QHBoxLayout()
        left_door_status_label = QLabel("Left Door Status:")
        left_door_status_label.setStyleSheet("font-size: 14px; font-weight: bold; color: black; padding-left: 40px;")
        self.left_door_status = QPushButton("CLOSE")
        self.left_door_status.setStyleSheet("background-color: red; max-width: 80px; border: 2px solid black; border-radius: 5px; padding: 3px;")
        left_door_layout.addWidget(left_door_status_label)
        left_door_layout.addWidget(self.left_door_status)
        left_door_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum))
        main_grid.addLayout(left_door_layout, 6, 3)



        train_engine_failure = QVBoxLayout()
        brake_failure = QVBoxLayout()
        signal_pickup_failure = QVBoxLayout()
        all_failures = QHBoxLayout()
        all_failures.setSpacing(5)  # Set the spacing to 5 pixels

        # Create the label for "Train Engine Failure"
        train_engine_fail_label = QLabel('<div style="text-align: center;">Train Engine<br>Failure</div>')
        train_engine_fail_label.setStyleSheet("font-size: 12px; font-weight: bold; color: black;")

        # Create the green indicator button
        engine_fail_indicator = QPushButton()
        engine_fail_indicator.setFixedSize(40, 40)  # Set a fixed size for the indicator button
        engine_fail_indicator = QPushButton()
        engine_fail_indicator.setFixedSize(40, 40)  # Set a fixed size for the indicator button
        engine_fail_indicator.setStyleSheet("background-color: green; border-radius: 20px; border: 2px solid black;")  # Green for no failure
        self.failure_timer = QTimer(self)
        self.failure_timer.timeout.connect(lambda: update_engine_failure_status(self.engine_fail))
        self.failure_timer.start(1000)  # Check every 1000 milliseconds (1 second)
        
        def update_engine_failure_status(failure: bool):
            # print(f"Engine failure status in Function: {failure}")
            if failure:
                engine_fail_indicator.setStyleSheet("background-color: red; border-radius: 20px; border: 2px solid black;")  # Red for failure
                QTimer.singleShot(3000, lambda: (engine_fail_indicator.setStyleSheet("background-color: green; border-radius: 20px; border: 2px solid black;"), setattr(self, 'engine_fail', False)))

            else:
                engine_fail_indicator.setStyleSheet("background-color: green; border-radius: 20px; border: 2px solid black;")  # Green for no failure

        # Create a vertical box layout for the train engine failure section
        train_engine_failure = QVBoxLayout()
        train_engine_failure.setSpacing(0)  # Set spacing to 0 to remove space between items

        # Add widgets to the vertical box layout
        train_engine_failure.addWidget(train_engine_fail_label, alignment=Qt.AlignmentFlag.AlignCenter)
        train_engine_failure.addWidget(engine_fail_indicator, alignment=Qt.AlignmentFlag.AlignCenter)

        # Brake Failure
        brake_fail_label = QLabel("Brake Failure")
        brake_fail_label.setStyleSheet("font-size: 12px; font-weight: bold; color: black; padding-left: 10px;")
        brake_fail_indicator = QPushButton()
        brake_fail_indicator.setFixedSize(40, 40)  # Set a fixed size for the indicator button
        brake_fail_indicator.setStyleSheet("background-color: green; border-radius: 20px; border: 2px solid black;")
        self.failure_timer = QTimer(self)
        self.failure_timer.timeout.connect(lambda: update_brake_failure_status(self.brake_fail))
        self.failure_timer.start(1000)  # Check every 1000 milliseconds (1 second)
        
        def update_brake_failure_status(failure: bool):
            # print(f"Brake failure status in Function: {failure}")
            if failure:
                brake_fail_indicator.setStyleSheet("background-color: red; border-radius: 20px; border: 2px solid black;")  # Red for failure
                QTimer.singleShot(3000, lambda: (brake_fail_indicator.setStyleSheet("background-color: green; border-radius: 20px; border: 2px solid black;"), setattr(self, 'brake_fail', False)))

            else:
                brake_fail_indicator.setStyleSheet("background-color: green; border-radius: 20px; border: 2px solid black;")  # Green for no failure
        brake_failure.addWidget(brake_fail_label, alignment=Qt.AlignmentFlag.AlignCenter)
        brake_failure.addWidget(brake_fail_indicator, alignment=Qt.AlignmentFlag.AlignCenter)

        # Signal Pickup Failure
        signal_fail_label =  QLabel('<div style="text-align: center;">Signal Pickup<br>Failure</div>')
        signal_fail_label.setStyleSheet("font-size: 12px; font-weight: bold; color: black; padding-left: 10px;")
        signal_fail_indicator = QPushButton()
        signal_fail_indicator.setFixedSize(40, 40)  # Set a fixed size for the indicator button
        signal_fail_indicator.setStyleSheet("background-color: green; border-radius: 20px; border: 2px solid black; padding-left: 10px;")
        self.failure_timer = QTimer(self)
        self.failure_timer.timeout.connect(lambda: update_signal_failure_status(self.signal_fail))
        self.failure_timer.start(1000)  # Check every 1000 milliseconds (1 second)
        
        def update_signal_failure_status(failure: bool):
            # print(f"Signal failure status in Function: {failure}")
            if failure:
                signal_fail_indicator.setStyleSheet("background-color: red; border-radius: 20px; border: 2px solid black;")  # Red for failure
                QTimer.singleShot(3000, lambda: (signal_fail_indicator.setStyleSheet("background-color: green; border-radius: 20px; border: 2px solid black;"), setattr(self, 'signal_fail', False)))
            else:
                signal_fail_indicator.setStyleSheet("background-color: green; border-radius: 20px; border: 2px solid black;")  # Green for no failure
        signal_pickup_failure.addWidget(signal_fail_label, alignment=Qt.AlignmentFlag.AlignCenter)
        signal_pickup_failure.addWidget(signal_fail_indicator, alignment=Qt.AlignmentFlag.AlignCenter)

        all_failures.addLayout(train_engine_failure)
        all_failures.addLayout(brake_failure)
        all_failures.addLayout(signal_pickup_failure)

        # Add the vertical box layout to the main grid at position (9, 1)
        main_grid.addLayout(all_failures, 8, 1)



        # Emergency Brake Button (Bottom-Right)
        self.emergency_brake_button = QPushButton("EMERGENCY BRAKE")
        self.emergency_brake_button.setStyleSheet("border: 3px solid black; margin-left: 40px; background-color: red; color: white; font-size: 20px; font-weight: bold; padding: 50px; border-radius: 10px;")
        self.emergency_brake_button.pressed.connect(self.apply_emergency_brake)
        self.emergency_brake_button.pressed.connect(self.start_braking)
        self.emergency_brake_button.released.connect(self.stop_braking)
        main_grid.addWidget(self.emergency_brake_button, 8, 3)

        # Add Components to the Main Layout
        main_layout.addLayout(title_banner)
        main_layout.addLayout(main_grid)
        

        # Set Main Layout
        self.setLayout(main_layout)
        
        
        
        
        
    ####################################################################
    # Functions to handle the backend logic of Train Controller Module #
    ####################################################################
    
    def set_manual_mode(self):
        self.operation_mode = 1
        # Disable the setpoint speed input field
        self.setpoint_speed_edit.setEnabled(True)
        # Disable the brake button
        self.brake_button.setEnabled(True)
        # Disable the interior lights button
        self.interior_lights_status.setEnabled(True)
        # Disable the exterior lights button
        self.exterior_lights_status.setEnabled(True)
        # Disable the left door button
        self.left_door_status.setEnabled(True)
        # Disable the right door button
        self.right_door_status.setEnabled(True)
        # Disable the emergency brake button
        self.emergency_brake_button.setEnabled(True)
        # Disable the service brake button
        self.brake_button.setEnabled(True)
        print("Operation Mode set to Manual")
        
    def set_automatic_mode(self):
        self.operation_mode = 0
        # Disable the setpoint speed input field
        self.setpoint_speed_edit.setEnabled(False)
        # Disable the brake button
        self.brake_button.setEnabled(False)
        # Disable the interior lights button
        self.interior_lights_status.setEnabled(False)
        # Disable the exterior lights button
        self.exterior_lights_status.setEnabled(False)
        # Disable the left door button
        self.left_door_status.setEnabled(False)
        # Disable the right door button
        self.right_door_status.setEnabled(False)
        # Disable the emergency brake button
        self.emergency_brake_button.setEnabled(False)
        # Disable the service brake button
        self.brake_button.setEnabled(False)
        print("Operation Mode set to Automatic")
    
    def handle_commanded_speed(self, speed: float):
        self.commanded_speed = speed
        print(f"Commanded speed: {self.commanded_speed}")
        self.commanded_speed_edit.setText(f"{speed:.2f} mph")
        
    def handle_commanded_authority(self, authority: float):
        self.commanded_authority = authority
        print(f"Commanded authority: {self.commanded_authority}")
        self.commanded_authority_edit.setText(f"{authority:.2f} ft")
    
    def update_commanded_authority(self):
        if self.signal_fail == False:
            self.commanded_authority -= 1
            # self.commanded_authority -= self.current_position
            self.commanded_authority_edit.setText(f"{self.commanded_authority:.2f} ft")
            if self.commanded_authority < 0.0:
                self.commanded_authority = 0.0
                self.commanded_authority_edit.setText("0.00 ft")
            if self.commanded_authority == 0.0:
                # Turn left and right doors to open
                self.left_door_status.setText("OPEN")
                self.left_door_status.setStyleSheet("background-color: green; max-width: 80px; border: 2px solid black; border-radius: 5px; padding: 3px;")
                self.right_door_status.setText("OPEN")
                self.right_door_status.setStyleSheet("background-color: green; max-width: 80px; border: 2px solid black; border-radius: 5px; padding: 3px;")
                self.communicator.announcement_signal.emit(f"Arrived at {self.next_station} Station")
                self.commanded_authority_edit.setText("0.00 ft")
                self.commanded_authority = 0.0
                print("Authority reached 0.0 ft")
    
    def handle_engine_failure(self, status: bool):
        if status == True:
            self.engine_fail = True
        else:
            self.engine_fail = False
        # print(f"Engine failure status: {status}")

    def handle_brake_failure(self, status: bool):
        if status == True:
            self.brake_fail = True
        else:
            self.brake_fail = False
        # print(f"Brake failure status: {status}")

    def handle_signal_failure(self, status: bool):
        if status == True:
            self.signal_fail = True
        else:
            self.signal_fail = False
        # print(f"Signal failure status: {status}")

    def handle_station_name(self, station_name: str):
        self.next_station = station_name
        print(f"Next Station: {self.next_station}")
        
    def handle_passenger_brake_command(self, status: bool):
        if status:
            self.passenger_brake = True
            if status and not hasattr(self, 'passenger_brake_popup_shown'):
                self.passenger_brake_popup_shown = True
                msg_box = QMessageBox()
                msg_box.setWindowTitle("Passenger Brake")
                msg_box.setText("Passenger brake has been pressed.")
                msg_box.setStyleSheet("font-size: 14px;")
                QTimer.singleShot(3000, msg_box.accept)  # Close the message box after 5 seconds
                msg_box.exec()
                
                while self.current_velocity > 0:
                    # Ensure velocity doesn't go negative
                    if self.current_velocity < 0:
                        self.current_velocity = 0

                    # Apply the formula: v_new = v_current + (a * dt)
                    dt = 2  # Set the elapsed time interval (2 seconds)
                    self.current_velocity += -2.73 * dt

                    # Ensure velocity doesn't drop below zero
                    if self.current_velocity < 0:
                        self.current_velocity = 0

                    # Print current velocity
                    print(f"Current Velocity: {self.current_velocity:.2f} mph")
                    self.current_speed_edit.setText(f"{self.current_velocity:.2f} mph")
                    QCoreApplication.processEvents()  # Process events to update the UI

                    # Wait for 2 seconds before the next update
                    time.sleep(dt)
                    
                    
            elif not status:
                self.passenger_brake_popup_shown = False
        else:
            self.passenger_brake = False
        print(f"Passenger brake command status: {status}")
        
    def update_desired_temperature(self):
        temp = int(self.temp_input.text())
        if 70 <= temp <= 100:
            self.desired_temperature = temp
            print(f"Desired temperature set to: {self.desired_temperature}°F")
            if self.current_temperature < self.desired_temperature:
                self.desired_temperature += 0.01
            else:
                self.desired_temperature -= 0.01
            self.reach_temperature()
        else:
            print("Temperature out of range. Please enter a value between 70°F and 100°F.")
            
    def reach_temperature(self, k=0.3, time_step=0.5):
        initial_temp = self.current_temperature
        desired_temp = self.desired_temperature

        current_temp = initial_temp
        # self.current_temperature = current_temp
        while abs(current_temp - desired_temp) > 0.01:  # Tolerance for stopping
            # Calculate the change in temperature using a first-order equation
            dT = k * (desired_temp - current_temp)
            
            # Update the current temperature
            current_temp += dT
            
            # Print the current temperature
            # self.current_temperature = current_temp
            self.current_temperature = current_temp
            self.update_current_temp_display(current_temp)
            QCoreApplication.processEvents()  # Process events to update the UI
            print(f"Current Temperature: {current_temp:.2f}°F")
            time.sleep(time_step)

        print(f"Reached Desired Temperature: {current_temp:.2f}°F")
        
    def update_current_temp_display(self, current_temp):
        self.current_temperature = current_temp
        self.current_temp_edit.setText(f"{self.current_temperature:.2f} °F")
        
    def toggle_interior_lights(self, status: bool):
        if status:
            self.interior_lights = False
            self.interior_lights_status.setText("OFF")
            self.interior_lights_status.setStyleSheet("background-color: #888c8b; max-width: 80px; border: 2px solid black; border-radius: 5px; padding: 3px;")
            print("Interior lights turned OFF")
        else:
            self.interior_lights = True
            self.interior_lights_status.setText("ON")
            self.interior_lights_status.setStyleSheet("background-color: #f5c842; max-width: 80px; border: 2px solid black; border-radius: 5px; padding: 3px;")
            print("Interior lights turned ON")
            
    def toggle_exterior_lights(self, status: bool):
        if status:
            self.exterior_lights = False
            self.exterior_lights_status.setText("OFF")
            self.exterior_lights_status.setStyleSheet("background-color: #888c8b; max-width: 80px; border: 2px solid black; border-radius: 5px; padding: 3px;")
            print("Exterior lights turned OFF")
        else:
            self.exterior_lights = True
            self.exterior_lights_status.setText("ON")
            self.exterior_lights_status.setStyleSheet("background-color: #f5c842; max-width: 80px; border: 2px solid black; border-radius: 5px; padding: 3px;")
            print("Exterior lights turned ON")
            
    def updated_set_kp(self, kp: float):
        if self.current_position == 0 or self.current_velocity == 0.0:
            self.kp = kp
            print(f"Updated Kp: {self.kp}")
        else:
            # Pop up saying cannot change Kp while train is moving
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Error")
            msg_box.setText("Cannot change Kp while the train is moving.")
            msg_box.setStyleSheet("font-size: 14px;")
            QTimer.singleShot(3000, msg_box.accept)  # Close the message box after 3 seconds
            msg_box.exec()
        
    def updated_set_ki(self, ki: float):
        if self.current_position == 0 or self.current_velocity == 0.0:
            self.ki = ki
            print(f"Updated Ki: {self.ki}")
        else:
            # Pop up saying cannot change Kp while train is moving
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Error")
            msg_box.setText("Cannot change Ki while the train is moving.")
            msg_box.setStyleSheet("font-size: 14px;")
            QTimer.singleShot(3000, msg_box.accept)  # Close the message box after 3 seconds
            msg_box.exec()
            
    def update_train_position(self):
        self.current_position = self.previous_position + (self.dt / 2) * (self.current_velocity + self.previous_velocity)
        
        # Updating the previous variables for next iteration
        self.previous_position = self.current_position
        self.previous_velocity = self.current_velocity
        
        print(f"Current Position: {self.current_position:.2f} ft")

        
    # Must be triggered everytime the desired speed changes
    # Setpoint Speed input
    # Commanded Speed
    # Service Brake
    # Emergency Brake
    # Commanded Speed
    def update_power_command(self):
        
        # Determining speed bound
        if self.desired_velocity > self.speed_limit:
            self.desired_velocity = self.speed_limit
        else:
            self.desired_velocity = self.desired_velocity
            
        # If the train needs to go slower, then power is zero and brakes are applied to go slower
        if self.current_velocity > self.desired_velocity:
            self.power_command = 0
            print("Service Brake Applied")
            # Break out of function here
            return self.power_command
            
        # Print desired and current speed
        print(f"Desired Speed: {self.desired_velocity:.2f} m/s, Current Speed: {self.current_velocity:.2f} m/s")
        
        # Finding the velocity error
        self.ek_current = self.desired_velocity - self.current_velocity
        print(f"Velocity Error: {self.ek_current:.2f} m/s")
        
        # Finding the power command
        self.power_command = self.kp * self.ek_current + self.ki * self.uk_current
        print(f"Power Command FINAL: {self.power_command:.2f} kW")

        # Using the different cases from lecture slides
        if self.power_command < self.max_power:
            self.uk_current = self.uk_previous + (self.dt / 2) * (self.ek_current + self.ek_previous)
        else:
            self.uk_current = self.uk_previous

        # Updating the previous variables for next iteration
        self.ek_previous = self.ek_current
        # Use, CLass, Sequence Diagram Order
        self.uk_previous = self.uk_current
        
        # Power command bound
        if self.power_command > self.max_power:
            self.power_command = self.max_power
        elif self.power_command < 0:
            self.power_command = 0
            print("Service Brake Applied")
        else:
            self.power_command = self.power_command
            
        self.power_command_edit.setText(f"{self.power_command:.2f} kW")
        print(f"Power Command: {self.power_command:.2f} kW")
        
        self.current_velocity = self.desired_velocity

            
        return self.power_command

    # def update_current_velocity(self, current_velocity, power_command, friction_coefficient, max_velocity, serviceBrake=False, emergencyBrake=False):
    #     dt = 5
        
    #     # Mass of full train
    #     mass = 56700
        
    #     # FORCE
    #     if current_velocity == 0:
    #         if serviceBrake or emergencyBrake:
    #             force = 0
    #         else:
    #             force = 1
    #     else:
    #         force = power_command / current_velocity
    #         print(f"Force: {force:.2f} N")
            
    #         frictional_force = friction_coefficient * mass * 9.8
            
    #         if force < frictional_force:
    #             print("Train has stopped moving")
                
    #         force -= frictional_force
            
    #         print(f"Frictional Force: {frictional_force:.2f} N")
            
    #     # ACCERLATION - Max acceleration is 0.5 m/s^2
    #     acceleration = force / mass
        
    #     if (acceleration > 0.5 and not serviceBrake and not emergencyBrake):
    #         acceleration = 0.5
        
    #     # VELOCITY - Max velocity is 19.44 m/s
    #     new_velocity = current_velocity + (dt / 2) * (acceleration + self.previous_acceleration)
        
    #     if (new_velocity >= max_velocity):
    #         new_velocity = max_velocity # m/s
            
    #     if (new_velocity <= 0):
    #         new_velocity = 0
        
    #     new_position = self.current_position + (dt / 2) * (new_velocity + current_velocity)
    #     print(f"New Velocity: {new_velocity:.2f} m/s, New Position: {new_position:.2f} m")

    #     self.previous_acceleration = acceleration
    #     self.current_position = new_position

    #     return new_velocity

    def update_speed(self):
            dt = 1
            new_speed = self.current_velocity  # Initialize new_speed with current_velocity
            if self.driver_emergency_brake_command:
                print("Emergency Brake Applied Here")
                new_speed = self.calculate_speed(self.current_velocity * 0.44704, self.emergency_brake_deceleration, dt) / 0.44704
            elif self.driver_service_brake_command:
                new_speed = self.calculate_speed(self.current_velocity * 0.44704, self.service_brake_deceleration, dt) / 0.44704
    
            if new_speed < 0:
                new_speed = 0.0
                # Set current speed UI display to 0.0
                self.current_speed_edit.setText("0.0 mph")
            
            self.current_velocity = round(new_speed, 2)
            print(f"Current Time: {dt} s")
            print(f"Current Speed: {self.current_velocity} km/h")
            
            if new_speed == 0.0:
                print("Train Stopped")
                self.timer.stop()
    
    def calculate_speed(self, u, a, t):
        return u + (a * t)
    
    def start_braking(self):
        self.brake_timer = QTimer(self)
        self.brake_timer.timeout.connect(self.update_speed)
        self.brake_timer.start(1000)  # Update every 1000 ms (1 second)
        print("Braking Started")
        # Turn brake status indicator to ON
        self.brake_status.setText("ON")
        self.brake_status.setStyleSheet("background-color: #f5c842; max-width: 80px; border: 2px solid black; border-radius: 5px; padding: 3px;")
        self.timer.start(1000)  # Update every 100 ms

    def stop_braking(self):
        self.timer.stop()
        # Update initial speed to the current speed for the next braking session
        # Turn brake status indicator to OFF
        self.brake_status.setText("OFF")
        self.brake_status.setStyleSheet("background-color: #888c8b; max-width: 80px; border: 2px solid black; border-radius: 5px; padding: 3px;")
        self.elapsed_timer.invalidate()
        print("Braking Stopped")
        self.driver_emergency_brake_command = False
        self.driver_service_brake_command = False
        self.current_velocity = self.current_velocity
        
    # When pressed by the driver (different deceleartion rate)
    def apply_emergency_brake(self):
        self.driver_emergency_brake_command = True
        print("Emergency Brake Activated!")
        # Additional logic for stopping the train
        # Add logic for stopping train using Physics equations - Done in update_speed()

    # When pressed by the driver (different deceleration rate)
    def apply_service_brake(self):
        self.driver_service_brake_command = True
        print("Service Brake Applied.")
        # Logic to gradually slow down the train
         # Add logic for stopping train using Physics equations - Done in update_speed()
         
    def update_current_speed(self, speed):
        self.current_velocity = speed
        self.current_speed_edit.setText(f"{self.current_velocity:.2f} mph")
        print(f"Current Speed updated to {self.current_velocity} mph")
        
    def update_setpoint_speed_calculations(self):   
        if self.operation_mode == 1:    
            # update value of setpoint speed to user input value
            self.desired_velocity = float(self.setpoint_speed_edit.text()) 
            # Update my current speed in the UI to the setpoint speed entered by the user
            self.current_speed_edit.setText(f"{self.desired_velocity} mph")    # Good updated value
            
            # PROBLEM: The current speed is not updating to the setpoint speed entered by the user if this is not here
            # DO I EVEN NEED THIS??
            
            print(f"Desired Speed: {self.desired_velocity} mph")    # Good updated value
            
            if self.desired_velocity > self.speed_limit:  
                self.desired_velocity = self.speed_limit
                self.setpoint_speed_edit.setText(str(self.speed_limit))
                
                # Display a message box indicating the speed entered is higher than the speed limit for that track
                msg_box = QMessageBox()
                msg_box.setWindowTitle("Speed Limit Exceeded")
                msg_box.setText(f"Setpoint speed cannot exceed the speed limit of {self.speed_limit} mph.")
                msg_box.setStyleSheet("font-size: 14px;")
                QTimer.singleShot(3000, msg_box.accept)  # Close the message box after 3 seconds
                msg_box.exec()
                
                # Increase speed until the desired speed is reached
                # while self.current_velocity < self.setpoint_speed:
                self.power_command = self.update_power_command()
                    # self.update_current_velocity(self.setpoint_speed, self.current_velocity, 1, self.mass, self.friction_coefficient)
            else:
                print(f"Setpoint Speed updated to {self.desired_velocity} mph")
                # while self.current_velocity < self.setpoint_speed:
                self.power_command = self.update_power_command()
                print(f"Power Command: {self.power_command}")
                    # self.update_current_velocity(self.setpoint_speed, self.current_velocity, 1, self.mass, self.friction_coefficient)
            
                
    def update_button_styles(self):
        if self.operation_mode == 1:
            self.manual_button.setStyleSheet("margin-top: 10px; margin-left: 10px; background-color: green; color: white; max-width: 100px; border-radius: 5px; padding-top: 10px; padding-bottom: 10px; border: 2px solid black;")
            self.automatic_button.setStyleSheet("margin-top: 10px; margin-left: 10px; background-color: gray; color: white; max-width: 100px; border-radius: 5px; padding-top: 10px; padding-bottom: 10px; border: 2px solid black;")
        else:
            self.manual_button.setStyleSheet("margin-top: 10px; margin-left: 10px; background-color: gray; color: white; max-width: 100px; border-radius: 5px; padding-top: 10px; padding-bottom: 10px; border: 2px solid black;")
            self.automatic_button.setStyleSheet("margin-top: 10px; margin-left: 10px; background-color: green; color: white; max-width: 100px; border-radius: 5px; padding-top: 10px; padding-bottom: 10px; border: 2px solid black;")
            
    def handle_current_velocity(self, velocity: float):
        self.current_velocity = velocity
        print(f"Current Velocity: {self.current_velocity}")
        self.current_speed_edit.setText(f"{self.current_velocity:.2f} mph")
        # self.update_train_position()
    
    
if __name__ == "__main__":
    app = QApplication([])
    communicator = Communicate()
    window = TrainControllerUI(communicator)
    window.show()
    app.exec()
