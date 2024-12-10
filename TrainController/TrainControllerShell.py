import sys
import os

import os
from PyQt6.QtWidgets import QApplication

# from TrainController import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from TrainController.TrainController import *
from Resources.TrainTrainControllerComm import TrainTrainController as Communicate
from TrainController.ControllerToShellCommuicate import *

class TrainControllerShell:
    def __init__(self, communicator: Communicate, communicator2: ControllerToShellCommunicate):
        # Making a list of needed Train Controller UI instances
        self.train_controller_list: list[TrainControllerUI] = []
        self.train_engineer_list: list[TrainEngineerUI] = []
        
        # Setting up the parameters
        self.communicator = communicator
        self.communicator2 = communicator2
        
        # Initializing the variables needed
        self.counter = 0
        self.train_counter = 0
        self.previous_train_id = None
        self.total_train_id = None
        
        # Calling all of the necessary __init__ functions
        self.communicator.train_count_signal.connect(self.handle_train_id)
        self.read_from_train_model()
        

    ############################
    # TRAIN ID HANDLE FROM CTC #
    ############################

    def handle_train_id(self, train_id: int):
        if train_id != 0:
            self.previous_train_id = self.total_train_id
            self.total_train_id = train_id
            if self.total_train_id != self.previous_train_id:
                if train_id > len(self.train_controller_list):
                    for _ in range(train_id - self.train_counter):
                        self.counter += 1
                        self.train_counter += 1
                        
                        # Want Software for all trains except for the second train dispatched
                        if self.counter != 2:
                            # print("Software Train Controller is Initialized")
                            self.create_and_add_train_controller_and_engineer_ui(True)
                        # self.create_and_add_train_controller_and_engineer_ui(True)
                            
                        # Only want Hardware for second Train that was dispatched
                        elif self.counter == 2:
                            # print("Hardware Train Controller is Initialized")
                            self.create_and_add_train_controller_and_engineer_ui(False)
                            
                elif train_id < len(self.train_controller_list):
                    self.train_counter -= 1
                    self.remove_train_controller_and_engineer_ui(self.train_controller_list[0], self.train_engineer_list[0])
        
    ###########################################################
    # IMPLEMENT ADD/REMOVE TRAIN CONTROLLER UI FUNCTIONS HERE #
    ###########################################################

    def remove_train_controller_and_engineer_ui(self, train_controller_ui: TrainControllerUI, train_engineer_ui: TrainEngineerUI):
        if train_controller_ui in self.train_controller_list and train_engineer_ui in self.train_engineer_list:
            self.train_controller_list.remove(train_controller_ui)
            self.train_engineer_list.remove(train_engineer_ui)

    def create_and_add_train_controller_and_engineer_ui(self, module: bool):
        new_train_controller_ui, new_train_engineer_ui = self.create_new_train_controller_and_engineer_ui(module)
        self.train_controller_list.append(new_train_controller_ui)
        self.train_engineer_list.append(new_train_engineer_ui)
        self.train_controller_list[self.train_counter - 1].setWindowTitle("Train Controller " + str(self.train_counter))
        self.train_engineer_list[self.train_counter - 1].setWindowTitle("Train Engineer " + str(self.train_counter))
        self.train_controller_list[self.train_counter - 1].show()
        self.train_engineer_list[self.train_counter - 1].show()
            
    def create_new_train_controller_and_engineer_ui(self, module: bool):
        doors = Doors()
        tuning = Tuning()
        brake_status = BrakeStatus(self.communicator)
        power_class = PowerCommand(brake_status, tuning, module)
        speed_control = SpeedControl(power_class, brake_status, self.communicator)
        failure_modes = FailureModes(speed_control, power_class)
        lights = Lights(speed_control)
        temperature = Temperature()
        position = Position(doors, failure_modes, speed_control, power_class, self.communicator, lights, brake_status, 'Green')
        
        train_controller_ui = TrainControllerUI(self.communicator, self.communicator2, doors, tuning, brake_status, power_class, speed_control, failure_modes, position, lights, temperature)
        train_engineer_ui = TrainEngineerUI(tuning, power_class)
        return train_controller_ui, train_engineer_ui
    
    
    ########################################################
    # IMPLEMENT READ/WRITE TRAIN CONTROLLER FUNCTIONS HERE #
    ########################################################
    
    def write_to_train_model(self):
        # Sending all as lists to the train model
        power_commands = [train_controller.power_class.power_command for train_controller in self.train_controller_list]
        self.communicator.power_command_signal.emit(power_commands)
        
        service_brake_commands = [train_controller.brake_class.driver_service_brake_command for train_controller in self.train_controller_list]
        manual_service_brake_commands = [train_controller.brake_class.manual_driver_service_brake_command for train_controller in self.train_controller_list]  
        service_brake_commands = [s or m for s, m in zip(service_brake_commands, manual_service_brake_commands)]
        self.communicator.service_brake_command_signal.emit(service_brake_commands)
        
        emergency_brake_commands = [train_controller.brake_class.driver_emergency_brake_command for train_controller in self.train_controller_list]
        manual_emergency_brake_commands = [train_controller.brake_class.manual_driver_emergency_brake_command for train_controller in self.train_controller_list]
        emergency_brake_commands = [e or m for e, m in zip(emergency_brake_commands, manual_emergency_brake_commands)]
        self.communicator.emergency_brake_command_signal.emit(emergency_brake_commands)
        
        desired_temperatures = [train_controller.temperature.desired_temperature for train_controller in self.train_controller_list]
        self.communicator.desired_temperature_signal.emit(desired_temperatures)
        
        exterior_lights = [train_controller.lights.exterior_lights for train_controller in self.train_controller_list]
        manual_exterior_lights = [train_controller.lights.manual_exterior_lights for train_controller in self.train_controller_list]
        exterior_lights = [e or m for e, m in zip(exterior_lights, manual_exterior_lights)]
        self.communicator.exterior_lights_signal.emit(exterior_lights)
        
        interior_lights = [train_controller.lights.interior_lights for train_controller in self.train_controller_list]
        manual_interior_lights = [train_controller.lights.manual_interior_lights for train_controller in self.train_controller_list]
        interior_lights = [m or il for m, il in zip(manual_interior_lights, interior_lights)]
        self.communicator.interior_lights_signal.emit(interior_lights)
        
        
        left_doors = [train_controller.doors.left_door for train_controller in self.train_controller_list]
        self.communicator.left_door_signal.emit(left_doors)
        
        right_doors = [train_controller.doors.right_door for train_controller in self.train_controller_list]
        self.communicator.right_door_signal.emit(right_doors)
        
        announcements = [train_controller.position.announcement for train_controller in self.train_controller_list]
        self.communicator.announcement_signal.emit(announcements)
        
    def read_from_train_model(self):
        self.communicator.commanded_speed_signal.connect(self.update_commanded_speed)
        self.communicator.commanded_authority_signal.connect(self.update_commanded_authority)
        self.communicator.current_velocity_signal.connect(self.update_current_velocity)
        self.communicator.engine_failure_signal.connect(self.update_engine_failure)
        self.communicator.brake_failure_signal.connect(self.update_brake_failure)
        self.communicator.signal_failure_signal.connect(self.update_signal_failure)
        self.communicator.passenger_brake_command_signal.connect(self.update_passenger_brake_command)
        self.communicator.actual_temperature_signal.connect(self.update_actual_temperature)
        self.communicator.polarity_signal.connect(self.update_polarity)
        
    def update_commanded_speed(self, commanded_speed: list):
        # print(f"Commanded Speed in Train Controller Shell: {commanded_speed}")
        if len(self.train_controller_list):
            if len(commanded_speed):
                for i in range(len(commanded_speed)):
                    if i < len(self.train_controller_list):
                        if commanded_speed[i] == 0:
                            self.train_controller_list[i].speed_control.handle_commanded_speed(0)
                        else:
                            self.train_controller_list[i].speed_control.handle_commanded_speed(commanded_speed[i])
                    # print(f"Commanded Speed {i + 1}: {commanded_speed}")
            
    def update_commanded_authority(self, commanded_authority: list):
        # print(f"Commanded Authority in Train Controller Shell: {commanded_authority}")
        if len(self.train_controller_list):
            if len(commanded_authority):
                for i in range(len(commanded_authority)):
                    if i < len(self.train_controller_list):
                        self.train_controller_list[i].position.handle_commanded_authority(commanded_authority[i])
                    # print(f"Commanded Authority {i + 1}: {commanded_authority}")
                    
    def update_current_velocity(self, current_velocity: list):
        if len(self.train_controller_list):
            for i in range(len(current_velocity)):
                if i < len(self.train_controller_list):
                    self.train_controller_list[i].speed_control.handle_current_velocity(current_velocity[i])
                # print(f"Current Velocity {i + 1}: {current_velocity}")

    def update_engine_failure(self, engine_failure: list):
        if len(self.train_controller_list):
            for i in range(len(engine_failure)):
                if i < len(self.train_controller_list):
                    self.train_controller_list[i].failure_modes.handle_engine_failure(engine_failure[i])
            # # print(f"Engine Failure: {engine_failure}")

    def update_brake_failure(self, brake_failure: list):
        if len(self.train_controller_list):
            for i in range(len(brake_failure)):
                if i < len(self.train_controller_list):
                    self.train_controller_list[i].failure_modes.handle_brake_failure(brake_failure[i])
            # # print(f"Brake Failure: {brake_failure}")

    def update_signal_failure(self, signal_failure: list):
        if len(self.train_controller_list):
            for i in range(len(signal_failure)):
                if i < len(self.train_controller_list):
                    self.train_controller_list[i].failure_modes.handle_signal_failure(signal_failure[i])
            # # print(f"Signal Failure: {signal_failure}")

    def update_passenger_brake_command(self, passenger_brake_command: list):
        if len(self.train_controller_list):
            for i in range(len(passenger_brake_command)):
                if i < len(self.train_controller_list):
                    self.train_controller_list[i].brake_class.handle_passenger_brake_command(passenger_brake_command[i])
                    if passenger_brake_command[i]:
                        self.train_controller_list[i].speed_control.desired_velocity = 0
            # # print(f"Passenger Brake Command: {passenger_brake_command}")

    def update_actual_temperature(self, actual_temperature: list):
        if len(self.train_controller_list):
            for i in range(len(actual_temperature)):
                if i < len(self.train_controller_list):
                    self.train_controller_list[i].temperature.current_temperature = actual_temperature[i]
                    self.train_controller_list[i].update_current_temp_display(actual_temperature[i])
                # print(f"Actual Temperature: {actual_temperature}")

    def update_polarity(self, polarity: list):
        # print(f"Polarity in Train Controller Shell = {polarity}")
        if len(self.train_controller_list):
            for i in range(len(polarity)):
                if i < len(self.train_controller_list):
                    self.train_controller_list[i].position.handle_polarity_change(polarity[i])
                ## print(f"Polarity: {polarity}")
  
# Add main function here
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     train_trainControllerComm = Communicate()
#     doors = Doors()
#     tuning = Tuning()
#     brake_status = BrakeStatus(train_trainControllerComm)
#     power_class = PowerCommand(brake_status, tuning)
#     speed_control = SpeedControl(power_class, brake_status, train_trainControllerComm)
#     failure_modes = FailureModes(speed_control, power_class)
#     lights = Lights(speed_control)
#     temperature = Temperature()
#     position = Position(doors, failure_modes, speed_control, power_class, train_trainControllerComm, lights, brake_status)
    
#     trainControllerUI = TrainControllerUI(train_trainControllerComm, doors, tuning, brake_status, power_class, speed_control, failure_modes, position, lights, temperature)

#     trainControllerShell = TrainControllerShell(train_trainControllerComm, trainControllerUI)
#     sys.exit(app.exec())