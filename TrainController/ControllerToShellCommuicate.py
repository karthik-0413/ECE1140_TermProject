from PyQt6.QtCore import pyqtSignal, QObject

class ControllerToShellCommunicate(QObject):
    
    # Shell -> Controller
    train_id_list = pyqtSignal(list)                # int

    
    # Controller -> Shell
    selected_train_id = pyqtSignal(int)             # int