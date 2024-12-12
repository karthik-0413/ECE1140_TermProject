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
from TrackModel.track_model_ui import Ui_TrackModel
from Resources.TrackTrainComm import TrackTrainModelComm
from TrackModel.track_model import track_model
from Resources.WaysideTrackComm import WaysideControllerTrackComm
from TrackController.wayside_shell import wayside_shell_class

from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtCore import QTimer
import sys

# Function to be triggered by clock tick
def handle_clock_tick(seconds, train_controller_shell, train_model_data, track_model_backend, wayside_shell_object, ctc_frontend):
    if seconds % 2 == 0:
        ctc_frontend.ctc.write_to_communicate_objects()
        wayside_shell_object.write()
        track_model_backend.write()
        train_model_data.train_data.write_to_trainController_trackModel()
        train_controller_shell.write_to_train_model()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Instantiate components
    comm1 = CTCTrain()
    comm2 = WaysideControllerTrackComm()
    comm3 = TrackTrainModelComm()
    comm4 = CTCWaysideControllerComm()
    comm5 = TrainTrainController()

    # CTC Office
    ctc_window = QMainWindow()
    ctc_ui = CTC_frontend(comm1, comm4)
    ctc_ui.setupUi(ctc_window)

    # Wayside Controller
    wayside_shell_object = wayside_shell_class(comm4, comm2)

    # Track Model
    track_model_ui = Ui_TrackModel()
    track_model_backend = track_model(comm3, comm2)

    # Train Model
    tm_window = MainWindow(comm1, comm5, comm3)

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

    # Clock Setup
    clock = StopwatchEngine()
    clock.initiate()

    timer = QTimer()
    timer.timeout.connect(lambda: handle_clock_tick(clock.elapsed_seconds, tc_shell_window, tm_window, track_model_backend, wayside_shell_object, ctc_ui))
    timer.start(100)

    clockUI = ClockDisplay(clock)

    # Launcher Page
    class LauncherWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Launcher")
            self.setGeometry(100, 100, 300, 400)

            layout = QVBoxLayout()

            # Add buttons for each UI
            self.ctc_button = QPushButton("Open CTC UI")
            self.ctc_button.clicked.connect(ctc_window.show)
            layout.addWidget(self.ctc_button)

            self.train_model_button = QPushButton("Open Train Model UI")
            self.train_model_button.clicked.connect(tm_window.show)
            layout.addWidget(self.train_model_button)

            self.train_controller_button = QPushButton("Open Train Controller UI")
            self.train_controller_button.clicked.connect(tc_window.show)
            layout.addWidget(self.train_controller_button)

            self.track_model_button = QPushButton("Open Track Model UI")
            # self.track_model_button.clicked.connect(track_model_ui.show)
            layout.addWidget(self.track_model_button)

            self.clock_ui_button = QPushButton("Open Clock UI")
            self.clock_ui_button.clicked.connect(clockUI.show)
            layout.addWidget(self.clock_ui_button)

            container = QWidget()
            container.setLayout(layout)
            self.setCentralWidget(container)

    launcher = LauncherWindow()
    launcher.show()

    sys.exit(app.exec())