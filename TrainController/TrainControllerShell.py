import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from TrainController.TrainController import *
import os
from PyQt6.QtWidgets import QApplication

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Resources.TrainTrainControllerComm import TrainTrainController as Communicate

class TrainControllerShell:
    def __init__(self, communicator: Communicate, trainControllerUI: TrainControllerUI):
        # Making a list of needed Train Controller UI instances
        self.train_controller_list: list[TrainControllerUI] = []
        self.train_engineer_list: list[TrainEngineerUI] = []
        
        # Setting up the parameters
        self.communicator = communicator
        self.trainControllerUI = trainControllerUI
        
        # Initializing the variables needed
        self.current_train_id = 1
        self.train_count = 1
        
        # Calling all of the necessary __init__ functions
        self.create_and_add_train_controller_and_engineer_ui()
        self.connect_signals()
        # self.communicator.train_count_signal.connect(self.handle_train_id)
        self.read_from_train_model()
        
        
    
    def connect_signals(self):
        for train_controller in self.train_controller_list:
            train_controller.speed_control.current_velocity_signal.connect(self.handle_current_speed)
            train_controller.speed_control.commanded_speed_signal.connect(self.handle_commanded_speed)
            train_controller.position.commanded_authority_signal.connect(self.handle_commanded_authority)
            train_controller.temperature.current_temperature_signal.connect(self.handle_current_temperature)
            train_controller.failure_modes.engine_failure_signal.connect(self.handle_engine_failure_status)
            train_controller.failure_modes.brake_failure_signal.connect(self.handle_brake_failure_status)
            train_controller.failure_modes.signal_failure_signal.connect(self.handle_signal_failure_status)
            train_controller.power_class.power_command_signal.connect(self.handle_power_command)
            train_controller.lights.exterior_lights_signal.connect(self.handle_exterior_lights)
            train_controller.lights.interior_lights_signal.connect(self.handle_interior_lights)
            train_controller.doors.left_door_update.connect(self.handle_left_door)
            train_controller.doors.right_door_update.connect(self.handle_right_door)
            train_controller.brake_class.driver_brake_signal.connect(self.handle_driver_brake_status)
            train_controller.brake_class.service_brake_signal.connect(self.handle_service_brake_status)
            train_controller.brake_class.emergency_brake_signal.connect(self.handle_emergency_brake_status)
            train_controller.brake_class.passenger_brake_command_signal.connect(self.handle_passenger_brake_status)
            
        # self.train_controller_list[self.current_train_id - 1].train_id_signal.connect(self.handle_train_id)
            
        # Making sure to update UI
        # self.update_UI()
          
    def update_UI(self):
        # This function should be using the trainControllerUI instance to update the UI
        self.trainControllerUI.update_current_speed(self.train_controller_list[self.current_train_id - 1].speed_control.current_velocity)
        self.trainControllerUI.update_commanded_speed(self.train_controller_list[self.current_train_id - 1].speed_control.commanded_speed)
        self.trainControllerUI.update_commanded_authority(self.train_controller_list[self.current_train_id - 1].position.commanded_authority)
        self.trainControllerUI.update_power_command(self.train_controller_list[self.current_train_id - 1].power_class.power_command)
        self.trainControllerUI.update_engine_failure_status(self.train_controller_list[self.current_train_id - 1].failure_modes.engine_fail)
        self.trainControllerUI.update_brake_failure_status(self.train_controller_list[self.current_train_id - 1].failure_modes.brake_fail)
        self.trainControllerUI.update_signal_failure_status(self.train_controller_list[self.current_train_id - 1].failure_modes.signal_fail)
        self.trainControllerUI.update_service_brake_status(self.train_controller_list[self.current_train_id - 1].brake_class.driver_service_brake_command)
        self.trainControllerUI.update_emergency_brake_status(self.train_controller_list[self.current_train_id - 1].brake_class.driver_emergency_brake_command)
        self.trainControllerUI.update_current_temperature(self.train_controller_list[self.current_train_id - 1].temperature.current_temperature)
        self.trainControllerUI.update_exterior_lights(self.train_controller_list[self.current_train_id - 1].lights.exterior_lights)
        self.trainControllerUI.update_interior_lights(self.train_controller_list[self.current_train_id - 1].lights.interior_lights)
        self.trainControllerUI.update_left_door(self.train_controller_list[self.current_train_id - 1].doors.left_door)
        self.trainControllerUI.update_right_door(self.train_controller_list[self.current_train_id - 1].doors.right_door)
        self.trainControllerUI.update_driver_brake_status(self.train_controller_list[self.current_train_id - 1].brake_class.driver_brake_status)
        self.trainControllerUI.update_passenger_brake_status(self.train_controller_list[self.current_train_id - 1].brake_class.passenger_brake)
        # self.write_to_train_model()
        
    
    ############################
    # TRAIN ID HANDLE FROM CTC #
    ############################
        
    def handle_train_id(self, train_id: int):
        print(f"Train ID: {train_id}")
        self.current_train_id = train_id
        
        # Set self.trainControllerUI to the current train controller UI in the list
        self.trainControllerUI = self.train_controller_list[self.current_train_id - 1]
        # self.update_UI()
        # self.connect_signals()
        
        
    ###########################################################
    # IMPLEMENT ADD/REMOVE TRAIN CONTROLLER UI FUNCTIONS HERE #
    ###########################################################

    def remove_train_controller_and_engineer_ui(self, train_controller_ui: TrainControllerUI, train_engineer_ui: TrainEngineerUI):
        if train_controller_ui in self.train_controller_list and train_engineer_ui in self.train_engineer_list:
            self.train_controller_list.remove(train_controller_ui)
            self.train_engineer_list.remove(train_engineer_ui)

    def create_and_add_train_controller_and_engineer_ui(self):
        new_train_controller_ui, new_train_engineer_ui = self.create_new_train_controller_and_engineer_ui()
        self.train_controller_list.append(new_train_controller_ui)
        self.train_engineer_list.append(new_train_engineer_ui)
        if len(self.train_controller_list) == 1:
            new_train_controller_ui.show()
            new_train_engineer_ui.show()
            
    def create_new_train_controller_and_engineer_ui(self):
        doors = Doors()
        tuning = Tuning()
        brake_status = BrakeStatus(self.communicator)
        power_class = PowerCommand(brake_status, tuning)
        speed_control = SpeedControl(power_class, brake_status, self.communicator)
        failure_modes = FailureModes(speed_control, power_class)
        lights = Lights(speed_control)
        temperature = Temperature()
        position = Position(doors, failure_modes, speed_control, power_class, self.communicator, lights)
        
        train_controller_ui = TrainControllerUI(self.communicator, doors, tuning, brake_status, power_class, speed_control, failure_modes, position, lights, temperature)
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
        self.communicator.service_brake_command_signal.emit(service_brake_commands)
        
        emergency_brake_commands = [train_controller.brake_class.driver_emergency_brake_command for train_controller in self.train_controller_list]
        self.communicator.emergency_brake_command_signal.emit(emergency_brake_commands)
        
        desired_temperatures = [train_controller.temperature.desired_temperature for train_controller in self.train_controller_list]
        self.communicator.desired_temperature_signal.emit(desired_temperatures)
        
        exterior_lights = [train_controller.lights.exterior_lights for train_controller in self.train_controller_list]
        self.communicator.exterior_lights_signal.emit(exterior_lights)
        
        interior_lights = [train_controller.lights.interior_lights for train_controller in self.train_controller_list]
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
        # self.communicator.train_count_signal.connect(self.update_train_count)
        
    def update_commanded_speed(self, commanded_speed: list):
        for i in range(len(commanded_speed)):
            self.train_controller_list[i].speed_control.handle_commanded_speed(commanded_speed[i])
            print(f"Commanded Speed: {commanded_speed[i]}")

    def update_commanded_authority(self, commanded_authority: list):
        for i in range(len(commanded_authority)):
            self.train_controller_list[i].position.handle_commanded_authority(commanded_authority[i])
        print(f"Commanded Authority: {commanded_authority}")

    def update_current_velocity(self, current_velocity: list):
        for i in range(len(current_velocity)):
            self.train_controller_list[i].speed_control.handle_current_velocity(current_velocity[i])
        print(f"Current Velocity: {current_velocity}")

    def update_engine_failure(self, engine_failure: list):
        for i in range(len(engine_failure)):
            self.train_controller_list[i].failure_modes.handle_engine_failure(engine_failure[i])
        print(f"Engine Failure: {engine_failure}")

    def update_brake_failure(self, brake_failure: list):
        for i in range(len(brake_failure)):
            self.train_controller_list[i].failure_modes.handle_brake_failure(brake_failure[i])
        print(f"Brake Failure: {brake_failure}")

    def update_signal_failure(self, signal_failure: list):
        for i in range(len(signal_failure)):
            self.train_controller_list[i].failure_modes.handle_signal_failure(signal_failure[i])
        print(f"Signal Failure: {signal_failure}")

    def update_passenger_brake_command(self, passenger_brake_command: list):
        for i in range(len(passenger_brake_command)):
            self.train_controller_list[i].brake_class.handle_passenger_brake_command(passenger_brake_command[i])
        print(f"Passenger Brake Command: {passenger_brake_command}")

    def update_actual_temperature(self, actual_temperature: list):
        # for i in range(len(actual_temperature)):
        #     self.train_controller_list[i].temperature.update_current_temp_display(actual_temperature[i])
        print(f"Actual Temperature: {actual_temperature}")

    def update_polarity(self, polarity: list):
        for i in range(len(polarity)):
            self.train_controller_list[i].position.handle_polarity_change(polarity[i])
        print(f"Polarity: {polarity}")

    # def update_train_count(self, train_count: int):
    #     if self.train_count > train_count:
    #         self.remove_train_controller_and_engineer_ui(self.train_controller_list[0], self.train_engineer_list[0])
    #         print(f"Train count decreased to {train_count}")
    #     elif self.train_count < train_count:
    #         self.create_and_add_train_controller_and_engineer_ui()
    #         print(f"Train count increased to {train_count}")
    #     self.train_count = train_count
            
    #     self.train_count = train_count
        
        
    ################################################################
    # IMPLEMENT CONNECT UI CHANGES TRAIN CONTROLLER FUNCTIONS HERE #
    ################################################################
        
    def handle_commanded_speed(self, commanded_speed: float):
        if self.train_controller_list:
            self.train_controller_list[self.current_train_id - 1].update_commanded_speed(commanded_speed)
            self.train_controller_list[self.current_train_id - 1].speed_control.commanded_speed = commanded_speed

    def handle_commanded_authority(self, commanded_authority: float):
        if self.train_controller_list:
            self.train_controller_list[self.current_train_id - 1].update_commanded_authority(commanded_authority)
            self.train_controller_list[self.current_train_id - 1].position.commanded_authority = commanded_authority

    def handle_current_temperature(self, current_temperature: float):
        if self.train_controller_list:
            self.train_controller_list[self.current_train_id - 1].update_current_temperature(current_temperature)
            self.train_controller_list[self.current_train_id - 1].temperature.current_temperature = current_temperature

    def handle_engine_failure_status(self, engine_failure: bool):
        if self.train_controller_list:
            self.train_controller_list[self.current_train_id - 1].update_engine_failure_status(engine_failure)
            self.train_controller_list[self.current_train_id - 1].failure_modes.engine_fail = engine_failure

    def handle_brake_failure_status(self, brake_failure: bool):
        if self.train_controller_list:
            self.train_controller_list[self.current_train_id - 1].update_brake_failure_status(brake_failure)
            self.train_controller_list[self.current_train_id - 1].failure_modes.brake_fail = brake_failure

    def handle_signal_failure_status(self, signal_failure: bool):
        if self.train_controller_list:
            self.train_controller_list[self.current_train_id - 1].update_signal_failure_status(signal_failure)
            self.train_controller_list[self.current_train_id - 1].failure_modes.signal_fail = signal_failure

    def handle_power_command(self, power_command: float):
        # if self.train_controller_list:
            # power_commands = [train_controller.power_class.power_command for train_controller in self.train_controller_list]
            # self.communicator.power_command_signal.emit(power_commands)
        self.train_controller_list[self.current_train_id - 1].update_power_command(power_command)
        # self.train_controller_list[self.current_train_id - 1].power_class.power_command = power_command

    def handle_exterior_lights(self, exterior_lights: bool):
        if self.train_controller_list:
            self.train_controller_list[self.current_train_id - 1].update_exterior_lights(exterior_lights)
            self.train_controller_list[self.current_train_id - 1].lights.exterior_lights = exterior_lights

    def handle_interior_lights(self, interior_lights: bool):
        if self.train_controller_list:
            self.train_controller_list[self.current_train_id - 1].update_interior_lights(interior_lights)
            self.train_controller_list[self.current_train_id - 1].lights.interior_lights = interior_lights

    def handle_left_door(self, left_door: bool):
        if self.train_controller_list:
            self.train_controller_list[self.current_train_id - 1].update_left_door(left_door)
            self.train_controller_list[self.current_train_id - 1].doors.left_door = left_door

    def handle_right_door(self, right_door: bool):
        if self.train_controller_list:
            self.train_controller_list[self.current_train_id - 1].update_right_door(right_door)
            self.train_controller_list[self.current_train_id - 1].doors.right_door = right_door

    def handle_driver_brake_status(self, driver_brake_status: bool):
        if self.train_controller_list:
            self.train_controller_list[self.current_train_id - 1].update_driver_brake_status(driver_brake_status)
            self.train_controller_list[self.current_train_id - 1].brake_class.driver_brake_status = driver_brake_status

    def handle_service_brake_status(self, service_brake_status: bool):
        if self.train_controller_list:
            self.train_controller_list[self.current_train_id - 1].update_service_brake_status(service_brake_status)
            self.train_controller_list[self.current_train_id - 1].brake_class.driver_service_brake_command = service_brake_status

    def handle_emergency_brake_status(self, emergency_brake_status: bool):
        if self.train_controller_list:
            self.train_controller_list[self.current_train_id - 1].update_emergency_brake_status(emergency_brake_status)
            self.train_controller_list[self.current_train_id - 1].brake_class.driver_emergency_brake_command = emergency_brake_status

    def handle_passenger_brake_status(self, passenger_brake_status: bool):
        if self.train_controller_list:
            self.train_controller_list[self.current_train_id - 1].update_passenger_brake_status(passenger_brake_status)
            self.train_controller_list[self.current_train_id - 1].brake_class.passenger_brake = passenger_brake_status

    def handle_current_speed(self, current_speed: float):
        if self.train_controller_list:
            self.train_controller_list[self.current_train_id - 1].update_current_speed(current_speed)
            self.train_controller_list[self.current_train_id - 1].speed_control.current_velocity = current_speed

    def handle_desired_temperature(self, desired_temperature: float):
        if self.train_controller_list:
            self.train_controller_list[self.current_train_id - 1].temperature.desired_temperature = desired_temperature
        
        
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
#     position = Position(doors, failure_modes, speed_control, power_class, train_trainControllerComm, lights)
    
#     trainControllerUI = TrainControllerUI(train_trainControllerComm, doors, tuning, brake_status, power_class, speed_control, failure_modes, position, lights, temperature)

#     trainControllerShell = TrainControllerShell(train_trainControllerComm, trainControllerUI)
#     sys.exit(app.exec())