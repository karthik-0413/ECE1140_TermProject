# CTC_communicate.py

from PyQt6.QtCore import pyqtSignal, QObject

class CTCTrain(QObject):
    """Communication class for CTC and Train Model."""

    # CTC -> Train Model
    # Parameter is int representing the current train count
    dispatch_train_signal = pyqtSignal(int)    # Current train count
