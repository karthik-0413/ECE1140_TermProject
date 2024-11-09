from CTC_Office.CTC_frontend import CTC_frontend
from TrainModel.main import MainWindow
from TrainModel.CTC_communicate import CTC_Train_Model_Communicate
from PyQt6.QtWidgets import QApplication, QMainWindow
from Resources.CTCTrain import CTCTrain
from Resources.TrainTrainControllerComm import TrainTrainController
from TrainController.TrainController import *
from TrainController.TrainControllerShell import TrainControllerShell

import sys

if __name__ == '__main__':
    # CTC Setup
    ctc_app = QApplication(sys.argv)
    ctc_window = QMainWindow()

    # Train Model Setup
    tm_app = QApplication(sys.argv)
    
    # Train Controller Setup
    tc_app = QApplication(sys.argv)

    # CTC -> Train Model Communication
    comm1 = CTC_Train_Model_Communicate()
    
    # Train Model -> Train Controller Communication
    comm5 = TrainTrainController()
    
    
    # CTC
    ctc_ui = CTC_frontend(comm1)
    ctc_ui.setupUi(ctc_window)

    # Train Model
    tm_window = MainWindow(comm1)
    
    # Train Controller
    doors = Doors()
    tuning = Tuning()
    brake_status = BrakeStatus(comm5)
    power_class = PowerCommand(brake_status, tuning)
    speed_control = SpeedControl(power_class, brake_status, comm5)
    failure_modes = FailureModes(speed_control, power_class)
    lights = Lights(speed_control)
    temperature = Temperature()
    position = Position(doors, failure_modes, speed_control, power_class, comm5, lights)
    
    tc_window = TrainControllerUI(comm5, doors, tuning, brake_status, power_class, speed_control, failure_modes, position, lights, temperature)
    tc_shell_window = TrainControllerShell(comm5, tc_window)


    ctc_window.show()
    tm_window.show()
    sys.exit(tm_app.exec())


    sys.exit(ctc_app.exec())
    

