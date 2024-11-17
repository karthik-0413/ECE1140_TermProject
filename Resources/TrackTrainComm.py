from PyQt6.QtCore import pyqtSignal, QObject

class TrackTrainModelComm(QObject):
    
    # Track Model -> Train Model
    commanded_speed_signal = pyqtSignal(list)        #km/hr
    commanded_authority_signal = pyqtSignal(list)    # Blocks
    block_grade_signal = pyqtSignal(list)          # %   
    block_elevation_signal = pyqtSignal(list)      # m
    polarity_signal = pyqtSignal(list)              # If flipped, then train has moved onto next block
    number_passenger_boarding_signal = pyqtSignal(list) # People
    
    # Train Model -> Track Model
    position_signal = pyqtSignal(list)             # m
    number_passenger_leaving_signal = pyqtSignal(list) # People
    seat_vacancy_signal = pyqtSignal(list)            # People