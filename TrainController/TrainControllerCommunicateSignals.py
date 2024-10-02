from PyQt6.QtCore import pyqtSignal, QObject

class Communicate(QObject):
    engine_failure_signal = pyqtSignal(bool)
    brake_failure_signal = pyqtSignal(bool)
    signal_failure_signal = pyqtSignal(bool)
    passenger_brake_command_signal = pyqtSignal(bool)
    commanded_speed_signal = pyqtSignal(float)
    commanded_authority_signal = pyqtSignal(float)
    engineer_kp_signal = pyqtSignal(float)
    engineer_ki_signal = pyqtSignal(float)
    announcement_signal = pyqtSignal(str)
    station_name_signal = pyqtSignal(str)
    current_velocity_signal = pyqtSignal(float)