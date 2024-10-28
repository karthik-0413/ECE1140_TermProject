from PyQt6.QtCore import pyqtSignal, QObject

class CTCTrain(QObject):
    
    # CTC -> Train Model
    dispatch_train_signal = pyqtSignal(bool)    # 1 = Dispatch, 0 = Do not dispatch