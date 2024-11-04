# ctc_communicate.py

from PyQt6.QtCore import QObject, pyqtSignal

class CTCCommunicate(QObject):
    """Class to simulate communication with the CTC system."""

    current_train_count_signal = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.current_train_count = 0  # Initial value indicating no trains on the tracks

    def update_current_train_count(self, count):
        """Simulate receiving a new train count from the CTC."""
        self.current_train_count = count
        self.current_train_count_signal.emit(self.current_train_count)
