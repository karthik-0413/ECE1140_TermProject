from TrainControllerUIClasses import *
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Resources.TrainTrainControllerComm import TrainTrainController as Communicate

class TrainControllerShell:
    def __init__(self, communicator: Communicate, trainControllerUI: TrainControllerUI):
        # Making a list of needed Train Controller UI instances
        self.train_controller_list: list[TrainControllerUI] = []
        self.engineer_controller_list: list[TrainEngineerUI] = []
        
        # Setting up the parameters
        self.communicator = communicator
        self.trainControllerUI = trainControllerUI
        # self.trainControllerUI.show()
        
        # Initializing the variables needed
        self.current_train_id = 1
        self.train_count = 2
        
        # Calling all of the necessary __init__ functions
        self.read_from_train_model()
        self.create_and_add_train_controller_ui()
        self.create_and_add_train_controller_ui()
        self.train_controller_list[self.current_train_id - 1].train_id_signal.emit(self.handle_train_id)
        
    
    
    #######################
    # QUESTIONS TO ANSWER #
    #######################
    # 1. Is the connect_signals function supposed to only handle one TrainController instance or all of them?
    # 2. Is the update_UI function supposed to be trainControllerUI or train_controller_list? - I set self.trainControllerUI = self.train_controller_list[self.current_train_id - 1]
    
    
    
    def connect_signals(self):
        self.trainControllerUI.speed_control.current_velocity_signal.connect(self.update_current_speed)
        self.trainControllerUI.speed_control.commanded_speed_signal.connect(self.update_commanded_speed)
        self.trainControllerUI.position.commanded_authority_signal.connect(self.update_commanded_authority)
        self.trainControllerUI.temperature.current_temperature_signal.connect(self.update_current_temperature)
        self.trainControllerUI.failure_modes.engine_failure_signal.connect(self.update_engine_failure_status)
        self.trainControllerUI.failure_modes.brake_failure_signal.connect(self.update_brake_failure_status)
        self.trainControllerUI.failure_modes.signal_failure_signal.connect(self.update_signal_failure_status)
        self.trainControllerUI.power_class.power_command_signal.connect(self.update_power_command)
        self.trainControllerUI.lights.exterior_lights_signal.connect(self.update_exterior_lights)
        self.trainControllerUI.lights.interior_lights_signal.connect(self.update_interior_lights)
        self.trainControllerUI.doors.left_door_update.connect(self.update_left_door)
        self.trainControllerUI.doors.right_door_update.connect(self.update_right_door)
        self.trainControllerUI.brake_class.driver_brake_signal.connect(self.update_driver_brake_status)
        self.trainControllerUI.brake_class.service_brake_signal.connect(self.update_service_brake_status)
        self.trainControllerUI.brake_class.emergency_brake_signal.connect(self.update_emergency_brake_status)
        self.trainControllerUI.brake_class.passenger_brake_command_signal.connect(self.update_passenger_brake_status)
        self.trainControllerUI.desired_temperature_signal.connect(self.handle_desired_temperature)
        
        
    def update_UI(self):
        # This function should be using the trainControllerUI instance to update the UI
        self.trainControllerUI.update_current_speed(self.train_controller_list[self.current_train_id - 1].speed_control.current_velocity)
        self.trainControllerUI.update_commanded_speed(self.train_controller_list[self.current_train_id - 1].speed_control.commanded_speed)
        self.trainControllerUI.update_commanded_authority(self.train_controller_list[self.current_train_id - 1].position.commanded_authority)
        print(f"Power commanddddd: {self.train_controller_list[self.current_train_id - 1].power_class.power_command}")
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
        
        
        
    ############################
    # TRAIN ID HANDLE FROM CTC #
    ############################
        
    def handle_train_id(self, train_id: int):
        print(f"Train ID: {train_id}")
        self.current_train_id = train_id
        # Set self.trainControllerUI to the current train controller UI in the list
        self.trainControllerUI = self.train_controller_list[self.current_train_id - 1]
        
        
    ###########################################################
    # IMPLEMENT ADD/REMOVE TRAIN CONTROLLER UI FUNCTIONS HERE #
    ###########################################################

    def remove_train_controller_ui(self, train_controller_ui: TrainControllerUI):
        if train_controller_ui in self.train_controller_list:
            self.train_controller_list.remove(train_controller_ui)

    def create_and_add_train_controller_ui(self):
        new_train_controller_ui = self.create_train_controller_ui()
        self.train_controller_list.append(new_train_controller_ui)
        # if len(self.train_controller_list) == 1:
        #     new_train_controller_ui.show()

    def create_new_train_controller_ui(self):
        doors = Doors()
        tuning = Tuning()
        brake_status = BrakeStatus(self.communicator)
        power_class = PowerCommand(brake_status, tuning)
        speed_control = SpeedControl(power_class, brake_status, self.communicator)
        failure_modes = FailureModes(speed_control, power_class)
        lights = Lights(speed_control)
        temperature = Temperature()
        position = Position(doors, failure_modes, speed_control, power_class, self.communicator, lights)
        
        return TrainControllerUI(self.communicator, doors, tuning, brake_status, power_class, speed_control, failure_modes, position, lights, temperature)
        
        
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
        self.communicator.train_count_signal.connect(self.update_train_count)
        
    def update_commanded_speed(self, commanded_speed: list):
        for i in range(commanded_speed):
            self.train_controller_list[i].speed_control.handle_commanded_speed(commanded_speed[i])
            
    def update_commanded_authority(self, commanded_authority: list):
        for i in range(commanded_authority):
            self.train_controller_list[i].position.handle_commanded_authority(commanded_authority[i])
        
    def update_current_velocity(self, current_velocity: list):
        for i in range(current_velocity):
            self.train_controller_list[i].speed_control.handle_current_velocity(current_velocity[i])
        
    def update_engine_failure(self, engine_failure: list):
        for i in range(engine_failure):
            self.train_controller_list[i].failure_modes.handle_engine_failure(engine_failure[i])
            
    def update_brake_failure(self, brake_failure: list):
        for i in range(brake_failure):
            self.train_controller_list[i].failure_modes.handle_brake_failure(brake_failure[i])
            
    def update_signal_failure(self, signal_failure: list):
        for i in range(signal_failure):
            self.train_controller_list[i].failure_modes.handle_signal_failure(signal_failure[i])
            
    def update_passenger_brake_command(self, passenger_brake_command: list):
        for i in range(passenger_brake_command):
            self.train_controller_list[i].brake_class.handle_passenger_brake_command(passenger_brake_command[i])
            
    def update_actual_temperature(self, actual_temperature: list):
        for i in range(actual_temperature):
            self.train_controller_list[i].temperature.update_current_temp_display(actual_temperature[i])
            
    def update_polarity(self, polarity: list):
        for i in range(polarity):
            self.train_controller_list[i].position.handle_polarity_change(polarity[i])
            
    def update_train_count(self, train_count: int):
        if self.train_count > train_count:
            self.remove_train_controller_ui(self.train_controller_list[0])
            # self.remove_engineer_controller_ui(self.engineer_controller_list[0])
        elif self.train_count < train_count:
            self.create_and_add_train_controller_ui()
            # self.add_engineer_controller_ui()
            
        self.train_count = train_count
        
        
        
        
        
        
        
        
        
        
        
        
# Add main function here
if __name__ == "__main__":
    app = QApplication(sys.argv)
    train_trainControllerComm = Communicate()
    doors = Doors()
    tuning = Tuning()
    brake_status = BrakeStatus(train_trainControllerComm)
    power_class = PowerCommand(brake_status, tuning)
    speed_control = SpeedControl(power_class, brake_status, train_trainControllerComm)
    failure_modes = FailureModes(speed_control, power_class)
    lights = Lights(speed_control)
    temperature = Temperature()
    position = Position(doors, failure_modes, speed_control, power_class, train_trainControllerComm, lights)
    
    trainControllerUI = TrainControllerUI(train_trainControllerComm, doors, tuning, brake_status, power_class, speed_control, failure_modes, position, lights, temperature)
    # trainControllerUI.show()
    trainControllerShell = TrainControllerShell(train_trainControllerComm, trainControllerUI)
    sys.exit(app.exec())
        