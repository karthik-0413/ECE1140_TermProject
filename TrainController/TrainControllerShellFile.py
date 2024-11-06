from TrainControllerUIClasses import *
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Resources.TrainTrainControllerComm import TrainTrainController as Communicate

class TrainControllerShell:
    def __init__(self, train_trainControllerComm: Communicate, trainControllerUI: TrainControllerUI):
        self.train_controller_list: list[TrainControllerUI] = []
        self.engineer_window_list: list[TrainEngineerUI] = []
        self.communicator = train_trainControllerComm
        self.trainControllerUI = trainControllerUI
        self.train_count = 1
        self.train_id = 1
        self.read_from_train_model()
        self.new_TrainControllerUI_instance()
        self.get_small_classes_emit_connect()
        
        # Connect function for dropdown selection for train ID and the train count for the CTC
        self.train_controller_list[self.train_id - 1].train_id_signal.connect(self.handle_train_id)
        self.communicator.train_count_signal.connect(self.calculate_train_count)
        
        
        
    
    def get_small_classes_emit_connect(self):
        # So, each element in the train controller list has its own signal for the small classes
        for train_controller in self.train_controller_list:
            train_controller.speed_control.current_velocity_signal.connect(self.update_current_speed)
            train_controller.speed_control.commanded_speed_signal.connect(self.update_commanded_speed)
            train_controller.position.commanded_authority_signal.connect(self.update_commanded_authority)
            train_controller.temperature.current_temperature_signal.connect(self.update_current_temperature)
            train_controller.failure_modes.engine_failure_signal.connect(self.update_engine_failure_status)
            train_controller.failure_modes.brake_failure_signal.connect(self.update_brake_failure_status)
            train_controller.failure_modes.signal_failure_signal.connect(self.update_signal_failure_status)
            train_controller.power_class.power_command_signal.connect(self.update_power_command)
            train_controller.lights.exterior_lights_signal.connect(self.update_exterior_lights)
            train_controller.lights.interior_lights_signal.connect(self.update_interior_lights)
            train_controller.doors.left_door_update.connect(self.update_left_door)
            train_controller.doors.right_door_update.connect(self.update_right_door)
            train_controller.brake_class.driver_brake_signal.connect(self.update_driver_brake_status)
            train_controller.brake_class.service_brake_signal.connect(self.update_service_brake_status)
            train_controller.brake_class.emergency_brake_signal.connect(self.update_emergency_brake_status)
            train_controller.brake_class.passenger_brake_command_signal.connect(self.update_passenger_brake_status)
            train_controller.desired_temperature_signal.connect(self.handle_desired_temperature)
        # Making sure to update UI
        self.update_UI()
        
    def update_commanded_speed(self, commanded_speed: float):
        self.train_controller_list[self.train_id - 1].update_commanded_speed(commanded_speed)

    def update_commanded_authority(self, commanded_authority: float):
        self.train_controller_list[self.train_id - 1].update_commanded_authority(commanded_authority)

    def update_current_temperature(self, current_temperature: float):
        self.train_controller_list[self.train_id - 1].update_current_temperature(current_temperature)

    def update_engine_failure_status(self, engine_failure: bool):
        self.train_controller_list[self.train_id - 1].update_engine_failure_status(engine_failure)

    def update_brake_failure_status(self, brake_failure: bool):
        self.train_controller_list[self.train_id - 1].update_brake_failure_status(brake_failure)

    def update_signal_failure_status(self, signal_failure: bool):
        self.train_controller_list[self.train_id - 1].update_signal_failure_status(signal_failure)

    def update_power_command(self, power_command: float):
        # for train_controller in self.train_controller_list:
        print(f"In shell case: {power_command}")
        self.train_controller_list[self.train_id - 1].update_power_command(power_command)
        self.write_to_train_model()
            # self.update_UI()

    def update_exterior_lights(self, exterior_lights: bool):
        self.train_controller_list[self.train_id - 1].update_exterior_lights(exterior_lights)

    def update_interior_lights(self, interior_lights: bool):
        print("Updating interior lights")
        self.train_controller_list[self.train_id - 1].update_interior_lights(interior_lights)

    def update_left_door(self, left_door: bool):
        self.train_controller_list[self.train_id - 1].update_left_door(left_door)

    def update_right_door(self, right_door: bool):
        self.train_controller_list[self.train_id - 1].update_right_door(right_door)

    def update_driver_brake_status(self, driver_brake_status: bool):
        self.train_controller_list[self.train_id - 1].update_driver_brake_status(driver_brake_status)

    def update_service_brake_status(self, service_brake_status: bool):
        self.train_controller_list[self.train_id - 1].update_service_brake_status(service_brake_status)

    def update_emergency_brake_status(self, emergency_brake_status: bool):
        self.train_controller_list[self.train_id - 1].update_emergency_brake_status(emergency_brake_status)

    def update_passenger_brake_status(self, passenger_brake_status: bool):
        self.train_controller_list[self.train_id - 1].update_passenger_brake_status(passenger_brake_status)
         
    def update_current_speed(self, current_speed: float):
        self.train_controller_list[self.train_id - 1].update_current_speed(current_speed)
        
    def update_UI(self):
        # # This function should be using the trainControllerUI instance to update the UI
        # self.trainControllerUI.current_velocity_signal.emit(self.train_controller_list[self.train_id - 1].speed_control.current_velocity)
        # self.trainControllerUI.commanded_speed_signal.emit(self.train_controller_list[self.train_id - 1].speed_control.commanded_speed)
        # self.trainControllerUI.commanded_authority_signal.emit(self.train_controller_list[self.train_id - 1].position.commanded_authority)
        # print(f"Power commanddddd: {self.train_controller_list[self.train_id - 1].power_class.power_command}")
        # self.trainControllerUI.update_power_command(self.train_controller_list[self.train_id - 1].power_class.power_command)
        # self.trainControllerUI.engine_failure_signal.emit(self.train_controller_list[self.train_id - 1].failure_modes.engine_fail)
        # self.trainControllerUI.brake_failure_signal.emit(self.train_controller_list[self.train_id - 1].failure_modes.brake_fail)
        # self.trainControllerUI.signal_failure_signal.emit(self.train_controller_list[self.train_id - 1].failure_modes.signal_fail)
        # self.trainControllerUI.service_brake_signal.emit(self.train_controller_list[self.train_id - 1].brake_class.driver_service_brake_command)
        # self.trainControllerUI.emergency_brake_signal.emit(self.train_controller_list[self.train_id - 1].brake_class.driver_emergency_brake_command)
        # self.trainControllerUI.desired_temperature_signal.emit(self.train_controller_list[self.train_id - 1].temperature.desired_temperature)
        # self.trainControllerUI.actual_temperature_signal.emit(self.train_controller_list[self.train_id - 1].temperature.current_temperature)
        # self.trainControllerUI.exterior_lights_signal.emit(self.train_controller_list[self.train_id - 1].lights.exterior_lights)
        # self.trainControllerUI.interior_lights_signal.emit(self.train_controller_list[self.train_id - 1].lights.interior_lights)
        # self.trainControllerUI.left_door_signal.emit(self.train_controller_list[self.train_id - 1].doors.left_door)
        # self.trainControllerUI.right_door_signal.emit(self.train_controller_list[self.train_id - 1].doors.right_door)
        # self.trainControllerUI.driver_brake_signal.emit(self.train_controller_list[self.train_id - 1].brake_class.driver_brake_status)
        # self.trainControllerUI.passenger_brake_command_signal.emit(self.train_controller_list[self.train_id - 1].brake_class.passenger_brake)
        # This function should be using the trainControllerUI instance to update the UI
        
        
        
        # Update the UI with the current index of the train controller list
        self.trainControllerUI.update_current_speed(self.train_controller_list[self.train_id - 1].speed_control.current_velocity)
        self.trainControllerUI.update_commanded_speed(self.train_controller_list[self.train_id - 1].speed_control.commanded_speed)
        self.trainControllerUI.update_commanded_authority(self.train_controller_list[self.train_id - 1].position.commanded_authority)
        print(f"Power commanddddd: {self.train_controller_list[self.train_id - 1].power_class.power_command}")
        self.trainControllerUI.update_power_command(self.train_controller_list[self.train_id - 1].power_class.power_command)
        self.trainControllerUI.update_engine_failure_status(self.train_controller_list[self.train_id - 1].failure_modes.engine_fail)
        self.trainControllerUI.update_brake_failure_status(self.train_controller_list[self.train_id - 1].failure_modes.brake_fail)
        self.trainControllerUI.update_signal_failure_status(self.train_controller_list[self.train_id - 1].failure_modes.signal_fail)
        self.trainControllerUI.update_service_brake_status(self.train_controller_list[self.train_id - 1].brake_class.driver_service_brake_command)
        self.trainControllerUI.update_emergency_brake_status(self.train_controller_list[self.train_id - 1].brake_class.driver_emergency_brake_command)
        self.trainControllerUI.update_current_temperature(self.train_controller_list[self.train_id - 1].temperature.current_temperature)
        self.trainControllerUI.update_exterior_lights(self.train_controller_list[self.train_id - 1].lights.exterior_lights)
        self.trainControllerUI.update_interior_lights(self.train_controller_list[self.train_id - 1].lights.interior_lights)
        self.trainControllerUI.update_left_door(self.train_controller_list[self.train_id - 1].doors.left_door)
        self.trainControllerUI.update_right_door(self.train_controller_list[self.train_id - 1].doors.right_door)
        self.trainControllerUI.update_driver_brake_status(self.train_controller_list[self.train_id - 1].brake_class.driver_brake_status)
        self.trainControllerUI.update_passenger_brake_status(self.train_controller_list[self.train_id - 1].brake_class.passenger_brake)
        self.write_to_train_model()
        
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
        self.communicator.current_velocity_signal.connect(self.handle_current_velocity)
        self.communicator.commanded_speed_signal.connect(self.handle_commanded_speed)
        self.communicator.commanded_authority_signal.connect(self.handle_commanded_authority)
        self.communicator.engine_failure_signal.connect(self.handle_engine_failure)
        self.communicator.brake_failure_signal.connect(self.handle_brake_failure)
        self.communicator.signal_failure_signal.connect(self.handle_signal_failure)
        self.communicator.passenger_brake_command_signal.connect(self.handle_passenger_brake_command)
        self.communicator.actual_temperature_signal.connect(self.handle_actual_temperature)
        self.communicator.polarity_signal.connect(self.handle_polarity)
        
    def calculate_train_count(self, count):
        if self.train_count > count:
            self.remove_train_controller_ui(self.train_controller_list[0])
            self.remove_engineer_window_ui(self.engineer_window_list[0])
        elif self.train_count < count:
            self.new_TrainControllerUI_instance()
            self.new_EngineerUI_instance()
            
        self.train_count = count
        
    def handle_train_id(self, train_id: int):
        print(f"Train ID: {train_id}")
        self.train_id = train_id
        
        self.trainControllerUI = self.train_controller_list[self.train_id - 1]
        # self.get_small_classes_emit_connect()
        # Making sure to update UI
        self.update_UI()
 
    def handle_desired_temperature(self, desired_temperature: float):
        self.train_controller_list[self.train_id - 1].temperature.desired_temperature = desired_temperature
        
    def handle_current_velocity(self, velocity: list):
        for i in range(len(velocity)):
            self.train_controller_list[i].speed_control.handle_current_velocity(velocity[i])
            
    def handle_commanded_speed(self, commanded_speed: list):
        for i in range(len(commanded_speed)):
            self.train_controller_list[i].speed_control.handle_commanded_speed(commanded_speed[i])
            
    def handle_commanded_authority(self, commanded_authority: list):
        for i in range(len(commanded_authority)):
            self.train_controller_list[i].position.handle_commanded_authority(commanded_authority[i])
            
    def handle_engine_failure(self, engine_failure: list):
        for i in range(len(engine_failure)):
            self.train_controller_list[i].failure_modes.handle_engine_failure(engine_failure[i])
            
    def handle_brake_failure(self, brake_failure: list):
        for i in range(len(brake_failure)):
            self.train_controller_list[i].failure_modes.handle_brake_failure(brake_failure[i])
            
    def handle_signal_failure(self, signal_failure: list):
        for i in range(len(signal_failure)):
            self.train_controller_list[i].failure_modes.handle_signal_failure(signal_failure[i])
            
    def handle_passenger_brake_command(self, passenger_brake_command: list):
        for i in range(len(passenger_brake_command)):
            self.train_controller_list[i].brake_class.handle_passenger_brake_command(passenger_brake_command[i])
            
    def handle_actual_temperature(self, actual_temperature: list):
        for i in range(len(actual_temperature)):
            self.train_controller_list[i].temperature.update_current_temp_display(actual_temperature[i])
            
    def handle_polarity(self, polarity: list):
        for i in range(len(polarity)):
            self.train_controller_list[i].position.handle_polarity_change(polarity[i])
        
        
    def add_train_controller_ui(self, train_controller_ui: TrainControllerUI):
        self.train_controller_list.append(train_controller_ui)
    
    def remove_train_controller_ui(self, train_controller_ui: TrainControllerUI):
        if train_controller_ui in self.train_controller_list:
            self.train_controller_list.remove(train_controller_ui)

    def new_TrainControllerUI_instance(self):
        new_train_controller_ui = self.create_train_controller_ui()
        self.add_train_controller_ui(new_train_controller_ui)
        if len(self.train_controller_list) == 1:
            self.trainControllerUI = self.train_controller_list[0]
            self.trainControllerUI.show()

    def create_train_controller_ui(self):
        # Same as before
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

    def add_engineer_window_ui(self, engineer_ui: TrainEngineerUI):
        self.engineer_window_list.append(engineer_ui)

    def remove_engineer_window_ui(self, engineer_ui: TrainEngineerUI):
        if engineer_ui in self.engineer_window_list:
            engineer_ui.close()
            self.engineer_window_list.remove(engineer_ui)
            
    def new_EngineerUI_instance(self):
        new_engineer_ui = self.create_engineer_ui()
        self.add_engineer_window_ui(new_engineer_ui)

    def create_engineer_ui(self):
        tuning = Tuning()
        return TrainEngineerUI(tuning)

# GET TRAIN ID NUMBER FROM UI TO SHELL CLASS VIA SIGNALS - DONE
# EMIT ALL VALUES THAT NEED TO BE SENT TO THE TRAIN MODEL (WITH INDEX) - DONE


# UPDATE TRAIN CONTROLLER UI TO MAKE IT SO THAT THE CORRESPONDING TRAIN ID VALUES ARE DISPLAYED

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