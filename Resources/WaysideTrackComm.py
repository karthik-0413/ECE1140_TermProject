from PyQt6.QtCore import pyqtSignal, QObject

class WaysideControllerTrackComm(QObject):
    
    # Wayside Controller -> Track Model
    commanded_speed_signal = pyqtSignal(list)        #km/hr
    commanded_authority_signal = pyqtSignal(list)    # Blocks
    switch_cmd_signal = pyqtSignal(list)             # 0: left, 1: right
    signal_cmd_signal = pyqtSignal(list)             # 0: red, 1: green
    crossing_cmd_signal = pyqtSignal(list)           # 0: open, 1: closed
    
    # Track Model -> Wayside Controller
    block_occupancies_signal = pyqtSignal(list)      # 0: unoccupied, 1: occupied