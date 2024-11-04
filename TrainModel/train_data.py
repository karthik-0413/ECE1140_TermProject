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

        # Initialize train count to 0
        self.train_count = 0  # Number of active trains

        # Initialize lists with at least one default element
        self.initialize_train_lists()

        # Connect signals from CTC
        self.ctc_communicate.current_train_count_signal.connect(self.update_train_count)

        # Read from Train Controller and Track Model
        self.read_from_trainController_trackModel()

        # Start periodic train updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_train_state)
        self.timer.start(1000)  # Update every second

    def initialize_train_lists(self):
        """Initialize the lists that hold per-train data with one default element."""
        # Initialize all lists with one default element
        self.cabin_temperature = [0]
        self.maximum_capacity = [0]
        self.passenger_count = [0]
        self.crew_count = [0]
        self.maximum_speed = [0]
        self.current_speed = [0]
        self.total_car_weight = [0]

        self.train_length = [0]
        self.train_height = [0]
        self.train_width = [0]
        self.number_of_cars = [0]
        self.single_car_tare_weight = [0]

        self.announcement_text = [""]

        # Train Control Input Variables
        self.commanded_power = [0]
        self.commanded_speed_tc = [0]
        self.commanded_speed = [0]
        self.authority = [0]
        self.commanded_authority = [0]
        self.service_brake = [False]
        self.exterior_light = [False]
        self.interior_light = [False]
        self.emergency_brake = [False]
        self.beacon_station = [""]

        # Cabin Control Variables
        self.desired_temperature = [0]
        self.train_left_door = [False]
        self.train_right_door = [False]
        self.advertisement = [""]
        self.passenger_boarding = [0]

        # Variables for the buttons
        self.interior_light_on = [False]
        self.exterior_light_on = [False]
        self.left_door_open = [False]
        self.right_door_open = [False]
        self.passenger_emergency_brake = [False]

        # Added variables for dynamic information
        self.current_acceleration = [0.0]
        self.available_seats = [0]
        self.current_train_weight = [0.0]

        # Variables for static information
        self.static_cars = [0]
        self.static_length = [0.0]
        self.static_width = [0.0]
        self.static_height = [0.0]
        self.static_empty_train_weight = [0.0]

        # Position Variables
        self.current_position = [0.0]
        self.grade = [0.0]
        self.elevation = [0.0]
        self.polarity = [True]

        # Failure Modes
        self.engine_failure = [False]
        self.brake_failure = [False]
        self.signal_failure = [False]

        # Dispatch Control
        self.dispatch_train = [False]

    def update_train_count(self, new_train_count):
        """Update the number of trains based on the count received from the CTC."""
        if new_train_count > self.train_count:
            # Add new trains
            for _ in range(new_train_count - self.train_count):
                self.add_new_train()
        elif new_train_count < self.train_count:
            # Remove trains from the left (earliest trains)
            for _ in range(self.train_count - new_train_count):
                self.remove_earliest_train()
        # Update the train count
        self.train_count = new_train_count
        # Emit data changed signal
        self.data_changed.emit()
        # Send current train count to Train Controller
        self.tc_communicate.train_count_signal.emit(self.train_count)

    def add_new_train(self):
        """Add a new train to the data lists."""
        if self.train_count == 0:
            # Replace default element with real train data
            self.cabin_temperature[0] = 78
            self.maximum_capacity[0] = 222
            self.passenger_count[0] = 100
            self.crew_count[0] = 2
            self.maximum_speed[0] = 70  # Adjusted to 70 as per your example
            self.current_speed[0] = 0
            self.total_car_weight[0] = 40.9

            self.train_length[0] = 32.2 * 3.28084  # Convert meters to feet
            self.train_height[0] = 3.42 * 3.28084
            self.train_width[0] = 2.65 * 3.28084
            self.number_of_cars[0] = 1
            self.single_car_tare_weight[0] = 40.9

            self.announcement_text[0] = "Welcome aboard!"

            # Train Control Input Variables
            self.commanded_power[0] = 0
            self.commanded_speed_tc[0] = 0
            self.commanded_speed[0] = 0
            self.authority[0] = 0
            self.commanded_authority[0] = 0
            self.service_brake[0] = False
            self.exterior_light[0] = True
            self.interior_light[0] = True
            self.emergency_brake[0] = False
            self.beacon_station[0] = "Station Alpha"

            # Cabin Control Variables
            self.desired_temperature[0] = 76
            self.train_left_door[0] = False
            self.train_right_door[0] = False
            self.advertisement[0] = "Picture1"
            self.passenger_boarding[0] = 0

            # Variables for the buttons
            self.interior_light_on[0] = True
            self.exterior_light_on[0] = True
            self.left_door_open[0] = False
            self.right_door_open[0] = False
            self.passenger_emergency_brake[0] = False

            # Added variables for dynamic information
            self.current_acceleration[0] = 0.0
            self.available_seats[0] = self.maximum_capacity[0] - self.passenger_count[0]
            self.current_train_weight[0] = 40.9

            # Variables for static information
            self.static_cars[0] = 1
            self.static_length[0] = self.train_length[0]
            self.static_width[0] = self.train_width[0]
            self.static_height[0] = self.train_height[0]
            self.static_empty_train_weight[0] = 40.9

            # Position Variables
            self.current_position[0] = 0.0
            self.grade[0] = 0.0
            self.elevation[0] = 0.0
            self.polarity[0] = True

            # Failure Modes
            self.engine_failure[0] = False
            self.brake_failure[0] = False
            self.signal_failure[0] = False

            # Dispatch Control
            self.dispatch_train[0] = True  # Set to True to simulate a dispatched train

        def remove_earliest_train(self):
            """Remove data for the first train (front of the list)."""
            if self.train_count > 0:
                # Reset the first element to default values
                self.cabin_temperature[0] = 0
                self.maximum_capacity[0] = 0
                self.passenger_count[0] = 0
                self.crew_count[0] = 0
                self.maximum_speed[0] = 0
                self.current_speed[0] = 0
                self.total_car_weight[0] = 0

                self.train_length[0] = 0
                self.train_height[0] = 0
                self.train_width[0] = 0
                self.number_of_cars[0] = 0
                self.single_car_tare_weight[0] = 0

                self.announcement_text[0] = ""

                # Train Control Input Variables
                self.commanded_power[0] = 0
                self.commanded_speed_tc[0] = 0
                self.commanded_speed[0] = 0
                self.authority[0] = 0
                self.commanded_authority[0] = 0
                self.service_brake[0] = False
                self.exterior_light[0] = False
                self.interior_light[0] = False
                self.emergency_brake[0] = False
                self.beacon_station[0] = ""

                # Cabin Control Variables
                self.desired_temperature[0] = 0
                self.train_left_door[0] = False
                self.train_right_door[0] = False
                self.advertisement[0] = ""
                self.passenger_boarding[0] = 0

                # Variables for the buttons
                self.interior_light_on[0] = False
                self.exterior_light_on[0] = False
                self.left_door_open[0] = False
                self.right_door_open[0] = False
                self.passenger_emergency_brake[0] = False

                # Added variables for dynamic information
                self.current_acceleration[0] = 0.0
                self.available_seats[0] = 0
                self.current_train_weight[0] = 0.0

                # Variables for static information
                self.static_cars[0] = 0
                self.static_length[0] = 0.0
                self.static_width[0] = 0.0
                self.static_height[0] = 0.0
                self.static_empty_train_weight[0] = 0.0

                # Position Variables
                self.current_position[0] = 0.0
                self.grade[0] = 0.0
                self.elevation[0] = 0.0
                self.polarity[0] = True

                # Failure Modes
                self.engine_failure[0] = False
                self.brake_failure[0] = False
                self.signal_failure[0] = False

                # Dispatch Control
                self.dispatch_train[0] = False

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

    # Handler methods for incoming signals from Train Controller
    def set_power_command(self, power_list):
        if len(power_list) < max(1, self.train_count):
            # Ensure the list is long enough
            power_list = power_list + [0] * (max(1, self.train_count) - len(power_list))
        self.commanded_power = power_list
        self.data_changed.emit()

    def set_service_brake(self, state_list):
        if len(state_list) < max(1, self.train_count):
            state_list = state_list + [False] * (max(1, self.train_count) - len(state_list))
        self.service_brake = state_list
        self.data_changed.emit()

    def set_emergency_brake(self, state_list):
        if len(state_list) < max(1, self.train_count):
            state_list = state_list + [False] * (max(1, self.train_count) - len(state_list))
        self.emergency_brake = state_list
        self.data_changed.emit()

    def set_desired_temperature(self, temp_list):
        if len(temp_list) < max(1, self.train_count):
            temp_list = temp_list + [0] * (max(1, self.train_count) - len(temp_list))
        self.desired_temperature = temp_list
        self.cabin_temperature = temp_list
        self.data_changed.emit()

    def set_exterior_light(self, state_list):
        if len(state_list) < max(1, self.train_count):
            state_list = state_list + [False] * (max(1, self.train_count) - len(state_list))
        self.exterior_light = state_list
        self.exterior_light_on = state_list
        self.data_changed.emit()

    def set_interior_light(self, state_list):
        if len(state_list) < max(1, self.train_count):
            state_list = state_list + [False] * (max(1, self.train_count) - len(state_list))
        self.interior_light = state_list
        self.interior_light_on = state_list
        self.data_changed.emit()

    def set_left_door(self, state_list):
        if len(state_list) < max(1, self.train_count):
            state_list = state_list + [False] * (max(1, self.train_count) - len(state_list))
        self.train_left_door = state_list
        self.left_door_open = state_list
        self.data_changed.emit()

    def set_right_door(self, state_list):
        if len(state_list) < max(1, self.train_count):
            state_list = state_list + [False] * (max(1, self.train_count) - len(state_list))
        self.train_right_door = state_list
        self.right_door_open = state_list
        self.data_changed.emit()

    def set_announcement(self, announcement_list):
        # Ensure the list has at least one element
        if len(announcement_list) < max(1, self.train_count):
            announcement_list = announcement_list + [""] * (max(1, self.train_count) - len(announcement_list))
        self.announcement_text = announcement_list
        self.announcement.emit(announcement_list)
        self.data_changed.emit()

    def set_grade(self, grade_list):
        if len(grade_list) < max(1, self.train_count):
            grade_list = grade_list + [0.0] * (max(1, self.train_count) - len(grade_list))
        self.grade = grade_list
        self.data_changed.emit()

    def set_engine_failure_from_tc(self, state_list):
        if len(state_list) < max(1, self.train_count):
            state_list = state_list + [False] * (max(1, self.train_count) - len(state_list))
        self.engine_failure = state_list
        self.data_changed.emit()

    def set_brake_failure_from_tc(self, state_list):
        if len(state_list) < max(1, self.train_count):
            state_list = state_list + [False] * (max(1, self.train_count) - len(state_list))
        self.brake_failure = state_list
        self.data_changed.emit()

    def set_signal_failure_from_tc(self, state_list):
        if len(state_list) < max(1, self.train_count):
            state_list = state_list + [False] * (max(1, self.train_count) - len(state_list))
        self.signal_failure = state_list
        self.data_changed.emit()

    def set_passenger_emergency_brake(self, state_list):
        if len(state_list) < max(1, self.train_count):
            state_list = state_list + [False] * (max(1, self.train_count) - len(state_list))
        self.passenger_emergency_brake = state_list
        self.data_changed.emit()

    # Handler methods for incoming signals from Track Model
    def set_track_commanded_speed(self, speed_list):
        # Ensure the list is long enough
        if len(speed_list) < max(1, self.train_count):
            speed_list = speed_list + [0] * (max(1, self.train_count) - len(speed_list))
        self.commanded_speed_tc = speed_list
        self.commanded_speed = [speed * 0.621371 for speed in speed_list]  # Convert km/h to mph
        self.data_changed.emit()

    def set_track_commanded_authority(self, authority_list):
        # Ensure the list is long enough
        if len(authority_list) < max(1, self.train_count):
            authority_list = authority_list + [0] * (max(1, self.train_count) - len(authority_list))
        self.authority = authority_list
        self.commanded_authority = [auth * 3.28084 for auth in authority_list]  # Convert meters to feet
        self.data_changed.emit()

    def set_block_grade(self, grade_list):
        if len(grade_list) < max(1, self.train_count):
            grade_list = grade_list + [0.0] * (max(1, self.train_count) - len(grade_list))
        self.grade = grade_list
        self.data_changed.emit()

    def set_block_elevation(self, elevation_list):
        if len(elevation_list) < max(1, self.train_count):
            elevation_list = elevation_list + [0.0] * (max(1, self.train_count) - len(elevation_list))
        self.elevation = elevation_list
        self.data_changed.emit()

    def set_track_polarity(self, polarity_list):
        if len(polarity_list) < max(1, self.train_count):
            polarity_list = polarity_list + [True] * (max(1, self.train_count) - len(polarity_list))
        self.polarity = polarity_list
        self.data_changed.emit()

    def set_passenger_boarding(self, boarding_list):
        # Ensure the list is long enough
        if len(boarding_list) < max(1, self.train_count):
            boarding_list = boarding_list + [0] * (max(1, self.train_count) - len(boarding_list))
        self.passenger_boarding = boarding_list
        for index, number in enumerate(boarding_list):
            if index >= self.train_count:
                continue  # Prevent IndexError
            self.passenger_count[index] += number
            if self.passenger_count[index] > self.maximum_capacity[index]:
                self.passenger_count[index] = self.maximum_capacity[index]
            self.update_train_weight(index)
        self.data_changed.emit()

    def update_train_weight(self, index):
        """Update the train's weight based on passenger count."""
        empty_train_weight_kg = 40.9 * 1000  # Empty train weight in kg
        passenger_weight_kg = self.passenger_count[index] * 68.0388  # Each passenger weighs 68.0388 kg
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

            # Removed station determination logic as per your request
            # Set passengers_leaving to 0 or handle differently if needed
            passengers_leaving_list[index] = 0

        # After updating all trains, emit updated lists to Train Controller and Track Model
        self.write_to_trainController_trackModel(passengers_leaving_list)

        # Emit data_changed signal
        self.data_changed.emit()

    def write_to_trainController_trackModel(self, passengers_leaving_list):
        # Send signals to Train Controller
        self.tc_communicate.current_velocity_signal.emit(self.current_speed)
        self.tc_communicate.actual_temperature_signal.emit(self.cabin_temperature)
        self.tc_communicate.passenger_brake_command_signal.emit(self.passenger_emergency_brake)
        self.tc_communicate.polarity_signal.emit(self.polarity)
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
