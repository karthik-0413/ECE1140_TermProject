import time
import json
import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QLabel, QComboBox
)
from PyQt6.QtCore import Qt, QCoreApplication, pyqtSignal, QObject, QTimer
from PyQt6.QtGui import QDoubleValidator
from TrainController.TrainControllerHW import send_data_to_pi
from TrainController.ControllerToShellCommuicate import ControllerToShellCommunicate as Communicate2
# from TrainControllerHW import send_numbers_to_pi

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Resources.TrainTrainControllerComm import TrainTrainController as Communicate


class Doors(QObject):
    right_door_update = pyqtSignal(bool)
    left_door_update = pyqtSignal(bool)
    
    def __init__(self):
        super().__init__()
        self.left_door = False
        self.right_door = False
 
    def open_left_door(self):
        self.left_door = True
        self.left_door_update.emit(self.left_door)
        # # print("Left door opened")
        
    def open_right_door(self):
        self.right_door = True
        self.right_door_update.emit(self.right_door)
        # # print("Right door opened")
        
    def close_left_door(self):
        self.left_door = False
        self.left_door_update.emit(self.left_door)
        # # print("Left door closed")
        
    def close_right_door(self):
        self.right_door = False
        self.right_door_update.emit(self.right_door)
        # # print("Right door closed")

class Tuning(QObject):
    kp_changed = pyqtSignal(float)
    ki_changed = pyqtSignal(float)
    
    def __init__(self):
        super().__init__()
        self.kp = 7173.0
        self.ki = 15.0
        
    def set_kp(self, kp):
        self.kp = kp
        self.kp_changed.emit(float(self.kp))
        # # print(f"Kp set to {self.kp}")
        
    def set_ki(self, ki):
        self.ki = ki
        self.ki_changed.emit(float(self.ki))
        # # print(f"Ki set to {self.ki}")
        
    def get_kp(self):
        return self.kp
    
    def get_ki(self):
        return self.ki
       
class BrakeStatus(QObject):
    service_brake_signal = pyqtSignal(bool)
    manual_service_brake_signal = pyqtSignal(bool)
    emergency_brake_signal = pyqtSignal(bool)
    passenger_brake_command_signal = pyqtSignal(bool)
    driver_brake_signal = pyqtSignal(bool)
    
    def __init__(self, communicator: Communicate):
        super().__init__()
        self.driver_service_brake_command = False
        self.manual_driver_service_brake_command = False
        self.driver_emergency_brake_command = False
        self.manual_driver_emergency_brake_command = False
        self.driver_brake_status = False
        self.passenger_brake = False
        self.entered_lower = False
        self.reaching_station = False
        self.no_again = True
        self.station_auto_mode = False
        self.communicator = communicator
        
    def manual_apply_service_brake(self):
        self.manual_driver_service_brake_command = True
        self.manual_service_brake_signal.emit(self.manual_driver_service_brake_command)
        # # print("Service Brake Applied")
        
    def manual_no_apply_service_brake(self):
        self.manual_driver_service_brake_command = False
        self.manual_service_brake_signal.emit(self.manual_driver_service_brake_command)
        # # print("Service Brake Released")
        
    def manual_apply_emergency_brake(self):
        self.manual_driver_emergency_brake_command = True
        self.emergency_brake_signal.emit(self.manual_driver_emergency_brake_command)
        # # print("Service Brake Applied")
        
    def manual_no_apply_emergency_brake(self):
        self.manual_driver_emergency_brake_command = False
        self.emergency_brake_signal.emit(self.manual_driver_emergency_brake_command)
        # # print("Service Brake Released")
        
    def apply_emergency_brake(self):
        # Always going to go to 0
        # self.desired_speed = 0.0
        self.driver_emergency_brake_command = True
        self.emergency_brake_signal.emit(self.driver_emergency_brake_command)
        # self.speed_control.desired_velocity = 0.0
        # self.power_class.update_power_command(self.speed_control.current_velocity, self.speed_control.desired_velocity)
        # self.communicator.emergency_brake_command_signal.emit(self.driver_emergency_brake_command)
        # self.communicator.emergency_brake_command_signal.emit([self.driver_emergency_brake_command])
        # # print("Emergency Brake Activated!")
        
    def apply_service_brake(self):
        self.driver_service_brake_command = True
        self.service_brake_signal.emit(self.driver_service_brake_command)
        # # print("Service Brake Applied.")
        
    def no_apply_emergency_brake(self):
        self.driver_emergency_brake_command = False
        self.emergency_brake_signal.emit(self.driver_emergency_brake_command)
        # self.communicator.emergency_brake_command_signal.emit([self.driver_emergency_brake_command])
        # self.send_emergency_brake_command(self.driver_emergency_brake_command)
        # # print("Emergency Brake Dectivated!")
        
    def no_apply_service_brake(self):
        self.driver_service_brake_command = False
        self.service_brake_signal.emit(self.driver_service_brake_command)
        # self.send_service_brake_command(self.driver_service_brake_command)
        # # print("Service Brake Released.")
    
    def handle_emergency_brake_command(self, status: bool):
        self.apply_emergency_brake()
        # if not status:
        #     self.driver_emergency_brake_command = True
        #     self.emergency_brake_signal.emit(self.driver_emergency_brake_command)
        #     # # print("Emergency Brake Applied")
        # elif status:
        #     self.driver_emergency_brake_command = False
        #     self.emergency_brake_signal.emit(self.driver_emergency_brake_command)
        #     # # print("Emergency Brake Released")
        
    def handle_passenger_brake_command(self, status: bool):
        if status:
            # Turn on the passenger brake indcator until current velocity is 0
            self.passenger_brake = True
            self.driver_emergency_brake_command = True
            self.passenger_brake_command_signal.emit(self.driver_emergency_brake_command)
            # # print("Passenger Brake Applied")
        elif not status:
            # self.driver_emergency_brake_command = False
            self.passenger_brake = False
            self.passenger_brake_command_signal.emit(self.driver_emergency_brake_command)
            # # print("Passenger Brake Released")
            
    def get_emergency_brake_status(self):
        return self.driver_emergency_brake_command
    
class PowerCommand(QObject):
    power_command_signal = pyqtSignal(float)
    
    def __init__(self, brake_status: BrakeStatus, tuning: Tuning, module: bool = True):
        super().__init__()
        self.max_power = 120000
        self.uk_current = 0.0
        self.ek_current = 0.0
        self.uk_previous = 0.0
        self.ek_previous = 0.0
        self.power_command = 0.0
        self.tuning = tuning
        self.brake_status = brake_status
        self.module = module     # 1 for Software, 0 for Hardware
        self.service_brake = False
        self.emergency_brake = False
        self.raspberry_pi_hostname = '192.168.0.204'
        self.raspberry_pi_port = 22
        self.raspberry_pi_username = 'maj214'
        self.raspberry_pi_password = 'password'
        
    def update_kp(self, kp):
        self.tuning.kp = kp
        # # print(f"Kp set to {self.tuning.kp} in Power Command Class")
        
    def update_ki(self, ki):
        self.tuning.ki = ki
        # # print(f"Ki set to {self.tuning.ki} in Power Command Class")
        
    # def hardware_update_power_command(self, power: float):
        
        
    def update_power_command(self, current_velocity: float, desired_velocity: float, operation_mode: int = 0):
        # print(f"Current Speed: {current_velocity:.2f} m/s, Desired Speed: {desired_velocity:.2f} m/s")

        if self.module == 1:
            if self.brake_status.station_auto_mode == True and operation_mode == 0:
                self.power_command = 0
                self.power_command_signal.emit(self.power_command)
            
            else:
                if self.brake_status.reaching_station:
                    self.power_command = 0
                    self.power_command_signal.emit(self.power_command)
                    self.brake_status.apply_service_brake()
                    if current_velocity == 0.0:
                        self.brake_status.no_apply_service_brake()
                        self.brake_status.reaching_station = False
                
                elif self.brake_status.entered_lower == True:
                    # # print("Entered Lower")
                    self.power_command = 0
                    self.power_command_signal.emit(self.power_command)
                    self.brake_status.apply_service_brake()
                    if current_velocity < desired_velocity or current_velocity == 0.0:
                        print("Entered Lower")
                        self.brake_status.no_apply_service_brake()
                        self.brake_status.entered_lower = False
                        self.brake_status.no_again = False
                        self.power_command = 0.0
                
                # Murphy Failures
                elif desired_velocity == 0.0:
                    self.power_command = 0
                    self.power_command_signal.emit(self.power_command)
                    self.brake_status.apply_emergency_brake()
                    if current_velocity == 0.0:
                        self.brake_status.no_apply_emergency_brake()
                    # Put Brake Status has OFF
                    # self.brake_status.no_apply_service_brake()
                    # self.brake_status.no_apply_emergency_brake()
                    
                elif self.brake_status.driver_emergency_brake_command or self.brake_status.driver_service_brake_command or self.brake_status.manual_driver_service_brake_command:
                    self.power_command = 0
                    self.power_command_signal.emit(self.power_command)
                    # self.brake_status.apply_emergency_brake()
                    # if current_velocity == 0.0:
                    #     self.brake_status.no_apply_emergency_brake()
                    
                elif round(desired_velocity, 2) == round(current_velocity, 2):
                    self.power_command = 0
                    # Put Brake Status has OFF
                    # self.brake_status.no_apply_service_brake()
                    self.power_command_signal.emit(self.power_command)
                    
                elif current_velocity > desired_velocity:
                    self.power_command = 0
                    self.power_command_signal.emit(self.power_command)
                    # Slow down until it reaches desired velocity
                    if current_velocity > desired_velocity:
                        self.brake_status.apply_service_brake()
                    elif current_velocity < desired_velocity:
                        self.brake_status.no_apply_service_brake()
                    
                elif current_velocity < desired_velocity:
                    # self.brake_status.no_apply_service_brake()
                    # if self.module == 1:
                    # self.brake_status.no_apply_service_brake()
                    # # print(f"Desired Speed: {desired_velocity:.2f} m/s, Current Speed: {current_velocity:.2f} m/s")
                    
                    # Finding the velocity error
                    self.ek_current = desired_velocity - current_velocity
                    
                    # Using the different cases from lecture slides
                    if self.power_command < self.max_power:
                        self.uk_current = self.uk_previous + (0.25 / 2) * (self.ek_current + self.ek_previous)
                    else:
                        self.uk_current = self.uk_previous
                    
                    # Finding the power command
                    self.power_command = self.tuning.kp * self.ek_current + self.tuning.ki * self.uk_current

                    # Updating the previous variables for the next iteration
                    self.ek_previous = self.ek_current
                    self.uk_previous = self.uk_current
                        
                    # elif self.module == 0:
                    #     result = send_data_to_pi([desired_velocity, current_velocity, self.ek_current, self.max_power, self.uk_current, self.uk_previous, self.ek_previous, self.tuning.kp, self.tuning.ki])
                    #     print(f"Result:{result}")
                    #     if result:
                    #         # Split the result string into a list of values
                    #         result_list = list(map(float, result.split(',')))
                    #         self.power_command, self.ek_previous, self.uk_previous, self.uk_current, self.ek_current = result_list
                    
                    
                    # Power command bound
                    if self.power_command > self.max_power:
                        self.power_command = self.max_power
                        self.power_command_signal.emit(self.power_command)
                        # Put Brake Status has OFF
                        # self.brake_status.driver_brake_status = False
                        # self.brake_status.driver_service_brake_command = False
                        # self.brake_status.driver_brake_status = False
                        # self.brake_status.driver_emergency_brake_command = False
                        # self.brake_status.no_apply_service_brake()
                        # self.brake_status.no_apply_emergency_brake()
                        
                    elif self.power_command <= 0:
                        self.power_command_signal.emit(self.power_command)
                        # print("NEGAIVE POWER COMMAND")
                        # Brake until current velocity is equal to desired velocity, so until power_command = 0
                        self.power_command = 0
                        # self.brake_status.driver_service_brake_command = True
                        # self.brake_status.driver_brake_status = True
                        # self.brake_status.driver_emergency_brake_command = False
                        # # print("Service Brake Applied")
                        # self.brake_status.no_apply_service_brake()
                        # self.brake_status.no_apply_emergency_brake()
                        
                    else:
                        self.power_command = self.power_command
                        self.power_command_signal.emit(self.power_command)
                        # self.reset_service_brake_button_style()
                        # self.brake_status.driver_service_brake_command = False
                        # self.brake_status.driver_brake_status = False
                        # self.brake_status.driver_emergency_brake_command = False
                        # self.brake_status.no_apply_service_brake()
                        # self.brake_status.no_apply_emergency_brake()
                        
        if self.module == 0:
            result = send_data_to_pi([desired_velocity, current_velocity, self.ek_current, self.max_power, self.uk_current, self.uk_previous, self.ek_previous, self.tuning.kp, self.tuning.ki, self.brake_status.station_auto_mode, self.brake_status.reaching_station, self.brake_status.entered_lower, self.brake_status.no_again, self.brake_status.driver_emergency_brake_command, self.brake_status.driver_service_brake_command, self.brake_status.manual_driver_service_brake_command])
            # print(f"Result:{result}")
            if result:
                # Split the result string into a list of values
                # result_list = list(map(float, result.split(',')))
                
                
                # Split the result string by commas
                result_list = result.split(',')
                # for i in range(len(result_list)):
                #     print(f"Data Type: {type(result_list[i])}") # Everything is a string
                    
                for i in range(len(result_list)):
                    # print(f"Number of Elements: {len(result_list)}")
                    result_list[i] = self.convert_element(result_list[i], i)
                    # print(f"Data Type: {type(result_list[i])}") # Everything is a string
                
                # Apply the conversion to each element
                # parsed_result = [self.convert_element(el) for el in result_list]
                
                self.power_command, self.ek_previous, self.uk_previous, self.uk_current, self.ek_current, self.brake_status.station_auto_mode, self.brake_status.reaching_station, self.brake_status.entered_lower, self.brake_status.no_again, self.brake_status.driver_emergency_brake_command, self.brake_status.driver_service_brake_command, self.brake_status.manual_driver_service_brake_command = result_list
                self.power_command_signal.emit(self.power_command)
                
                if self.brake_status.driver_service_brake_command == True:
                    self.brake_status.apply_service_brake()
                elif self.brake_status.driver_service_brake_command == False:
                    self.brake_status.no_apply_service_brake()
                if self.brake_status.driver_emergency_brake_command == True:
                    self.brake_status.apply_emergency_brake()
                elif self.brake_status.driver_emergency_brake_command == False:
                    self.brake_status.no_apply_emergency_brake()
                    


    def convert_element(self, element, index):
        if index < 5:
            try:
                print(f"Converting element {index} '{element}' to float")
                return float(element)  # Convert the first five elements to float
            except ValueError:
                print(f"Could not convert element {index} '{element}' to float, returning as is")
                return element  # If conversion fails, return as is
        else:
            if element == ' True':
                print(f"Converting element {index} '{element}' to True")
                return True
            elif element == ' False':
                print(f"Converting element {index} '{element}' to False")
                return False
            else:
                print(f"Element {index} '{element}' is neither 'True' nor 'False', returning as is")
                return element
                       
