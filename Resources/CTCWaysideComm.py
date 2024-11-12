from PyQt6.QtCore import pyqtSignal, QObject

class CTCWaysideControllerComm(QObject):
    
    # CTC -> Wayside
    suggested_speed_signal = pyqtSignal(list)    # km/hr
    suggested_authority_signal = pyqtSignal(list) # Blocks
    current_block_number_signal = pyqtSignal(list)
    
    # Wayside -> CTC
    block_occupancy_signal = pyqtSignal(list)