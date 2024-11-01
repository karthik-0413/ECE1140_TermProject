# train_controller_communicate.py

from PyQt6.QtCore import pyqtSignal, QObject

class TrainControllerCommunicate(QObject):

    # Train Controller -> Train Model
    power_command_signal = pyqtSignal(int, float)  # index, power
    service_brake_command_signal = pyqtSignal(int, bool)
    emergency_brake_command_signal = pyqtSignal(int, bool)
    desired_temperature_signal = pyqtSignal(int, float)
    exterior_lights_signal = pyqtSignal(int, bool)
    interior_lights_signal = pyqtSignal(int, bool)
    left_door_signal = pyqtSignal(int, bool)
    right_door_signal = pyqtSignal(int, bool)
    announcement_signal = pyqtSignal(int, str)
    grade_signal = pyqtSignal(int, float)
    train_count_signal = pyqtSignal(int)  # New signal to send train count to Train Controller

    # Train Model -> Train Controller
    current_velocity_signal = pyqtSignal(int, float)
    commanded_speed_signal = pyqtSignal(int, int)
    commanded_authority_signal = pyqtSignal(int, int)
    engine_failure_signal = pyqtSignal(int, bool)
    brake_failure_signal = pyqtSignal(int, bool)
    signal_failure_signal = pyqtSignal(int, bool)
    passenger_brake_command_signal = pyqtSignal(int, bool)
    actual_temperature_signal = pyqtSignal(int, float)
    polarity_signal = pyqtSignal(int, bool)