class SpeedControl(QObject):
    commanded_speed_signal = pyqtSignal(float)
    current_velocity_signal = pyqtSignal(float)
    
    def __init__(self, power_class: PowerCommand, brake_status: BrakeStatus, communicator: Communicate):
        super().__init__()
        self.commanded_speed = 0.0
        self.setpoint_speed = 0.0
        self.setpoint_speed_submit = False
        self.speed_limit = 100.0
        self.operation_mode = 0 # 1 for manual, 0 for automatic
        self.current_velocity = 0.0
        self.desired_velocity = 0.0
        self.power_class = power_class
        self.brake_status = brake_status
        self.communicator = communicator
        self.max_speed = 0.0
        self.prev_service_brake = False
        self.prev_emergency_brake = False
        self.prev_speed_limit = 0.0
        # self.entered_lower = False
        self.find_max_speed()
        self.set_auto_mode()
        
    def find_max_speed(self):
        # Commanded speed already in m/s, so no need to convert
        # Speed limit already in m/s, so no need to convert)
        # self.max_speed = min(self.speed_limit, self.commanded_speed)
        self.max_speed = self.commanded_speed
        # # print(f"Speed Limit: {self.speed_limit}")
        # # print(f"Commanded Speed: {self.commanded_speed}")
        # # print(f"Max Speed: {self.max_speed}")
        # # print(f"Max Speed: {self.max_speed}")
        
    def update_speed_limit(self, speed: float):
        pass
        # km/hr to m/s
        # self.prev_speed_limit = self.speed_limit
        # self.speed_limit = speed / 3.6
        # self.find_max_speed()
        
        # if self.speed_limit < self.prev_speed_limit:
        #     self.brake_status.entered_lower = True
        #     self.desired_velocity = self.speed_limit
        #     self.power_class.update_power_command(self.current_velocity, self.desired_velocity)
        #     # # print("Entered Lower")
        # # # print(f"Speed Limit: {self.speed_limit} Km/Hr")
        
    def handle_current_velocity(self, speed: float):
        if speed == 0:
            self.current_velocity = 0
            self.current_velocity_signal.emit(self.current_velocity)
            if self.brake_status.driver_emergency_brake_command:
                self.brake_status.no_apply_emergency_brake()
                self.desired_velocity = 0.0
            if self.brake_status.driver_service_brake_command:
                self.brake_status.no_apply_service_brake()
                self.desired_velocity = 0.0
            # self.brake_status.passenger_brake = False
            # self.brake_status.driver_brake_status = False
            # self.brake_status.driver_service_brake_command = False
            # self.brake_status.driver_emergency_brake_command = False
            # self.communicator.passenger_brake_command_signal.emit(False)    
            
        if self.brake_status.driver_service_brake_command:
            self.prev_service_brake = True
            
        if self.brake_status.driver_emergency_brake_command:
            self.prev_emergency_brake = True
            
        if not self.brake_status.driver_service_brake_command:
            self.brake_status.no_apply_service_brake()
            if self.prev_service_brake:
                self.desired_velocity = speed
                self.prev_service_brake = False
                
        if not self.brake_status.driver_emergency_brake_command:
            self.brake_status.no_apply_emergency_brake()
            if self.prev_emergency_brake:
                self.desired_velocity = speed
                self.prev_emergency_brake = False
                
                
        # if self.brake_status.driver_service_brake_command and self.current_velocity < self.desired_velocity:
        #     self.brake_status.no_apply_service_brake()
        # elif self.brake_status.driver_service_brake_command and self.current_velocity > self.desired_velocity:
        #     self.brake_status.apply_service_brake()
                
            
        # if self.brake_status.driver_emergency_brake_command and speed == 0.0:
        #     self.brake_status.no_apply_emergency_brake()
            
        # if self.brake_status.driver_service_brake_command and speed == 0.0:
        #     self.brake_status.no_apply_service_brake()
            
        self.current_velocity = speed
        self.power_class.update_power_command(self.current_velocity, self.desired_velocity)
        
        if self.power_class.power_command == 0.0 and self.brake_status.driver_service_brake_command and self.current_velocity == 0.0:
            self.desired_velocity = 0
            
        self.current_velocity_signal.emit(self.current_velocity)
        # # print(f"Current Speed: {self.current_velocity:.2f} m/s")
        
    def handle_commanded_speed(self, speed: float):
        if speed == 0:
            self.commanded_speed = 0.0
            self.desired_velocity = 0.0
            self.commanded_speed_signal.emit(self.commanded_speed)
            self.power_class.update_power_command(self.current_velocity, self.desired_velocity)
            # Brake to 0 with E-Brake
        # print(f"Commanded Speed: {speed:.2f} km/hr")
        elif self.operation_mode == 1 and self.desired_velocity > speed / 3.6:
            self.commanded_speed = speed / 3.6
            self.commanded_speed_signal.emit(self.commanded_speed)
            self.update_setpoint_speed_calculations(speed / 3.6)
        elif self.operation_mode == 0 and self.desired_velocity > speed / 3.6:
            self.commanded_speed = speed / 3.6
            self.commanded_speed_signal.emit(self.commanded_speed)
            self.update_setpoint_speed_auto(self.commanded_speed)
        # Only goes through this if statement one time (when the commanded speed is processed to be lower than current commanded speed)
        elif self.commanded_speed > (speed / 3.6):
                # self.brake_status.entered_lower = True
                self.commanded_speed = speed / 3.6
                self.commanded_speed_signal.emit(self.commanded_speed)
                # print(f"Commanded Speed: {self.commanded_speed:.2f} m/s")
                # self.find_max_speed()
                # self.desired_velocity = self.commanded_speed
                # self.update_setpoint_speed_auto(self.commanded_speed)
                # if self.current_velocity > self.desired_velocity:
                #     self.brake_status.apply_service_brake()
                #     self.power_class.power_command = 0.0
                #     self.power_class.update_power_command(self.current_velocity, self.desired_velocity)
                # else:
                #     self.brake_status.no_apply_service_brake()
                #     self.power_class.power_command = 0.0
                #     self.power_class.update_power_command(self.current_velocity, self.desired_velocity)
        else:
            self.commanded_speed = speed / 3.6
            self.find_max_speed()
            if self.operation_mode == 0:
                self.desired_velocity = self.commanded_speed
                self.update_setpoint_speed_auto(self.commanded_speed)
            
            
                if self.current_velocity > self.desired_velocity:
                    self.brake_status.apply_service_brake()
                    self.power_class.power_command = 0.0
                    self.power_class.update_power_command(self.current_velocity, self.desired_velocity)
                else:
                    if self.brake_status.driver_service_brake_command:
                        if not self.brake_status.manual_driver_service_brake_command:
                            
                            
                            # CAUSES BREAK TO NOT STOP RIGHT BEFORE GOING BELOW THE COMMANDED SPEED (JUST GOES TO ZERO)
                            self.brake_status.no_apply_service_brake()
                            
                        elif self.brake_status.manual_driver_service_brake_command:
                            pass
                        
                        # If driver manually applies service brake, then the no_apply_service_brake() function should NOT be called
                        
                        
                        
                        # print(f"Commanded Speed: {self.commanded_speed:.2f} m/s")
                        self.desired_velocity = self.commanded_speed
                        # print(f"Desired Speed: {self.desired_velocity:.2f} m/s")
                        self.power_class.update_power_command(self.current_velocity, self.desired_velocity)
                    else:
                        self.power_class.update_power_command(self.current_velocity, self.desired_velocity)
                
                
            # if self.operation_mode == 0:
            #     self.desired_velocity = self.commanded_speed
            # self.update_setpoint_speed_auto(self.commanded_speed)
            self.commanded_speed_signal.emit(self.commanded_speed)
            # # print(f"Commanded Speed: {self.commanded_speed:.2f} m/s")
    
    def set_manual_mode(self):
        self.operation_mode = 1
        self.update_desired_speed()
        # Make sure to enable the setpoint speed edit
        
        # # print("Operation Mode set to Manual")
        
    def set_auto_mode(self):
        self.operation_mode = 0
        self.update_desired_speed()
        # Make sure to disbale the setpoint speed edit

        # # print("Operation Mode set to Automatic")
        
    def update_desired_speed(self):
        if self.operation_mode == 1:
            self.update_setpoint_speed_calculations(self.desired_velocity)
        elif self.operation_mode == 0:
            self.update_setpoint_speed_auto(self.commanded_speed)
            
    def update_setpoint_speed_calculations(self, speed: float):  
        # Put the setpoint speed input in a variable in m/s even though it is in mph
        self.max_speed = min(self.speed_limit, self.commanded_speed)
        # # print(f"Max Speed: {self.max_speed}")
        
        self.desired_velocity = speed
        
        if (self.desired_velocity) > self.max_speed:
            self.desired_velocity = self.max_speed
            # self.setpoint_speed_edit.setText(f"{max_speed * 2.237:.2f}")
                    
        # # print(f"Desired Speed: {self.desired_velocity} m/s")    # Good updated value
        
        self.power_class.update_power_command(self.current_velocity, self.desired_velocity, 1)
        self.power_class.power_command_signal.emit(self.power_class.power_command)
        if self.power_class.power_command == 0.0 and self.brake_status.driver_service_brake_command and self.current_velocity == 0.0:
            self.desired_velocity = 0
        # Update the power command display
        # self.power_command_edit.setText(f"{self.power_command:.2f}")
        # # print(f"Power Command: {self.power_class.power_command} kW")
 
    def update_setpoint_speed_auto(self, speed: float):
        if self.operation_mode == 0:
            # Put the setpoint speed input in a variable in m/s even though it is in mph
            self.max_speed = min(self.speed_limit, self.commanded_speed)
            # # print(f"Max Speed: {self.max_speed}")
            
            self.desired_velocity = speed
            
            if (self.desired_velocity) > self.max_speed:
                self.desired_velocity = self.max_speed
                    
            self.power_class.update_power_command(self.current_velocity, self.desired_velocity, 0)
            self.power_class.power_command_signal.emit(self.power_class.power_command)
            
            
            # I COMMENTED THIS OUT !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
            if self.power_class.power_command == 0.0 and self.brake_status.driver_service_brake_command and self.current_velocity == 0.0:
                self.desired_velocity = 0
            
            # I COMMENTED THIS OUT !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
            
            # Update the power command display
            # self.power_command_edit.setText(f"{self.power_command:.2f}")
            # # print(f"Power Command: {self.power_class.power_command} kW")

