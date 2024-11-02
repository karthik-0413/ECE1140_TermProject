import queue
from TrainControllerUIClasses import *
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Resources.TrainTrainControllerComm import TrainTrainController

class TrainControllerShell:
    def __init__(self, train_trainControllerComm: TrainTrainController):
        # Queue to hold TrainControllerUI objects
        self.train_controller_queue = queue.Queue()
        self.train_controller_list: list[TrainControllerUI] = []
        self.train_trainControllerComm = train_trainControllerComm
        self.train_controller_window = None
        self.engineer_window = None
        
    def append_train_controller_ui(self, train_controller_ui: TrainControllerUI):
        self.train_controller_queue.put(train_controller_ui)
    
    def pop_train_controller_ui(self):
        if not self.train_controller_queue.empty():
            self.train_controller_window = self.train_controller_queue.get()
        else:
            self.train_controller_window = None

    def show_TrainControllerUI(self):
        # Create instances of each UI window
        doors = Doors()
        tuning = Tuning()
        brake_status = BrakeStatus(self.train_trainControllerComm)
        power_class = PowerCommand(brake_status, tuning)
        speed_control = SpeedControl(power_class, brake_status, self.train_trainControllerComm)
        failure_modes = FailureModes(speed_control)
        lights = Lights(speed_control)
        temperature = Temperature()
        position = Position(doors, failure_modes, speed_control, power_class, self.train_trainControllerComm, lights)
        
        # Instantiate the UI components
        self.train_controller_window = TrainControllerUI(self.train_trainControllerComm, doors, tuning, brake_status, power_class, speed_control, failure_modes, position, lights, temperature)
        self.engineer_window = TrainEngineerUI(tuning)

        # Show the UI windows
        self.train_controller_window.show()
        self.engineer_window.show()

    # Function to be triggered by clock tick
    def handle_clock_tick(self):
        if not self.train_controller_queue.empty():
            train_controller = self.train_controller_queue.queue[0]  # Peek at the first item
            if self.clock.seconds_elapsed % 2 == 0:
                train_controller.write_to_train_model()
            else:
                train_controller.read_from_train_model()

    def write_to_train_model(self):
        if self.train_controller_window:
            self.train_controller_window.write_to_train_model()

    def read_from_train_model(self):
        if self.train_controller_window:
            self.train_controller_window.read_from_train_model()