from CTC_Office.CTC_frontend import CTC_frontend
from TrainModel.main import MainWindow
from TrainModel.CTC_communicate import CTC_Train_Model_Communicate
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import Qt, QTimer
from Resources.CTCTrain import CTCTrain
from Resources.CTCWaysideComm import CTCWaysideControllerComm
from Resources.Clock import *
from Resources.TrainTrainControllerComm import TrainTrainController
from TrainController.TrainController import *
from TrainController.TrainControllerShell import TrainControllerShell
from TrainModel.train_data import TrainData

import sys


# Function to be triggered by clock tick
def handle_clock_tick(seconds, train_controller_shell: TrainControllerShell, train_model_data: MainWindow, ctc_frontend: CTC_frontend):
    # print(f"Clock tick {seconds} seconds")
    if seconds % 2 == 0:
        train_model_data.train_data.write_to_trainController_trackModel()
        train_controller_shell.write_to_train_model()
        ctc_frontend.ctc.write_to_communicate_objects()
    # Create a QTimer to call handle_clock_tick every second
    # else:
    #     pass


def get_seconds_elapsed(seconds):
    # print(f"Elapsed time: {seconds} seconds")
    return seconds

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # CTC Setup
    ctc_window = QMainWindow()

    # Train Model Setup
    # (No need to create another QApplication)
    
    # Train Controller Setup
    # (No need to create another QApplication)

    # CTC -> Train Model Communication
    comm1 = CTC_Train_Model_Communicate()
    comm2 = CTCWaysideControllerComm()
    
    # Train Model -> Train Controller Communication
    comm5 = TrainTrainController()
    
    
    # CTC
    ctc = CTC_frontend(comm1, comm2)
    ctc.setupUi(ctc_window)

    # Train Model
    tm_window = MainWindow(comm1, comm5)
    
    # Train Controller
    doors = Doors()
    tuning = Tuning()
    brake_status = BrakeStatus(comm5)
    power_class = PowerCommand(brake_status, tuning)
    speed_control = SpeedControl(power_class, brake_status, comm5)
    failure_modes = FailureModes(speed_control, power_class)
    lights = Lights(speed_control)
    temperature = Temperature()
    position = Position(doors, failure_modes, speed_control, power_class, comm5, lights, brake_status)
    
    tc_window = TrainControllerUI(comm5, doors, tuning, brake_status, power_class, speed_control, failure_modes, position, lights, temperature)
    tc_shell_window = TrainControllerShell(comm5, tc_window)


    ctc_window.show()
    tm_window.show()
    
    # Clock Setup
    clock = StopwatchEngine()
    clock.initiate()
    
    
    timer = QTimer()
    timer.timeout.connect(lambda: handle_clock_tick(clock.elapsed_seconds, tc_shell_window, tm_window, ctc))
    timer.start(100)
    
    clockUI = ClockDisplay(clock)
    clockUI.show()
    
    # Timer to update every 
    # Use QTimer to trigger `handle_clock_tick` every second
    # while True:
    #     handle_clock_tick(tc_shell_window, tm_window, clock)


    sys.exit(app.exec())