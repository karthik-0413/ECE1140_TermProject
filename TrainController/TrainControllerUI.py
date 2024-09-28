from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QSlider, QCheckBox, QFrame, QSizePolicy, QSpacerItem
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon


class TrainControllerUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Train Controller")
        self.setStyleSheet("background-color: lightgray;")

        # Main Layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 15, 30, 10)

        # Tabs and Main Header
        tab_layout = QHBoxLayout()
        tab1 = QLabel("Train Controller")
        tab2 = QLabel("Engineer's View")
        tab3 = QLabel("Test Bench")
        tab_layout.addWidget(tab1)
        tab_layout.addWidget(tab2)
        tab_layout.addWidget(tab3)

        # Title Label
        title_banner = QHBoxLayout()
        title_label = QLabel("Train Controller")
        title_label.setStyleSheet("font-size: 30px; font-weight: bold; color: black; background-color: blue;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Train ID Combo Box in the header
        self.train_id_combo = QComboBox()
        self.train_id_combo.addItems(["1", "2", "3"])
        self.train_id_combo.setStyleSheet("background-color: white; color: black;")
        self.train_id_combo.setEnabled(False)
        title_banner.addWidget(title_label, 3)
        title_banner.addWidget(QLabel("Train ID:"), 0)
        title_banner.addWidget(self.train_id_combo, 0)

        # Main Grid Layout for UI Elements
        main_grid = QGridLayout()

        # LEFT SECTION (Speed Controls and Operation Mode)
        # Speed Information
        current_speed_label = QLabel("Current Speed:")
        current_speed_label.setStyleSheet("font-size: 14px; font-weight: bold; color: black; margin-top: 50px; margin-right: 100px")
        main_grid.addWidget(current_speed_label, 0, 0)
        self.current_speed_edit = QLineEdit("50")
        self.current_speed_edit.setText(self.current_speed_edit.text() + " mph")
        self.current_speed_edit.setEnabled(False)
        self.current_speed_edit.setStyleSheet("margin-bottom: -20px; background-color: lightgray; max-width: 100px; border-radius: 5px; color: black; margin-bottom: 10px; border: 2px solid black;")
        main_grid.addWidget(self.current_speed_edit, 1, 0)

        commanded_speed_label = QLabel("Commanded Speed:")
        commanded_speed_label.setStyleSheet("font-size: 14px; font-weight: bold; color: black;")
        main_grid.addWidget(commanded_speed_label, 2, 0)
        self.commanded_speed_edit = QLineEdit("55")
        self.commanded_speed_edit.setText(self.commanded_speed_edit.text() + " mph")
        self.commanded_speed_edit.setEnabled(False)
        self.commanded_speed_edit.setStyleSheet("background-color: lightgray; max-width: 100px; border-radius: 5px; color: black; margin-bottom: 10px; border: 2px solid black;")
        main_grid.addWidget(self.commanded_speed_edit, 3, 0)

        commanded_authority_label = QLabel("Commanded Authority:")
        commanded_authority_label.setStyleSheet("font-size: 14px; font-weight: bold; color: black;")
        main_grid.addWidget(commanded_authority_label, 4, 0)
        self.commanded_authority_edit = QLineEdit("500")
        self.commanded_authority_edit.setText(self.commanded_authority_edit.text() + " feet")
        self.commanded_authority_edit.setEnabled(False)
        self.commanded_authority_edit.setStyleSheet("background-color: lightgray; max-width: 100px; border-radius: 5px; color: black; margin-bottom: 35px; border: 2px solid black;")
        main_grid.addWidget(self.commanded_authority_edit, 5, 0)

        # Operational Mode
        operational_mode_label = QLabel("Operational Mode:")
        operational_mode_label.setStyleSheet("font-size: 14px; font-weight: bold; color: black; margin-bottom 30px;")
        main_grid.addWidget(operational_mode_label, 6, 0)
        
        self.manual_button = QPushButton("Manual")
        self.manual_button.setStyleSheet("margin-top: 10px; margin-left: 10px; background-color: green; color: white; max-width: 100px; border-radius: 5px; padding-top: 10px; padding-bottom: 10px; border: 2px solid black;")
        main_grid.addWidget(self.manual_button, 7, 0)

        self.automatic_button = QPushButton("Automatic")
        self.automatic_button.setStyleSheet("margin-top: 20px; margin-left: 10px; background-color: white; color: black; max-width: 100px; border-radius: 5px; padding-top: 10px; padding-bottom: 10px; border: 2px solid black;")
        main_grid.addWidget(self.automatic_button, 8, 0)

        # CENTER SECTION (Setpoint Speed and Power Command)
        setpoint_label = QLabel("Setpoint Speed")
        setpoint_label.setStyleSheet("font-size: 30px; font-weight: bold; color: black;")
        main_grid.addWidget(setpoint_label, 2, 1, 1, 1, Qt.AlignmentFlag.AlignCenter)

        setpoint_layout = QHBoxLayout()
        self.setpoint_speed_edit = QLineEdit("50")
        self.setpoint_speed_edit.setStyleSheet("margin-left: 95px; max-width: 100px; color: black; border: 2px solid black; border-radius: 5px; padding: 5px;")
        self.setpoint_speed_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setpoint_unit = QLabel("mph")
        self.setpoint_unit.setStyleSheet("font-size: 12px; color: black;")
        setpoint_layout.addWidget(self.setpoint_speed_edit)
        setpoint_layout.addWidget(self.setpoint_unit)
        main_grid.addLayout(setpoint_layout, 3, 1, 1, 1, Qt.AlignmentFlag.AlignCenter)

        # Checkmark
        self.setpoint_check = QPushButton()
        self.setpoint_check.setIcon(QIcon('Eo_circle_green_checkmark.png'))
        self.setpoint_check.setStyleSheet("background-color: white; border: none; padding: 0px;")
        main_grid.addWidget(self.setpoint_check, 1, 3)

        # Power Command (Centered Narrower Input Box)
        power_command_label = QLabel("Power Command")
        power_command_label.setStyleSheet("font-size: 25px; font-weight: bold; color: black;")
        power_command_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_grid.addWidget(power_command_label, 7, 1, 1, 1)

        power_command_layout = QHBoxLayout()
        self.power_command_edit = QLineEdit("5.5")
        self.power_command_edit.setStyleSheet("font-size: 20px; max-width: 100px; color: black; border: 2px solid black; border-radius: 5px; padding: 5px;")
        self.power_command_edit.setEnabled(False)
        self.power_command_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.power_unit = QLabel("kWatts")
        self.power_unit.setStyleSheet("font-size: 12px; color: black;")
        self.power_command_edit.setStyleSheet("margin-left: 90px; max-width: 100px; color: black; border: 2px solid black; border-radius: 5px; padding: 5px; background-color: lightgray;")
        self.power_unit.setStyleSheet("font-size: 12px; color: black; background-color: lightgray;")
        power_command_layout.addWidget(self.power_command_edit)
        power_command_layout.addWidget(self.power_unit)
        main_grid.addLayout(power_command_layout, 8, 1, 1, 1, Qt.AlignmentFlag.AlignCenter)

        # RIGHT SECTION (Train Controls)
        current_temp_label = QLabel("Current Train Temperature")
        current_temp_label.setStyleSheet("font-size: 12px; font-weight: bold; color: white; padding-left: 50px;")
        main_grid.addWidget(current_temp_label, 0, 4)
        self.current_temp_edit = QLineEdit("72")
        self.current_temp_edit.setEnabled(False)
        self.current_temp_edit.setStyleSheet("background-color: lightgray; max-width: 100px; color: black; margin-bottom: 10px; margin-left: 50px;")
        main_grid.addWidget(self.current_temp_edit, 1, 4)

        desired_temp_label = QLabel("Desired Train Temperature")
        desired_temp_label.setStyleSheet("font-size: 12px; font-weight: bold; color: white; padding-left: 50px;")
        main_grid.addWidget(desired_temp_label, 2, 4)
        self.temp_slider = QSlider(Qt.Orientation.Horizontal)
        self.temp_slider.setRange(60, 100)
        self.temp_slider.setValue(72)
        self.temp_value_label = QLabel(str(self.temp_slider.value()))
        self.temp_value_label.setStyleSheet("color: white; padding-left: 10px;")
        main_grid.addWidget(self.temp_value_label, 3, 4)

        main_grid.addWidget(self.temp_slider, 5, 4)

        # Lights
        main_grid.addWidget(QLabel("Interior Lights:"), 6, 4)
        self.interior_light_check = QCheckBox()
        main_grid.addWidget(self.interior_light_check, 6, 5)

        main_grid.addWidget(QLabel("Exterior Lights:"), 7, 4)
        self.exterior_light_check = QCheckBox()
        main_grid.addWidget(self.exterior_light_check, 7, 5)

        # Door Status
        main_grid.addWidget(QLabel("Right Door Status:"), 9, 4)
        self.right_door_status = QPushButton("OPEN")
        self.right_door_status.setStyleSheet("background-color: green;")
        main_grid.addWidget(self.right_door_status, 9, 5)

        main_grid.addWidget(QLabel("Left Door Status:"), 10, 4)
        self.left_door_status = QPushButton("CLOSE")
        self.left_door_status.setStyleSheet("background-color: red;")
        main_grid.addWidget(self.left_door_status, 10, 5)

        # Bottom Layout for Indicators and Brakes
        bottom_layout = QHBoxLayout()

        # Service Brake Button (Bottom-Left)
        service_brake_button = QPushButton("SERVICE BRAKE")
        service_brake_button.setStyleSheet("background-color: yellow; font-size: 20px; border-radius: 10px;  font-weight: bold; color: black; border: 3px solid black; padding: 50px;")
        bottom_layout.addWidget(service_brake_button, 0, Qt.AlignmentFlag.AlignLeft)

        # Fault Indicators in the Bottom-Center
        fault_group = QFrame()
        fault_layout = QGridLayout()

        # Train Engine Failure
        train_engine_fail_label = QLabel("Train Engine Failure")
        train_engine_fail_label.setStyleSheet("font-size: 14px; font-weight: bold; color: black;")
        engine_fail_indicator = QPushButton()
        engine_fail_indicator.setStyleSheet("background-color: green;")
        fault_layout.addWidget(train_engine_fail_label, 0, 0, Qt.AlignmentFlag.AlignCenter)
        fault_layout.addWidget(engine_fail_indicator, 1, 0, Qt.AlignmentFlag.AlignCenter)

        # Brake Failure
        brake_fail_label = QLabel("Brake Failure")
        brake_fail_label.setStyleSheet("font-size: 14px; font-weight: bold; color: black;")
        brake_fail_indicator = QPushButton()
        brake_fail_indicator.setStyleSheet("background-color: red;")
        fault_layout.addWidget(brake_fail_label, 0, 1, Qt.AlignmentFlag.AlignCenter)
        fault_layout.addWidget(brake_fail_indicator, 1, 1, Qt.AlignmentFlag.AlignCenter)

        # Signal Pickup Failure
        signal_fail_label = QLabel("Signal Pickup Failure")
        signal_fail_label.setStyleSheet("font-size: 14px; font-weight: bold; color: black;")
        signal_fail_indicator = QPushButton()
        signal_fail_indicator.setStyleSheet("background-color: green;")
        fault_layout.addWidget(signal_fail_label, 0, 2, Qt.AlignmentFlag.AlignCenter)
        fault_layout.addWidget(signal_fail_indicator, 1, 2, Qt.AlignmentFlag.AlignCenter)

        fault_group.setLayout(fault_layout)
        bottom_layout.addWidget(fault_group, 1, Qt.AlignmentFlag.AlignCenter)

        # Emergency Brake Button (Bottom-Right)
        emergency_brake_button = QPushButton("EMERGENCY BRAKE")
        emergency_brake_button.setStyleSheet("background-color: red; color: white; font-size: 20px; font-weight: bold; padding: 50px;")
        bottom_layout.addWidget(emergency_brake_button, 0, Qt.AlignmentFlag.AlignRight)

        # Add Components to the Main Layout
        main_layout.addLayout(tab_layout)
        main_layout.addLayout(title_banner)
        main_layout.addLayout(main_grid)
        main_layout.addLayout(bottom_layout)

        # Set Main Layout
        self.setLayout(main_layout)


if __name__ == "__main__":
    app = QApplication([])
    window = TrainControllerUI()
    window.show()
    app.exec()
