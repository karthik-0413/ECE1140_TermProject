from PyQt6.QtCore import pyqtSignal, QObject

class ClockComm(QObject):

    elapsed_seconds = pyqtSignal(int)
    speed_factor = pyqtSignal(int)