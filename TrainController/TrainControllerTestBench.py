import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton, QTextEdit
from PyQt6.QtCore import QObject
from TrainControllerCommunicateSignals import Communicate

class TrainControllerTestBench(QObject):
    def __init__(self, communicator: Communicate):
        super().__init__()
        
        # Integer variables
        self.current_speed = 0
        self.commanded_speed = 0
        self.commanded_authority = 0
        self.mass_of_train = 0
        self.acceleration = 0
        self.passengers = 0
        self.train_weight = 0  # New variable
        self.current_velocity = 0  # New variable
        
        # String variables
        self.beacon_destination_location = ""
        self.announcement = ""
        
        # Boolean variables
        self.train_engine_failure = False
        self.brake_failure = False
        self.signal_pickup_failure = False
        self.passenger_brake_command = False
        self.apply_changes = False
        
    def get_all_variables(self):
        return {
            'current_speed': self.current_speed,
            'commanded_speed': self.commanded_speed,
            'commanded_authority': self.commanded_authority,
            'mass_of_train': self.mass_of_train,
            'acceleration': self.acceleration,
            'passengers': self.passengers,
            'train_weight': self.train_weight,
            'current_velocity': self.current_velocity,  # New variable
            'beacon_destination_location': self.beacon_destination_location,
            'announcement': self.announcement,
            'train_engine_failure': self.train_engine_failure,
            'brake_failure': self.brake_failure,
            'signal_pickup_failure': self.signal_pickup_failure,
            'passenger_brake_command': self.passenger_brake_command,
            'apply_changes': self.apply_changes
        }

