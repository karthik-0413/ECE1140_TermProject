# train_data.py

from PyQt6.QtCore import QObject, pyqtSignal
from power import calculate_train_speed
import random

class TrainData(QObject):
    """Class representing the data and state of a train."""
    data_changed = pyqtSignal()
    announcement = pyqtSignal(str)
    current_velocity_signal = pyqtSignal(float)

    def __init__(self, tc_communicate, tm_communicate, ctc_communicate):
        super().__init__()

        self.tc_communicate = tc_communicate
        self.tm_communicate = tm_communicate
        self.ctc_communicate = ctc_communicate

        # Variables for the data values
        self.cabin_temperature = 78  # degrees Fahrenheit (Actual Temperature)
        self.maximum_capacity = 222  # passengers
        self.passenger_count = 100
        self.crew_count = 2
        self.maximum_speed = 50  # mph
        self.current_speed = 40  # mph
        self.total_car_weight = 40.9  # tons (empty train weight)

        self.train_length_m = 32.2  # meters
        self.train_height_m = 3.42  # meters
        self.train_width_m = 2.65  # meters
        self.train_length = self.train_length_m * 3.28084  # feet (converted)
        self.train_height = self.train_height_m * 3.28084  # feet (converted)
        self.train_width = self.train_width_m * 3.28084  # feet (converted)
        self.number_of_cars = 1  # variable
        self.single_car_tare_weight = 40.9  # tons

        self.announcement_text = "RED ALERT"
        dispatch_train = 0

        # Train Control Input Variables
        self.commanded_power = 90  # kW
        self.commanded_speed_tc = 80  # km/h
        self.commanded_speed = self.commanded_speed_tc * 0.621371  # mph (converted)
        self.authority = 15  # number of blocks
        self.commanded_authority = self.authority * 3.28084  # ft (converted)
        self.service_brake = False
        self.exterior_light = True
        self.interior_light = True
        self.emergency_brake = False
        self.beacon_station = "Station Alpha"  # Default station

        # Cabin Control Variables
        self.desired_temperature = 76  # °F
        self.cabin_temperature = self.desired_temperature  # °F (Actual Temperature)
        self.train_left_door = False
        self.train_right_door = False
        self.advertisement = "Picture1"
        self.passenger_boarding = 0  # Number of passengers boarding at next station (default 0)

        # Variables for the buttons
        self.interior_light_on = self.interior_light
        self.exterior_light_on = self.exterior_light
        self.left_door_open = self.train_left_door
        self.right_door_open = self.train_right_door
        self.passenger_emergency_brake = False

        # Added variables for dynamic information
        self.current_acceleration = 0.3  # ft/s²
        self.available_seats = self.maximum_capacity - self.passenger_count
        self.current_train_weight = 40.9  # t (will be updated based on passengers)

        # Variables for static information
        self.static_cars = self.number_of_cars
        self.static_length = self.train_length  # ft
        self.static_width = self.train_width  # ft
        self.static_height = self.train_height  # ft
        self.static_empty_train_weight = self.single_car_tare_weight  # t

        # Update train weight based on initial passenger count
        self.update_train_weight()

        # Added variable for automatic service brake
        self.auto_service_brake = False

        # Position Variables
        self.current_position = 0.0  # meters
        self.grade = 0.0  # percentage
        self.elevation = 0.0  # meters

        # Failure Modes
        self.engine_failure = False
        self.brake_failure = False
        self.signal_failure = False

        # Read from Train Controller and Track Model
        self.read_from_trainController_trackModel()

        # Variable to indicate if the train is at a station
        self.at_station = False

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

        # Connect incoming signals from Track Model
        self.tm_communicate.commanded_speed_signal.connect(self.set_track_commanded_speed)
        self.tm_communicate.commanded_authority_signal.connect(self.set_track_commanded_authority)
        self.tm_communicate.block_grade_signal.connect(self.set_block_grade)
        self.tm_communicate.block_elevation_signal.connect(self.set_block_elevation)
        self.tm_communicate.polarity_signal.connect(self.set_track_polarity)
        self.tm_communicate.number_passenger_boarding_signal.connect(self.set_passenger_boarding)

        #connect incoming signals from CTC
        self.ctc_communicate.dispatch_train_signal.connect(self.set_dispatch_train)
        #GPT
    def set_dispatch_train(self, number):
        # Train should only start moving if this signal is received
        self.dispatch_train = number
        pass

    def write_to_trainController_trackModel(self):
        self.update_train_state()

    # Handler methods for incoming signals from Train Controller
    def set_power_command(self, power):
        self.set_value('commanded_power', power)

    def set_service_brake(self, state):
        self.set_value('service_brake', state)

    def set_emergency_brake(self, state):
        self.set_value('emergency_brake', state)

    def set_desired_temperature(self, temp):
        self.set_value('desired_temperature', temp)

    def set_exterior_light(self, state):
        self.set_value('exterior_light', state)

    def set_interior_light(self, state):
        self.set_value('interior_light', state)

    def set_left_door(self, state):
        self.set_value('train_left_door', state)

    def set_right_door(self, state):
        self.set_value('train_right_door', state)

    def set_announcement(self, announcement):
        self.announcement.emit(announcement)
        self.set_value('announcement_text', announcement)

    def set_grade(self, grade):
        self.set_value('grade', grade)

    # Handler methods for incoming signals from Track Model
    def set_track_commanded_speed(self, speed):
        self.set_value('commanded_speed_tc', speed)

    def set_track_commanded_authority(self, authority):
        self.set_value('authority', authority)

    def set_block_grade(self, grade):
        self.set_value('grade', grade)

    def set_block_elevation(self, elevation):
        self.set_value('elevation', elevation)

    def set_track_polarity(self, polarity):
        self.set_value('polarity', polarity)

    def set_passenger_boarding(self, number):
        self.set_value('passenger_boarding', number)
        # Update passenger count and train weight when passengers board
        self.passenger_count += number
        if self.passenger_count > self.maximum_capacity:
            self.passenger_count = self.maximum_capacity
        self.update_train_weight()
        self.data_changed.emit()

    def update_train_weight(self):
        """Update the train's weight based on passenger count."""
        empty_train_weight_kg = 40.9 * 1000  # Empty train weight in kg
        passenger_weight_kg = self.passenger_count * 68.0388  # Each passenger weighs 150 lbs (68.0388 kg)
        total_weight_kg = empty_train_weight_kg + passenger_weight_kg
        self.current_train_weight = total_weight_kg / 1000  # Convert back to tonnes
        self.total_car_weight = self.current_train_weight  # Update total car weight
        self.available_seats = self.maximum_capacity - self.passenger_count  # Update available seats
        self.data_changed.emit()

    def set_value(self, var_name, value):
        """Set the value of a variable and emit data_changed signal."""
        setattr(self, var_name, value)
        # Update dependent variables
        if var_name == 'desired_temperature':
            self.cabin_temperature = value
        if var_name == 'exterior_light':
            self.exterior_light_on = value
        if var_name == 'interior_light':
            self.interior_light_on = value
        if var_name == 'train_left_door':
            self.left_door_open = value
        if var_name == 'train_right_door':
            self.right_door_open = value
        if var_name == 'number_of_cars':
            self.static_cars = value
        if var_name == 'commanded_speed_tc':
            # Convert km/h to mph
            self.commanded_speed = value * 0.621371
        if var_name == 'passenger_count':
            self.update_train_weight()
        self.data_changed.emit()

    def update_train_state(self, delta_t=1.0):
        """Update the train's state."""
        # Call the calculate_train_speed function
        calculate_train_speed(self, delta_t)

        # Determine if the train is at a station (for simplicity, let's assume position modulo some value)
        if int(self.current_position) % 1000 < 5:
            self.at_station = True
        else:
            self.at_station = False

        # Generate random number of passengers leaving if doors are open and at station
        passengers_leaving = 0
        if self.at_station and (self.left_door_open or self.right_door_open):
            if self.passenger_count > 0:
                passengers_leaving = random.randint(1, self.passenger_count)
                self.passenger_count -= passengers_leaving
                self.update_train_weight()
                # Emit signal to Track Model
                self.tm_communicate.number_passenger_leaving_signal.emit(passengers_leaving)

        # Send signals to Train Controller
        self.tc_communicate.current_velocity_signal.emit(self.current_speed)
        self.tc_communicate.actual_temperature_signal.emit(self.cabin_temperature)
        self.tc_communicate.passenger_brake_command_signal.emit(self.passenger_emergency_brake)
        self.tc_communicate.polarity_signal.emit(True)  # Example value
        self.tc_communicate.commanded_speed_signal.emit(self.commanded_speed_tc)
        self.tc_communicate.commanded_authority_signal.emit(self.authority)
        self.tc_communicate.dispatch_train_signal.emit(self.dispatch_train)

        # Send failure signals
        self.tc_communicate.engine_failure_signal.emit(self.engine_failure)
        self.tc_communicate.brake_failure_signal.emit(self.brake_failure)
        self.tc_communicate.signal_failure_signal.emit(self.signal_failure)

        # Send signals to Track Model
        self.tm_communicate.position_signal.emit(self.current_position)
        self.tm_communicate.number_passenger_leaving_signal.emit(passengers_leaving)
        self.tm_communicate.seat_vacancy_signal.emit(self.available_seats)

        self.data_changed.emit()
