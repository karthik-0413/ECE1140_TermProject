from PyQt6.QtCore import pyqtSignal, QObject

class CTCWaysideControllerComm(QObject):
    
    # CTC -> Wayside
    suggested_speed_signal = pyqtSignal(list)     # km/hr SSpeed of every block - (If no train exists at location, speed = None)
    suggested_authority_signal = pyqtSignal(list) # Blocks same here as above None = no train


    
    # Wayside -> CTC
    block_occupancy_signal = pyqtSignal(list)     # bools