# track_model_communicate.py

from PyQt6.QtCore import pyqtSignal, QObject

class TrackModelCommunicate(QObject):
    # From Train Model to Track Model
    position_signal = pyqtSignal(float)
    passengers_disembarking_signal = pyqtSignal(int)
    seat_vacancy_signal = pyqtSignal(int)

    # From Track Model to Train Model
    track_commanded_speed_signal = pyqtSignal(int)
    track_commanded_authority_signal = pyqtSignal(int)
    block_info_signal = pyqtSignal(float, float, bool)
    track_polarity_signal = pyqtSignal(bool)
    track_signal_status_signal = pyqtSignal(bool, int)
