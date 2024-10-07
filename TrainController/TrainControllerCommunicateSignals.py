from PyQt6.QtCore import pyqtSignal, QObject

class Communicate(QObject):
    # Failure Modes
    engine_failure_signal = pyqtSignal(bool)
    brake_failure_signal = pyqtSignal(bool)
    signal_failure_signal = pyqtSignal(bool)
    
    # Passenger Brake Command
    passenger_brake_command_signal = pyqtSignal(bool)
    
    # Speed & Authority Signals
    current_velocity_signal = pyqtSignal(float)
    commanded_speed_signal = pyqtSignal(float)
    commanded_authority_signal = pyqtSignal(float)
    
    # Engineer Signals
    engineer_kp_signal = pyqtSignal(float)
    engineer_ki_signal = pyqtSignal(float)
    
    # Announcement Signals
    announcement_signal = pyqtSignal(str)
    station_name_signal = pyqtSignal(str)