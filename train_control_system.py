from CTC_Office.CTC_frontend import CTC_frontend
from TrainModel.main import MainWindow
from TrainModel.CTC_communicate import CTC_Train_Model_Communicate
from PyQt6.QtWidgets import QApplication, QMainWindow

import sys

if __name__ == '__main__':
    ctc_app = QApplication(sys.argv)
    ctc_window = QMainWindow()

    tm_app = QApplication(sys.argv)

    comm = CTC_Train_Model_Communicate()

    ctc_ui = CTC_frontend(comm)
    ctc_ui.setupUi(ctc_window)


    tm_window = MainWindow(comm)


    ctc_window.show()
    tm_window.show()
    sys.exit(tm_app.exec())


    sys.exit(ctc_app.exec())
    

