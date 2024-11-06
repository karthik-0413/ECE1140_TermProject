from PyQt6.QtCore import pyqtSignal, QObject

class WaysideControllerTrackComm(QObject):
    
    # Wayside -> Track Model
    commanded_speed_signal = pyqtSignal(int)    #km/hr
    commanded_authority_signal = pyqtSignal(int)    # Blocks
    switch_command_signal = pyqtSignal(list)    
    signal_command_signal = pyqtSignal(list)
    crossing_command_signal = pyqtSignal(bool)
    
    # Track Model -> Wayside
    block_occupancy_signal = pyqtSignal(list)