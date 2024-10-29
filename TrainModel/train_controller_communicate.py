# train_controller_communicate.py

from PyQt6.QtCore import pyqtSignal, QObject

class TrainControllerCommunicate(QObject):
    # From Train Controller to Train Model
    power_command_signal = pyqtSignal(float)
    door_command_signal = pyqtSignal(bool)
    light_command_signal = pyqtSignal(bool)
    service_brake_signal = pyqtSignal(bool)
    emergency_brake_signal = pyqtSignal(bool)
    desired_temperature_signal = pyqtSignal(float)
    announcement_signal = pyqtSignal(str)
    station_name_signal = pyqtSignal(str)

    # From Train Model to Train Controller
    commanded_speed_signal = pyqtSignal(int)
    commanded_authority_signal = pyqtSignal(int)
    current_temperature_signal = pyqtSignal(float)
    signal_status_signal = pyqtSignal(bool, int)
    current_velocity_signal = pyqtSignal(float)
    polarity_signal = pyqtSignal(bool)
    passenger_brake_signal = pyqtSignal(bool)

    # Failure Signals
    engine_failure_signal = pyqtSignal(bool)
    brake_failure_signal = pyqtSignal(bool)
    signal_failure_signal = pyqtSignal(bool)
