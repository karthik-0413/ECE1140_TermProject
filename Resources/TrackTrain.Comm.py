from PyQt6.QtCore import pyqtSignal, QObject

class TrackTrainComm(QObject):
    
    # Track Model -> Train Model
    commanded_speed_signal = pyqtSignal(int)        #km/hr
    commanded_authority_signal = pyqtSignal(int)    # Blocks
    block_grade_signal = pyqtSignal(float)          # %   
    block_elevation_signal = pyqtSignal(float)      # m
    block_underground_signal = pyqtSignal(bool)     # 1 = Underground, 0 = Above ground
    polarity_signal = pyqtSignal(bool)              # If flipped, then train has moved onto next block
    signal_status_signal = pyqtSignal(list)           # [6, 1, 2, 0] - First and Third = A block that the switch connects, Second and Fourth = Status of that
    number_passenger_boarding_signal = pyqtSignal(int) # People
    
    # Train Model -> Track Model
    position_signal = pyqtSignal(float)             # m
    number_passener_leaving_signal = pyqtSignal(int) # People
    seat_vacancy_signal = pyqtSignal(int)            # People