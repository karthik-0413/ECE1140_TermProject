import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton, QTextEdit
from PyQt6.QtCore import pyqtSignal, QObject

class TrainController(QObject):
    def __init__(self):
        super().__init__()
        
        # Integer variables
        self.current_speed = 0
        self.commanded_speed = 0
        self.commanded_authority = 0
        self.mass_of_train = 0
        self.acceleration = 0
        self.passengers = 0
        self.train_weight = 0  # New variable
        
        # String variables
        self.beacon_destination_location = ""
        self.announcement = ""
        
        # Boolean variables
        self.train_engine_failure = False
        self.brake_failure = False
        self.signal_pickup_failure = False
        self.passenger_brake_command = False
        self.apply_changes = False

class TrainControllerUI(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
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
        hbox_beacon.addWidget(self.beacon_input)
        
        layout.addLayout(hbox_beacon)
        
        # Create input fields and labels
        self.create_input_field(layout, "Current Speed:", "current_speed")
        self.create_input_field(layout, "Commanded Speed:", "commanded_speed")
        self.create_input_field(layout, "Commanded Authority:", "commanded_authority")
        self.create_input_field(layout, "Acceleration:", "acceleration")
        self.create_input_field(layout, "Passengers:", "passengers")
        self.create_input_field(layout, "Train Weight:", "train_weight")  # New input field
        
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
        
    def create_input_field(self, layout, label_text, variable_name):
        vbox = QVBoxLayout()
        
        label = QLabel(label_text)
        vbox.addWidget(label)
        
        line_edit = QLineEdit()
        line_edit.setText(str(getattr(self.controller, variable_name)))
        line_edit.setStyleSheet("border-radius: 10px;")
        line_edit.textChanged.connect(lambda text, var=variable_name: self.update_variable(var, text))
        vbox.addWidget(line_edit)
        
        layout.addLayout(vbox)
        
    def create_failure_button(self, layout, label_text, variable_name):
        button = QPushButton(label_text)
        button.setStyleSheet("background-color: green; color: white; border-radius: 5px; border: 2px solid black; padding: 5px;")
        button.clicked.connect(lambda: self.toggle_failure(button, variable_name))
        layout.addWidget(button)
        
    def update_variable(self, variable_name, text):
        try:
            value = int(text)
        except ValueError:
            value = 0
        setattr(self.controller, variable_name, value)
        
    def toggle_failure(self, button, variable_name):
        current_value = getattr(self.controller, variable_name)
        new_value = not current_value
        setattr(self.controller, variable_name, new_value)
        button.setStyleSheet("background-color: red; color: white; border-radius: 5px; border: 2px solid black; padding: 5px" if new_value else "background-color: green; color: white; border-radius: 5px; border: 2px solid black; padding: 5px")
        print(f"{variable_name} is now {'enabled' if new_value else 'disabled'}")
        
    def toggle_passenger_brake_command(self):
        self.controller.passenger_brake_command = not self.controller.passenger_brake_command
        self.passenger_brake_button.setStyleSheet("background-color: red; color: white; font-weight: bold; border-radius: 5px; border: 2px solid black; padding: 5px;" if self.controller.passenger_brake_command else "background-color: red; color: white; font-weight: bold; border-radius: 5px; border: 2px solid black; padding: 5px;")
        print(f"Passenger brake command is now {'enabled' if self.controller.passenger_brake_command else 'disabled'}")
        
    def apply_changes(self):
        self.controller.apply_changes = True
        self.controller.beacon_destination_location = self.beacon_input.text()
        self.announcement_output.setText(f"Train {self.train_id_dropdown.currentText()} changes applied.")
        
        # Update the controller variables with the current input values
        for child in self.findChildren(QLineEdit):
            variable_name = child.objectName()
            if variable_name:
                self.update_variable(variable_name, child.text())
        
        # Print all variables to the terminal
        print("Current Speed:", self.controller.current_speed)
        print("Commanded Speed:", self.controller.commanded_speed)
        print("Commanded Authority:", self.controller.commanded_authority)
        print("Acceleration:", self.controller.acceleration)
        print("Passengers:", self.controller.passengers)
        print("Train Weight:", self.controller.train_weight)
        print("Beacon Destination Location:", self.controller.beacon_destination_location)
        print("Train Engine Failure:", self.controller.train_engine_failure)
        print("Brake Failure:", self.controller.brake_failure)
        print("Signal Pickup Failure:", self.controller.signal_pickup_failure)
        print("Passenger Brake Command:", self.controller.passenger_brake_command)
        print("Changes applied")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    controller = TrainController()
    ex = TrainControllerUI(controller)
    sys.exit(app.exec())
