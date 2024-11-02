# CTC_communicate.py

from PyQt6.QtCore import pyqtSignal, QObject

class CTCTrain(QObject):
    """Communication class for CTC and Train Model."""

    # CTC -> Train Model
    current_train_count_signal = pyqtSignal(int)    # Current train count (int)
