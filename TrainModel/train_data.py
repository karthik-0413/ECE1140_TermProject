# train_data.py

from PyQt6.QtCore import QObject, pyqtSignal, QTimer
from power import calculate_train_speed


class TrainData(QObject):
    """Class representing the data and state of a train."""
    data_changed = pyqtSignal()

    def __init__(self):
        super().__init__()
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

        self.announcement = "RED ALERT"

        # Train Control Input Variables
        self.commanded_power = 90  # kW
        self.commanded_speed_tc = 80  # km/h
        self.commanded_speed = self.commanded_speed_tc * 0.621371  # mph (converted)
        self.authority = 400  # m
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

        # Timer for updating train state every second
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_train_state)

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
        if var_name in ['service_brake', 'emergency_brake', 'passenger_emergency_brake']:
            # Start the timer when brakes are pressed
            self.start_timer()
        if var_name == 'commanded_power':
            # Start the timer when commanded power changes
            self.start_timer()
        self.data_changed.emit()

    def start_timer(self):
        """Start the train state update timer."""
        if not self.timer.isActive():
            self.timer.start(1000)  # Update every 1000 ms (1 second)

    def stop_timer(self):
        """Stop the train state update timer."""
        if self.timer.isActive():
            self.timer.stop()

    def update_train_state(self, delta_t=1.0):
        """Update the train's state."""
        # Call the calculate_train_speed function
        effective_power_command = calculate_train_speed(self, delta_t)

        self.data_changed.emit()

        # Stop the timer if the train has stopped and no power is commanded
        if self.current_speed == 0 and (effective_power_command == 0 or self.current_acceleration == 0):
            self.stop_timer()
