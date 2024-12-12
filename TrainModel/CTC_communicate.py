# CTC_communicate.py

from PyQt6.QtCore import QObject, pyqtSignal

class CTC_Train_Model_Communicate(QObject):
    """Class to simulate communication with the CTC system."""

    current_train_count_signal = pyqtSignal(int)
