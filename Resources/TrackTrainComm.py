from PyQt6.QtCore import pyqtSignal, QObject

class TrackTrainModelComm(QObject):
    
    # Track Model -> Train Model
    commanded_speed_signal = pyqtSignal(int)        #km/hr
    commanded_authority_signal = pyqtSignal(int)    # Blocks
    block_grade_signal = pyqtSignal(float)          # %   
    block_elevation_signal = pyqtSignal(float)      # m
    polarity_signal = pyqtSignal(bool)              # If flipped, then train has moved onto next block
    number_passenger_boarding_signal = pyqtSignal(int) # People
    
    # Train Model -> Track Model
    position_signal = pyqtSignal(float)             # m
    number_passenger_leaving_signal = pyqtSignal(int) # People
    seat_vacancy_signal = pyqtSignal(int)            # People