class FailureModes(QObject):
    engine_failure_signal = pyqtSignal(bool)
    brake_failure_signal = pyqtSignal(bool)
    signal_failure_signal = pyqtSignal(bool)
    
    def __init__(self, speed_control: SpeedControl, power_class: PowerCommand):
        super().__init__()
        self.engine_fail = False
        self.brake_fail = False
        self.signal_fail = False
        self.speed_control = speed_control
        self.power_class = power_class
        
    def handle_engine_failure(self, status: bool):
        if status == True:
            self.engine_fail = True
            self.engine_failure_signal.emit(self.engine_fail)
            # Set current velocity to 0
            self.speed_control.desired_velocity = 0.0
            self.power_class.update_power_command(self.speed_control.current_velocity, self.speed_control.desired_velocity)
            # self.current_speed_edit.setText(f"{self.current_velocity:.2f} mph")
            # Divet in Emergency Brake
            # self.apply_emergency_brake()
            # self.divet_in_emergency_brake_buttons()
            # QTimer.singleShot(3000, self.reset_emergency_brake_button_style)
        else:
            self.engine_fail = False
            self.engine_failure_signal.emit(self.engine_fail)

    def handle_brake_failure(self, status: bool):
        if status == True:
            self.brake_fail = True
            self.brake_failure_signal.emit(self.brake_fail)
            # Set current velocity to 0
            self.speed_control.desired_velocity = 0.0
            self.power_class.update_power_command(self.speed_control.current_velocity, self.speed_control.desired_velocity)
            # self.current_speed_edit.setText(f"{self.current_velocity:.2f} mph")
            # Divet in Emergency Brake
            # self.apply_emergency_brake()
            # self.divet_in_emergency_brake_buttons()
            # QTimer.singleShot(3000, self.reset_emergency_brake_button_style)
        else:
            self.brake_fail = False
            self.brake_failure_signal.emit(self.brake_fail)
    
    def handle_signal_failure(self, status: bool):
        if status == True:
            self.signal_fail = True
            self.signal_failure_signal.emit(self.signal_fail)
            # Set current velocity to 0
            self.speed_control.desired_velocity = 0.0
            self.power_class.update_power_command(self.speed_control.current_velocity, self.speed_control.desired_velocity)
            # self.current_speed_edit.setText(f"{self.current_velocity:.2f} mph")
            # Divet in Emergency Brake
            # self.apply_emergency_brake()
            # self.divet_in_emergency_brake_buttons()
            # QTimer.singleShot(3000, self.reset_emergency_brake_button_style)
        else:
            self.signal_fail = False
            self.signal_failure_signal.emit(self.signal_fail)
        
class Lights(QObject):
    exterior_lights_signal = pyqtSignal(bool)
    interior_lights_signal = pyqtSignal(bool)
    
    def __init__(self, speed_control: SpeedControl):
        super().__init__()
        self.exterior_lights = False
        self.manual_exterior_lights = False
        self.interior_lights = False
        self.manual_interior_lights = False
        self.speed_control = speed_control
        
    def manual_turn_on_exterior_lights(self):
        self.manual_exterior_lights = True
        self.exterior_lights_signal.emit(self.manual_exterior_lights)
        # # print("Exterior Lights: ON")
        
    def manual_turn_off_exterior_lights(self):
        self.manual_exterior_lights = False
        self.exterior_lights_signal.emit(self.manual_exterior_lights)
        # # print("Exterior Lights: OFF")
        
    def manual_turn_on_interior_lights(self):
        self.manual_interior_lights = True
        self.interior_lights_signal.emit(self.manual_interior_lights)
        # # print("Interior Lights: ON")
        
    def manual_turn_off_interior_lights(self):
        self.manual_interior_lights = False
        self.interior_lights_signal.emit(self.manual_interior_lights)
        # # print("Interior Lights: OFF")
            
    def turn_on_exterior_lights(self):
        self.exterior_lights = True
        self.exterior_lights_signal.emit(self.exterior_lights)
        # # print("Exterior Lights: ON")
        
    def turn_off_exterior_lights(self):
        self.exterior_lights = False
        self.exterior_lights_signal.emit(self.exterior_lights)
        # # print("Exterior Lights: OFF")
        
    def turn_on_interior_lights(self):
        self.interior_lights = True
        self.interior_lights_signal.emit(self.interior_lights)
        # # print("Interior Lights: ON")
        
    def turn_off_interior_lights(self):
        self.interior_lights = False
        self.interior_lights_signal.emit(self.interior_lights)
        # # print("Interior Lights: OFF")
            
