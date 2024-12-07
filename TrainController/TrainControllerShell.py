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
    def __init__(self, communicator: Communicate, trainControllerUI: TrainControllerUI, communicator2: ControllerToShellCommunicate):
        # Making a list of needed Train Controller UI instances
        self.train_controller_list: list[TrainControllerUI] = []
        self.train_engineer_list: list[TrainEngineerUI] = []
        
        # Setting up the parameters
        self.communicator = communicator
        self.communicator2 = communicator2
        # self.trainControllerUI = trainControllerUI
        
        # Initializing the variables needed
        self.counter = 0
        self.train_counter = 0
        self.current_train_id = 1
        self.train_count = 1
        self.previous_train_id = None
        self.total_train_id = None
        self.train_id_list = []
        self.total_commanded_authority = []
        self.previous_commanded_authority = []
        
        # Calling all of the necessary __init__ functions
        # self.create_and_add_train_controller_and_engineer_ui()
        # self.connect_signals_and_update_UI()
        self.communicator.train_count_signal.connect(self.handle_train_id)
        # self.communicator2.selected_train_id.connect(self.handle_selected_train_id)
        self.read_from_train_model()
        self.connect_signals_and_update_UI()
        
    
    # EXPLANATION: Yes, even though the connect_signals_and_update_UI function is called only once during __init__, 
    # the handler functions connected to the signals will always operate with the current value
    # of any dependent variables at the time the signal is emitted.
    
    
    # EXPLANATION: Every time a signal is emitted, it will call the same instance of the handler function, 
    # but it will execute the code within that handler using the current state of the object, 
    # including any updated values of variables like current_train_id.
    
    def connect_signals_and_update_UI(self):
        if self.train_counter == len(self.train_controller_list):
            # print(f"Inside If Statement in connect_signals_and_update_UI function - Train Counter: {self.train_counter}")   # This works
            # for train_controller in self.train_controller_list:
            for i in range(len(self.train_controller_list)):
    
                # ALL OF THE VALUES ARE ONLY ONE (NOT A LIST)
                self.train_controller_list[i].speed_control.current_velocity_signal.connect(self.handle_current_speed)
                self.train_controller_list[i].speed_control.commanded_speed_signal.connect(self.handle_commanded_speed)
                self.train_controller_list[i].position.commanded_authority_signal.connect(self.handle_commanded_authority)
                self.train_controller_list[i].temperature.current_temperature_signal.connect(self.handle_current_temperature)
                self.train_controller_list[i].failure_modes.engine_failure_signal.connect(self.handle_engine_failure_status)
                self.train_controller_list[i].failure_modes.brake_failure_signal.connect(self.handle_brake_failure_status)
                self.train_controller_list[i].failure_modes.signal_failure_signal.connect(self.handle_signal_failure_status)
                self.train_controller_list[i].power_class.power_command_signal.connect(self.handle_power_command)
                self.train_controller_list[i].lights.exterior_lights_signal.connect(self.handle_exterior_lights)
                self.train_controller_list[i].lights.interior_lights_signal.connect(self.handle_interior_lights)
                self.train_controller_list[i].doors.left_door_update.connect(self.handle_left_door)
                self.train_controller_list[i].doors.right_door_update.connect(self.handle_right_door)
                self.train_controller_list[i].brake_class.driver_brake_signal.connect(self.handle_driver_brake_status)
                self.train_controller_list[i].brake_class.service_brake_signal.connect(self.handle_service_brake_status)
                self.train_controller_list[i].brake_class.manual_service_brake_signal.connect(self.handle_service_brake_status)
                self.train_controller_list[i].brake_class.emergency_brake_signal.connect(self.handle_emergency_brake_status)
                self.train_controller_list[i].brake_class.passenger_brake_command_signal.connect(self.handle_passenger_brake_status)
    
            # self.train_controller_list[self.current_train_id - 1].train_id_signal.connect(self.handle_train_id)
    
            # Making sure to update UI
            # self.update_UI()
          
    def update_UI(self):
        # print("Update UI Function Called")
        if self.train_counter == len(self.train_controller_list):
            for train_controller in self.train_controller_list:
                pass
                # train_controller.update_current_speed(train_controller.speed_control.current_velocity)
                # train_controller.update_commanded_speed(train_controller.speed_control.commanded_speed)
                # train_controller.update_commanded_authority(train_controller.position.commanded_authority)
                # train_controller.update_power_command(train_controller.power_class.power_command)
                # train_controller.update_engine_failure_status(train_controller.failure_modes.engine_fail)
                # train_controller.update_brake_failure_status(train_controller.failure_modes.brake_fail)
                # train_controller.update_signal_failure_status(train_controller.failure_modes.signal_fail)
                # train_controller.update_service_brake_status(train_controller.brake_class.driver_service_brake_command)
                # train_controller.update_emergency_brake_status(train_controller.brake_class.driver_emergency_brake_command)
                # train_controller.update_current_temperature(train_controller.temperature.current_temperature)
                # train_controller.update_exterior_lights(train_controller.lights.exterior_lights)
                # train_controller.update_interior_lights(train_controller.lights.interior_lights)
                # train_controller.update_left_door(train_controller.doors.left_door)
                # train_controller.update_right_door(train_controller.doors.right_door)
                # train_controller.update_driver_brake_status(train_controller.brake_class.driver_brake_status)
                # train_controller.update_passenger_brake_status(train_controller.brake_class.passenger_brake)
            # self.write_to_train_model()
        

    ############################
    # TRAIN ID HANDLE FROM CTC #
    ############################
    
    def handle_selected_train_id(self, selected_train_id: int):
        
        # WHEN ANOTHER TRAIN IS SELECTED IN THE DROPDOWN, THE CURRENT VALUES ARE FROZEN AND DO NOT CHANGE UNTIL I GO BACK TO THE INITIAL TRAIN
        
        self.current_train_id = selected_train_id
        # self.trainControllerUI = self.train_controller_list[self.current_train_id - 1]
        self.connect_signals_and_update_UI()
        # self.update_UI()
        
    def handle_train_id(self, train_id: int):
        if train_id != 0:
            self.previous_train_id = self.total_train_id
            self.total_train_id = train_id
            if self.total_train_id != self.previous_train_id:
                # print(f"Train ID: {train_id}")
                self.train_id_list.append(train_id)
                # print("Updated Train ID List Emitted")
                
                
                # Need a list of train ids to keep track of the number of trains on track. eg. [0, 1, 2] means there are 3 trains on track
                # This list should be sent to the TrainControllerUI everytime it is updated to update the dropdown options
                # Use the index of the selected train id in the dropdown in the train id list in order to index all of the variables eg. this value should be the current_train_id value
                # The TrainControllerShell should also have a signal that sends the selected train id to the TrainControllerUI to update the UI with the corresponding train controller values
                # When a train arrives back to the yard and is removed, then the train id should be removed from the list and the train controller/engineer UI should be removed from the list in order to align the train id list with the number of trains on track
                
                
                # Connect signals function shold have that for-loop and within the handle functions, the update_UI function should be called
                
                # if len(self.train_controller_list) > 0:
                #     self.no_read_from_train_model()
                #     print("No Read from Train Model")
                
                if train_id > len(self.train_controller_list):
                    self.counter += 1
                    self.train_counter += 1
                    
                    
                    ##########################################################################################################
                    # ERROR: WHEN THE SECOND TRAIN IS DISPATCHED, THE TRAIN CONTROLLER LIST IS NOT GETTING APPENDED PROPERLY #
                    ##########################################################################################################
                    # Problem is with the read_from_train_model function. It is not updating the corrent number of trains on track
                    
                    # Want Software for all trains except for the second train dispatched
                    # if self.counter != 2:
                    self.create_and_add_train_controller_and_engineer_ui(True)
                    # if not QApplication.instance():
                    # app = QApplication(sys.argv)
                    
                    # sys.exit(app.exec())
                    # self.current_train_id = train_id
                    # self.update_signal_connections()  # Connect Signals for smaller classes from the TrainControllerUI file
                    # print(f"Train ID List: {self.train_id_list}")
                    # self.communicator2.train_id_list.emit(self.train_id_list)
                        
                    # Only want Hardware for second Train that was dispatched
                    # elif self.counter == 2:
                    #     self.create_and_add_train_controller_and_engineer_ui(False)
                    #     # self.current_train_id = train_id
                    #     self.connect_signals_and_update_UI()
                    #     self.read_from_train_model() 
                    #     print(f"Train ID List: {self.train_id_list}")
                    #     self.communicator2.train_id_list.emit(self.train_id_list)
                elif train_id < len(self.train_controller_list):
                    self.train_counter -= 1
                    self.remove_train_controller_and_engineer_ui(self.train_controller_list[0], self.train_engineer_list[0])
                    # self.read_from_train_model()
                    


                # BEFORE:
                # # print(f"Train ID: {train_id}")
                # self.current_train_id = train_id
                
                # Set self.trainControllerUI to the current train controller UI in the list
                if self.train_controller_list and train_id == 1:
                    self.trainControllerUI = self.train_controller_list[self.current_train_id - 1]
                    self.connect_signals_and_update_UI()
                    
                # self.update_UI()    
                # self.connect_signals_and_update_UI()
            
        
    ###########################################################
    # IMPLEMENT ADD/REMOVE TRAIN CONTROLLER UI FUNCTIONS HERE #
    ###########################################################

    def remove_train_controller_and_engineer_ui(self, train_controller_ui: TrainControllerUI, train_engineer_ui: TrainEngineerUI):
        if train_controller_ui in self.train_controller_list and train_engineer_ui in self.train_engineer_list:
            self.train_controller_list.remove(train_controller_ui)
            self.train_engineer_list.remove(train_engineer_ui)
            self.train_id_list.pop(0)
            self.connect_signals_and_update_UI()
            # self.update_UI()
            
            # self.update_signal_connections()
            # self.read_from_train_model()
            self.communicator2.train_id_list.emit(self.train_id_list)

    def create_and_add_train_controller_and_engineer_ui(self, module: bool):
        new_train_controller_ui, new_train_engineer_ui = self.create_new_train_controller_and_engineer_ui(module)
        self.train_controller_list.append(new_train_controller_ui)
        # print(f"Size of Train Controller List: {len(self.train_controller_list)}")
        self.train_engineer_list.append(new_train_engineer_ui)
        self.train_controller_list[self.train_counter - 1].show()
        self.train_engineer_list[self.train_counter - 1].show()
        QApplication.processEvents()
        self.connect_signals_and_update_UI()
        # self.update_UI()
        
        # self.read_from_train_model()
        # self.update_signal_connections()
        # if self.counter == 1:
        # new_train_controller_ui.show()
        # new_train_engineer_ui.show()
            
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
        
    # def no_read_from_train_model(self):
    #     self.communicator.commanded_speed_signal.disconnect(self.update_commanded_speed)
    #     self.communicator.commanded_authority_signal.disconnect(self.update_commanded_authority)
    #     self.communicator.current_velocity_signal.disconnect(self.update_current_velocity)
    #     self.communicator.engine_failure_signal.disconnect(self.update_engine_failure)
    #     self.communicator.brake_failure_signal.disconnect(self.update_brake_failure)
    #     self.communicator.signal_failure_signal.disconnect(self.update_signal_failure)
    #     self.communicator.passenger_brake_command_signal.disconnect(self.update_passenger_brake_command)
    #     self.communicator.actual_temperature_signal.disconnect(self.update_actual_temperature)
    #     self.communicator.polarity_signal.disconnect(self.update_polarity)
    #     # self.communicator.train_count_signal.disconnect(self.update_train_count)
        
    def update_commanded_speed(self, commanded_speed: list):
        # For all Trains - WORKS
        print(f"Commanded Speed in Train Controller Shell = {commanded_speed}")
        if len(self.train_controller_list):
            if len(commanded_speed):
                for i in range(len(commanded_speed)):
                    if i < len(self.train_controller_list):
                        # print(f"Index: {i}")
                        if commanded_speed[i] == 0:
                            self.train_controller_list[i].speed_control.handle_commanded_speed(30)
                        else:
                            self.train_controller_list[i].speed_control.handle_commanded_speed(commanded_speed[i])
                    
                    for i in range(len(self.train_controller_list)):
                        pass
                        # print(f"Commanded Speed {i + 1}: {self.train_controller_list[i].speed_control.commanded_speed}")
        
        
        
        # BEFORE:
        # print(f"Commanded Speed in shell class: {commanded_speed}")
        # if len(commanded_speed):
        #     if commanded_speed[0] == 0:
        #         self.train_controller_list[0].speed_control.handle_commanded_speed(0)
        #     else:
        #         for i in range(len(commanded_speed)):
        #             self.train_controller_list[0].speed_control.handle_commanded_speed(commanded_speed[0])
        #             # # print(f"Commanded Speed: {commanded_speed[i]}")

    def update_commanded_authority(self, commanded_authority: list):
        # I THINK THIS IS CORRECT                 
        if len(self.train_controller_list):
            if len(commanded_authority):
                for i in range(len(commanded_authority)):
                    if i < len(self.train_controller_list):
                        # print(f"Index: {i}")
                        self.train_controller_list[i].position.handle_commanded_authority(commanded_authority[i])
                    
                    # for i in range(len(self.train_controller_list)):
                    #     pass
                    #     # print(f"Commanded Speed {i + 1}: {self.train_controller_list[i].speed_control.commanded_speed}")
        
        
        # self.previous_commanded_authority = self.total_commanded_authority.copy()
        # self.total_commanded_authority = commanded_authority.copy()    # current c_auth
        # print(f"Commanded Authority in Train Controller Shell = {commanded_authority}")
        
        # if len(self.train_controller_list):
        #     # For all Trains - WORKS
        #     if len(self.total_commanded_authority):
        #         # Subsequent times the commanded authority is received
        #         if len(self.previous_commanded_authority):
        #             for i in range(len(self.total_commanded_authority)):
        #                 if i < len(self.train_controller_list):
        #                     if self.total_commanded_authority[i] != self.previous_commanded_authority[i]:
        #                         # print(f"Commanded Authority {i + 1}: {self.total_commanded_authority[i]}")
        #                         self.train_controller_list[i].position.handle_commanded_authority(commanded_authority[i])
                                
        #         # First time the commanded authority is received
        #         else:
        #             if len(self.train_controller_list):
        #                 for i in range(len(self.total_commanded_authority)):
        #                     if i < len(self.train_controller_list):
        #                         # print(f"Commanded Authority {i + 1}: {self.total_commanded_authority[i]}")
        #                         self.train_controller_list[i].position.handle_commanded_authority(commanded_authority[i])
               
        
        # BEFORE:
        # if len(self.total_commanded_authority):
        #     if len(self.previous_commanded_authority):
        #         if self.total_commanded_authority[0] != self.previous_commanded_authority[0]:
        #             for j in range(len(self.total_commanded_authority)):
        #                 self.train_controller_list[0].position.handle_commanded_authority(commanded_authority[0])
        #     else:
        #         self.train_controller_list[0].position.handle_commanded_authority(commanded_authority[0])
        
    # def update_commanded_authority(self, commanded_authority: list):
    #     self.previous_commanded_authority = self.total_commanded_authority.copy()
    #     self.total_commanded_authority = commanded_authority.copy()  # Current commanded authority
    #     print(f"Commanded Authority in Train Controller Shell = {commanded_authority}")
        
    #     # Initialize tracking list if not already done
    #     if not hasattr(self, 'processed_indices'):
    #         self.processed_indices = [False] * len(self.train_controller_list)
        
    #     if len(self.train_controller_list):
    #         for i in range(len(self.total_commanded_authority)):
    #             if i < len(self.train_controller_list):
    #                 # Check if this index has already been processed
    #                 if not self.processed_indices[i] and self.total_commanded_authority[i] is not None:
    #                     # Process this index for the first time
    #                     self.train_controller_list[i].position.handle_commanded_authority(self.total_commanded_authority[i])
    #                     self.processed_indices[i] = True  # Mark as processed


    def update_current_velocity(self, current_velocity: list):
        if len(self.train_controller_list):
            for i in range(len(current_velocity)):
                if i < len(self.train_controller_list):
                    self.train_controller_list[i].speed_control.handle_current_velocity(current_velocity[i])
                    # print(f"Current Velocity {i + 1}: {current_velocity[i]}")
                # print(f"Current Velocity { i + 1}: {current_velocity}")

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
                    self.train_controller_list[i].temperature.update_current_temp_display(actual_temperature[i])
        # print(f"Actual Temperature: {actual_temperature}")

    def update_polarity(self, polarity: list):
        if len(self.train_controller_list):
            for i in range(len(polarity)):
                if i < len(self.train_controller_list):
                    self.train_controller_list[i].position.handle_polarity_change(polarity[i])
                ## print(f"Polarity: {polarity}")

    # def update_train_count(self, train_count: int):
    #     if self.train_count > train_count:
    #         self.remove_train_controller_and_engineer_ui(self.train_controller_list[0], self.train_engineer_list[0])
    #         # # print(f"Train count decreased to {train_count}")
    #     elif self.train_count < train_count:
    #         self.create_and_add_train_controller_and_engineer_ui()
    #         # # print(f"Train count increased to {train_count}")
    #     self.train_count = train_count
            
    #     self.train_count = train_count
        
        
    ################################################################
    # IMPLEMENT CONNECT UI CHANGES TRAIN CONTROLLER FUNCTIONS HERE #
    ################################################################
        
    def handle_commanded_speed(self, commanded_speed: float):
        if self.train_controller_list:
            for i in range(len(self.train_controller_list)):
                if self.train_counter == len(self.train_controller_list):
                    self.train_controller_list[self.train_counter - 1].update_commanded_speed(commanded_speed)
                    # self.update_UI()
                    self.train_controller_list[self.train_counter - 1].speed_control.commanded_speed = commanded_speed

    def handle_commanded_authority(self, commanded_authority: float):
        if self.train_controller_list:
            for i in range(len(self.train_controller_list)):
                if self.train_counter == len(self.train_controller_list):
                    self.train_controller_list[self.train_counter - 1].update_commanded_authority(commanded_authority)
                    # self.update_UI()
                    self.train_controller_list[self.train_counter - 1].position.commanded_authority = commanded_authority

    def handle_current_temperature(self, current_temperature: float):
        if self.train_controller_list:
            for i in range(len(self.train_controller_list)):
                if self.train_counter == len(self.train_controller_list):
                    self.train_controller_list[self.train_counter - 1].update_current_temperature(current_temperature)
                    # self.update_UI()
                    self.train_controller_list[self.train_counter - 1].temperature.current_temperature = current_temperature

    def handle_engine_failure_status(self, engine_failure: bool):
        if self.train_controller_list:
            for i in range(len(self.train_controller_list)):
                if self.train_counter == len(self.train_controller_list):
                    self.train_controller_list[self.train_counter - 1].update_engine_failure_status(engine_failure)
                    # self.update_UI()
                    self.train_controller_list[self.train_counter - 1].failure_modes.engine_fail = engine_failure

    def handle_brake_failure_status(self, brake_failure: bool):
        if self.train_controller_list:
            for i in range(len(self.train_controller_list)):
                if self.train_counter == len(self.train_controller_list):
                    self.train_controller_list[self.train_counter - 1].update_brake_failure_status(brake_failure)
                    # self.update_UI()
                    self.train_controller_list[self.train_counter - 1].failure_modes.brake_fail = brake_failure

    def handle_signal_failure_status(self, signal_failure: bool):
        if self.train_controller_list:
            for i in range(len(self.train_controller_list)):
                if self.train_counter == len(self.train_controller_list):
                    self.train_controller_list[self.train_counter - 1].update_signal_failure_status(signal_failure)
                    # self.update_UI()
                    self.train_controller_list[self.train_counter - 1].failure_modes.signal_fail = signal_failure

    def handle_power_command(self, power_command: float):
        if self.train_controller_list:
            for i in range(len(self.train_controller_list)):
                if self.train_counter == len(self.train_controller_list):
                    self.train_controller_list[self.train_counter - 1].update_power_command(power_command)
                    # self.update_UI()
                    self.train_controller_list[self.train_counter - 1].power_class.power_command = power_command
                    # print(f"Power Command {i + 1}: {power_command}")

    def handle_exterior_lights(self, exterior_lights: bool):
        if self.train_controller_list:
            for i in range(len(self.train_controller_list)):
                if self.train_counter == len(self.train_controller_list):
                    self.train_controller_list[self.train_counter - 1].update_exterior_lights(exterior_lights)
                    # self.update_UI()
                    self.train_controller_list[self.train_counter - 1].lights.exterior_lights = exterior_lights

    def handle_interior_lights(self, interior_lights: bool):
        if self.train_controller_list:
            for i in range(len(self.train_controller_list)):
                if self.train_counter == len(self.train_controller_list):
                    self.train_controller_list[self.train_counter - 1].update_interior_lights(interior_lights)
                    # self.update_UI()
                    self.train_controller_list[self.train_counter - 1].lights.interior_lights = interior_lights

    def handle_left_door(self, left_door: bool):
        if self.train_controller_list:
            for i in range(len(self.train_controller_list)):
                if self.train_counter == len(self.train_controller_list):
                    self.train_controller_list[self.train_counter - 1].update_left_door(left_door)
                    # self.update_UI()
                    self.train_controller_list[self.train_counter - 1].doors.left_door = left_door

    def handle_right_door(self, right_door: bool):
        if self.train_controller_list:
            for i in range(len(self.train_controller_list)):
                if self.train_counter == len(self.train_controller_list):
                    self.train_controller_list[self.train_counter - 1].update_right_door(right_door)
                    # self.update_UI()
                    self.train_controller_list[self.train_counter - 1].doors.right_door = right_door

    def handle_driver_brake_status(self, driver_brake_status: bool):
        if self.train_controller_list:
            for i in range(len(self.train_controller_list)):
                if self.train_counter == len(self.train_controller_list):
                    self.train_controller_list[self.train_counter - 1].update_driver_brake_status(driver_brake_status)
                    # self.update_UI()
                    self.train_controller_list[self.train_counter - 1].brake_class.driver_brake_status = driver_brake_status

    def handle_service_brake_status(self, service_brake_status: bool):
        if self.train_controller_list:
            # print(f"Service Brake Status: {service_brake_status}")    # Displays True only once when it is pressed, but remains True until speed = 0 and then becomes False
            for i in range(len(self.train_controller_list)):
                if self.train_counter == len(self.train_controller_list):
                    self.train_controller_list[self.train_counter - 1].update_service_brake_status(service_brake_status)
                    # self.update_UI()
                    self.train_controller_list[self.train_counter - 1].brake_class.driver_service_brake_command = service_brake_status

    def handle_manual_service_brake_status(self, manual_service_brake_status: bool):
        if self.train_controller_list:
            for i in range(len(self.train_controller_list)):
                if self.train_counter == len(self.train_controller_list):
                    self.train_controller_list[self.train_counter - 1].update_manual_service_brake_status(manual_service_brake_status)
                    # self.update_UI()
                    self.train_controller_list[self.train_counter - 1].brake_class.manual_driver_service_brake_command = manual_service_brake_status

    def handle_emergency_brake_status(self, emergency_brake_status: bool):
        if self.train_controller_list:
            for i in range(len(self.train_controller_list)):
                if self.train_counter == len(self.train_controller_list):
                    self.train_controller_list[self.train_counter - 1].update_emergency_brake_status(emergency_brake_status)
                    # self.update_UI()
                    self.train_controller_list[self.train_counter - 1].brake_class.driver_emergency_brake_command = emergency_brake_status

    def handle_passenger_brake_status(self, passenger_brake_status: bool):
        if self.train_controller_list:
            for i in range(len(self.train_controller_list)):
                if self.train_counter == len(self.train_controller_list):
                    self.train_controller_list[self.train_counter - 1].update_passenger_brake_status(passenger_brake_status)
                    # self.update_UI()
                    self.train_controller_list[self.train_counter - 1].brake_class.passenger_brake = passenger_brake_status

    def handle_current_speed(self, current_speed: float):
        if self.train_controller_list:
            for i in range(len(self.train_controller_list)):
                if self.train_counter == len(self.train_controller_list):
                    self.train_controller_list[self.train_counter - 1].update_current_speed(current_speed)
                    # self.update_UI()
                    self.train_controller_list[self.train_counter - 1].speed_control.current_velocity = current_speed

    def handle_desired_temperature(self, desired_temperature: float):
        if self.train_controller_list:
            for i in range(len(self.train_controller_list)):
                if self.train_counter == len(self.train_controller_list):
                    self.train_controller_list[self.train_counter - 1].temperature.desired_temperature = desired_temperature
            
    # def handle_commanded_speed(self, commanded_speed: float):
    #     if self.train_controller_list:
    #         self.train_controller_list[self.current_train_id - 1].update_commanded_speed(commanded_speed)
    #         # self.update_UI()
    #         self.train_controller_list[self.current_train_id - 1].speed_control.commanded_speed = commanded_speed

    # def handle_commanded_authority(self, commanded_authority: float):
    #     if self.train_controller_list:
    #         self.train_controller_list[self.current_train_id - 1].update_commanded_authority(commanded_authority)
    #         # self.update_UI()
    #         self.train_controller_list[self.current_train_id - 1].position.commanded_authority = commanded_authority

    # def handle_current_temperature(self, current_temperature: float):
    #     if self.train_controller_list:
    #         self.train_controller_list[self.current_train_id - 1].update_current_temperature(current_temperature)
    #         # self.update_UI()
    #         self.train_controller_list[self.current_train_id - 1].temperature.current_temperature = current_temperature

    # def handle_engine_failure_status(self, engine_failure: bool):
    #     if self.train_controller_list:
    #         self.train_controller_list[self.current_train_id - 1].update_engine_failure_status(engine_failure)
    #         # self.update_UI()
    #         self.train_controller_list[self.current_train_id - 1].failure_modes.engine_fail = engine_failure

    # def handle_brake_failure_status(self, brake_failure: bool):
    #     if self.train_controller_list:
    #         self.train_controller_list[self.current_train_id - 1].update_brake_failure_status(brake_failure)
    #         # self.update_UI()
    #         self.train_controller_list[self.current_train_id - 1].failure_modes.brake_fail = brake_failure

    # def handle_signal_failure_status(self, signal_failure: bool):
    #     if self.train_controller_list:
    #         self.train_controller_list[self.current_train_id - 1].update_signal_failure_status(signal_failure)
    #         # self.update_UI()
    #         self.train_controller_list[self.current_train_id - 1].failure_modes.signal_fail = signal_failure

    # def handle_power_command(self, power_command: float):
    #     if self.train_controller_list:
    #         self.train_controller_list[self.current_train_id - 1].update_power_command(power_command)
    #         # self.update_UI()
    #         self.train_controller_list[self.current_train_id - 1].power_class.power_command = power_command

    # def handle_exterior_lights(self, exterior_lights: bool):
    #     if self.train_controller_list:
    #         self.train_controller_list[self.current_train_id - 1].update_exterior_lights(exterior_lights)
    #         # self.update_UI()
    #         self.train_controller_list[self.current_train_id - 1].lights.exterior_lights = exterior_lights

    # def handle_interior_lights(self, interior_lights: bool):
    #     if self.train_controller_list:
    #         self.train_controller_list[self.current_train_id - 1].update_interior_lights(interior_lights)
    #         # self.update_UI()
    #         self.train_controller_list[self.current_train_id - 1].lights.interior_lights = interior_lights

    # def handle_left_door(self, left_door: bool):
    #     if self.train_controller_list:
    #         self.train_controller_list[self.current_train_id - 1].update_left_door(left_door)
    #         # self.update_UI()
    #         self.train_controller_list[self.current_train_id - 1].doors.left_door = left_door

    # def handle_right_door(self, right_door: bool):
    #     if self.train_controller_list:
    #         self.train_controller_list[self.current_train_id - 1].update_right_door(right_door)
    #         # self.update_UI()
    #         self.train_controller_list[self.current_train_id - 1].doors.right_door = right_door

    # def handle_driver_brake_status(self, driver_brake_status: bool):
    #     if self.train_controller_list:
    #         self.train_controller_list[self.current_train_id - 1].update_driver_brake_status(driver_brake_status)
    #         # self.update_UI()
    #         self.train_controller_list[self.current_train_id - 1].brake_class.driver_brake_status = driver_brake_status

    # def handle_service_brake_status(self, service_brake_status: bool):
    #     if self.train_controller_list:
    #         # print(f"Service Brake Status: {service_brake_status}")    # Displays True only once when it is pressed, but remains True until speed = 0 and then becomes False
    #         self.train_controller_list[self.current_train_id - 1].update_service_brake_status(service_brake_status)
    #         # self.update_UI()
    #         self.train_controller_list[self.current_train_id - 1].brake_class.driver_service_brake_command = service_brake_status
            
    # def handle_manual_service_brake_status(self, manual_service_brake_status: bool):
    #     if self.train_controller_list:
    #         self.train_controller_list[self.current_train_id - 1].update_manual_service_brake_status(manual_service_brake_status)
    #         # self.update_UI()
    #         self.train_controller_list[self.current_train_id - 1].brake_class.manual_driver_service_brake_command = manual_service_brake_status

    # def handle_emergency_brake_status(self, emergency_brake_status: bool):
    #     if self.train_controller_list:
    #         self.train_controller_list[self.current_train_id - 1].update_emergency_brake_status(emergency_brake_status)
    #         # self.update_UI()
    #         self.train_controller_list[self.current_train_id - 1].brake_class.driver_emergency_brake_command = emergency_brake_status

    # def handle_passenger_brake_status(self, passenger_brake_status: bool):
    #     if self.train_controller_list:
    #         self.train_controller_list[self.current_train_id - 1].update_passenger_brake_status(passenger_brake_status)
    #         # self.update_UI()
    #         self.train_controller_list[self.current_train_id - 1].brake_class.passenger_brake = passenger_brake_status

    # def handle_current_speed(self, current_speed: float):
    #     if self.train_controller_list:
    #         self.train_controller_list[self.current_train_id - 1].update_current_speed(current_speed)
    #         # self.update_UI()
    #         self.train_controller_list[self.current_train_id - 1].speed_control.current_velocity = current_speed

    # def handle_desired_temperature(self, desired_temperature: float):
    #     if self.train_controller_list:
    #         self.train_controller_list[self.current_train_id - 1].temperature.desired_temperature = desired_temperature
        
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