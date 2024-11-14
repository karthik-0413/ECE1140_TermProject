# train_data.py

from PyQt6.QtCore import QObject, pyqtSignal, QTimer
from TrainModel.power import calculate_train_speed
import random  # For simulating passenger departures
from Resources.TrainTrainControllerComm import TrainTrainController
from Resources.TrackTrainComm import TrackTrainModelComm

class TrainData(QObject):
    """Class representing the data and state of all trains."""
    data_changed = pyqtSignal()
    announcement = pyqtSignal(list)  # List of announcements for all trains

    def __init__(self, tc_communicate: TrainTrainController, tm_communicate: TrackTrainModelComm, ctc_communicate):
        super().__init__()

        self.tc_communicate = tc_communicate
        self.tm_communicate = tm_communicate
        self.ctc_communicate = ctc_communicate

        # List to store data for each train
        self.train_count = 0  # Initial train count

        self.passengers_leaving_list = []  # List to store passengers leaving at each station

        # Initialize lists for train data
        self.cabin_temperature = []
        self.maximum_capacity = []
        self.passenger_count = []
        self.crew_count = []
        self.maximum_speed = []
        self.current_speed = []       # in m/s for calculations
        self.current_speed_UI = []    # in mph for UI
        self.total_car_weight = []

        self.train_length = []
        self.train_height = []
        self.train_width = []
        self.number_of_cars = []
        self.single_car_tare_weight = []
        self.emergency_brake_active = []

        self.announcement_text = []

        # Train Control Input Variables
        self.commanded_power = []
        self.commanded_speed_tc = []    # from Track Model, in km/h
        self.commanded_speed = []       # converted to m/s
        self.commanded_speed_UI = []    # converted to mph for UI
        self.authority = []             # from Track Model, in blocks
        self.commanded_authority = []   # Blocks
        self.service_brake = []
        self.exterior_light = []
        self.interior_light = []
        self.emergency_brake = []
        self.beacon = []  # List to store beacon messages

        # Cabin Control Variables
        self.desired_temperature = []
        self.train_left_door = []
        self.train_right_door = []
        self.advertisement = []
        self.passenger_boarding = []  # Number of passengers boarding from Track Model

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
        self.current_position = []  # in meters
        self.grade = []
        self.elevation = []
        self.polarity = []

        # Failure Modes
        self.engine_failure = []
        self.brake_failure = []
        self.signal_failure = []

        # Dispatch Control
        self.dispatch_train = []

        # Variables to track previous door states
        self.previous_left_door_open = []
        self.previous_right_door_open = []

        # Read from Train Controller and Track Model
        self.read_from_trainController_trackModel()
        self.read_from_ctc()

        # Start periodic train updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_train_state)
        self.timer.start(100)  # Update every 0.1 second

        # Start train updates
        self.start_train_updates()

    def initialize_train(self):
        """Initialize data for a new train."""
        # Append default values for a new train
        self.cabin_temperature.append(78)  # Fahrenheit
        self.maximum_capacity.append(222)
        self.passenger_count.append(100)
        self.crew_count.append(2)
        self.maximum_speed.append(70)  # mph
        self.current_speed.append(0.0)   # m/s
        self.current_speed_UI.append(0.0) # mph
        self.total_car_weight.append(40.9)  # tons

        self.train_length.append(32.2)  # meters
        self.emergency_brake_active.append(False)
        self.train_height.append(3.42)  # meters
        self.train_width.append(2.65)   # meters
        self.number_of_cars.append(1)
        self.single_car_tare_weight.append(40.9)  # tons

        self.announcement_text.append("Welcome aboard!")

        # Train Control Input Variables
        self.commanded_power.append(0)  # kW
        self.commanded_speed_tc.append(40)  # km/h from Track Model
        self.commanded_speed.append(40)     # Convert km/h to m/s
        self.commanded_speed_UI.append(40)  # Convert km/h to mph
        self.authority.append(20)           # authority in blocks
        self.commanded_authority.append(20) # Blocks
        self.service_brake.append(False)
        self.exterior_light.append(False)
        self.interior_light.append(False)
        self.emergency_brake.append(False)
        self.beacon.append("")  # Initialize beacon message

        # Cabin Control Variables
        self.desired_temperature.append(76)
        self.train_left_door.append(False)
        self.train_right_door.append(False)
        self.advertisement.append("Picture1")
        self.passenger_boarding.append(0)  # Initialize to 0

        # Variables for the buttons
        self.interior_light_on.append(False)
        self.exterior_light_on.append(False)
        self.left_door_open.append(False)
        self.right_door_open.append(False)
        self.passenger_emergency_brake.append(False)

        # Added variables for dynamic information
        self.current_acceleration.append(0.0)  # m/s^2
        self.available_seats.append(self.maximum_capacity[-1] - self.passenger_count[-1])
        self.current_train_weight.append(40.9)  # tons

        # Variables for static information
        self.static_cars.append(1)
        self.static_length.append(self.train_length[-1])  # meters
        self.static_width.append(self.train_width[-1])    # meters
        self.static_height.append(self.train_height[-1])  # meters
        self.static_empty_train_weight.append(40.9)       # tons

        # Position Variables
        self.current_position.append(0.0)  # meters
        self.grade.append(0.0)
        self.elevation.append(0.0)
        self.polarity.append(True)

        # Failure Modes
        self.engine_failure.append(False)
        self.brake_failure.append(False)
        self.signal_failure.append(False)

        # Dispatch Control
        self.dispatch_train.append(True)  # Set to True to simulate a dispatched train

        # Initialize previous door states
        self.previous_left_door_open.append(False)
        self.previous_right_door_open.append(False)

    def update_train_count(self, new_train_count):
        """Update the number of trains based on the count received from the CTC."""
        if new_train_count > self.train_count:
            # Add new trains
            for _ in range(new_train_count - self.train_count):
                self.initialize_train()
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

    def remove_earliest_train(self):
        """Remove data for the first train (front of the list)."""
        if self.train_count > 0:
            # Remove first elements from all lists
            self.cabin_temperature.pop(0)
            self.emergency_brake_active.pop(0)
            self.maximum_capacity.pop(0)
            self.passenger_count.pop(0)
            self.crew_count.pop(0)
            self.maximum_speed.pop(0)
            self.current_speed.pop(0)
            self.current_speed_UI.pop(0)
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
            self.commanded_speed_UI.pop(0)
            self.authority.pop(0)
            self.commanded_authority.pop(0)
            self.service_brake.pop(0)
            self.exterior_light.pop(0)
            self.interior_light.pop(0)
            self.emergency_brake.pop(0)
            self.beacon.pop(0)

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
            self.polarity.pop(0)

            # Failure Modes
            self.engine_failure.pop(0)
            self.brake_failure.pop(0)
            self.signal_failure.pop(0)

            # Dispatch Control
            self.dispatch_train.pop(0)

            # Remove previous door states
            self.previous_left_door_open.pop(0)
            self.previous_right_door_open.pop(0)

    def read_from_trainController_trackModel(self):
        """Connect incoming signals from Train Controller and Track Model."""
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

        # Connect incoming signals from Track Model
        self.tm_communicate.commanded_speed_signal.connect(self.set_track_commanded_speed)
        self.tm_communicate.commanded_authority_signal.connect(self.set_track_commanded_authority)
        self.tm_communicate.block_grade_signal.connect(self.set_block_grade)
        self.tm_communicate.block_elevation_signal.connect(self.set_block_elevation)
        self.tm_communicate.polarity_signal.connect(self.set_track_polarity)
        self.tm_communicate.number_passenger_boarding_signal.connect(self.set_passenger_boarding)

    def read_from_ctc(self):
        """Connect incoming signals from CTC."""
        self.ctc_communicate.current_train_count_signal.connect(self.update_train_list)

    def update_train_list(self, ctc_train_count):
        """Update train data lists based on current train count from CTC."""
        current_train_count = self.train_count
        if ctc_train_count > current_train_count:
            # Add new trains
            for _ in range(ctc_train_count - current_train_count):
                self.initialize_train()
        elif ctc_train_count < current_train_count:
            # Remove earliest trains
            for _ in range(current_train_count - ctc_train_count):
                self.remove_earliest_train()

        # Update train count
        self.train_count = ctc_train_count
        # print("Train Count:", self.train_count)  # # print for debugging

        # Send current train count to Train Controller
        # self.tc_communicate.train_count_signal.emit(self.train_count)

        # self.write_to_trainController_trackModel()

        # Emit data_changed signal
        self.data_changed.emit()

    # Handler methods for incoming signals from Train Controller
    def set_power_command(self, power_list):
        """Handle power command signals from Train Controller."""
        # # print power_list for debugging
        # print("Power Command List in Train Model:", power_list)
        if len(power_list) < max(1, self.train_count):
            # Ensure the list is long enough
            power_list = power_list + [0] * (max(1, self.train_count) - len(power_list))
        self.commanded_power = power_list
        self.data_changed.emit()

    def set_service_brake(self, state_list):
        """Handle service brake signals from Train Controller."""
        # print("Service Brake List in Train Model:", state_list)
        if len(state_list) < max(1, self.train_count):
            state_list = state_list + [False] * (max(1, self.train_count) - len(state_list))
        self.service_brake = state_list
        self.data_changed.emit()

    def set_emergency_brake(self, state_list: list):
        """Handle emergency brake signals from Train Controller."""
        # if True in state_list:
        # print("Emergency Brake List in Train Model:", state_list)
            # self.passenger_emergency_brake = state_list
        # print("Emergency Brake List in Train Model:", state_list)
        if len(state_list) < max(1, self.train_count):
            state_list = state_list + [False] * (max(1, self.train_count) - len(state_list))
        self.emergency_brake = state_list
        self.data_changed.emit()

    def set_desired_temperature(self, temp_list):
        """Handle desired temperature signals from Train Controller."""
        if len(temp_list) < max(1, self.train_count):
            temp_list = temp_list + [0] * (max(1, self.train_count) - len(temp_list))
        self.desired_temperature = temp_list
        self.cabin_temperature = temp_list  # Assuming desired temp sets cabin temp
        self.data_changed.emit()

    def set_exterior_light(self, state_list):
        """Handle exterior light signals from Train Controller."""
        if len(state_list) < max(1, self.train_count):
            state_list = state_list + [False] * (max(1, self.train_count) - len(state_list))
        self.exterior_light = state_list
        self.exterior_light_on = state_list
        self.data_changed.emit()

    def set_interior_light(self, state_list):
        """Handle interior light signals from Train Controller."""
        if len(state_list) < max(1, self.train_count):
            state_list = state_list + [False] * (max(1, self.train_count) - len(state_list))
        self.interior_light = state_list
        self.interior_light_on = state_list
        self.data_changed.emit()

    def set_left_door(self, state_list):
        """Handle left door signals from Train Controller."""
        if len(state_list) < max(1, self.train_count):
            state_list = state_list + [False] * (max(1, self.train_count) - len(state_list))
        self.train_left_door = state_list
        self.left_door_open = state_list
        self.data_changed.emit()

    def set_right_door(self, state_list):
        """Handle right door signals from Train Controller."""
        if len(state_list) < max(1, self.train_count):
            state_list = state_list + [False] * (max(1, self.train_count) - len(state_list))
        self.train_right_door = state_list
        self.right_door_open = state_list
        self.data_changed.emit()

    def set_announcement(self, announcement_list):
        """Handle announcement signals from Train Controller."""
        # Ensure the list has at least one element
        if len(announcement_list) < max(1, self.train_count):
            announcement_list = announcement_list + [""] * (max(1, self.train_count) - len(announcement_list))
        self.announcement_text = announcement_list
        self.announcement.emit(announcement_list)
        self.data_changed.emit()

    # Handler methods for incoming signals from Track Model
    def set_track_commanded_speed(self, speed_list):
        """Handle commanded speed signals from Track Model."""
        # Ensure the list is long enough
        if len(speed_list) < max(1, self.train_count):
            speed_list = speed_list + [0] * (max(1, self.train_count) - len(speed_list))
        self.commanded_speed_tc = speed_list
        # Convert km/h to m/s for calculations
        self.commanded_speed = [speed / 3.6 for speed in speed_list]  #UUU
        # Convert m/s to mph for UI
        self.commanded_speed_UI = [speed * 2.23694 for speed in self.commanded_speed]
        self.data_changed.emit()

    def set_track_commanded_authority(self, authority_list):
        """Handle commanded authority signals from Track Model."""
        # Ensure the list is long enough
        if len(authority_list) < max(1, self.train_count):
            authority_list = authority_list + [0] * (max(1, self.train_count) - len(authority_list))
        self.authority = authority_list
        self.commanded_authority = authority_list #UUU
        self.data_changed.emit()

    def set_block_grade(self, grade_list):
        """Handle block grade signals from Track Model."""
        if len(grade_list) < max(1, self.train_count):
            grade_list = grade_list + [0.0] * (max(1, self.train_count) - len(grade_list))
        self.grade = grade_list
        self.data_changed.emit()

    def set_block_elevation(self, elevation_list):
        """Handle block elevation signals from Track Model."""
        if len(elevation_list) < max(1, self.train_count):
            elevation_list = elevation_list + [0.0] * (max(1, self.train_count) - len(elevation_list))
        self.elevation = elevation_list
        self.data_changed.emit()

    def set_track_polarity(self, polarity_list):
        """Handle polarity signals from Track Model."""
        if len(polarity_list) < max(1, self.train_count):
            polarity_list = polarity_list + [True] * (max(1, self.train_count) - len(polarity_list))
        self.polarity = polarity_list
        print(f"train: {self.polarity}")
        self.data_changed.emit()

    def set_passenger_boarding(self, boarding_list):
        """Handle passenger boarding signals from Track Model."""
        # Ensure the list is long enough
        if len(boarding_list) < max(1, self.train_count):
            boarding_list = boarding_list + [0] * (max(1, self.train_count) - len(boarding_list))
        self.passenger_boarding = boarding_list
        self.data_changed.emit()

    def update_train_state(self):
        """Update the state of all trains."""
        # Prepare lists to collect data for signals that need them
        self.passengers_leaving_list = [0] * self.train_count
            

        for index in range(self.train_count):
            # if self.emergency_brake[index] and self.current_speed[0] == 0.0:
            #     self.emergency_brake[index] = False
            # Calculate train speed; brake logic is handled in power.py
            calculate_train_speed(self, index)

            # Detect door open transitions
            door_open_now = self.left_door_open[index] or self.right_door_open[index]
            door_open_prev = self.previous_left_door_open[index] or self.previous_right_door_open[index]

            if door_open_now and not door_open_prev:
                # Door has just been opened
                # Generate a random number of passengers to alight (<= current passengers)
                if self.passenger_count[index] > 0:
                    passengers_alighting = random.randint(0, self.passenger_count[index])
                else:
                    passengers_alighting = 0
                self.passengers_leaving_list[index] = passengers_alighting
                # Receive passengers_boarding from stored value
                passengers_boarding = self.passenger_boarding[index]
                # Update passenger count
                self.passenger_count[index] = max(
                    0,
                    self.passenger_count[index] - passengers_alighting + passengers_boarding
                )
                # Ensure passenger count does not exceed maximum capacity
                if self.passenger_count[index] > self.maximum_capacity[index]:
                    self.passenger_count[index] = self.maximum_capacity[index]

            # Update previous door states
            self.previous_left_door_open[index] = self.left_door_open[index]
            self.previous_right_door_open[index] = self.right_door_open[index]

        # After all passenger calculations, update train weights
        for index in range(self.train_count):
            self.update_train_weight(index)

        # After updating all trains, emit updated lists to Train Controller and Track Model
        self.write_to_trainController_trackModel()

        # After emitting the data, reset passenger_emergency_brake entries
        # for index in range(self.train_count):
        #     if self.passenger_emergency_brake[index] and self.current_speed[index] == 0:
        #         self.passenger_emergency_brake[index] = False

        # Emit data_changed signal
        self.data_changed.emit()

    def update_train_weight(self, index):
        """Update the train's weight based on passenger count."""
        empty_train_weight_kg = self.static_empty_train_weight[index] * 1000  # Empty train weight in kg
        passenger_weight_kg = self.passenger_count[index] * 68.0388  # Each passenger weighs 68.0388 kg
        total_weight_kg = empty_train_weight_kg + passenger_weight_kg
        self.current_train_weight[index] = total_weight_kg / 1000  # Convert back to tons
        self.total_car_weight[index] = self.current_train_weight[index]  # Update total car weight
        self.available_seats[index] = self.maximum_capacity[index] - self.passenger_count[index]  # Update available seats
        self.data_changed.emit()

    def write_to_trainController_trackModel(self):
        """Send updated data to Train Controller and Track Model via communication classes."""
        # Send data to Train Controller
        self.tc_communicate.commanded_speed_signal.emit(self.commanded_speed_tc)  # mph for UI
        self.tc_communicate.commanded_authority_signal.emit(self.commanded_authority)
        self.tc_communicate.current_velocity_signal.emit(self.current_speed)  # m/s
        self.tc_communicate.engine_failure_signal.emit(self.engine_failure)
        self.tc_communicate.brake_failure_signal.emit(self.brake_failure)
        self.tc_communicate.signal_failure_signal.emit(self.signal_failure)
        self.tc_communicate.actual_temperature_signal.emit(self.cabin_temperature)  # Fahrenheit
        self.tc_communicate.polarity_signal.emit(self.polarity)  # Pass polarity to Train Controller
        self.tc_communicate.passenger_brake_command_signal.emit(self.passenger_emergency_brake)
        # self.tc_communicate.train_count_signal.emit(self.train_count)

        # Send data to Track Model
        self.tm_communicate.position_signal.emit(self.current_position)  # meters
        self.tm_communicate.number_passenger_leaving_signal.emit(self.passengers_leaving_list)
        self.tm_communicate.seat_vacancy_signal.emit(self.available_seats)

    def set_value(self, var_list, index, value):
        """Set the value in the list at the given index and emit data_changed signal."""
        var_list[index] = value
        self.data_changed.emit()

    def start_train_updates(self):
        """Start a timer to periodically update train states."""
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_train_state)
        self.timer.start(1000)  # Update every 1 second

    def update_failure_button(self, train_index, label, state):
        """Update the failure status based on the label."""
        if label == "Signal Pickup Failure:":
            self.signal_failure[train_index] = state
        elif label == "Train Engine Failure:":
            self.engine_failure[train_index] = state
        elif label == "Brake Failure:":
            self.brake_failure[train_index] = state
        self.data_changed.emit()