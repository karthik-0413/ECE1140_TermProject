import time
import json
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QMessageBox
)
from PyQt6.QtCore import Qt, QElapsedTimer, QTimer
from TrainControllerIntegratedCommunicateSignals import IntegratedCommunicate

class TrainIntegratedControllerUI(QWidget):
    def __init__(self, communicator: IntegratedCommunicate):
        super().__init__()
        
        # Switch Status & Polarity of Tracks (knows when entered new block and the status of the block)
        self.polarity = True
        self.enable_switch_status = False
        self.switch_status = False
        
        # Beacon Inputs of the different block numbers from current station to next
        self.beacon_block_numbers_inputs = [1, 2, 3]
        self.final_beacon_block_numbers_inputs = [i - 1 for i in self.beacon_block_numbers_inputs]
        
        # Variables needed for the Track Layouts (GREEN LINE)
        self.green_block_number = []
        self.green_speed_limit = []
        self.green_block_grade = []
        self.green_block_elevation = []
        self.green_infrastucture = []
        self.green_station_side = []
        self.green_block_length = []
        self.green_underground = []
        
        # Variables needed for the Track Layouts (RED LINE)
        self.red_block_number = []
        self.red_speed_limit = []
        self.red_block_grade = []
        self.red_block_elevation = []
        self.red_infrastucture = []
        self.red_station_side = []
        self.red_block_length = []
        self.red_underground = []   
        
        
        # Load the track layout data from GreenLine.json file in Track Layouts folder
        with open('TrainController/Track Layouts/GreenLine.json', 'r') as file:
            data = json.load(file)
            
            for entry in data:
                self.green_block_elevation.append(entry['ELEVATION (M)'])
                self.green_block_grade.append(entry['Block Grade (%)'])
                self.green_speed_limit.append(entry['Speed Limit (Km/Hr)'])
                self.green_underground.append('UNDERGROUND' in entry['Infrastructure'])
                self.green_infrastucture.append(entry['Infrastructure'])
                self.green_station_side.append(entry['Station Side'])
                self.green_block_length.append(entry['Block Length (m)'])
                self.green_block_number.append(entry['Block Number'])
                
            
        # Load the track layout data from GreenLine.json file in Track Layouts folder
        with open('TrainController/Track Layouts/RedLine.json', 'r') as file:
            data = json.load(file)
            
            for entry in data:
                self.red_block_elevation.append(entry['ELEVATION (M)'])
                self.red_block_grade.append(entry['Block Grade (%)'])
                self.red_speed_limit.append(entry['Speed Limit (Km/Hr)'])
                self.red_underground.append('UNDERGROUND' in entry['Infrastructure'])
                self.red_infrastucture.append(entry['Infrastructure'])
                self.red_station_side.append(entry['Station Side'])
                self.red_block_length.append(entry['Block Length (m)'])
                self.red_block_number.append(entry['Block Number'])
                
        
        # For for pyqtsignals file
        self.communicator = communicator

        # For Timer
        self.elapsed_timer = QElapsedTimer()
        self.timer = QTimer()
        
        # Train Specs
        self.max_power = 120000

        # For the failure modes
        self.engine_fail = False
        self.brake_fail = False
        self.signal_fail = False
        
        # For the passenger brake
        self.passenger_brake = False
        
        # Temperature Values
        self.current_temperature = 65.0
        self.desired_temperature = 0.0
        
        # For the toggling the different status lights
        self.exterior_lights = False
        self.interior_lights = False
        self.left_door = False
        self.right_door = False
        self.brake_status = False
        
        # Engineer's Values
        self.kp = 7173.0
        self.ki = 15.0
        
        # Vital Variables
        self.commanded_speed = 10   # 10 m/s = 22.3694 mph
        self.commanded_authority = 750.0
        
        # Key input and output
        self.current_velocity = 0.0
        self.previous_velocity = 0.0
        self.power_command = 0.0
        self.next_station = 'Shadyside'
        
        # Inputs by User
        self.setpoint_speed = 0.0
        self.setpoint_speed_submit = False
        self.operation_mode = 1    # 1 for manual, 0 for automatic
        self.speed_limit = 13.89    # Speed Limit in mph (50km/hr)
        
        # Everything Interactable for the User
        self.driver_service_brake_command = False
        self.driver_emergency_brake_command = False
        
        # Variable needed for updating position
        self.current_position = 0.0
        self.previous_position = 0.0
        
        # Variables needed for power command
        self.desired_velocity = 0.0
        self.uk_current = 0.0
        self.ek_current = 0.0
        self.uk_previous = 0.0
        self.ek_previous = 0.0
        self.dt = 1.0
        
        
        # Call the calculate_brake_distance function every millisecond
        self.timer.start(1000)
        self.timer.timeout.connect(self.calculate_brake_distance)

    
        # For Train Engineers Inputs
        self.communicator.engineer_kp_signal.connect(self.updated_set_kp)
        self.communicator.engineer_ki_signal.connect(self.updated_set_ki)
        
        # For Train Model Inputs
        self.communicator.current_velocity_signal.connect(self.handle_current_velocity)
        self.communicator.commanded_speed_signal.connect(lambda speed: self.handle_commanded_speed(speed) if not self.signal_fail else None)
        self.communicator.commanded_authority_signal.connect(self.handle_commanded_authority)
        self.communicator.engine_failure_signal.connect(self.handle_engine_failure)
        self.communicator.brake_failure_signal.connect(self.handle_brake_failure)
        self.communicator.signal_failure_signal.connect(self.handle_signal_failure)
        self.communicator.passenger_brake_command_signal.connect(self.handle_passenger_brake_command)
        self.communicator.station_name_signal.connect(self.handle_station_name)
        self.communicator.actual_temperature_signal.connect(self.handle_actual_temperature)
        self.communicator.blocks_between_stations_signal.connect(self.handle_blocks_between_stations)
        self.communicator.switch_status_signal.connect(self.handle_switch_status)
        self.communicator.enable_switch_status_signal.connect(self.handle_enable_switch_status)
        
        # For Train Model Outputs
        self.communicator.power_command_signal.connect(self.send_power_command)
        self.communicator.service_brake_command_signal.connect(self.send_service_brake_command)
        self.communicator.emergency_brake_command_signal.connect(self.send_emergency_brake_command)
        self.communicator.desired_temperature_signal.connect(self.send_desired_temperature_command)
        self.communicator.exterior_lights_signal.connect(self.send_exterior_lights_command)
        self.communicator.interior_lights_signal.connect(self.send_interior_lights_command)
        self.communicator.left_door_signal.connect(self.send_left_door_command)
        self.communicator.right_door_signal.connect(self.send_right_door_command)
        self.communicator.announcement_signal.connect(self.send_announcement)
        
        
        
        ###############################
        # User Interface STARTS HERE  #
        ###############################
        
        
        # Set the window title and background color
        self.setWindowTitle("Train Controller")
        self.setStyleSheet("background-color: lightgray;")

        # Main Layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 15, 30, 10)

        # Title Label
        title_banner = QHBoxLayout()
        title_banner.setSpacing(0)
        title_label = QLabel("Train Controller")
        title_label.setStyleSheet("font: Times New Roman; font-size: 30px; font-weight: bold; color: white; background-color: blue; border-radius: 10px; padding: 10px;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_banner.addWidget(title_label)

        # Title Container
        title_container = QWidget()
        title_container.setLayout(title_banner)
        title_container.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(title_container)

        # Main Grid Layout for UI Elements
        main_grid = QGridLayout()
        
        
        
        ####################################################
        # SPEED & AUTHORITY CONTROLS IN THE USER INTERFACE #
        ####################################################


        # CURRENT SPEED SECTION
        self.current_speed_box = QVBoxLayout()
        self.current_speed_label = QLabel("Current Speed:")
        self.current_speed_label.setStyleSheet("padding-top: 10px; font-size: 14px; font-weight: bold; color: black; margin-top: 0px; margin-right: 100px")

        # Displaying the current speed in UI
        self.current_speed_edit = QLineEdit(f"{self.current_velocity * 2.23694:.2f}")
        self.timer.start(1000)  # Update every 1000 milliseconds (1 second)
        self.timer.timeout.connect(lambda: self.handle_current_speed())
        self.timer.timeout.connect(self.update_current_position)
        self.current_speed_edit.setText(self.current_speed_edit.text() + " mph")
        self.current_speed_edit.setEnabled(False)
        self.current_speed_edit.setStyleSheet("background-color: lightgray; max-width: 100px; border-radius: 5px; color: black; border: 2px solid black; padding: 2px;")
        self.current_speed_box.addWidget(self.current_speed_label)
        self.current_speed_box.addWidget(self.current_speed_edit)
        self.current_speed_box.addSpacerItem(QSpacerItem(0, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        main_grid.addLayout(self.current_speed_box, 0, 0)



        # COMMANDED SPEED SECTION
        self.commanded_speed_box = QVBoxLayout()
        self.commanded_speed_label = QLabel("Recommended Speed:")
        self.commanded_speed_label.setStyleSheet("font-size: 14px; font-weight: bold; color: black;")
        
        # Displaying the commanded speed in UI
        self.commanded_speed_edit = QLineEdit(str(self.commanded_speed))
        self.commanded_speed_edit.setText(self.commanded_speed_edit.text() + " mph")
        self.timer.start(1000)
        self.timer.timeout.connect(lambda: self.update_commanded_speed() if not self.signal_fail else None)
        self.commanded_speed_edit.setEnabled(False)
        self.commanded_speed_edit.setStyleSheet("background-color: lightgray; max-width: 100px; border-radius: 5px; color: black; border: 2px solid black; padding: 2px;")
        self.commanded_speed_box.addWidget(self.commanded_speed_label)
        self.commanded_speed_box.addWidget(self.commanded_speed_edit)
        self.commanded_speed_box.addSpacerItem(QSpacerItem(0, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        main_grid.addLayout(self.commanded_speed_box, 1, 0)



        # COMMANDED AUTHORITY SECTION
        self.commanded_authority_box = QVBoxLayout()
        self.commanded_authority_label = QLabel("Commanded Authority:")
        self.commanded_authority_label.setStyleSheet("font-size: 14px; font-weight: bold; color: black;")
        self.commanded_authority_edit = QLineEdit(str(self.commanded_authority))
        self.timer.start(1000)  # Update every 100 ms
        self.timer.timeout.connect(lambda: self.update_commanded_authority() if not self.signal_fail else None)
        self.commanded_authority_edit.setText(self.commanded_authority_edit.text() + " feet")
        self.commanded_authority_edit.setEnabled(False)
        self.commanded_authority_edit.setStyleSheet("background-color: lightgray; max-width: 100px; border-radius: 5px; color: black; margin-bottom: 35px; border: 2px solid black; padding: 2px;")
        self.commanded_authority_box.addWidget(self.commanded_authority_label)
        self.commanded_authority_box.addWidget(self.commanded_authority_edit)
        main_grid.addLayout(self.commanded_authority_box, 2, 0)
        
        
        
        
        # SETPOINT SPEED SECTION
        self.setpoint_box = QVBoxLayout()
        self.setpoint_label = QLabel("Setpoint Speed")
        self.setpoint_label.setStyleSheet("padding-left: 20px; font-size: 30px; font-weight: bold; color: black;")
        self.setpoint_box.addWidget(self.setpoint_label, alignment=Qt.AlignmentFlag.AlignCenter)  # Add to setpoint_box with center alignment

        # Setpoint Layout
        self.setpoint_layout = QHBoxLayout()
        self.setpoint_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins

        # Setpoint Speed Input Box
        self.setpoint_speed_edit = QLineEdit()
        self.setpoint_speed_edit.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.setpoint_speed_edit.setPlaceholderText("50")
        self.setpoint_speed_edit.setStyleSheet("margin-left: 50px; max-width: 100px; color: black; border: 2px solid black; border-radius: 5px; padding: 5px;")
        self.setpoint_speed_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Setpoint Speed Unit Label
        self.setpoint_unit = QLabel("mph")
        self.setpoint_unit.setStyleSheet("font-size: 12px; color: black;")
        
        # Setpoint Confirm Button
        self.setpoint_confirm = QPushButton("OK")
        self.setpoint_confirm.setStyleSheet("background-color: green; color: white; border: 2px solid black; padding: 5px; border-radius: 5px;")
        self.setpoint_confirm.clicked.connect(self.update_setpoint_speed_calculations)

        # Add widgets to setpoint_layout
        self.setpoint_layout.addWidget(self.setpoint_speed_edit, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setpoint_layout.addWidget(self.setpoint_unit, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setpoint_layout.addWidget(self.setpoint_confirm, alignment=Qt.AlignmentFlag.AlignCenter)

        # Add setpoint_layout to setpoint_box
        self.setpoint_box.addLayout(self.setpoint_layout)

        # Finally, add setpoint_box to the main grid at the desired position
        main_grid.addLayout(self.setpoint_box, 1, 1, 1, 1, Qt.AlignmentFlag.AlignCenter)
        
        
        
        
        #############################################
        # BOTH BRAKE CONTROLS IN THE USER INTERFACE #
        #############################################

        # Service Brake Button
        self.brake_button = QPushButton("SERVICE BRAKE")
        self.brake_button.setStyleSheet("margin-top: 40px; background-color: yellow; font-size: 16px; border-radius: 10px; font-weight: bold; color: black; border: 3px solid black; padding-top: 20px; max-width: 150px; padding-bottom: 20px")
        self.brake_button.pressed.connect(self.divet_in_service_brake_button)
        self.brake_button.pressed.connect(self.apply_service_brake)
        self.brake_button.released.connect(self.reset_service_brake_button_style)
        self.brake_button.released.connect(self.no_apply_service_brake)
        
        main_grid.addWidget(self.brake_button, 8, 0)  # Ensure it spans across two columns
        
        
        # Emergency Brake Button
        self.emergency_brake_button = QPushButton("EMERGENCY BRAKE")
        self.emergency_brake_button.setStyleSheet("border: 3px solid black; margin-left: 40px; background-color: red; color: white; font-size: 20px; font-weight: bold; padding: 50px; border-radius: 10px;")
        self.emergency_brake_button.pressed.connect(self.apply_emergency_brake)
        self.emergency_brake_button.pressed.connect(self.divet_in_emergency_brake_buttons)
        self.emergency_brake_button.released.connect(self.no_apply_emergency_brake)
        self.emergency_brake_button.released.connect(self.reset_emergency_brake_button_style)
        main_grid.addWidget(self.emergency_brake_button, 8, 3)
        
        
        
        
        #############################################
        # INDICATORS CONTROLS IN THE USER INTERFACE #
        #############################################

        # INTERIOR LIGHTS CONTROL
        self.interior_lights_layout = QHBoxLayout()
        self.interior_lights_label = QLabel("Interior Lights Status:")
        self.interior_lights_label.setStyleSheet("font-size: 14px; font-weight: bold; color: black; padding-left: 40px;")
        self.interior_lights_status = QPushButton("ON")
        self.interior_lights_status.setStyleSheet("background-color: #f5c842; max-width: 80px; border: 2px solid black; border-radius: 5px; padding: 3px;")
        self.interior_lights_status.pressed.connect(lambda: self.toggle_interior_lights(self.interior_lights))
        self.interior_lights_layout.addWidget(self.interior_lights_label)
        self.interior_lights_layout.addWidget(self.interior_lights_status)
        self.interior_lights_layout.addSpacerItem(QSpacerItem(20, 20))
        main_grid.addLayout(self.interior_lights_layout, 2, 3)
        
        
        # EXTERIOR LIGHTS CONTROL
        self.exterior_lights_layout = QHBoxLayout()
        self.exterior_lights_label = QLabel("Exterior Lights Status:")
        self.exterior_lights_label.setStyleSheet("font-size: 14px; font-weight: bold; color: black; padding-left: 40px;")
        self.exterior_lights_status = QPushButton("OFF")
        self.exterior_lights_status.setStyleSheet("background-color: #888c8b; max-width: 80px; border: 2px solid black; border-radius: 5px; padding: 3px;")
        self.exterior_lights_status.pressed.connect(lambda: self.toggle_exterior_lights(self.exterior_lights))
        self.exterior_lights_layout.addWidget(self.exterior_lights_label)
        self.exterior_lights_layout.addWidget(self.exterior_lights_status)
        self.exterior_lights_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum))
        main_grid.addLayout(self.exterior_lights_layout, 3, 3)
        
        
        # BRAKE STATUS CONTROL
        self.brake_status_layout = QHBoxLayout()
        self.brake_status_label = QLabel("Driver Brake Status:")
        self.brake_status_label.setStyleSheet("font-size: 14px; font-weight: bold; color: black; padding-left: 40px;")
        self.brake_status = QPushButton("OFF")
        # stylesheet for off
        self.brake_status.setStyleSheet("background-color: #888c8b; max-width: 80px; border: 2px solid black; border-radius: 5px; padding: 3px;")
        self.brake_status_layout.addWidget(self.brake_status_label)
        self.brake_status_layout.addWidget(self.brake_status)
        self.brake_status_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum))
        main_grid.addLayout(self.brake_status_layout, 4, 3)
        
        
        # PASSENGER BRAKE STATUS CONTROL
        self.passenger_brake_layout = QHBoxLayout()
        self.passenger_brake_label = QLabel("Passenger Brake Status:")
        self.passenger_brake_label.setStyleSheet("font-size: 14px; font-weight: bold; color: black; padding-left: 40px;")
        self.passenger_brake_status = QPushButton("OFF")
        self.passenger_brake_status.setStyleSheet("background-color: #888c8b; max-width: 80px; border: 2px solid black; border-radius: 5px; padding: 3px;")
        self.passenger_brake_layout.addWidget(self.passenger_brake_label)
        self.passenger_brake_layout.addWidget(self.passenger_brake_status)
        self.passenger_brake_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum))
        main_grid.addLayout(self.passenger_brake_layout, 5, 3)
        
        
        # RIGHT DOOR STATUS CONTROL
        self.right_door_layout = QHBoxLayout()
        self.right_door_status_label = QLabel("Right Door Status:")
        self.right_door_status_label.setStyleSheet("font-size: 14px; font-weight: bold; color: black; padding-left: 40px;")
        self.right_door_status = QPushButton("CLOSE")
        self.right_door_status.setStyleSheet("background-color: red; max-width: 80px; border: 2px solid black; border-radius: 5px; padding: 3px;")
        self.right_door_status.pressed.connect(lambda: self.toggle_right_door(self.right_door))
        self.right_door_layout.addWidget(self.right_door_status_label)
        self.right_door_layout.addWidget(self.right_door_status)
        self.right_door_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum))
        main_grid.addLayout(self.right_door_layout, 6, 3)
        
        
        # LEFT DOOR STATUS CONTROL
        self.left_door_layout = QHBoxLayout()
        self.left_door_status_label = QLabel("Left Door Status:")
        self.left_door_status_label.setStyleSheet("font-size: 14px; font-weight: bold; color: black; padding-left: 40px;")
        self.left_door_status = QPushButton("CLOSE")
        self.left_door_status.setStyleSheet("background-color: red; max-width: 80px; border: 2px solid black; border-radius: 5px; padding: 3px;")
        self.left_door_status.pressed.connect(lambda: self.toggle_left_door(self.left_door))
        self.left_door_layout.addWidget(self.left_door_status_label)
        self.left_door_layout.addWidget(self.left_door_status)
        self.left_door_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum))
        main_grid.addLayout(self.left_door_layout, 7, 3)
        
        
        
        
        ################################################
        # FAILURE MODES CONTROLS IN THE USER INTERFACE #
        ################################################
        
        # TRAIN ENGINE FAILURE
        self.train_engine_failure = QVBoxLayout()
        self.train_engine_failure.setSpacing(0)
        
        # Create the label for "Train Engine Failure"
        self.train_engine_fail_label = QLabel('<div style="text-align: center;">Train Engine<br>Failure</div>')
        self.train_engine_fail_label.setStyleSheet("font-size: 12px; font-weight: bold; color: black;")

        # Create the green indicator button
        self.engine_fail_indicator = QPushButton()
        self.engine_fail_indicator.setFixedSize(40, 40)  # Set a fixed size for the indicator button
        self.engine_fail_indicator = QPushButton()
        self.engine_fail_indicator.setFixedSize(40, 40)  # Set a fixed size for the indicator button
        self.engine_fail_indicator.setStyleSheet("background-color: green; border-radius: 20px; border: 2px solid black;")  # Green for no failure
        self.failure_timer = QTimer(self)
        self.failure_timer.timeout.connect(lambda: self.update_engine_failure_status(self.engine_fail))
        self.failure_timer.start(1000)  # Check every 1000 milliseconds (1 second)
        
        # Add widgets to the vertical box layout
        self.train_engine_failure.addWidget(self.train_engine_fail_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.train_engine_failure.addWidget(self.engine_fail_indicator, alignment=Qt.AlignmentFlag.AlignCenter)
        
        
        # BRAKE FAILURE
        self.brake_failure = QVBoxLayout()
        
        # Create the label for "Brake Failure"
        self.brake_fail_label = QLabel("Brake Failure")
        self.brake_fail_label.setStyleSheet("font-size: 12px; font-weight: bold; color: black; padding-left: 10px;")
        
        # Create the green indicator button
        self.brake_fail_indicator = QPushButton()
        self.brake_fail_indicator.setFixedSize(40, 40)  # Set a fixed size for the indicator button
        self.brake_fail_indicator.setStyleSheet("background-color: green; border-radius: 20px; border: 2px solid black; padding-left: 100px;")
        self.failure_timer = QTimer(self)
        self.failure_timer.timeout.connect(lambda: self.update_brake_failure_status(self.brake_fail))
        self.failure_timer.start(1000)  # Check every 1000 milliseconds (1 second)
        
        # Add widgets to the vertical box layout
        self.brake_failure.addWidget(self.brake_fail_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.brake_failure.addWidget(self.brake_fail_indicator, alignment=Qt.AlignmentFlag.AlignCenter)
        
        
        # SIGNAL PICKUP FAILURE
        self.signal_pickup_failure = QVBoxLayout()
        
        # Create the label for "Signal Pickup Failure"
        self.signal_fail_label =  QLabel('<div style="text-align: center;">Signal Pickup<br>Failure</div>')
        self.signal_fail_label.setStyleSheet("font-size: 12px; font-weight: bold; color: black; padding-left: 10px;")
        
        # Create the green indicator button
        self.signal_fail_indicator = QPushButton()
        self.signal_fail_indicator.setFixedSize(40, 40)  # Set a fixed size for the indicator button
        self.signal_fail_indicator.setStyleSheet("background-color: green; border-radius: 20px; border: 2px solid black; padding-left: 10px;")
        self.failure_timer = QTimer(self)
        self.failure_timer.timeout.connect(lambda: self.update_signal_failure_status(self.signal_fail))
        self.failure_timer.start(1000)  # Check every 1000 milliseconds (1 second)
        
        # Add widgets to the vertical box layout
        self.signal_pickup_failure.addWidget(self.signal_fail_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.signal_pickup_failure.addWidget(self.signal_fail_indicator, alignment=Qt.AlignmentFlag.AlignCenter)
        
        
        # Add all failure modes to a horizontal layout
        self.all_failure_modes = QHBoxLayout()
        self.all_failure_modes.setSpacing(5)
        
        self.all_failure_modes.addLayout(self.train_engine_failure)
        self.all_failure_modes.addLayout(self.brake_failure)
        self.all_failure_modes.addLayout(self.signal_pickup_failure)
        
        # Add the failure mode layout to the main grid
        main_grid.addLayout(self.all_failure_modes, 8, 1)
        
        
        
        
        ##############################################
        # TEMPERATURE CONTROLS IN THE USER INTERFACE #
        ##############################################
        
        # CURRENT TEMPERATURE SECTION
        
        # Create a vertical box layout for the current temperature
        self.current_temp_box = QVBoxLayout()
        self.current_temp_label = QLabel("Current Train Temperature:")
        self.current_temp_label.setStyleSheet("font-size: 14px; font-weight: bold; color: black; padding-left: 40px;")
        self.current_temp_edit = QLineEdit(f"{self.current_temperature}")
        self.current_temp_edit.setText(f"{self.current_temperature} °F")
        
        # Set the current temperature to be uneditable
        self.current_temp_edit.setEnabled(False)
        self.current_temp_edit.setStyleSheet("background-color: lightgray; max-width: 100px; color: black; margin-left: 45px; border: 2px solid black; border-radius: 5px; padding: 2px;")
        self.current_temp_box.addWidget(self.current_temp_label)
        self.current_temp_box.addWidget(self.current_temp_edit)
        self.current_temp_box.addSpacerItem(QSpacerItem(0, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        main_grid.addLayout(self.current_temp_box, 0, 3)
        
        
        # DESIRED TEMPERATURE SECTION
        
        # Create a vertical box layout for the desired temperature
        self.desired_temp_box = QVBoxLayout()
        self.desired_temp_label = QLabel("Desired Train Temperature:")
        self.desired_temp_label.setStyleSheet("font-size: 14px; font-weight: bold; color: black; padding-left: 40px;")
        
        # Create a QLineEdit for numeric temperature input
        self.temp_input = QLineEdit()
        self.temp_input.setStyleSheet("max-width: 100px; color: black; margin-left: 40px; border: 2px solid black; border-radius: 5px; padding: 3px;")
        self.temp_input.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.temp_input.setPlaceholderText("Enter temperature (70°F to 100°F)")  # Optional placeholder text
        self.temp_input.editingFinished.connect(self.update_desired_temperature)
        self.desired_temp_box.addWidget(self.desired_temp_label)
        self.desired_temp_box.addWidget(self.temp_input)
        
        # Add the QLineEdit to the main grid at the desired position
        main_grid.addLayout(self.desired_temp_box, 1, 3)
        
        
        

        ###################################################
        # OPERATIONAL MODE CONTROLS IN THE USER INTERFACE #
        ###################################################
        
        # OPERATIONAL MODE
        self.operational_mode_label = QLabel("Operational Mode:")
        self.operational_mode_label.setStyleSheet("font-size: 14px; font-weight: bold; color: black; margin-bottom 30px;")
        main_grid.addWidget(self.operational_mode_label, 4, 0)
        
        # MANUAL MODE BUTTON
        self.manual_button = QPushButton("Manual")
        self.manual_button.clicked.connect(self.set_manual_mode)
        main_grid.addWidget(self.manual_button, 5, 0)

        # AUTOMATIC MODE BUTTON
        self.automatic_button = QPushButton("Automatic")
        self.automatic_button.clicked.connect(self.set_automatic_mode)
        main_grid.addWidget(self.automatic_button, 6, 0)
        
        self.operation_mode_timer = QTimer(self)
        self.operation_mode_timer.timeout.connect(self.update_button_styles)
        self.operation_mode_timer.start(10)  # Check every 10 milliseconds
        
        
        
        
        ################################################
        # POWER COMMAND CONTROLS IN THE USER INTERFACE #
        ################################################
        
        # POWER COMMAND SECTION
        self.power_command_label = QLabel("Power Command")
        self.power_command_label.setStyleSheet("font-size: 25px; font-weight: bold; color: black; padding-left: 22px;")
    
        self.power_command_layout = QHBoxLayout()
        self.power_command_edit = QLineEdit(str(self.power_command))
        
        self.power_command_edit.setStyleSheet("font-size: 20px; max-width: 100px; color: black; border: 2px solid black; border-radius: 5px; padding: 5px;")
        self.power_command_edit.setEnabled(False)
        self.power_command_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.power_unit = QLabel("kWatts")
        self.power_unit.setStyleSheet("font-size: 16px; color: black;")
        self.power_command_edit.setStyleSheet("margin-left: 50px; max-width: 100px; color: black; border: 2px solid black; border-radius: 5px; padding: 5px; background-color: lightgray;")
        self.power_unit.setStyleSheet("font-size: 12px; color: black; background-color: lightgray;")
        self.power_command_layout.addWidget(self.power_command_edit, alignment=Qt.AlignmentFlag.AlignCenter)
        self.power_command_layout.addWidget(self.power_unit, alignment=Qt.AlignmentFlag.AlignCenter)
        
        main_grid.addWidget(self.power_command_label, 4, 1, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        main_grid.addLayout(self.power_command_layout, 5, 1, 1, 1, Qt.AlignmentFlag.AlignCenter)

        
        # Add Components to the Main Layout
        main_layout.addLayout(title_banner)
        main_layout.addLayout(main_grid)
        

        # Set Main Layout
        self.setLayout(main_layout)
        
        
    
        
    ####################################################################
    # FUNCTIONS TO HANDLE THE BACKEND LOGIC OF TRAIN CONTROLLER MODULE #
    ####################################################################
    
    
    #######################################
    # PYQT SIGNALS FUNCTIONS FOR HANDLING #
    #######################################
    
        
    def handle_current_speed(self):
        # # print(f"Current Speed: {self.current_velocity}")
        self.current_speed_edit.setText(f"{self.current_velocity * 2.23694:.2f} mph")
        
    def updated_set_kp(self, kp: float):
        if self.current_position == 0 or self.current_velocity == 0.0:
            self.kp = kp
            # # print(f"Updated Kp: {self.kp}")
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
            # # print(f"Updated Ki: {self.ki}")
        else:
            # Pop up saying cannot change Kp while train is moving
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Error")
            msg_box.setText("Cannot change Ki while the train is moving.")
            msg_box.setStyleSheet("font-size: 14px;")
            QTimer.singleShot(3000, msg_box.accept)  # Close the message box after 3 seconds
            msg_box.exec()

    def handle_station_name(self, station_name: str):
        self.next_station = station_name
        # # print(f"Next Station: {self.next_station}")
        
    
    
    #################################
    # TEMPERATURE CONTROL FUNCTIONS #
    #################################
    
    def update_desired_temperature(self):
        temp = float(self.temp_input.text())
        if 60 <= temp <= 75:
            self.desired_temperature = temp
            # # print(f"Desired temperature set to: {self.desired_temperature}°F")
        else:
            # # print("Temperature out of range. Please enter a value between 60°F and 75.")
            
        self.send_desired_temperature_command(self.desired_temperature)
    
    
    
    ############################
    # OPERATION MODE FUNCTIONS #
    ############################
    
    def set_manual_mode(self):
        self.operation_mode = 1
        # Disable the setpoint speed input field
        self.setpoint_speed_edit.setEnabled(True)
        # # print("Operation Mode set to Manual")

    def set_automatic_mode(self):
        self.operation_mode = 0
        
        # ONLY WHEN CHANGING FROM MANUAL TO AUTOMATIC MODE - always pick the lowest of the speed limit and the commanded speed
        if self.desired_velocity < self.speed_limit and self.desired_velocity < self.commanded_speed and self.commanded_speed < self.speed_limit:
            # If the setpoint speed is less than the speed limit and the commanded speed
            self.desired_velocity = self.commanded_speed
            self.setpoint_speed_edit.clear()
            self.power_command = self.update_power_command()
            self.power_command_edit.setText(f"{self.power_command:.2f}")
            self.send_power_command(self.power_command)
        elif self.desired_velocity < self.speed_limit and self.desired_velocity < self.commanded_speed and self.commanded_speed > self.speed_limit:
            # If the setpoint speed is less than the speed limit and the commanded speed is greater than the speed limit
            self.desired_velocity = self.speed_limit
            self.current_speed_edit.setText(f"{self.current_velocity * 2.23694:.2f} mph")
            self.setpoint_speed_edit.clear()
            self.power_command = self.update_power_command()
            self.power_command_edit.setText(f"{self.power_command:.2f}")
            self.send_power_command(self.power_command)
            
           
        # Update the current speed display in UI for users
        self.current_speed_edit.setText(f"{self.current_velocity * 2.23694:.2f} mph")
    
        # Disable the setpoint speed input field
        self.setpoint_speed_edit.setEnabled(False)
        # # print("Operation Mode set to Automatic")


    
    #########################################
    # COMMANDED SPEED & AUTHORITY FUNCTIONS #
    #########################################
    
    def update_commanded_speed(self):  
        self.commanded_speed_edit.setText(f"{self.commanded_speed * 2.23694:.2f} mph")
        
    def update_commanded_authority(self):
        if self.signal_fail == False:
            self.commanded_authority_edit.setText(f"{self.commanded_authority * 3.281:.2f} ft")
            if self.commanded_authority < 0.0:
                self.commanded_authority = 0.0
                self.commanded_authority_edit.setText("0.00 ft")
            if self.commanded_authority == 0.0:
                # Send door status to Train Model
                for i in self.red_infrastucture:
                    if self.next_station in self.red_infrastucture[i]:
                        if "Left" in self.red_station_side[i]:
                            self.left_door = True
                            self.right_door = False
                            self.send_left_door_command(self.left_door)
                            self.send_right_door_command(self.right_door)
                        elif "Right" in self.red_station_side[i]:
                            self.left_door = False
                            self.right_door = True
                            self.send_left_door_command(self.left_door)
                            self.send_right_door_command(self.right_door)
                        elif "Left/Right" in self.red_station_side[i]:
                            self.left_door = True
                            self.right_door = True
                            self.send_left_door_command(self.left_door)
                            self.send_right_door_command(self.right_door)
                        else:
                            self.left_door = False
                            self.right_door = False
                            self.send_left_door_command(self.left_door)
                            self.send_right_door_command(self.right_door)
                            
                self.communicator.announcement_signal.emit(f"Arrived at {self.next_station} Station")
                self.commanded_authority_edit.setText("0.00 ft")
                self.commanded_authority = 0.0
                # # print("Authority reached 0.0 ft")
    
    
    
    ###############################
    # TOGGLE INDICATORS FUNCTIONS #
    ###############################
    
    def toggle_interior_lights(self, status: bool):
        if status and self.operation_mode == 1:
            self.interior_lights = False
            self.interior_lights_status.setText("OFF")
            self.interior_lights_status.setStyleSheet("background-color: #888c8b; max-width: 80px; border: 2px solid black; border-radius: 5px; padding: 3px;")
            self.send_interior_lights_command(self.interior_lights)
            # # print("Interior lights turned OFF")
        elif not status and self.operation_mode == 1:
            self.interior_lights = True
            self.interior_lights_status.setText("ON")
            self.interior_lights_status.setStyleSheet("background-color: #f5c842; max-width: 80px; border: 2px solid black; border-radius: 5px; padding: 3px;")
            self.send_interior_lights_command(self.interior_lights)
            # # print("Interior lights turned ON")

    def toggle_exterior_lights(self, status: bool):
        if status and self.operation_mode == 1:
            self.exterior_lights = False
            self.exterior_lights_status.setText("OFF")
            self.exterior_lights_status.setStyleSheet("background-color: #888c8b; max-width: 80px; border: 2px solid black; border-radius: 5px; padding: 3px;")
            self.send_exterior_lights_command(self.exterior_lights)
            # # print("Exterior lights turned OFF")
        elif not status and self.operation_mode == 1:
            self.exterior_lights = True
            self.exterior_lights_status.setText("ON")
            self.exterior_lights_status.setStyleSheet("background-color: #f5c842; max-width: 80px; border: 2px solid black; border-radius: 5px; padding: 3px;")
            self.send_exterior_lights_command(self.exterior_lights)
            # # print("Exterior lights turned ON")
            
    def toggle_right_door(self, status: bool):
        if status and self.current_velocity == 0.0 and self.operation_mode == 1:
            self.right_door = False
            self.right_door_status.setText("CLOSE")
            self.right_door_status.setStyleSheet("background-color: red; max-width: 80px; border: 2px solid black; border-radius: 5px; padding: 3px;")
            self.send_right_door_command(self.right_door)
            # # print("Right door closed")
        elif not status and self.current_velocity == 0.0 and self.operation_mode == 1:
            self.right_door = True
            self.right_door_status.setText("OPEN")
            self.right_door_status.setStyleSheet("background-color: green; max-width: 80px; border: 2px solid black; border-radius: 5px; padding: 3px;")
            self.send_right_door_command(self.right_door)
            # # print("Right door opened")
            
    def toggle_left_door(self, status: bool):
        if status and self.current_velocity == 0.0 and self.operation_mode == 1:
            self.left_door = False
            self.left_door_status.setText("CLOSE")
            self.left_door_status.setStyleSheet("background-color: red; max-width: 80px; border: 2px solid black; border-radius: 5px; padding: 3px;")
            self.send_left_door_command(self.right_door)
            # # print("Left door closed")
        elif not status and self.current_velocity == 0.0 and self.operation_mode == 1:
            self.left_door = True
            self.left_door_status.setText("OPEN")
            self.left_door_status.setStyleSheet("background-color: green; max-width: 80px; border: 2px solid black; border-radius: 5px; padding: 3px;")
            self.send_left_door_command(self.right_door)
            # # print("Left door opened")

   
   
    #########################
    # APPLY BRAKE FUNCTIONS #
    #########################
    
    def apply_emergency_brake(self):
        self.driver_emergency_brake_command = True
        self.send_emergency_brake_command(self.driver_emergency_brake_command)
        # # print("Emergency Brake Activated!")
        
    def apply_service_brake(self):
        self.driver_service_brake_command = True
        self.send_service_brake_command(self.driver_service_brake_command)
        # # print("Service Brake Applied.")
        
    def no_apply_emergency_brake(self):
        self.driver_emergency_brake_command = False
        self.send_emergency_brake_command(self.driver_emergency_brake_command)
        # # print("Emergency Brake Deactivated!")
        
    def no_apply_service_brake(self):
        self.driver_service_brake_command = False
        self.send_service_brake_command(self.driver_service_brake_command)
        # # print("Service Brake Released.")
        
    def calculate_brake_distance(self):
        # Calculate the brake distance
        brake_distance = (self.current_velocity ** 2) / (2 * 1.2)
        final_distance = brake_distance * 3.281
        if self.commanded_authority <= final_distance:
            # Divet in Service Brake
            self.divet_in_service_brake_button()
            
        if self.commanded_authority == 0:
            # Undivet the service brake
            self.reset_service_brake_button_style()
            
        # # print(f"Commanded Authority: {self.commanded_authority:.2f} ft")
        # # print(f"Brake Distance: {brake_distance:.2f} m")
        
    
    ##########################
    # POWER COMMAND FUNCTION #
    ##########################
   
    def update_power_command(self):
        if round(self.desired_velocity, 2) == round(self.current_velocity, 2):
            self.power_command = 0
            self.send_power_command(self.power_command)
            # Service brake should be not applied
            self.reset_service_brake_button_style()
            
            return self.power_command

        # # print(f"Desired Speed: {self.desired_velocity:.2f} m/s, Current Speed: {self.current_velocity:.2f} m/s")
        
        # Finding the velocity error
        self.ek_current = self.desired_velocity - self.current_velocity
        
        # Using the different cases from lecture slides
        if self.power_command < self.max_power:
            self.uk_current = self.uk_previous + (1.0 / 2) * (self.ek_current + self.ek_previous)
        else:
            self.uk_current = self.uk_previous
        
        # Finding the power command
        self.power_command = self.kp * self.ek_current + self.ki * self.uk_current

        # Updating the previous variables for the next iteration
        self.ek_previous = self.ek_current
        self.uk_previous = self.uk_current
        
        # Power command bound
        if self.power_command > self.max_power:
            self.power_command = self.max_power
            self.reset_service_brake_button_style()
        elif self.power_command <= 0:
            self.power_command = 0
            # # print("Service Brake Applied")
            # Press the service brake button in UI
            self.divet_in_service_brake_button()
        else:
            self.power_command = self.power_command
            self.reset_service_brake_button_style()
            
        self.send_power_command(self.power_command)
        
        # Returning the power command
        return self.power_command / 1000  # Convert to kW



    ###########################
    # SETPOINT SPEED FUNCTION #
    ###########################
    
    def update_setpoint_speed_calculations(self):  
        # Put the setpoint speed input in a variable in m/s even though it is in mph
        max_speed = min(self.speed_limit, self.commanded_speed)
        # # print(f"Min Speed: {max_speed}")
        
        self.desired_velocity = float(self.setpoint_speed_edit.text()) * 0.44704
        
        if (self.desired_velocity) > max_speed:
            self.desired_velocity = max_speed
            self.setpoint_speed_edit.setText(f"{max_speed * 2.237:.2f}")
                    
        # # print(f"Desired Speed: {self.desired_velocity} m/s")    # Good updated value
        
        self.power_command = self.update_power_command()
        self.send_power_command(self.power_command)
        # Update the power command display
        self.power_command_edit.setText(f"{self.power_command:.2f}")
        # # print(f"Power Command: {self.power_command} kW")
        
    
    
    ##########################
    # FAILURE MODE FUNCTIONS #
    ##########################
        
    def update_engine_failure_status(self, failure: bool):
        if failure:
            self.engine_fail_indicator.setStyleSheet("background-color: red; border-radius: 20px; border: 2px solid black;")  # Red for failure
            QTimer.singleShot(3000, lambda: (self.engine_fail_indicator.setStyleSheet("background-color: green; border-radius: 20px; border: 2px solid black;"), setattr(self, 'engine_fail', False)))

        else:
            self.engine_fail_indicator.setStyleSheet("background-color: green; border-radius: 20px; border: 2px solid black;")  # Green for no failure
            
    def update_brake_failure_status(self, failure: bool):
        if failure:
            self.brake_fail_indicator.setStyleSheet("background-color: red; border-radius: 20px; border: 2px solid black;")  # Red for failure
            QTimer.singleShot(3000, lambda: (self.brake_fail_indicator.setStyleSheet("background-color: green; border-radius: 20px; border: 2px solid black;"), setattr(self, 'brake_fail', False)))

        else:
            self.brake_fail_indicator.setStyleSheet("background-color: green; border-radius: 20px; border: 2px solid black;")  # Green for no failure
                
    def update_signal_failure_status(self, failure: bool):
        if failure:
            self.signal_fail = True
            self.signal_fail_indicator.setStyleSheet("background-color: red; border-radius: 20px; border: 2px solid black;")  # Red for failure
            QTimer.singleShot(3000, lambda: (self.signal_fail_indicator.setStyleSheet("background-color: green; border-radius: 20px; border: 2px solid black;"), setattr(self, 'signal_fail', False)))
        else:
            self.signal_fail = False
            self.signal_fail_indicator.setStyleSheet("background-color: green; border-radius: 20px; border: 2px solid black;")  # Green for no failure
                
    
    
    ############################
    # POSITION UPDATE FUNCTION #
    ############################
    
    def update_current_position(self):
        if self.signal_fail == False:
            timestep = 1.0
            self.current_position = self.previous_position + (timestep / 2) * (self.current_velocity + self.previous_velocity)
            self.commanded_authority -= self.current_position
            self.commanded_authority_edit.setText(f"{self.commanded_authority * 3.281:.2f} ft")
            self.previous_position = self.current_position
            
            position_counter = 0
            
            # If current position is found to be UNDERGROUND, then both interior and exterior lights should be turned on
            for i in self.red_infrastucture:
                position_counter += self.red_block_length[i]
                if self.current_position < position_counter:
                    if self.red_underground[i - 1] and self.red_underground[i - 1] == True:
                        self.toggle_interior_lights(True)
                        self.toggle_exterior_lights(True)
                        break
                    else:
                        self.toggle_interior_lights(False)
                        self.toggle_exterior_lights(False)
                        break
                        
            # # print(f"Current Position: {self.current_position:.2f} m")
            
   
   
   
    ################################################
    # BRAKE DIVET FUNCTIONS AND OTHER UI FUNCTIONS #
    ################################################
    
    def divet_in_service_brake_button(self):
        self.apply_service_brake()
        self.brake_button.setStyleSheet("margin-top: 40px; background-color: #B8860B; font-size: 16px; border-radius: 10px; font-weight: bold; color: black; border: 3px solid black; padding-top: 20px; max-width: 150px; padding-bottom: 20px;")
        # Put button status in UI to ON
        self.brake_status.setText("ON")
        self.brake_status.setStyleSheet("background-color: #f5c842; max-width: 80px; border: 2px solid black; border-radius: 5px; padding: 3px;")
        self.brake_button.released.connect(self.reset_brake_status)

    def reset_service_brake_button_style(self):
        self.no_apply_service_brake()
        self.brake_button.setStyleSheet("margin-top: 40px; background-color: yellow; font-size: 16px; border-radius: 10px; font-weight: bold; color: black; border: 3px solid black; padding-top: 20px; max-width: 150px; padding-bottom: 20px;")
        # Turn the brake status to OFF
        self.brake_status.setText("OFF")
        self.brake_status.setStyleSheet("background-color: #888c8b; max-width: 80px; border: 2px solid black; border-radius: 5px; padding: 3px;")

    def divet_in_emergency_brake_buttons(self):
        self.apply_emergency_brake()
        self.emergency_brake_button.setStyleSheet("border: 3px solid black; margin-left: 40px; background-color: darkred; color: white; font-size: 20px; font-weight: bold; padding: 50px; border-radius: 10px;")
        # Put button status in UI to ON
        self.brake_status.setText("ON")
        self.brake_status.setStyleSheet("background-color: #f5c842; max-width: 80px; border: 2px solid black; border-radius: 5px; padding: 3px;")
        self.emergency_brake_button.released.connect(self.reset_brake_status)
        
    def reset_emergency_brake_button_style(self):
        self.no_apply_emergency_brake()
        self.emergency_brake_button.setStyleSheet("border: 3px solid black; margin-left: 40px; background-color: red; color: white; font-size: 20px; font-weight: bold; padding: 50px; border-radius: 10px;")
        # Turn the brake status to OFF
        self.brake_status.setText("OFF")
        self.brake_status.setStyleSheet("background-color: #888c8b; max-width: 80px; border: 2px solid black; border-radius: 5px; padding: 3px;")

    def reset_brake_status(self):
        self.brake_status.setText("OFF")
        self.brake_status.setStyleSheet("background-color: #888c8b; max-width: 80px; border: 2px solid black; border-radius: 5px; padding: 3px;")
       
    def update_button_styles(self):
        if self.operation_mode == 1:
            self.manual_button.setStyleSheet("margin-top: 10px; margin-left: 10px; background-color: green; color: white; max-width: 100px; border-radius: 5px; padding-top: 10px; padding-bottom: 10px; border: 2px solid black;")
            self.automatic_button.setStyleSheet("margin-top: 10px; margin-left: 10px; background-color: gray; color: white; max-width: 100px; border-radius: 5px; padding-top: 10px; padding-bottom: 10px; border: 2px solid black;")
        else:
            self.manual_button.setStyleSheet("margin-top: 10px; margin-left: 10px; background-color: gray; color: white; max-width: 100px; border-radius: 5px; padding-top: 10px; padding-bottom: 10px; border: 2px solid black;")
            self.automatic_button.setStyleSheet("margin-top: 10px; margin-left: 10px; background-color: green; color: white; max-width: 100px; border-radius: 5px; padding-top: 10px; padding-bottom: 10px; border: 2px solid black;")
    
    
    ##########################
    # OUTPUTS TO TRAIN MODEL #
    ##########################
    
    def send_power_command(self):
        self.communicator.power_command_signal.emit(self.power_command)
        
    def send_service_brake_command(self):
        self.communicator.service_brake_command_signal.emit(self.driver_service_brake_command)

    def send_emergency_brake_command(self):
        self.communicator.emergency_brake_command_signal.emit(self.driver_emergency_brake_command)
        
    def send_desired_temperature_command(self):
        self.communicator.desired_temperature_signal.emit(self.desired_temperature)
        
    def send_interior_lights_command(self):
        self.communicator.interior_lights_signal.emit(self.interior_lights)
        
    def send_exterior_lights_command(self):
        self.communicator.exterior_lights_signal.emit(self.exterior_lights)
    
    def send_left_door_command(self):
        self.communicator.left_door_signal.emit(self.left_door)
        
    def send_right_door_command(self):
        self.communicator.right_door_signal.emit(self.right_door)
        
    def send_announcement(self, announcement: str):
        self.communicator.announcement_signal.emit(announcement)
        
        
    ###########################
    # INPUTS FROM TRAIN MODEL #
    ###########################
    
    def handle_commanded_speed(self, speed: float):
        self.commanded_speed = speed / 2.237
        
        # Changing recommemded speed in the UI to the min between the commanded speed and the speed limit
        if self.commanded_speed < self.speed_limit:
            self.commanded_speed = self.commanded_speed
            self.commanded_speed_edit.setText(f"{self.commanded_speed * 2.237:.2f} mph")
        elif self.commanded_speed > self.speed_limit:
            self.commanded_speed = self.speed_limit
            self.commanded_speed_edit.setText(f"{self.commanded_speed * 2.237:.2f} mph")
            
        # # print(f"Commanded speed: {self.commanded_speed}")
        
        if self.operation_mode == 0:
            self.set_automatic_mode()
    
    def handle_commanded_authority(self, authority: float):
        self.commanded_authority = authority / 3.281
        # # print(f"Commanded authority: {self.commanded_authority}")
        # MUST close both doors here in UI
        self.left_door = False
        self.right_door = False
        self.send_left_door_command(self.left_door)
        self.send_right_door_command(self.right_door)
        self.left_door_status.setText("CLOSE")
        # Make the button red
        self.left_door_status.setStyleSheet("background-color: red; max-width: 80px; border: 2px solid black; border-radius: 5px; padding: 3px;")
        self.right_door_status.setText("CLOSE")
        # Make the button red
        self.right_door_status.setStyleSheet("background-color: red; max-width: 80px; border: 2px solid black; border-radius: 5px; padding: 3px;")
    
    def handle_current_velocity(self, velocity: float):
        # Convert velocity to m/s
        self.current_velocity = velocity / 2.23694
        # # print(f"Current Velocity: {self.current_velocity}")
        self.current_speed_edit.setText(f"{self.current_velocity * 2.23694:.2f} mph")
        self.power_command = self.update_power_command()
        self.send_power_command(self.power_command)
        self.power_command_edit.setText(f"{self.power_command:.2f}")
        self.previous_velocity = self.current_velocity
            
    def handle_engine_failure(self, status: bool):
        if status == True:
            self.engine_fail = True
            # Divet in Emergency Brake
            self.divet_in_emergency_brake_buttons()
            if self.current_velocity == 0.0:
                self.reset_emergency_brake_button_style()
                self.power_command = self.update_power_command()
                self.send_power_command(self.power_command)
                self.power_command_edit.setText(f"{self.power_command:.2f}")
        else:
            self.engine_fail = False

    def handle_brake_failure(self, status: bool):
        if status == True:
            self.brake_fail = True
            # Divet in Emergency Brake
            self.divet_in_emergency_brake_buttons()
            if self.current_velocity == 0.0:
                self.reset_emergency_brake_button_style()
                self.power_command = self.update_power_command()
                self.send_power_command(self.power_command)
                self.power_command_edit.setText(f"{self.power_command:.2f}")
        else:
            self.brake_fail = False
    
    def handle_signal_failure(self, status: bool):
        if status == True:
            self.signal_fail = True
            # Divet in Emergency Brake
            self.divet_in_emergency_brake_buttons()
            if self.current_velocity == 0.0:
                self.reset_emergency_brake_button_style()
                self.power_command = self.update_power_command()
                self.send_power_command(self.power_command)
                self.power_command_edit.setText(f"{self.power_command:.2f}")
        else:
            self.signal_fail = False
            
    def handle_passenger_brake_command(self, status: bool):
        if status:
            # Turn on the passenger brake indcator
            self.passenger_brake_status.setText("ON")
            self.passenger_brake_status.setStyleSheet("background-color: red; max-width: 80px; border: 2px solid black; border-radius: 5px; padding: 3px;")
        else:
            # Turn off the passenger brake indicator
            self.passenger_brake_status.setText("OFF")
            self.passenger_brake_status.setStyleSheet("background-color: #888c8b; max-width: 80px; border: 2px solid black; border-radius: 5px; padding: 3px;")
                
    def handle_actual_temperature(self, temperature: float):
        self.current_temperature = temperature
        self.current_temp_edit.setText(f"{self.current_temperature:.2f} °F")
        # # print(f"Current Temperature: {self.current_temperature} °F")
    
    def handle_blocks_between_stations(self, blocks: list[int]):
        self.final_beacon_block_numbers_inputs = [block - 1 for block in blocks]
        # # print(f"Final Beacon Block Numbers: {self.final_beacon_block_numbers_inputs}")
    
    def handle_switch_status(self, status: bool):
        if self.enable_switch_status:
            self.switch_status = status
            # # print(f"Switch Status: {self.switch_status}")
        
    def handle_enable_switch_status(self, status: bool):
        self.enable_switch_status = status
        # # print(f"Enable Switch Status: {self.enable_switch_status}")
    
    
    
    
    
    
#################
# MAIN FUNCTION #
#################

if __name__ == "__main__":#
    app = QApplication([])
    communicator = IntegratedCommunicate()
    window = TrainIntegratedControllerUI(communicator)
    window.show()
    app.exec()