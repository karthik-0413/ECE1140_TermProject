# track_model_communicate.py

from PyQt6.QtCore import pyqtSignal, QObject

class TrackModelCommunicate(QObject):

    # Track Model -> Train Model (sending lists of values for all trains)
    commanded_speed_signal = pyqtSignal(list)          # List of commanded speeds (km/hr)
    commanded_authority_signal = pyqtSignal(list)      # List of commanded authorities (blocks)
    block_grade_signal = pyqtSignal(list)              # List of block grades (%)
    block_elevation_signal = pyqtSignal(list)          # List of block elevations (m)
    polarity_signal = pyqtSignal(list)                 # List of polarity states
    number_passenger_boarding_signal = pyqtSignal(list)  # List of numbers of passengers boarding

    # Train Model -> Track Model (sending lists of values for all trains)
    position_signal = pyqtSignal(list)                 # List of positions (m)
    number_passenger_leaving_signal = pyqtSignal(list) # List of numbers of passengers leaving
    seat_vacancy_signal = pyqtSignal(list)             # List of seat vacancies (number of seats available)
