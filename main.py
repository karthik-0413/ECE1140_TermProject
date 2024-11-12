from PyQt6.QtWidgets import QApplication
from Resources.Clock import *
from Resources.TrainTrainControllerComm import TrainTrainController
from ECE1140_TermProject.TrainController.TrainController import *

class TrainSystem:
    def __init__(self, train_trainControllerComm: TrainTrainController, clock: StopwatchEngine):
        self.train_trainControllerComm = train_trainControllerComm
        self.clock = clock
        self.CTC_window = None
        self.wayside_controller_window = None
        self.track_model_window = None
        self.train_model_window = None
        self.train_controller_window = None
        self.engineer_window = None
        self.clock_UI = None

    def show_ClockUI(self):
        # Create and show the clock UI
        self.clock_UI = ClockDisplay(self.clock)
        self.clock_UI.show()
        
    def show_CTCUI(self):
        pass
    
    def show_WaysideControllerUI(self):
        pass
    
    def show_TrackModelUI(self):
        pass
    
    def show_TrainModelUI(self):
        pass

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
    def handle_clock_tick(self, train_controller: TrainControllerUI):
        if self.clock.time_updated % 2 == 0:
            train_controller.write_to_train_model()
        else:
            train_controller.read_from_train_model()    # Do not need since already in constructor of my UI class, but just for placeholder

def main():
    app = QApplication([])

    # Instantiate the controller and the clock
    train_trainControllerComm = TrainTrainController()
    clock = StopwatchEngine()
    
    # Start the clock
    clock.start_clock()
    clock.second_passed.connect(lambda second: # print(f"Clock tick: {second}"))

    # Create a TrainSystem to handle all UI components
    train_system = TrainSystem(train_trainControllerComm, clock)

    # Show the TrainControllerUI and EngineerUI
    train_system.show_TrainControllerUI()
    # In order to get more trains just call the function above again with a different train_trainControllerComm

    # Show the Clock UI
    train_system.show_ClockUI()

    # Instantiate the TrainControllerUI for reading/writing
    train_controller = train_system.train_controller_window

    # Use QTimer to trigger `handle_clock_tick` every second
    timer = QTimer()
    timer.timeout.connect(lambda: train_system.handle_clock_tick(train_controller))
    timer.start(100)  # Update every millisecond

    # Execute the application event loop
    app.exec()

if __name__ == "__main__":
    main()
