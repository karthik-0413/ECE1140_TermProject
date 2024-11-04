from CTC_Office.CTC_frontend import CTC_frontend
#from TrainModel.main import MainWindow
from TrainModel.CTC_communicate import CTCTrain
from PyQt6.QtWidgets import QApplication, QMainWindow

import sys

if __name__ == '__main__':
    ctc_app = QApplication(sys.argv)
    ctc_window = QMainWindow()

    comm = CTCTrain

    ctc_ui = CTC_frontend(comm)
    ctc_ui.setupUi(ctc_window)
    ctc_window.show()

    sys.exit(ctc_app.exec())
    

