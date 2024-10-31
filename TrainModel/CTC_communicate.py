from PyQt6.QtCore import pyqtSignal, QObject

class CTCTrain(QObject):
    
    # CTC -> Train Model
    # Param is int instead of bool that represents how many trains are on the tracks
    dispatch_train_signal = pyqtSignal(int)    # Number of trains on track


    