from PyQt6.QtCore import pyqtSignal, QObject

class Communicate(QObject):
    engine_failure_signal = pyqtSignal(bool)
    brake_failure_signal = pyqtSignal(bool)
    signal_failure_signal = pyqtSignal(bool)
    passenger_brake_command_signal = pyqtSignal(bool)