class Position(QObject):
    commanded_authority_signal = pyqtSignal(int)
    
    def __init__(self, doors: Doors, failure_modes: FailureModes, speed_control: SpeedControl, power_class: PowerCommand, communicator: Communicate, lights: Lights, brake_status: BrakeStatus, line: str):
        super().__init__()
        self.prev_authority = 0 # int
        self.commanded_authority = 111 + 1 - 1   # int
        self.next_authority = 1 # int
        self.station_name = 'Shadyside' # string
        self.announcement = '' # string
        self.polarity = True   # boolean
        # I need the block number of the station so that I can query into my infrastructure array and check what the station name is of that block
        self.communicator = communicator
        self.door = doors
        self.failure_modes = failure_modes
        self.speed_control = speed_control
        self.power_class = power_class
        self.light = lights
        self.brake_status = brake_status
        self.iterate = True
        self.repeat = False
        self.accept_authority = False
        self.line = line
        
        # Variables needed for the Track Layouts (GREEN LINE)
        self.green_station = []
        self.red_station = []
        self.green_station_door = []
        self.red_station_door = []
        self.green_speed_limit = []
        self.red_speed_limit = []
        self.green_underground = []
        self.red_underground = []
        self.green_default_path_blocks = [
            0, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, # 39
            85, 84, 83, 82, 81, 80, 79, 78, 77, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, # 33
            125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 29, 28, 27, 26, 25, 24, 23, # 33
            22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 151, 6, 5, 4, 3, 2, 1, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, # 42
            32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57 # 26
        ]
        self.red_default_path_blocks = [
            0, 9, 8, 7, 5, 4, 3, 2, 1, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48,
            49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 52, 51, 50, 49, 48, 47, 46, 45, 44, 43, 42, 41, 40, 39, 38, 37, 36, 35, 34, 33, 72, 73,
            74, 75, 76, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10
        ]
        
        if self.line == 'Green':
            self.current_block = self.green_default_path_blocks[0]  # int
        elif self.line == 'Red':
            self.current_block = self.red_default_path_blocks[0]    # int
        
        # Load the track layout data from GreenLine.json file in Track Layouts folder
        with open(os.path.join(os.path.dirname(__file__), 'Track Layouts', 'GreenLine.json'), 'r') as file:
            data = json.load(file)
            
            for entry in data:
                self.green_station.append(entry['Infrastructure'])
                self.green_underground.append(entry['Infrastructure'])
                self.green_station_door.append(entry['Station Side'])
                self.green_speed_limit.append(entry['Speed Limit (Km/Hr)'])
                
         # Load the track layout data from RedLine.json file in Track Layouts folder
        with open(os.path.join(os.path.dirname(__file__), 'Track Layouts', 'RedLine.json'), 'r') as file:
            data = json.load(file)
            
            for entry in data:
                self.red_station.append(entry['Infrastructure'])
                self.red_underground.append(entry['Infrastructure'])
                self.red_station_door.append(entry['Station Side'])
                self.red_speed_limit.append(entry['Speed Limit (Km/Hr)'])
        
    # Connect function for the Communicate class (Function is called every time the authority is changed OR decreased by 1)
    def handle_commanded_authority(self, authority: int):
        # print(f"Commanded Authority: {authority}")
        # # When the commanded authority goes from 1 -> 0, this print statement is not displayed, but it is displayed for 166 blocks
      
        if authority is not None:
            self.commanded_authority = authority - 1
            # print(f"Commanded Authority: {self.commanded_authority}")
        else:
            self.commanded_authority = 0
        self.commanded_authority_signal.emit(self.commanded_authority)
        
    # Connect function for the Communicate class
    def handle_polarity_change(self, polarity: bool):
        if polarity != self.polarity:
            self.polarity = polarity
            # self.speed_control.update_speed_limit(self.green_speed_limit[self.current_block])
            if self.commanded_authority >= 1:
                self.commanded_authority -= 1
                # # print(f"Commanded authority: {self.commanded_authority}")
                self.commanded_authority_signal.emit(self.commanded_authority)
                if self.commanded_authority == 0:
                    self.accept_authority = True
                    self.commanded_authority_signal.emit(0)
                    self.calculate_desired_speed()
                    # If current velocity is 0
                    # Start a timer to check every 100 ms
                    self.timer = QTimer()
                    self.timer.timeout.connect(self.check_current)
                    self.timer.start(100)
                    
            
            if self.line == 'Green':
                # Looping around the green line of the track
                if self.current_block == 57:
                    self.current_block = 0
                    # stop iterating over the blocks
                    self.iterate = False
                else:
                    if self.iterate == True:
                        current_index = self.green_default_path_blocks.index(self.current_block)
                        self.current_block = self.green_default_path_blocks[current_index + 1]
                    
                # self.check_current_block()
                self.check_block_underground()
                # self.calculate_desired_speed()
                # # print(f"Polarity: {self.polarity}")
            elif self.line == 'Red':
                # Looping around the green line of the track
                if self.current_block == 10:
                    self.current_block = 0
                    # stop iterating over the blocks
                    self.iterate = False
                else:
                    if self.iterate == True:
                        current_index = self.red_default_path_blocks.index(self.current_block)
                        self.current_block = self.red_default_path_blocks[current_index + 1]
                    
                # self.check_current_block()
                self.check_block_underground()
                # self.calculate_desired_speed()
                # # print(f"Polarity: {self.polarity}")
        
    def check_current(self):
        # print(f"Current Velocity: {self.speed_control.current_velocity}")
        # print(f"Current Block: {self.current_block}")
        if self.speed_control.current_velocity == 0.0 and not self.repeat:
            self.check_current_block()
            self.find_station_name()
            if self.speed_control.operation_mode == 0:
                self.brake_status.station_auto_mode = True
            self.accept_authority = True
        elif self.speed_control.current_velocity != 0.0 and self.repeat:
            self.repeat = False
            self.timer.stop()
        
    def check_block_underground(self):
        if self.line == 'Green':
            if "UNDERGROUND" in self.green_underground[self.current_block]:
                self.light.turn_on_exterior_lights()
                self.light.turn_on_interior_lights()
                # # print("Underground Block")
            elif "UNDERGROUND" not in self.green_underground[self.current_block] and (not self.light.manual_exterior_lights and not self.light.manual_interior_lights):  # Must check that the manual lights are not on
                self.light.turn_off_exterior_lights()
                self.light.turn_off_interior_lights()
            #     # # print("Above Ground Block")
        elif self.line == 'Red':
            if "UNDERGROUND" in self.red_underground[self.current_block]:
                self.light.turn_on_exterior_lights()
                self.light.turn_on_interior_lights()
                # # print("Underground Block")
            elif "UNDERGROUND" not in self.red_underground[self.current_block] and (not self.light.manual_exterior_lights and not self.light.manual_interior_lights):
                self.light.turn_off_exterior_lights()
                self.light.turn_off_interior_lights()
            #     # # print("Above Ground Block")
            
            
    def check_current_block(self):
        # # print(f"Current Block: {self.current_block}")
        # if self.commanded_authority == 0:
            # Open Doors
        if self.line == 'Green':
            if "Left" in self.green_station_door[self.current_block] and  "Right" not in self.green_station_door[self.current_block]:
                self.door.open_left_door()
                # # print("Left door opened")
            elif "Right" in self.green_station_door[self.current_block] and  "Left" not in self.green_station_door[self.current_block]:
                self.door.open_right_door()
                # # print("Right door opened")
            elif "Left" in self.green_station_door[self.current_block] and  "Right" in self.green_station_door[self.current_block]:
                self.door.open_left_door()
                self.door.open_right_door()
                # # print("Both doors opened")
            else:
                self.door.close_left_door()
                self.door.close_right_door()
                # # print("No doors opened")
                
            # Close doors after 60 seconds
            QTimer.singleShot(60000, self.close_doors)
            
        elif self.line == 'Red':
            if "Left" in self.red_station_door[self.current_block] and  "Right" not in self.red_station_door[self.current_block]:
                self.door.open_left_door()
                # # print("Left door opened")
            elif "Right" in self.red_station_door[self.current_block] and  "Left" not in self.red_station_door[self.current_block]:
                self.door.open_right_door()
                # # print("Right door opened")
            elif "Left" in self.red_station_door[self.current_block] and  "Right" in self.red_station_door[self.current_block]:
                self.door.open_left_door()
                self.door.open_right_door()
                # # print("Both doors opened")
            else:
                self.door.close_left_door()
                self.door.close_right_door()
                # # print("No doors opened")
                
            # Close doors after 60 seconds
            QTimer.singleShot(60000, self.close_doors)

    def close_doors(self):
        self.door.close_left_door()
        self.door.close_right_door()
        self.repeat = True
        if self.speed_control.operation_mode == 0:
            self.brake_status.station_auto_mode = False
        self.accept_authority = False
        self.commanded_authority_signal.emit(self.commanded_authority)
        # # print("Doors closed")
        
    def calculate_desired_speed(self):
        # if self.commanded_authority == 2:
        #     self.speed_control.desired_velocity = 10
        #     self.brake_status.reaching_station = True
        #     self.power_class.update_power_command(self.speed_control.current_velocity, self.speed_control.desired_velocity)
        # if self.commanded_authority == 1:
        #     self.speed_control.desired_velocity = 5
        #     self.brake_status.reaching_station = True
        #     self.power_class.update_power_command(self.speed_control.current_velocity, self.speed_control.desired_velocity)
        # if self.commanded_authority == 0:
        self.speed_control.desired_velocity = 0
        self.brake_status.reaching_station = True
        self.power_class.update_power_command(self.speed_control.current_velocity, self.speed_control.desired_velocity)
        
    def find_station_name(self):
        # Split the string by ';' and take the second part (station name)
        if self.line == 'Green':
            try:
                parts = self.green_station[self.current_block].split(';')
                if len(parts) > 1:
                    self.station_name = parts[1].strip()
                    self.announcement = f"Welcome to {self.station_name} Station"
                    # print(f"Station Name: {self.station_name}")
                    # print(f"Station Name: {self.station_name}")
                else:
                    # Handle cases where the expected format is not present
                    self.station_name = "Unknown"
                    self.announcement = "Welcome to the station"
            except IndexError:
                self.station_name = "Unknown"
                self.announcement = "Welcome to the station"
            # pass
        elif self.line == 'Red':
            try:
                parts = self.red_station[self.current_block].split(';')
                if len(parts) > 1:
                    self.station_name = parts[1].strip()
                    self.announcement = f"Welcome to {self.station_name} Station"
                    # print(f"Station Name: {self.station_name}")
                    # print(f"Station Name: {self.station_name}")
                else:
                    # Handle cases where the expected format is not present
                    self.station_name = "Unknown"
                    self.announcement = "Welcome to the station"
            except IndexError:
                self.station_name = "Unknown"
                self.announcement = "Welcome to the station"
            # pass

class Temperature(QObject):
    current_temperature_signal = pyqtSignal(float)
    
    def __init__(self):
        super().__init__()
        self.current_temperature = 65.0
        self.desired_temperature = 65.0
        
    # Use lambda function in the UI class to pass the temperature value
    def update_desired_temperature(self, temp):
        if 60 <= temp <= 75:
            self.desired_temperature = temp
            # # print(f"Desired temperature set to: {self.desired_temperature}°F")
            if self.current_temperature < self.desired_temperature:
                self.desired_temperature += 0.01
            else:
                self.desired_temperature -= 0.01
            self.reach_temperature()
        # else:
            
            # # print("Temperature out of range. Please enter a value between 60°F and 75.")

    def reach_temperature(self, k=0.3, time_step=0.5):
        initial_temp = self.current_temperature
        desired_temp = self.desired_temperature

        current_temp = initial_temp
        while abs(current_temp - desired_temp) > 0.01:  # Tolerance for stopping
            dT = k * (desired_temp - current_temp)
            
            current_temp += dT
            
            self.current_temperature = current_temp
            self.update_current_temp_display(current_temp)
            QCoreApplication.processEvents()  # Process events to update the UI
            # # print(f"Current Temperature: {current_temp:.2f}°F")
            time.sleep(time_step)

        # # print(f"Reached Desired Temperature: {current_temp:.2f}°F")

    def update_current_temp_display(self, current_temp):
        self.current_temperature = current_temp
        self.current_temperature_signal.emit(self.current_temperature)
            
