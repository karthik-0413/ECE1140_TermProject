import sys
import os
from PyQt6.QtGui import QFont, QPixmap, QImage
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QLabel,
    QVBoxLayout, QHBoxLayout, QStackedWidget, QSizePolicy, QGridLayout,
    QScrollArea, QLineEdit, QComboBox, QDialog, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal, QObject, QTimer

# Add the path to the 'TrainController' folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'TrainController')))

# Now you can import from TrainController
from TrainControllerIntegratedCommunicateSignals import IntegratedCommunicate


class TrainModel:
    def __init__(self, communicate: IntegratedCommunicate):
        self.integrated_communicate = communicate

    def send_signal(self, signal):
        self.integrated_communicate.send(signal)

    def receive_signal(self):
        return self.integrated_communicate.receive()