class TrainControllerTestBenchUI(QWidget):
    
    def __init__(self, communicator: Communicate):
        super().__init__()
        
        self.communicator = communicator
        
        self.announcement_output = ''
        
        # Connect signals to slots
        self.communicator.engine_failure_signal.connect(self.handle_engine_failure)
        self.communicator.brake_failure_signal.connect(self.handle_brake_failure)
        self.communicator.signal_failure_signal.connect(self.handle_signal_failure)
        self.communicator.passenger_brake_command_signal.connect(self.handle_passenger_brake_command)
        self.communicator.commanded_speed_signal.connect(self.handle_commanded_speed)
        self.communicator.commanded_authority_signal.connect(self.handle_commanded_authority)
        self.communicator.announcement_signal.connect(self.announcement_output_to_testbench) 
        
        
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Test Bench")
        layout.addWidget(title)
        
        # Train ID Dropdown
        hbox_train_id = QHBoxLayout()
        train_id_label = QLabel("Train ID:")
        hbox_train_id.addWidget(train_id_label)
        
        self.train_id_dropdown = QComboBox()
        self.train_id_dropdown.addItems(["1", "2", "3"])
        self.train_id_dropdown.setEnabled(False)  # Make the dropdown read-only
        self.train_id_dropdown.setStyleSheet("border-radius: 10px;")
        hbox_train_id.addWidget(self.train_id_dropdown)
        
        layout.addLayout(hbox_train_id)
        
        # Beacon Information
        hbox_beacon = QVBoxLayout()
        beacon_label = QLabel("Destination:")
        hbox_beacon.addWidget(beacon_label)
        
        self.beacon_input = QLineEdit()
        self.beacon_input.setStyleSheet("border-radius: 10px;")
        self.beacon_input.editingFinished.connect(self.emit_beacon_destination)
        hbox_beacon.addWidget(self.beacon_input)
        
        layout.addLayout(hbox_beacon)
        
        # Create input fields and labels
        self.create_input_field(layout, "Current Speed:", "current_speed")
        self.create_input_field(layout, "Commanded Speed:", "commanded_speed")
        self.create_input_field(layout, "Commanded Authority:", "commanded_authority")
        self.create_input_field(layout, "Acceleration:", "acceleration")
        self.create_input_field(layout, "Passengers:", "passengers")
        self.create_input_field(layout, "Train Weight:", "train_weight")  # New input field
        self.create_input_field(layout, "Current Velocity:", "current_velocity")  # New input field
        
        # Failure Simulations
        hbox_failures = QHBoxLayout()
        self.create_failure_button(hbox_failures, "Train Engine Failure", "train_engine_failure")
        self.create_failure_button(hbox_failures, "Brake Failure", "brake_failure")
        self.create_failure_button(hbox_failures, "Signal Pickup Failure", "signal_pickup_failure")
        layout.addLayout(hbox_failures)
        
        # Passenger Brake Command
        self.passenger_brake_button = QPushButton("PASSENGER BRAKE COMMAND")
        self.passenger_brake_button.setStyleSheet("background-color: red; color: white; font-weight: bold; border-radius: 5px; border: 2px solid black; padding: 5px;")
        self.passenger_brake_button.clicked.connect(self.toggle_passenger_brake_command)
        layout.addWidget(self.passenger_brake_button)
        
        # Apply Changes Button
        self.apply_changes_button = QPushButton("APPLY CHANGES")
        self.apply_changes_button.setStyleSheet("background-color: blue; color: white; border-radius: 5px; border: 2px solid black; padding: 5px;")
        self.apply_changes_button.clicked.connect(self.apply_changes)
        layout.addWidget(self.apply_changes_button)
        
        # Announcement Output
        announcement_label = QLabel("Announcement Output:")
        layout.addWidget(announcement_label)
        
        self.announcement_output = QTextEdit()
        self.announcement_output.setReadOnly(True)
        self.announcement_output.setText("")
        self.announcement_output.setPlaceholderText("Announcement output is shown here.")
        self.announcement_output.setStyleSheet("border-radius: 10px;")
        layout.addWidget(self.announcement_output)
        
        self.setLayout(layout)
        self.setWindowTitle('Train Controller')
        self.show()
        
    def emit_beacon_destination(self):
        beacon_destination = self.beacon_input.text()
        self.communicator.station_name_signal.emit(beacon_destination)
        
    def create_input_field(self, layout, label_text, variable_name):
        vbox = QVBoxLayout()
        
        label = QLabel(label_text)
        vbox.addWidget(label)
        
        line_edit = QLineEdit()
        line_edit.setObjectName(variable_name)
        line_edit.setStyleSheet("border-radius: 10px;")
        vbox.addWidget(line_edit)
        
        layout.addLayout(vbox)
        
    def create_failure_button(self, layout, label_text, variable_name):
        button = QPushButton(label_text)
        button.setStyleSheet("background-color: green; color: white; border-radius: 5px; border: 2px solid black; padding: 5px;")
        button.clicked.connect(lambda: self.toggle_failure(button, variable_name))
        layout.addWidget(button)
        
    def toggle_failure(self, button, variable_name):
        current_value = button.property("toggled")
        new_value = not current_value
        button.setProperty("toggled", new_value)
        button.setStyleSheet("background-color: red; color: white; border-radius: 5px; border: 2px solid black; padding: 5px" if new_value else "background-color: green; color: white; border-radius: 5px; border: 2px solid black; padding: 5px")
        print(f"{variable_name} is now {'enabled' if new_value else 'disabled'}")
        
        # Emit the corresponding signal
        if variable_name == "train_engine_failure":
            self.communicator.engine_failure_signal.emit(new_value)
        elif variable_name == "brake_failure":
            self.communicator.brake_failure_signal.emit(new_value)
        elif variable_name == "signal_pickup_failure":
            self.communicator.signal_failure_signal.emit(new_value)
        
    def toggle_passenger_brake_command(self):
        current_value = self.passenger_brake_button.property("toggled")
        new_value = not current_value
        self.passenger_brake_button.setProperty("toggled", new_value)
        self.passenger_brake_button.setStyleSheet("background-color: red; color: white; font-weight: bold; border-radius: 5px; border: 2px solid black; padding: 5px;" if new_value else "background-color: red; color: white; font-weight: bold; border-radius: 5px; border: 2px solid black; padding: 5px;")
        print(f"Passenger brake command is now {'enabled' if new_value else 'disabled'}")
        
        # Emit the signal
        self.communicator.passenger_brake_command_signal.emit(new_value)
        
    def apply_changes(self):
        variables = {
            'current_speed': self.findChild(QLineEdit, "current_speed").text(),
            'commanded_speed': self.findChild(QLineEdit, "commanded_speed").text(),
            'commanded_authority': self.findChild(QLineEdit, "commanded_authority").text(),
            'acceleration': self.findChild(QLineEdit, "acceleration").text(),
            'passengers': self.findChild(QLineEdit, "passengers").text(),
            'train_weight': self.findChild(QLineEdit, "train_weight").text(),
            'current_velocity': self.findChild(QLineEdit, "current_velocity").text(),  # New input field
            'beacon_destination_location': self.beacon_input.text(),
        }
        
        if variables['commanded_speed'].isdigit():
            self.communicator.commanded_speed_signal.emit(int(variables['commanded_speed']))
        else:
            print("Invalid commanded speed input")

        if variables['commanded_authority'].isdigit():
            self.communicator.commanded_authority_signal.emit(int(variables['commanded_authority']))
        else:
            print("Invalid commanded authority input")
         
        self.announcement_output.setText(f"Train {self.train_id_dropdown.currentText()} changes applied.")
        
        # Print all variables to the terminal
        print("Current Speed:", variables['current_speed'])
        print("Commanded Speed:", variables['commanded_speed'])
        print("Commanded Authority:", variables['commanded_authority'])
        print("Acceleration:", variables['acceleration'])
        print("Passengers:", variables['passengers'])
        print("Train Weight:", variables['train_weight'])
        print("Current Velocity:", variables['current_velocity'])  # New variable
        print("Beacon Destination Location:", variables['beacon_destination_location'])
        print("Changes applied")
        
    # Slots to handle signals
    def handle_engine_failure(self, state):
        print(f"Engine failure state changed to: {state}")
        
    def handle_brake_failure(self, state):
        print(f"Brake failure state changed to: {state}")
        
    def handle_signal_failure(self, state):
        print(f"Signal failure state changed to: {state}")
        
    def handle_passenger_brake_command(self, state):
        print(f"Passenger brake command state changed to: {state}")
        
    def handle_commanded_speed(self, speed):
        print(f"Commanded speed changed to: {speed}")
        
    def handle_commanded_authority(self, authority):
        print(f"Commanded authority changed to: {authority}")
        
    # Handle announcement output
    def announcement_output_to_testbench(self, announcement):
        self.announcement_output.setText(announcement)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    communicator = Communicate()
    controller = TrainControllerTestBench(communicator)
    ex = TrainControllerTestBenchUI(communicator)
    
    # Connect UI signals to controller slots
    # ex.engine_failure_signal.connect(controller.communicator.engine_failure_signal.emit)
    # ex.brake_failure_signal.connect(controller.communicator.brake_failure_signal.emit)
    # ex.signal_failure_signal.connect(controller.communicator.signal_failure_signal.emit)
    # ex.passenger_brake_command_signal.connect(controller.communicator.passenger_brake_command_signal.emit)
    # ex.apply_changes_signal.connect(lambda variables: controller.apply_changes_signal.emit(variables))
    
    sys.exit(app.exec())