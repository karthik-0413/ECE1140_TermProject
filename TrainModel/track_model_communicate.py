# track_model_communicate.py

from PyQt6.QtCore import pyqtSignal, QObject

class TrackModelCommunicate(QObject):

    # Track Model -> Train Model
    commanded_speed_signal = pyqtSignal(int, int)        # index, km/hr
    commanded_authority_signal = pyqtSignal(int, int)    # index, Blocks
    block_grade_signal = pyqtSignal(int, float)          # index, %
    block_elevation_signal = pyqtSignal(int, float)      # index, m
    polarity_signal = pyqtSignal(int, bool)              # index, If flipped, then train has moved onto next block
    number_passenger_boarding_signal = pyqtSignal(int, int)  # index, People

    # Train Model -> Track Model
    position_signal = pyqtSignal(int, float)             # index, m
    number_passenger_leaving_signal = pyqtSignal(int, int)  # index, People
    seat_vacancy_signal = pyqtSignal(int, int)           # index, People
