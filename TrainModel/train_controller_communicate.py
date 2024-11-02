# train_controller_communicate.py

from PyQt6.QtCore import pyqtSignal, QObject

class TrainControllerCommunicate(QObject):

    # Train Controller -> Train Model
    power_command_signal = pyqtSignal(list)  # List of power commands for all trains
    service_brake_command_signal = pyqtSignal(list)
    emergency_brake_command_signal = pyqtSignal(list)
    desired_temperature_signal = pyqtSignal(list)
    exterior_lights_signal = pyqtSignal(list)
    interior_lights_signal = pyqtSignal(list)
    left_door_signal = pyqtSignal(list)
    right_door_signal = pyqtSignal(list)
    announcement_signal = pyqtSignal(list)
    grade_signal = pyqtSignal(list)
    passenger_brake_command_signal = pyqtSignal(list)
    train_count_signal = pyqtSignal(int)  # Total number of trains

    # Train Model -> Train Controller
    current_velocity_signal = pyqtSignal(list)
    commanded_speed_signal = pyqtSignal(list)
    commanded_authority_signal = pyqtSignal(list)
    engine_failure_signal = pyqtSignal(list)
    brake_failure_signal = pyqtSignal(list)
    signal_failure_signal = pyqtSignal(list)
    actual_temperature_signal = pyqtSignal(list)
    polarity_signal = pyqtSignal(list)
