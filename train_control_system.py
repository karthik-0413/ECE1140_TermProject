from CTC_Office.CTC_frontend import CTC_frontend
from TrainModel.main import MainWindow
from TrainModel.CTC_communicate import CTC_Train_Model_Communicate
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import Qt, QTimer
from Resources.CTCTrain import CTCTrain
from Resources.CTCWaysideComm import CTCWaysideControllerComm
from Resources.Clock import *
from Resources.TrainTrainControllerComm import TrainTrainController
from TrainController.ControllerToShellCommuicate import *
from TrainController.TrainController import *
from TrainController.TrainControllerShell import TrainControllerShell
from TrainModel.train_data import TrainData
from TrackModel.track_model_ui import Ui_TrackModel
from Resources.TrackTrainComm import TrackTrainModelComm
from TrackModel.track_model import track_model
from Resources.WaysideTrackComm import WaysideControllerTrackComm

from TrackController.wayside_shell import wayside_shell_class

import sys
from time import sleep

# Upload track layout and PLC programs automatically
debug = True

# Function to be triggered by clock tick
def handle_clock_tick(seconds, train_controller_shell: TrainControllerShell, train_model_data: MainWindow, track_model_backend: track_model, wayside_shell_object: wayside_shell_class, ctc_frontend: CTC_frontend):
    if seconds % 2 == 0:
        ctc_frontend.ctc.write_to_communicate_objects()
        ## print("Writing to communicate objects")
        wayside_shell_object.write()
        track_model_backend.write()
        train_model_data.train_data.write_to_trainController_trackModel()
        train_controller_shell.write_to_train_model()
        
def get_seconds_elapsed(seconds):
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
    comm1 = CTCTrain()

    # Wayside Controller -> Track Model Communication
    comm2 = WaysideControllerTrackComm()

    # Track Model -> Train Model Communication
    comm3 = TrackTrainModelComm()
    
    comm4 = CTCWaysideControllerComm()
    
    # Train Model -> Train Controller Communication
    comm5 = TrainTrainController()

    # CTC <-> Wayside Controller Communication
    comm4 = CTCWaysideControllerComm()
    
    # Train Controller -> Train Controller Shell Communication
    comm6 = ControllerToShellCommunicate()
    
    # Clock Communication
    clock_comm = ClockComm()
    
    
    # CTC Office
    ctc_ui = CTC_frontend(comm1, comm4, clock_comm)
    ctc_ui.setupUi(ctc_window)
    ctc_window.setObjectName("CTC Office")
    ctc_window.setWindowTitle("CTC Office")

    # Wayside Controller
    wayside_shell_object = wayside_shell_class(comm4, comm2)

    # Track Model
    track_model_ui = Ui_TrackModel()
    track_model_backend = track_model(comm3, comm2)

    # Train Model
    tm_window = MainWindow(comm1, comm5, comm3, clock_comm)
    
    # Train Controller
    tc_shell_window = TrainControllerShell(comm5, comm6, clock_comm)

    # Show all windows
    ctc_window.show()
    tm_window.show()
    
    # Clock Setup
    clock = StopwatchEngine(clock_comm)
    clock.initiate()
    
    
    timer = QTimer()
    timer.timeout.connect(lambda: handle_clock_tick(clock.elapsed_seconds, tc_shell_window, tm_window, track_model_backend, wayside_shell_object, ctc_ui))
    timer.start(int(100 / clock.speed_factor))
    
    clockUI = ClockDisplay(clock)
    clockUI.show()

    
    if debug:

        track_model_backend.read_layout_file("TrackModel/green_layout.csv")

        plc_programs = ["TrackController/green_plc_1.py", "TrackController/green_plc_2.py", "TrackController/green_plc_3.py"]

        wayside_shell_object.execute_files(plc_programs)

        ctc_ui.ctc.upload_layout_to_line("CTC_Office/Green_Line_Layout.xlsx")
        
                # Update Lines Selector
        ctc_ui.LineSelectorComboBox.clear()
        ctc_ui.LineSelectorComboBox.addItem("Green")

        # Update Station Selector
        ctc_ui.StationSelector.clear()
        stations = ctc_ui.ctc.get_stations()
        # print("Stations = ", stations)
        ctc_ui.StationSelector.addItems(stations)

    
    # Timer to update every 
    # Use QTimer to trigger `handle_clock_tick` every second
    # while True:
    #     handle_clock_tick(tc_shell_window, tm_window, clock)


    sys.exit(app.exec())