from TrainControllerUIClasses import *
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Resources.TrainTrainControllerComm import TrainTrainController as Communicate

class TrainControllerShell:
    def __init__(self, train_trainControllerComm: Communicate, train_id_class: TrainID):
        self.train_controller_list: list[TrainControllerUI] = []
        self.engineer_window_list: list[TrainEngineerUI] = []
        self.communicator = train_trainControllerComm
        self.train_id_class = train_id_class
        self.train_count = 0
        self.train_id = 0
        self.get_train_count()
        self.handle_values_from_train_model()
        self.train_id_class.train_id_signal.connect(self.handle_train_id)
        
    def get_train_count(self):
        self.communicator.train_count_signal.connect(self.calculate_train_count)
        
    def calculate_train_count(self, count):
        if self.train_count > count:
            self.remove_train_controller_ui(self.train_controller_list[0])
            self.train_controller_list[0].close()
            self.remove_engineer_window_ui(self.engineer_window_list[0])
        elif self.train_count < count:
            self.show_TrainControllerUI()
            self.show_EngineerUI()
            
        self.train_count = count
        
    def handle_train_id(self, train_id: int):
        self.train_id = train_id
        
    def handle_values_from_train_model(self):
        self.communicator.current_velocity_signal.connect(self.handle_current_velocity)
        self.communicator.commanded_speed_signal.connect(self.handle_commanded_speed)
        self.communicator.commanded_authority_signal.connect(self.handle_commanded_authority)
        self.communicator.engine_failure_signal.connect(self.handle_engine_failure)
        self.communicator.brake_failure_signal.connect(self.handle_brake_failure)
        self.communicator.signal_failure_signal.connect(self.handle_signal_failure)
        self.communicator.passenger_brake_command_signal.connect(self.handle_passenger_brake_command)
        self.communicator.actual_temperature_signal.connect(self.handle_actual_temperature)
        self.communicator.polarity_signal.connect(self.handle_polarity)
        
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

    def show_TrainControllerUI(self):
        new_train_controller_ui = self.create_train_controller_ui()
        self.add_train_controller_ui(new_train_controller_ui)
        new_train_controller_ui.show()

    def create_train_controller_ui(self):
        # Same as before
        doors = Doors()
        tuning = Tuning()
        brake_status = BrakeStatus(self.communicator)
        power_class = PowerCommand(brake_status, tuning)
        speed_control = SpeedControl(power_class, brake_status, self.communicator)
        failure_modes = FailureModes(speed_control)
        lights = Lights(speed_control)
        temperature = Temperature()
        position = Position(doors, failure_modes, speed_control, power_class, self.communicator, lights)
        train_id = TrainID()
        
        return TrainControllerUI(self.communicator, doors, tuning, brake_status, power_class, speed_control, failure_modes, position, lights, temperature, train_id)

    def add_engineer_window_ui(self, engineer_ui: TrainEngineerUI):
        self.engineer_window_list.append(engineer_ui)

    def remove_engineer_window_ui(self, engineer_ui: TrainEngineerUI):
        if engineer_ui in self.engineer_window_list:
            engineer_ui.close()
            self.engineer_window_list.remove(engineer_ui)
            
    def show_EngineerUI(self):
        new_engineer_ui = self.create_engineer_ui()
        self.add_engineer_window_ui(new_engineer_ui)
        new_engineer_ui.show()

    def create_engineer_ui(self):
        tuning = Tuning()
        return TrainEngineerUI(tuning)

    def handle_clock_tick(self):
        for train_controller in self.train_controller_list:
            if self.clock.seconds_elapsed % 2 == 0:
                train_controller.write_to_train_model()
            else:
                train_controller.read_from_train_model()

    def write_to_train_model(self):
        if self.train_controller_list:
            self.train_controller_list[0].write_to_train_model()

    def read_from_train_model(self):
        if self.train_controller_list:
            self.train_controller_list[0].read_from_train_model()


# GET TRAIN ID NUMBER FROM UI TO SHELL CLASS VIA SIGNALS - DONE


# UPDATE TRAIN CONTROLLER UI TO MAKE IT SO THAT THE CORRESPONDING TRAIN ID VALUES ARE DISPLAYED
# EMIT ALL VALUES THAT NEED TO BE SENT TO THE TRAIN MODEL (WITH INDEX)
# 