class TrainEngineerUI(QWidget):
    def __init__(self, tuning: Tuning, power_class: PowerCommand):
        super().__init__()
        self.tuning = tuning
        self.power_class = power_class

        self.setWindowTitle('Train Engineer Controller')
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        layout.setSpacing(0)  # Remove spacing
        
        header_label = QLabel("Engineer's View")
        header_label.setStyleSheet("background-color: #2B78E4; color: white; font-size: 16px; padding: 5px;")
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header_label)
        
        self.table = QTableWidget(1, 3)
        self.table.setHorizontalHeaderLabels(['Train Number', 'Kp', 'Ki'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        train_number_item = QTableWidgetItem('1')  # Example train number
        train_number_item.setFlags(train_number_item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # Make non-editable
        self.table.setItem(0, 0, train_number_item)
        
        self.table.setItem(0, 1, QTableWidgetItem(str(self.tuning.get_kp())))
        self.table.setItem(0, 2, QTableWidgetItem(str(self.tuning.get_ki())))
        self.table.itemChanged.connect(self.update_values)
        
        # Hide the number column to the left of the train number column
        self.table.verticalHeader().setVisible(False)
        
        # Enable alternating row colors
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: white;
            }
            QTableWidget::item {
                color: black;
                background-color: #9FC5F8;
            }
            QTableWidget::item:alternate {
                background-color: white;
            }
            QTableWidget::item:selected {
                background-color: #2B78E4;
                color: white;
            }
            QHeaderView::section {
                background-color: lightgrey;
                color: black;
                font-weight: bold;
            }
        """)
        
        layout.addWidget(self.table)
        
        self.setLayout(layout)
        self.fill_empty_rows()
        
    def fill_empty_rows(self):
        # Calculate the number of rows that can fit in the available height
        row_height = self.table.verticalHeader().defaultSectionSize()
        available_height = self.table.viewport().height()
        num_rows = available_height // row_height
        
        # Add empty rows if needed
        current_row_count = self.table.rowCount()
        for _ in range(current_row_count, num_rows):
            self.table.insertRow(self.table.rowCount())
        
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.fill_empty_rows()
        
    def update_values(self, item):
        row = item.row()
        col = item.column()
          
        if col == 1:  # Kp column
            try:
                kp = float(item.text())
                # # print(f"Kp changed to {kp}")
                self.power_class.update_kp(kp)
                self.tuning.set_kp(kp)
                self.tuning.kp = kp
            except ValueError:
                item.setText(str(self.tuning.get_kp()))  # Reset to previous value if invalid
        elif col == 2:  # Ki column
            try:
                ki = float(item.text())
                # # print(f"Ki changed to {ki}")
                self.power_class.update_ki(ki)
                self.tuning.set_ki(ki)
                self.tuning.ki = ki
            except ValueError:
                item.setText(str(self.tuning.get_ki()))  # Reset to previous value if invalid
        
class TrainControllerUI(QWidget):
    # Pyqtsignals for UI Changes for Shell Class depending on the Train ID Selected
    train_id_signal = pyqtSignal(int)
    train_id_list_signal = pyqtSignal(list)
    
    def change_train_id(self, train_id_list):
        self.train_id_list = train_id_list
        # print(f"Train ID List Received in Controller File: {self.train_id_list}")
        

        # Clear the dropdown before updating items
        # SHOULD ONLY CLEAR IF THE ONLY ITEM IN THE DROPDOWN IS "No Trains Available"
        if self.dropdown.itemText(0) == "No Trains Available":
            self.dropdown.clear()
            self.selected_train_id = 0
            self.communicator2.selected_train_id.emit(self.selected_train_id)

        # Add all train IDs to the dropdown
        for train_id in self.train_id_list:
            if f"Train {train_id}" not in [self.dropdown.itemText(i) for i in range(self.dropdown.count())]:
                train_str = f"Train {train_id}"
                self.dropdown.addItem(train_str)
            # print(f"Train String: {train_str}")
            # self.dropdown.addItem(train_str)
            # print(f"Train ID Added: {train_str}")

        # Print Items in Dropdown - Works just not updating properly
        for i in range(self.dropdown.count()):
            pass
            # print(f"Item in Dropdown: {self.dropdown.itemText(i)}")

    
    def __init__(self, communicator: Communicate, communicator2: Communicate2, doors: Doors, tuning: Tuning, brake_class: BrakeStatus, power_class: PowerCommand, speed_control: SpeedControl, failure_modes: FailureModes, position: Position, lights: Lights, temperature: Temperature):
        super().__init__()
    
        # Train ID Variables
        self.selected_train_id = 0
        self.train_id_list = []
        
        # Make a copy of all sub-classes
        self.doors = doors
        self.tuning = tuning
        self.brake_class = brake_class
        self.power_class = power_class
        self.speed_control = speed_control
        self.failure_modes = failure_modes
        self.position = position
        self.lights = lights
        self.temperature = temperature
        
        # PyqtSignal Class to communicate with the Train Model
        self.communicator = communicator
        self.communicator2 = communicator2
        
        # self.power_class.power_command_signal.connect(self.change_power_UI)
        
        ###############################
        # User Interface STARTS HERE  #
        ###############################
        
        # Set the window title and background color
        self.setWindowTitle("Train Controller")
        self.setStyleSheet("background-color: lightgray;")

        # Main Layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 15, 30, 10)

        # Title Banner Layout
        title_banner = QHBoxLayout()
        title_banner.setSpacing(0)

        # Title Label
        title_label = QLabel("Train Controller")
        title_label.setStyleSheet("font: Times New Roman; font-size: 30px; font-weight: bold; color: white; background-color: #0055FF; border-radius: 10px; padding: 10px;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add the title label to the banner layout
        title_banner.addWidget(title_label)

        # Dropdown (ComboBox)
        self.dropdown = QComboBox()
        if self.train_id_list:
            self.dropdown.addItems([f"Train {train_id}" for train_id in self.train_id_list])
        else:
            self.dropdown.addItem("No Trains Available")
        self.dropdown.setStyleSheet("font: Times New Roman; font-size: 20px; padding: 5px; margin-left: 10px; border: 2px solid black;")  # Style the dropdown with black border
        self.dropdown.setFixedWidth(150)  # Set a fixed width for the dropdown if desired
        # self.dropdown.currentIndexChanged.connect(self.save_dropdown_selection)  # Connect to a method to save the selection
        
        # self.communicator2.train_id_list.connect(self.change_train_id)

        # Add dropdown to the title banner layout
        title_banner.addWidget(self.dropdown)

        # Title Container
        title_container = QWidget()
        title_container.setLayout(title_banner)
        title_container.setStyleSheet("background-color: #0055FF; border-radius: 10px;")  # Set background color and border radius
        title_container.setContentsMargins(0, 0, 0, 0)

        # Add the title container to the main layout
        main_layout.addWidget(title_container)

        # Main Grid Layout for UI Elements
        main_grid = QGridLayout()
        # Add your UI elements to the main_grid layout as needed

        # Example of adding the main grid to the main layout
        main_layout.addLayout(main_grid)
        
        
        
        ####################################################
        # SPEED & AUTHORITY CONTROLS IN THE USER INTERFACE #
        ####################################################
        #include which blocks are under the jurisdcition of each wayside


        # CURRENT SPEED SECTION
        self.current_speed_box = QVBoxLayout()
        self.current_speed_label = QLabel("Current Speed:")
        self.current_speed_label.setStyleSheet("padding-top: 10px; font-size: 14px; font-weight: bold; color: black; margin-top: 0px; margin-right: 100px")

        # Displaying the current speed in UI
        self.current_speed_edit = QLineEdit(f"{self.speed_control.current_velocity * 2.23694:.2f}")
        self.current_speed_edit.setText(self.current_speed_edit.text() + " mph")
        self.current_speed_edit.setEnabled(False)
        self.current_speed_edit.setStyleSheet("background-color: lightgray; max-width: 100px; border-radius: 5px; color: black; border: 2px solid black; padding: 2px;")
        self.current_speed_box.addWidget(self.current_speed_label)
        self.current_speed_box.addWidget(self.current_speed_edit)
        self.current_speed_box.addSpacerItem(QSpacerItem(0, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        main_grid.addLayout(self.current_speed_box, 0, 0)



        # COMMANDED SPEED SECTION
        self.commanded_speed_box = QVBoxLayout()
        self.commanded_speed_label = QLabel("Recommended Speed:")
        self.commanded_speed_label.setStyleSheet("font-size: 14px; font-weight: bold; color: black;")
        
        # Displaying the commanded speed in UI
        self.commanded_speed_edit = QLineEdit(str(self.speed_control.commanded_speed))
        self.commanded_speed_edit.setText(f"{self.speed_control.commanded_speed * 2.23694:.2f} mph")
        self.commanded_speed_edit.setEnabled(False)
        self.commanded_speed_edit.setStyleSheet("background-color: lightgray; max-width: 100px; border-radius: 5px; color: black; border: 2px solid black; padding: 2px;")
        self.commanded_speed_box.addWidget(self.commanded_speed_label)
        self.commanded_speed_box.addWidget(self.commanded_speed_edit)
        self.commanded_speed_box.addSpacerItem(QSpacerItem(0, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        main_grid.addLayout(self.commanded_speed_box, 1, 0)



        # COMMANDED AUTHORITY SECTION
        self.commanded_authority_box = QVBoxLayout()
        self.commanded_authority_label = QLabel("Commanded Authority:")
        self.commanded_authority_label.setStyleSheet("font-size: 14px; font-weight: bold; color: black;")
        self.commanded_authority_edit = QLineEdit(str(self.position.commanded_authority))
        self.commanded_authority_edit.setText(self.commanded_authority_edit.text() + " blocks")
        self.commanded_authority_edit.setEnabled(False)
        self.commanded_authority_edit.setStyleSheet("background-color: lightgray; max-width: 100px; border-radius: 5px; color: black; margin-bottom: 35px; border: 2px solid black; padding: 2px;")
        self.commanded_authority_box.addWidget(self.commanded_authority_label)
        self.commanded_authority_box.addWidget(self.commanded_authority_edit)
        main_grid.addLayout(self.commanded_authority_box, 2, 0)
        
        
        
        
        # SETPOINT SPEED SECTION
        self.setpoint_box = QVBoxLayout()
        self.setpoint_label = QLabel("Setpoint Speed")
        self.setpoint_label.setStyleSheet("padding-left: 20px; font-size: 30px; font-weight: bold; color: black;")
        self.setpoint_box.addWidget(self.setpoint_label, alignment=Qt.AlignmentFlag.AlignCenter)  # Add to setpoint_box with center alignment

        # Setpoint Layout
        self.setpoint_layout = QHBoxLayout()
        self.setpoint_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins

        # Setpoint Speed Input Box
        self.setpoint_speed_edit = QLineEdit()
        # Diable if self.operation_mode == 1
        self.setpoint_speed_edit.setEnabled(self.speed_control.operation_mode == 1)
        # Only number validation
        self.setpoint_speed_edit.setValidator(QDoubleValidator(0.0, 100.0, 2))
        self.setpoint_speed_edit.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.setpoint_speed_edit.setPlaceholderText("50")
        self.setpoint_speed_edit.setStyleSheet("margin-left: 50px; max-width: 100px; color: black; border: 2px solid black; border-radius: 5px; padding: 5px;")
        self.setpoint_speed_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Setpoint Speed Unit Label
        self.setpoint_unit = QLabel("mph")
        self.setpoint_unit.setStyleSheet("font-size: 12px; color: black;")
        
        # Setpoint Confirm Button
        self.setpoint_confirm = QPushButton("OK")
        self.setpoint_confirm.setStyleSheet("background-color: green; color: white; border: 2px solid black; padding: 5px; border-radius: 5px;")
        self.setpoint_confirm.clicked.connect(self.send_setpoint_speed)

        # Add widgets to setpoint_layout
        self.setpoint_layout.addWidget(self.setpoint_speed_edit, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setpoint_layout.addWidget(self.setpoint_unit, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setpoint_layout.addWidget(self.setpoint_confirm, alignment=Qt.AlignmentFlag.AlignCenter)

        # Add setpoint_layout to setpoint_box
        self.setpoint_box.addLayout(self.setpoint_layout)

        # Finally, add setpoint_box to the main grid at the desired position
        main_grid.addLayout(self.setpoint_box, 1, 1, 1, 1, Qt.AlignmentFlag.AlignCenter)
        
        
        
        
        #############################################
        # BOTH BRAKE CONTROLS IN THE USER INTERFACE #
        #############################################

        # Service Brake Button
        self.brake_button = QPushButton("SERVICE BRAKE")
        self.brake_button.setStyleSheet("margin-top: 40px; background-color: yellow; font-size: 16px; border-radius: 10px; font-weight: bold; color: black; border: 3px solid black; padding-top: 20px; max-width: 150px; padding-bottom: 20px")
        self.brake_button.pressed.connect(self.divet_in_service_brake_button)
        self.brake_button.released.connect(self.reset_service_brake_button_style)
        self.brake_button.pressed.connect(self.brake_class.manual_apply_service_brake)
        self.brake_button.released.connect(self.brake_class.manual_no_apply_service_brake)
        main_grid.addWidget(self.brake_button, 8, 0)  # Ensure it spans across two columns
        
        
        # Emergency Brake Button
        self.emergency_brake_button = QPushButton("EMERGENCY BRAKE")
        self.emergency_brake_button.setStyleSheet("border: 3px solid black; margin-left: 40px; background-color: red; color: white; font-size: 20px; font-weight: bold; padding: 50px; border-radius: 10px;")
        self.emergency_brake_button.pressed.connect(self.divet_in_emergency_brake_buttons)
        self.emergency_brake_button.released.connect(self.reset_emergency_brake_button_style)
        self.emergency_brake_button.pressed.connect(self.brake_class.manual_apply_emergency_brake)
        self.emergency_brake_button.released.connect(self.brake_class.manual_no_apply_emergency_brake)
        
        # self.emergency_brake_button.pressed.connect(self.handle_emergency_brake_button)
        # self.emergency_brake_button.pressed.connect(self.divet_in_emergency_brake_buttons)
        # self.emergency_brake_button.released.connect(self.reset_emergency_brake_button_style)
        # self.emergency_brake_button.pressed.connect(lambda: self.brake_class.pressed_emergency_brake.emit(True))
        # self.emergency_brake_button.pressed.connect(self.divet_in_emergency_brake_buttons)
        # self.emergency_brake_button.released.connect(self.reset_emergency_brake_button_style)
        # self.emergency_brake_button.released.connect(
        #     lambda: self.brake_class.pressed_emergency_brake.emit(False)
        # )
        main_grid.addWidget(self.emergency_brake_button, 8, 3)
        
        
        
        
        #############################################
        # INDICATORS CONTROLS IN THE USER INTERFACE #
        #############################################

        # INTERIOR LIGHTS CONTROL
        self.interior_lights_layout = QHBoxLayout()
        self.interior_lights_label = QLabel("Interior Lights Status:")
        self.interior_lights_label.setStyleSheet("font-size: 14px; font-weight: bold; color: black; padding-left: 40px;")
        self.interior_lights_status = QPushButton("OFF")
        self.interior_lights_status.setStyleSheet("background-color: #888c8b; max-width: 80px; border: 2px solid black; border-radius: 5px; padding: 3px;")
        self.interior_lights_status.pressed.connect(self.handle_interior_lights)
        self.interior_lights_layout.addWidget(self.interior_lights_label)
        self.interior_lights_layout.addWidget(self.interior_lights_status)
        self.interior_lights_layout.addSpacerItem(QSpacerItem(20, 20))
        main_grid.addLayout(self.interior_lights_layout, 2, 3)
        
        
        # EXTERIOR LIGHTS CONTROL
        self.exterior_lights_layout = QHBoxLayout()
        self.exterior_lights_label = QLabel("Exterior Lights Status:")
        self.exterior_lights_label.setStyleSheet("font-size: 14px; font-weight: bold; color: black; padding-left: 40px;")
        self.exterior_lights_status = QPushButton("OFF")
        self.exterior_lights_status.setStyleSheet("background-color: #888c8b; max-width: 80px; border: 2px solid black; border-radius: 5px; padding: 3px;")
        self.exterior_lights_status.pressed.connect(self.handle_exterior_lights)
        self.exterior_lights_layout.addWidget(self.exterior_lights_label)
        self.exterior_lights_layout.addWidget(self.exterior_lights_status)
        self.exterior_lights_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum))
        main_grid.addLayout(self.exterior_lights_layout, 3, 3)
        
        
        # BRAKE STATUS CONTROL
        self.brake_status_layout = QHBoxLayout()
        self.brake_status_label = QLabel("Driver Brake Status:")
        self.brake_status_label.setStyleSheet("font-size: 14px; font-weight: bold; color: black; padding-left: 40px;")
        self.brake_status = QPushButton("OFF")
        # stylesheet for off
        self.brake_status.setStyleSheet("background-color: #888c8b; max-width: 80px; border: 2px solid black; border-radius: 5px; padding: 3px;")
        self.brake_status_layout.addWidget(self.brake_status_label)
        self.brake_status_layout.addWidget(self.brake_status)
        self.brake_status_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum))
        main_grid.addLayout(self.brake_status_layout, 4, 3)
        
        
        # PASSENGER BRAKE STATUS CONTROL
        self.passenger_brake_layout = QHBoxLayout()
        self.passenger_brake_label = QLabel("Passenger Brake Status:")
        self.passenger_brake_label.setStyleSheet("font-size: 14px; font-weight: bold; color: black; padding-left: 40px;")
        self.passenger_brake_status = QPushButton("OFF")
        self.passenger_brake_status.setStyleSheet("background-color: #888c8b; max-width: 80px; border: 2px solid black; border-radius: 5px; padding: 3px;")
        self.passenger_brake_layout.addWidget(self.passenger_brake_label)
        self.passenger_brake_layout.addWidget(self.passenger_brake_status)
        self.passenger_brake_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum))
        main_grid.addLayout(self.passenger_brake_layout, 5, 3)
        
        
        # RIGHT DOOR STATUS CONTROL
        self.right_door_layout = QHBoxLayout()
        self.right_door_status_label = QLabel("Right Door Status:")
        self.right_door_status_label.setStyleSheet("font-size: 14px; font-weight: bold; color: black; padding-left: 40px;")
        self.right_door_status = QPushButton("CLOSE")
        self.right_door_status.setStyleSheet("background-color: red; max-width: 80px; border: 2px solid black; border-radius: 5px; padding: 3px;")
        self.right_door_status.pressed.connect(self.handle_right_door)
        self.right_door_layout.addWidget(self.right_door_status_label)
        self.right_door_layout.addWidget(self.right_door_status)
        self.right_door_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum))
        main_grid.addLayout(self.right_door_layout, 6, 3)
        
        
        # LEFT DOOR STATUS CONTROL
        self.left_door_layout = QHBoxLayout()
        self.left_door_status_label = QLabel("Left Door Status:")
        self.left_door_status_label.setStyleSheet("font-size: 14px; font-weight: bold; color: black; padding-left: 40px;")
        self.left_door_status = QPushButton("CLOSE")
        self.left_door_status.setStyleSheet("background-color: red; max-width: 80px; border: 2px solid black; border-radius: 5px; padding: 3px;")
        self.left_door_status.pressed.connect(self.handle_left_door)
        self.left_door_layout.addWidget(self.left_door_status_label)
        self.left_door_layout.addWidget(self.left_door_status)
        self.left_door_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum))
        main_grid.addLayout(self.left_door_layout, 7, 3)
        
        
        
        
        ################################################
        # FAILURE MODES CONTROLS IN THE USER INTERFACE #
        ################################################
        
        # TRAIN ENGINE FAILURE
        self.train_engine_failure = QVBoxLayout()
        self.train_engine_failure.setSpacing(0)
        
        # Create the label for "Train Engine Failure"
        self.train_engine_fail_label = QLabel('<div style="text-align: center;">Train Engine<br>Failure</div>')
        self.train_engine_fail_label.setStyleSheet("font-size: 12px; font-weight: bold; color: black;")

        # Create the green indicator button
        self.engine_fail_indicator = QPushButton()
        self.engine_fail_indicator.setFixedSize(40, 40)  # Set a fixed size for the indicator button
        self.engine_fail_indicator = QPushButton()
        self.engine_fail_indicator.setFixedSize(40, 40)  # Set a fixed size for the indicator button
        self.engine_fail_indicator.setStyleSheet("background-color: green; border-radius: 20px; border: 2px solid black;")  # Green for no failure
        
        # Add widgets to the vertical box layout
        self.train_engine_failure.addWidget(self.train_engine_fail_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.train_engine_failure.addWidget(self.engine_fail_indicator, alignment=Qt.AlignmentFlag.AlignCenter)
        
        
        # BRAKE FAILURE
        self.brake_failure = QVBoxLayout()
        
        # Create the label for "Brake Failure"
        self.brake_fail_label = QLabel("Brake Failure")
        self.brake_fail_label.setStyleSheet("font-size: 12px; font-weight: bold; color: black; padding-left: 10px;")
        
        # Create the green indicator button
        self.brake_fail_indicator = QPushButton()
        self.brake_fail_indicator.setFixedSize(40, 40)  # Set a fixed size for the indicator button
        self.brake_fail_indicator.setStyleSheet("background-color: green; border-radius: 20px; border: 2px solid black; padding-left: 100px;")
        
        # Add widgets to the vertical box layout
        self.brake_failure.addWidget(self.brake_fail_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.brake_failure.addWidget(self.brake_fail_indicator, alignment=Qt.AlignmentFlag.AlignCenter)
        
        
        # SIGNAL PICKUP FAILURE
        self.signal_pickup_failure = QVBoxLayout()
        
        # Create the label for "Signal Pickup Failure"
        self.signal_fail_label =  QLabel('<div style="text-align: center;">Signal Pickup<br>Failure</div>')
        self.signal_fail_label.setStyleSheet("font-size: 12px; font-weight: bold; color: black; padding-left: 10px;")
        
        # Create the green indicator button
        self.signal_fail_indicator = QPushButton()
        self.signal_fail_indicator.setFixedSize(40, 40)  # Set a fixed size for the indicator button
        self.signal_fail_indicator.setStyleSheet("background-color: green; border-radius: 20px; border: 2px solid black; padding-left: 10px;")
        
        # Add widgets to the vertical box layout
        self.signal_pickup_failure.addWidget(self.signal_fail_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.signal_pickup_failure.addWidget(self.signal_fail_indicator, alignment=Qt.AlignmentFlag.AlignCenter)
        
        
        # Add all failure modes to a horizontal layout
        self.all_failure_modes = QHBoxLayout()
        self.all_failure_modes.setSpacing(5)
        
        self.all_failure_modes.addLayout(self.train_engine_failure)
        self.all_failure_modes.addLayout(self.brake_failure)
        self.all_failure_modes.addLayout(self.signal_pickup_failure)
        
        # Add the failure mode layout to the main grid
        main_grid.addLayout(self.all_failure_modes, 8, 1)
        
        
        
        
        ##############################################
        # TEMPERATURE CONTROLS IN THE USER INTERFACE #
        ##############################################
        
        # CURRENT TEMPERATURE SECTION
        
        # Create a vertical box layout for the current temperature
        self.current_temp_box = QVBoxLayout()
        self.current_temp_label = QLabel("Current Train Temperature:")
        self.current_temp_label.setStyleSheet("font-size: 14px; font-weight: bold; color: black; padding-left: 40px;")
        self.current_temp_edit = QLineEdit(f"{self.temperature.current_temperature}")
        self.current_temp_edit.setText(f"{self.temperature.current_temperature} °F")
        
        # Set the current temperature to be uneditable
        self.current_temp_edit.setEnabled(False)
        self.current_temp_edit.setStyleSheet("background-color: lightgray; max-width: 100px; color: black; margin-left: 45px; border: 2px solid black; border-radius: 5px; padding: 2px;")
        self.current_temp_box.addWidget(self.current_temp_label)
        self.current_temp_box.addWidget(self.current_temp_edit)
        self.current_temp_box.addSpacerItem(QSpacerItem(0, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        main_grid.addLayout(self.current_temp_box, 0, 3)
        
        
        # DESIRED TEMPERATURE SECTION
        
        # Create a vertical box layout for the desired temperature
        self.desired_temp_box = QVBoxLayout()
        self.desired_temp_label = QLabel("Desired Train Temperature:")
        self.desired_temp_label.setStyleSheet("font-size: 14px; font-weight: bold; color: black; padding-left: 40px;")
        
        # Create a QLineEdit for numeric temperature input
        self.temp_input = QLineEdit()
        self.temp_input.setStyleSheet("max-width: 100px; color: black; margin-left: 40px; border: 2px solid black; border-radius: 5px; padding: 3px;")
        self.temp_input.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.temp_input.setPlaceholderText("Enter temperature (70°F to 100°F)")  # Optional placeholder text
        # self.temp_input.editingFinished.connect(self.send_desired_temperature)
        self.temp_input.editingFinished.connect(lambda: self.temperature.update_desired_temperature(float(self.temp_input.text())))
        self.desired_temp_box.addWidget(self.desired_temp_label)
        self.desired_temp_box.addWidget(self.temp_input)
        
        # Add the QLineEdit to the main grid at the desired position
        main_grid.addLayout(self.desired_temp_box, 1, 3)
        
        
        

        ###################################################
        # OPERATIONAL MODE CONTROLS IN THE USER INTERFACE #
        ###################################################
        
        # OPERATIONAL MODE
        self.operational_mode_label = QLabel("Operational Mode:")
        self.operational_mode_label.setStyleSheet("font-size: 14px; font-weight: bold; color: black; margin-bottom 30px;")
        main_grid.addWidget(self.operational_mode_label, 4, 0)
        
        # MANUAL MODE BUTTON
        self.manual_button = QPushButton("Manual")
        self.manual_button.setStyleSheet("margin-top: 10px; margin-left: 10px; background-color: gray; color: white; max-width: 100px; border-radius: 5px; padding-top: 10px; padding-bottom: 10px; border: 2px solid black;")
        self.manual_button.clicked.connect(self.send_manual_mode)
        main_grid.addWidget(self.manual_button, 5, 0)

        # AUTOMATIC MODE BUTTON
        self.automatic_button = QPushButton("Automatic")
        self.automatic_button.setStyleSheet("margin-top: 10px; margin-left: 10px; background-color: green; color: white; max-width: 100px; border-radius: 5px; padding-top: 10px; padding-bottom: 10px; border: 2px solid black;")
        self.automatic_button.clicked.connect(self.send_automatic_mode)
        main_grid.addWidget(self.automatic_button, 6, 0)
        
        
        
        ################################################
        # POWER COMMAND CONTROLS IN THE USER INTERFACE #
        ################################################
        
        # POWER COMMAND SECTION
        self.power_command_label = QLabel("Power Command")
        self.power_command_label.setStyleSheet("font-size: 25px; font-weight: bold; color: black; padding-left: 22px;")
    
        self.power_command_layout = QHBoxLayout()
        self.power_command_edit = QLineEdit(str(self.power_class.power_command))
        
        self.power_command_edit.setStyleSheet("font-size: 20px; max-width: 100px; color: black; border: 2px solid black; border-radius: 5px; padding: 5px;")
        self.power_command_edit.setEnabled(False)
        self.power_command_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.power_unit = QLabel("kWatts")
        self.power_unit.setStyleSheet("font-size: 16px; color: black;")
        self.power_command_edit.setStyleSheet("margin-left: 50px; max-width: 100px; color: black; border: 2px solid black; border-radius: 5px; padding: 5px; background-color: lightgray;")
        self.power_unit.setStyleSheet("font-size: 12px; color: black; background-color: lightgray;")
        self.power_command_layout.addWidget(self.power_command_edit, alignment=Qt.AlignmentFlag.AlignCenter)
        self.power_command_layout.addWidget(self.power_unit, alignment=Qt.AlignmentFlag.AlignCenter)
        
        main_grid.addWidget(self.power_command_label, 4, 1, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        main_grid.addLayout(self.power_command_layout, 5, 1, 1, 1, Qt.AlignmentFlag.AlignCenter)
        
        # # Making a button to test passenger brake
        # self.passenger_brake_button = QPushButton("Passenger Brake")
        # self.passenger_brake_button.setStyleSheet("background-color: red; color: white; border: 2px solid black; padding: 5px; border-radius: 5px;")
        # self.passenger_brake_button.pressed.connect(lambda: self.brake_class.handle_passenger_brake_command(True))
        # main_grid.addWidget(self.passenger_brake_button, 7, 0)

        
        # Add Components to the Main Layout
        main_layout.addLayout(title_banner)
        main_layout.addLayout(main_grid)
        

        # Set Main Layout
        self.setLayout(main_layout)
        
        
    
    def handle_emergency_brake_button(self):
        # self.brake_class.handle_emergency_brake_command(self.brake_class.driver_emergency_brake_command)
        if self.brake_class.driver_emergency_brake_command:
            self.brake_class.no_apply_emergency_brake()
            # self.reset_emergency_brake_button_style()
        else:
            self.brake_class.apply_emergency_brake()
            # self.divet_in_emergency_brake_buttons()

    def toggle_service_brake_button(self):
        if self.brake_class.manual_driver_service_brake_command:
            self.brake_class.manual_no_apply_service_brake()
            self.reset_service_brake_button_style()
        else:
            self.brake_class.manual_apply_service_brake()
            self.divet_in_service_brake_button()




    ############################################
    # FUNCTIONS TO UPDATE THE UI OF THE DRIVER #
    ############################################
    
    def update_current_speed(self, current_speed: float):
        self.current_speed_edit.setText(f"{current_speed * 2.23:.2f} mph")
    
    def update_commanded_speed(self, commanded_speed: float):
        self.commanded_speed_edit.setText(f"{commanded_speed * 2.237:.2f} mph")
    
    def update_commanded_authority(self, commanded_authority: float):
        self.commanded_authority_edit.setText(f"{commanded_authority} blocks")
        
    def update_left_door(self, door_status: bool):
        if door_status:
            self.left_door_status.setText("OPEN")
            self.left_door_status.setStyleSheet("background-color: green; max-width: 80px; border: 2px solid black; border-radius: 5px; padding: 3px;")
        else:
            self.left_door_status.setText("CLOSE")
            self.left_door_status.setStyleSheet("background-color: red; max-width: 80px; border: 2px solid black; border-radius: 5px; padding: 3px;")
            
    def update_right_door(self, door_status: bool):
        if door_status:
            self.right_door_status.setText("OPEN")
            self.right_door_status.setStyleSheet("background-color: green; max-width: 80px; border: 2px solid black; border-radius: 5px; padding: 3px;")
        else:
            self.right_door_status.setText("CLOSE")
            self.right_door_status.setStyleSheet("background-color: red; max-width: 80px; border: 2px solid black; border-radius: 5px; padding: 3px;")
        
    def handle_right_door(self):
        if self.speed_control.current_velocity == 0:
            if self.doors.right_door:
                self.doors.close_right_door()
            else:
                self.doors.open_right_door()
            
    def handle_left_door(self):
        if self.speed_control.current_velocity == 0:
            if self.doors.left_door:
                self.doors.close_left_door()
            else:
                self.doors.open_left_door()
            
    def handle_interior_lights(self):
        if self.speed_control.operation_mode == 1:
            if self.lights.manual_interior_lights:
                self.lights.manual_turn_off_interior_lights()
            else:
                # # print("Turning on interior lights")
                self.lights.manual_turn_on_interior_lights()
            
    def handle_exterior_lights(self):
        if self.speed_control.operation_mode == 1:
            if self.lights.manual_exterior_lights:
                self.lights.manual_turn_off_exterior_lights()
            else:
                self.lights.manual_turn_on_exterior_lights()
            
    def update_exterior_lights(self, lights_status: bool):
        if lights_status:
            self.exterior_lights_status.setText("ON")
            self.exterior_lights_status.setStyleSheet("background-color: #f5c842; max-width: 80px; border: 2px solid black; border-radius: 5px; padding: 3px;")
        else:
            self.exterior_lights_status.setText("OFF")
            self.exterior_lights_status.setStyleSheet("background-color: #888c8b; max-width: 80px; border: 2px solid black; border-radius: 5px; padding: 3px;")
            
    def update_interior_lights(self, lights_status: bool):
        if lights_status:
            self.interior_lights_status.setText("ON")
            self.interior_lights_status.setStyleSheet("background-color: #f5c842; max-width: 80px; border: 2px solid black; border-radius: 5px; padding: 3px;")
        else:
            self.interior_lights_status.setText("OFF")
            self.interior_lights_status.setStyleSheet("background-color: #888c8b; max-width: 80px; border: 2px solid black; border-radius: 5px; padding: 3px;")
    
    def update_power_command(self, power_command: float):
        # # print(f"Power Commandddd: {power_command}")
        # # print(f"Kp: {self.tuning.kp}")
        # # print(f"Ki: {self.tuning.ki}")
        self.power_command_edit.setText(f"{power_command / 1000:.2f}")
    
    def update_engine_failure_status(self, failure: bool):
        if failure:
            self.engine_fail_indicator.setStyleSheet("background-color: red; border-radius: 20px; border: 2px solid black;")  # Red for failure
        else:
            self.engine_fail_indicator.setStyleSheet("background-color: green; border-radius: 20px; border: 2px solid black;")  # Green for no failure
            
    def update_brake_failure_status(self, failure: bool):
        if failure:
            self.brake_fail_indicator.setStyleSheet("background-color: red; border-radius: 20px; border: 2px solid black;")  # Red for failure
        else:
            self.brake_fail_indicator.setStyleSheet("background-color: green; border-radius: 20px; border: 2px solid black;")  # Green for no failure
                
    def update_signal_failure_status(self, failure: bool):
        if failure:
            self.signal_fail_indicator.setStyleSheet("background-color: red; border-radius: 20px; border: 2px solid black;")  # Red for failure
        else:
            self.signal_fail_indicator.setStyleSheet("background-color: green; border-radius: 20px; border: 2px solid black;")  # Green for no failure
                
    def update_current_temperature(self, current_temperature: float):
        self.current_temp_edit.setText(f"{current_temperature:.2f} °F")
        # if current_temperature == self.temperature.desired_temperature:
        #     self.temp_input.clear()
    
    def update_passenger_brake_status(self, passenger_brake: bool):
        if passenger_brake:
            if self.brake_class.passenger_brake and not self.brake_class.manual_driver_emergency_brake_command:
                self.passenger_brake_status.setText("ON")
                self.passenger_brake_status.setStyleSheet("background-color: #f5c842; max-width: 80px; border: 2px solid black; border-radius: 5px; padding: 3px;")
            self.divet_in_emergency_brake_buttons()
        else:
            self.passenger_brake_status.setText("OFF")
            self.passenger_brake_status.setStyleSheet("background-color: #888c8b; max-width: 80px; border: 2px solid black; border-radius: 5px; padding: 3px;")
            self.reset_emergency_brake_button_style()
            
    def send_setpoint_speed(self):
        # 20 mph = 8.9408 m/s
        # print(f"Setpoint Speed: {float(self.setpoint_speed_edit.text()) * 0.44704}")
        if float(self.setpoint_speed_edit.text()) * 0.44704 > self.speed_control.max_speed:
            # Set setpoint speed input to max speed value
            self.setpoint_speed_edit.setText(f"{self.speed_control.max_speed * 2.23694:.2f}")
            
        if float(self.setpoint_speed_edit.text()) * 0.44704 < self.speed_control.desired_velocity:
            self.brake_class.entered_lower = True
            self.speed_control.desired_velocity = float(self.setpoint_speed_edit.text()) * 0.44704
            self.power_class.update_power_command(self.speed_control.current_velocity, self.speed_control.desired_velocity)
        else:
            self.speed_control.desired_velocity = float(self.setpoint_speed_edit.text()) * 0.44704
            
            self.speed_control.update_setpoint_speed_calculations(float(self.setpoint_speed_edit.text()) * 0.44704)
            
    def send_manual_mode(self):
        # Enable setpoint speed input
        self.setpoint_speed_edit.setEnabled(True)
        self.speed_control.set_manual_mode()
        self.manual_button.setStyleSheet("margin-top: 10px; margin-left: 10px; background-color: green; color: white; max-width: 100px; border-radius: 5px; padding-top: 10px; padding-bottom: 10px; border: 2px solid black;")
        self.automatic_button.setStyleSheet("margin-top: 10px; margin-left: 10px; background-color: gray; color: white; max-width: 100px; border-radius: 5px; padding-top: 10px; padding-bottom: 10px; border: 2px solid black;")
        
    def send_automatic_mode(self):
        # Disable setpoint speed input
        self.setpoint_speed_edit.setEnabled(False)
        # self.setpoint_speed_edit.clear()
        self.speed_control.set_auto_mode()
        self.automatic_button.setStyleSheet("margin-top: 10px; margin-left: 10px; background-color: green; color: white; max-width: 100px; border-radius: 5px; padding-top: 10px; padding-bottom: 10px; border: 2px solid black;")
        self.manual_button.setStyleSheet("margin-top: 10px; margin-left: 10px; background-color: gray; color: white; max-width: 100px; border-radius: 5px; padding-top: 10px; padding-bottom: 10px; border: 2px solid black;")
        
    def update_driver_brake_status(self, brake_status: bool):
        if brake_status:
            self.brake_status.setText("ON")
            self.brake_status.setStyleSheet("background-color: #f5c842; max-width: 80px; border: 2px solid black; border-radius: 5px; padding: 3px;")
        else:
            self.brake_status.setText("OFF")
            self.brake_status.setStyleSheet("background-color: #888c8b; max-width: 80px; border: 2px solid black; border-radius: 5px; padding: 3px;")
            
    def update_service_brake_status(self, brake_status: bool):
        if brake_status or self.brake_class.manual_driver_service_brake_command:
            # print(f"Service Brake Status: {brake_status}")
            # self.brake_status.setText("ON")
            # self.brake_status.setStyleSheet("background-color: #f5c842; max-width: 80px; border: 2px solid black; border-radius: 5px; padding: 3px;")
            # Divet in service break in UI
            self.divet_in_service_brake_button()
        else:
            # self.brake_status.setText("OFF")
            # self.brake_status.setStyleSheet("background-color: #888c8b; max-width: 80px; border: 2px solid black; border-radius: 5px; padding: 3px;")
            self.reset_service_brake_button_style()
            
    def update_emergency_brake_status(self, brake_status: bool):
        if brake_status:
            # print(f"Emergency Brake Status: {brake_status}")
            # self.brake_status.setText("ON")
            # self.brake_status.setStyleSheet("background-color: #f5c842; max-width: 80px; border: 2px solid black; border-radius: 5px; padding: 3px;")
            self.divet_in_emergency_brake_buttons()
        else:
            # self.brake_status.setText("OFF")
            # self.brake_status.setStyleSheet("background-color: #888c8b; max-width: 80px; border: 2px solid black; border-radius: 5px; padding: 3px;")
            self.reset_emergency_brake_button_style()
        
    # def send_desired_temperature(self):
    #     self.temperature.desired_temperature = float(self.temp_input.text())
    #     # # print(f"Desired Temperature: {self.temperature.desired_temperature}")
        
    def save_dropdown_selection(self):
        # If Train 1 is selected, then the currentIndex is 0 AND we should emit 1 as the train id to the shell class
        # self.communicator2.selected_train_id.emit(self.dropdown.currentIndex() + 1)
        
        # Index of the selected train id. eg. If Train 1 is selected, then the index is 0
        index_of_train_id = self.dropdown.currentIndex()
        
        # print(f"Index of Train ID: {index_of_train_id}")
        
        # We want to index the variable lists in the shell class with this index
        self.selected_train_id = self.train_id_list[index_of_train_id]
        
        self.communicator2.selected_train_id.emit(self.selected_train_id)
        print(f"Selected Train ID: {self.selected_train_id}")
        
        
    ####################################################################
    # FUNCTIONS TO HANDLE THE BACKEND LOGIC OF TRAIN CONTROLLER MODULE #
    ####################################################################
    
    def write_to_train_model(self):
        self.communicator.power_command_signal.emit(self.power_class.power_command)
        self.communicator.service_brake_command_signal.emit(self.brake_class.driver_service_brake_command)
        self.communicator.emergency_brake_command_signal.emit(self.brake_class.driver_emergency_brake_command) 
        self.communicator.desired_temperature_signal.emit(self.temperature.desired_temperature)
        self.communicator.exterior_lights_signal.emit(self.lights.interior_lights)
        self.communicator.interior_lights_signal.emit(self.lights.exterior_lights)
        self.communicator.left_door_signal.emit(self.doors.left_door)
        self.communicator.right_door_signal.emit(self.doors.right_door)
        self.communicator.announcement_signal.emit(self.position.announcement)
    
    def read_from_train_model(self):
        self.communicator.current_velocity_signal.connect(self.speed_control.handle_current_velocity)
        self.communicator.commanded_speed_signal.connect(self.speed_control.handle_commanded_speed)
        self.communicator.commanded_authority_signal.connect(self.position.handle_commanded_authority)
        self.communicator.engine_failure_signal.connect(self.failure_modes.handle_engine_failure)
        self.communicator.brake_failure_signal.connect(self.failure_modes.handle_brake_failure)
        self.communicator.signal_failure_signal.connect(self.failure_modes.handle_signal_failure)
        self.communicator.passenger_brake_command_signal.connect(self.brake_class.handle_passenger_brake_command)
        self.communicator.actual_temperature_signal.connect(self.temperature.update_current_temp_display)
        self.communicator.polarity_signal.connect(self.position.handle_polarity_change)
        

    ############################################
    # BRAKE DIVET FUNCTIONS FOR USER INTERFACE #
    ############################################
    
    def divet_in_service_brake_button(self):
        self.brake_button.setStyleSheet("margin-top: 40px; background-color: #B8860B; font-size: 16px; border-radius: 10px; font-weight: bold; color: black; border: 3px solid black; padding-top: 20px; max-width: 150px; padding-bottom: 20px;")
        self.reset_brake_status(self.brake_class.driver_service_brake_command, self.brake_class.driver_emergency_brake_command)
        
    def reset_service_brake_button_style(self):
        self.brake_button.setStyleSheet("margin-top: 40px; background-color: yellow; font-size: 16px; border-radius: 10px; font-weight: bold; color: black; border: 3px solid black; padding-top: 20px; max-width: 150px; padding-bottom: 20px;")
        self.reset_brake_status(self.brake_class.driver_service_brake_command, self.brake_class.driver_emergency_brake_command)
        
    def divet_in_emergency_brake_buttons(self):
        self.emergency_brake_button.setStyleSheet("border: 3px solid black; margin-left: 40px; background-color: darkred; color: white; font-size: 20px; font-weight: bold; padding: 50px; border-radius: 10px;")
        self.reset_brake_status(self.brake_class.driver_service_brake_command, self.brake_class.driver_emergency_brake_command)
        
    def reset_emergency_brake_button_style(self):
        self.emergency_brake_button.setStyleSheet("border: 3px solid black; margin-left: 40px; background-color: red; color: white; font-size: 20px; font-weight: bold; padding: 50px; border-radius: 10px;")
        # Turn the brake status to OFF
        # self.brake_status.setText("OFF")
        # self.brake_status.setStyleSheet("background-color: #888c8b; max-width: 80px; border: 2px solid black; border-radius: 5px; padding: 3px;")
        self.reset_brake_status(self.brake_class.driver_service_brake_command, self.brake_class.driver_emergency_brake_command)

    def reset_brake_status(self, service_brake: bool = False, emergency_brake: bool = False):
        if service_brake or emergency_brake:
            self.brake_status.setText("ON")
            self.brake_status.setStyleSheet("background-color: #f5c842; max-width: 80px; border: 2px solid black; border-radius: 5px; padding: 3px;")
        else:
            self.brake_status.setText("OFF")
            self.brake_status.setStyleSheet("background-color: #888c8b; max-width: 80px; border: 2px solid black; border-radius: 5px; padding: 3px;")
    
    # def change_power_UI(self):
    #     self.power_command_edit.setText(f"{self.power_class.power_command / 1000:.2f}")

    
#################
# MAIN FUNCTION #
#################

# if __name__ == "__main__":#
#     app = QApplication([])
#     communicator = Communicate()
#     doors = Doors()
#     tuning = Tuning()
#     brake_status = BrakeStatus(communicator)
#     power_class = PowerCommand(brake_status, tuning)
#     speed_control = SpeedControl(power_class, brake_status, communicator)
#     failure_modes = FailureModes(speed_control, power_class)
#     lights = Lights(speed_control)
#     temperature = Temperature()
#     communicator = Communicate()
#     position = Position(doors, failure_modes, speed_control, power_class, lights, communicator)
#     window = TrainControllerUI(communicator, doors, tuning, brake_status, power_class, speed_control, failure_modes, position, lights, temperature)
#     window.show()
    
#     # Show engineer window as well
#     engineer_window = TrainEngineerUI(tuning)
#     engineer_window.show()
#     app.exec()