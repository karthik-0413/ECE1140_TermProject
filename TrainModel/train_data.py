# train_data.py

from PyQt6.QtCore import QObject, pyqtSignal, QTimer
from power import calculate_train_speed
import random

class TrainData(QObject):
    """Class representing the data and state of all trains."""
    data_changed = pyqtSignal()
    announcement = pyqtSignal(list)  # List of announcements for all trains

    def __init__(self, tc_communicate, tm_communicate, ctc_communicate):
        super().__init__()

        self.tc_communicate = tc_communicate
        self.tm_communicate = tm_communicate
        self.ctc_communicate = ctc_communicate

        # List to store data for each train
        self.train_count = 0  # Initial train count

        # Initialize lists for train data
        self.cabin_temperature = []
        self.maximum_capacity = []
        self.passenger_count = []
        self.crew_count = []
        self.maximum_speed = []
        self.current_speed = []
        self.total_car_weight = []

        self.train_length = []
        self.train_height = []
        self.train_width = []
        self.number_of_cars = []
        self.single_car_tare_weight = []

        self.announcement_text = []

        # Train Control Input Variables
        self.commanded_power = []
        self.commanded_speed_tc = []
        self.commanded_speed = []
        self.authority = []
        self.commanded_authority = []
        self.service_brake = []
        self.exterior_light = []
        self.interior_light = []
        self.emergency_brake = []
        self.beacon_station = []

        # Cabin Control Variables
        self.desired_temperature = []
        self.train_left_door = []
        self.train_right_door = []
        self.advertisement = []
        self.passenger_boarding = []

        # Variables for the buttons
        self.interior_light_on = []
        self.exterior_light_on = []
        self.left_door_open = []
        self.right_door_open = []
        self.passenger_emergency_brake = []

        # Added variables for dynamic information
        self.current_acceleration = []
        self.available_seats = []
        self.current_train_weight = []

        # Variables for static information
        self.static_cars = []
        self.static_length = []
        self.static_width = []
        self.static_height = []
        self.static_empty_train_weight = []

        # Position Variables
        self.current_position = []
        self.grade = []
        self.elevation = []

        # Failure Modes
        self.engine_failure = []
        self.brake_failure = []
        self.signal_failure = []

        # Dispatch Control
        self.dispatch_train = []

        # Variable to indicate if the train is at a station
        self.at_station = []

        # Read from Train Controller and Track Model
        self.read_from_trainController_trackModel()

        # Read from CTC
        self.read_from_ctc()

        # Initialize an initial train
        self.initialize_train()

    def initialize_train(self):
        """Initialize data for a new train."""
        # Default values for a new train
        self.cabin_temperature.append(78)
        self.maximum_capacity.append(222)
        self.passenger_count.append(100)
        self.crew_count.append(2)
        self.maximum_speed.append(50)
        self.current_speed.append(0)
        self.total_car_weight.append(40.9)

        self.train_length.append(32.2 * 3.28084)  # Convert meters to feet
        self.train_height.append(3.42 * 3.28084)
        self.train_width.append(2.65 * 3.28084)
        self.number_of_cars.append(1)
        self.single_car_tare_weight.append(40.9)

        self.announcement_text.append("Welcome aboard!")

        # Train Control Input Variables
        self.commanded_power.append(0)
        self.commanded_speed_tc.append(0)
        self.commanded_speed.append(0)
        self.authority.append(0)
        self.commanded_authority.append(0)
        self.service_brake.append(False)
        self.exterior_light.append(True)
        self.interior_light.append(True)
        self.emergency_brake.append(False)
        self.beacon_station.append("Station Alpha")

        # Cabin Control Variables
        self.desired_temperature.append(76)
        self.train_left_door.append(False)
        self.train_right_door.append(False)
        self.advertisement.append("Picture1")
        self.passenger_boarding.append(0)

        # Variables for the buttons
        self.interior_light_on.append(True)
        self.exterior_light_on.append(True)
        self.left_door_open.append(False)
        self.right_door_open.append(False)
        self.passenger_emergency_brake.append(False)

        # Added variables for dynamic information
        self.current_acceleration.append(0.0)
        self.available_seats.append(self.maximum_capacity[-1] - self.passenger_count[-1])
        self.current_train_weight.append(40.9)

        # Variables for static information
        self.static_cars.append(1)
        self.static_length.append(self.train_length[-1])
        self.static_width.append(self.train_width[-1])
        self.static_height.append(self.train_height[-1])
        self.static_empty_train_weight.append(40.9)

        # Position Variables
        self.current_position.append(0.0)
        self.grade.append(0.0)
        self.elevation.append(0.0)

        # Failure Modes
        self.engine_failure.append(False)
        self.brake_failure.append(False)
        self.signal_failure.append(False)

        # Dispatch Control
        self.dispatch_train.append(True)  # Set to True to simulate a dispatched train

        # At Station
        self.at_station.append(False)

        # Update train count
        self.train_count += 1

        # Emit data_changed signal
        self.data_changed.emit()

    def remove_train(self):
        """Remove data for the first train (front of the list)."""
        if self.train_count > 0:
            self.cabin_temperature.pop(0)
            self.maximum_capacity.pop(0)
            self.passenger_count.pop(0)
            self.crew_count.pop(0)
            self.maximum_speed.pop(0)
            self.current_speed.pop(0)
            self.total_car_weight.pop(0)

            self.train_length.pop(0)
            self.train_height.pop(0)
            self.train_width.pop(0)
            self.number_of_cars.pop(0)
            self.single_car_tare_weight.pop(0)

            self.announcement_text.pop(0)

            # Train Control Input Variables
            self.commanded_power.pop(0)
            self.commanded_speed_tc.pop(0)
            self.commanded_speed.pop(0)
            self.authority.pop(0)
            self.commanded_authority.pop(0)
            self.service_brake.pop(0)
            self.exterior_light.pop(0)
            self.interior_light.pop(0)
            self.emergency_brake.pop(0)
            self.beacon_station.pop(0)

            # Cabin Control Variables
            self.desired_temperature.pop(0)
            self.train_left_door.pop(0)
            self.train_right_door.pop(0)
            self.advertisement.pop(0)
            self.passenger_boarding.pop(0)

            # Variables for the buttons
            self.interior_light_on.pop(0)
            self.exterior_light_on.pop(0)
            self.left_door_open.pop(0)
            self.right_door_open.pop(0)
            self.passenger_emergency_brake.pop(0)

            # Added variables for dynamic information
            self.current_acceleration.pop(0)
            self.available_seats.pop(0)
            self.current_train_weight.pop(0)

            # Variables for static information
            self.static_cars.pop(0)
            self.static_length.pop(0)
            self.static_width.pop(0)
            self.static_height.pop(0)
            self.static_empty_train_weight.pop(0)

            # Position Variables
            self.current_position.pop(0)
            self.grade.pop(0)
            self.elevation.pop(0)

            # Failure Modes
            self.engine_failure.pop(0)
            self.brake_failure.pop(0)
            self.signal_failure.pop(0)

            # Dispatch Control
            self.dispatch_train.pop(0)

            # At Station
            self.at_station.pop(0)

            # Update train count
            self.train_count -= 1

            # Emit data_changed signal
            self.data_changed.emit()

    def read_from_trainController_trackModel(self):
        # Connect incoming signals from Train Controller
        self.tc_communicate.power_command_signal.connect(self.set_power_command)
        self.tc_communicate.service_brake_command_signal.connect(self.set_service_brake)
        self.tc_communicate.emergency_brake_command_signal.connect(self.set_emergency_brake)
        self.tc_communicate.desired_temperature_signal.connect(self.set_desired_temperature)
        self.tc_communicate.exterior_lights_signal.connect(self.set_exterior_light)
        self.tc_communicate.interior_lights_signal.connect(self.set_interior_light)
        self.tc_communicate.left_door_signal.connect(self.set_left_door)
        self.tc_communicate.right_door_signal.connect(self.set_right_door)
        self.tc_communicate.announcement_signal.connect(self.set_announcement)
        self.tc_communicate.grade_signal.connect(self.set_grade)
        self.tc_communicate.engine_failure_signal.connect(self.set_engine_failure_from_tc)
        self.tc_communicate.brake_failure_signal.connect(self.set_brake_failure_from_tc)
        self.tc_communicate.signal_failure_signal.connect(self.set_signal_failure_from_tc)
        self.tc_communicate.passenger_brake_command_signal.connect(self.set_passenger_emergency_brake)

        # Connect incoming signals from Track Model
        self.tm_communicate.commanded_speed_signal.connect(self.set_track_commanded_speed)
        self.tm_communicate.commanded_authority_signal.connect(self.set_track_commanded_authority)
        self.tm_communicate.block_grade_signal.connect(self.set_block_grade)
        self.tm_communicate.block_elevation_signal.connect(self.set_block_elevation)
        self.tm_communicate.polarity_signal.connect(self.set_track_polarity)
        self.tm_communicate.number_passenger_boarding_signal.connect(self.set_passenger_boarding)

    def read_from_ctc(self):
        # Connect incoming signals from CTC
        self.ctc_communicate.dispatch_train_signal.connect(self.update_train_list)

    def update_train_list(self, ctc_train_count):
        current_train_count = self.train_count
        if ctc_train_count > current_train_count:
            # Add new trains
            for _ in range(ctc_train_count - current_train_count):
                self.initialize_train()
        elif ctc_train_count < current_train_count:
            # Remove trains from the front
            for _ in range(current_train_count - ctc_train_count):
                self.remove_train()
        # Emit data_changed signal
        self.data_changed.emit()

        # Send current train count to Train Controller
        self.tc_communicate.train_count_signal.emit(self.train_count)

    # Handler methods for incoming signals from Train Controller
    def set_power_command(self, power_list):
        self.commanded_power = power_list
        self.data_changed.emit()

    def set_service_brake(self, state_list):
        self.service_brake = state_list
        self.data_changed.emit()

    def set_emergency_brake(self, state_list):
        self.emergency_brake = state_list
        self.data_changed.emit()

    def set_desired_temperature(self, temp_list):
        self.desired_temperature = temp_list
        self.cabin_temperature = temp_list
        self.data_changed.emit()

    def set_exterior_light(self, state_list):
        self.exterior_light = state_list
        self.exterior_light_on = state_list
        self.data_changed.emit()

    def set_interior_light(self, state_list):
        self.interior_light = state_list
        self.interior_light_on = state_list
        self.data_changed.emit()

    def set_left_door(self, state_list):
        self.train_left_door = state_list
        self.left_door_open = state_list
        self.data_changed.emit()

    def set_right_door(self, state_list):
        self.train_right_door = state_list
        self.right_door_open = state_list
        self.data_changed.emit()

    def set_announcement(self, announcement_list):
        self.announcement_text = announcement_list
        self.announcement.emit(announcement_list)
        self.data_changed.emit()

    def set_grade(self, grade_list):
        self.grade = grade_list
        self.data_changed.emit()

    def set_engine_failure_from_tc(self, state_list):
        self.engine_failure = state_list
        self.data_changed.emit()

    def set_brake_failure_from_tc(self, state_list):
        self.brake_failure = state_list
        self.data_changed.emit()

    def set_signal_failure_from_tc(self, state_list):
        self.signal_failure = state_list
        self.data_changed.emit()

    def set_passenger_emergency_brake(self, state_list):
        self.passenger_emergency_brake = state_list
        self.data_changed.emit()

    # Handler methods for incoming signals from Track Model
    def set_track_commanded_speed(self, speed_list):
        self.commanded_speed_tc = speed_list
        self.commanded_speed = [speed * 0.621371 for speed in speed_list]  # Convert km/h to mph
        self.data_changed.emit()

    def set_track_commanded_authority(self, authority_list):
        self.authority = authority_list
        self.commanded_authority = [auth * 3.28084 for auth in authority_list]  # Convert meters to feet
        self.data_changed.emit()

    def set_block_grade(self, grade_list):
        self.grade = grade_list
        self.data_changed.emit()

    def set_block_elevation(self, elevation_list):
        self.elevation = elevation_list
        self.data_changed.emit()

    def set_track_polarity(self, polarity_list):
        # Handle polarity if needed
        self.data_changed.emit()

    def set_passenger_boarding(self, boarding_list):
        self.passenger_boarding = boarding_list
        for index, number in enumerate(boarding_list):
            self.passenger_count[index] += number
            if self.passenger_count[index] > self.maximum_capacity[index]:
                self.passenger_count[index] = self.maximum_capacity[index]
            self.update_train_weight(index)
        self.data_changed.emit()

    def update_train_weight(self, index):
        """Update the train's weight based on passenger count."""
        empty_train_weight_kg = 40.9 * 1000  # Empty train weight in kg
        passenger_weight_kg = self.passenger_count[index] * 68.0388  # Each passenger weighs 150 lbs (68.0388 kg)
        total_weight_kg = empty_train_weight_kg + passenger_weight_kg
        self.current_train_weight[index] = total_weight_kg / 1000  # Convert back to tonnes
        self.total_car_weight[index] = self.current_train_weight[index]  # Update total car weight
        self.available_seats[index] = self.maximum_capacity[index] - self.passenger_count[index]  # Update available seats
        self.data_changed.emit()

    def update_train_state(self):
        """Update the state of all trains."""
        # Prepare lists to collect data for signals that need them
        passengers_leaving_list = [0] * self.train_count

        for index in range(self.train_count):
            if self.dispatch_train[index]:
                # Call the calculate_train_speed function
                calculate_train_speed(self, index)
            else:
                # Train is not dispatched; it remains stationary
                self.current_speed[index] = 0
                self.current_acceleration[index] = 0

            # Determine if the train is at a station (simplified logic)
            if int(self.current_position[index]) % 1000 < 5:
                self.at_station[index] = True
            else:
                self.at_station[index] = False

            # Generate random number of passengers leaving if doors are open and at station
            passengers_leaving = 0
            if self.at_station[index] and (self.left_door_open[index] or self.right_door_open[index]):
                if self.passenger_count[index] > 0:
                    passengers_leaving = random.randint(1, self.passenger_count[index])
                    self.passenger_count[index] -= passengers_leaving
                    self.update_train_weight(index)
            passengers_leaving_list[index] = passengers_leaving

        # After updating all trains, emit updated lists to Train Controller and Track Model
        self.write_to_trainController_trackModel(passengers_leaving_list)

        # Emit data_changed signal
        self.data_changed.emit()

    def write_to_trainController_trackModel(self, passengers_leaving_list):
        # Send signals to Train Controller
        self.tc_communicate.current_velocity_signal.emit(self.current_speed)
        self.tc_communicate.actual_temperature_signal.emit(self.cabin_temperature)
        self.tc_communicate.passenger_brake_command_signal.emit(self.passenger_emergency_brake)
        self.tc_communicate.polarity_signal.emit([True] * self.train_count)  # Example values
        self.tc_communicate.commanded_speed_signal.emit(self.commanded_speed_tc)
        self.tc_communicate.commanded_authority_signal.emit(self.authority)

        # Send failure signals
        self.tc_communicate.engine_failure_signal.emit(self.engine_failure)
        self.tc_communicate.brake_failure_signal.emit(self.brake_failure)
        self.tc_communicate.signal_failure_signal.emit(self.signal_failure)

        # Send signals to Track Model
        self.tm_communicate.position_signal.emit(self.current_position)
        self.tm_communicate.seat_vacancy_signal.emit(self.available_seats)
        self.tm_communicate.number_passenger_leaving_signal.emit(passengers_leaving_list)

    def set_value(self, var_list, index, value):
        """Set the value in the list at the given index and emit data_changed signal."""
        var_list[index] = value
        self.data_changed.emit()

    def start_train_updates(self):
        """Start a timer to periodically update train states."""
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_train_state)
        self.timer.start(1000)  # Update every 1 second
