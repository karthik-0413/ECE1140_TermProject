from PyQt6.QtCore import pyqtSignal, QObject

class CTCWaysideControllerComm(QObject):
    
    # CTC -> Wayside
    suggested_speed_signal = pyqtSignal(int)    # km/hr
    suggested_authority_signal = pyqtSignal(int) # Blocks
    
    # Wayside -> CTC
    block_occupancy_signal = pyqtSignal(list)