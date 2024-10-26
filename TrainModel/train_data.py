# train_data.py

from PyQt6.QtCore import QObject, pyqtSignal, QTimer


class TrainData(QObject):
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
        self.commanded_power = 90  # kw
        self.commanded_speed_tc = 80  # km/h
        self.commanded_speed = self.commanded_speed_tc * 0.621371  # mph (converted)
        self.authority = 400  # m
        self.commanded_authority = self.authority * 3.28084  # ft (converted)
        self.service_brake = False  # Changed to boolean
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

    # Method to update train weight based on passenger count
    def update_train_weight(self):
        empty_train_weight_kg = 40.9 * 1000  # Empty train weight in kg
        passenger_weight_kg = self.passenger_count * 68.0388  # Each passenger weighs 150 lbs (68.0388 kg)
        total_weight_kg = empty_train_weight_kg + passenger_weight_kg
        self.current_train_weight = total_weight_kg / 1000  # Convert back to tonnes
        self.total_car_weight = self.current_train_weight  # Update total car weight
        self.available_seats = self.maximum_capacity - self.passenger_count  # Update available seats
        self.data_changed.emit()

    # Add setter methods to emit signal on data change
    def set_value(self, var_name, value):
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
        if not self.timer.isActive():
            self.timer.start(1000)  # Update every 1000 ms (1 second)

    def stop_timer(self):
        if self.timer.isActive():
            self.timer.stop()

    def update_train_state(self, delta_t=1.0):
        mass = self.current_train_weight * 1000  # Convert to kg

        current_velocity = self.current_speed * 0.44704  # Convert mph to m/s

        power_command_kw = self.commanded_power
        max_power_kw = 120

        # Use a local variable for effective power command
        effective_power_command_kw = power_command_kw

        # Limit effective commanded power
        if effective_power_command_kw > max_power_kw:
            effective_power_command_kw = max_power_kw
        elif effective_power_command_kw < 0:
            effective_power_command_kw = 0

        effective_power_command = effective_power_command_kw * 1000  # Convert kW to W

        # Calculate speed limit
        speed_limit_mps = min(self.commanded_speed, self.maximum_speed) * 0.44704  # Convert mph to m/s

        # Check if current speed exceeds speed limit
        if current_velocity > speed_limit_mps:
            self.auto_service_brake = True
        else:
            self.auto_service_brake = False

        # If emergency brake is engaged, turn off service brake
        if self.emergency_brake or self.passenger_emergency_brake:
            self.service_brake = False
            self.auto_service_brake = False

        # Check for brakes
        if self.emergency_brake or self.passenger_emergency_brake:
            acceleration = -2.73  # m/s²
            effective_power_command = 0
        elif self.service_brake or self.auto_service_brake:
            acceleration = -1.2  # m/s²
            effective_power_command = 0
        else:
            # Calculate force
            if current_velocity == 0:
                force = effective_power_command / 0.1  # Prevent division by zero
            else:
                force = effective_power_command / current_velocity

            frictional_force = 0.002 * mass * 9.8

            if force < frictional_force:
                force = 0
            else:
                force -= frictional_force

            acceleration = force / mass

            if acceleration > 0.5:
                acceleration = 0.5  # Cap positive acceleration to +0.5 m/s²

        new_velocity = current_velocity + acceleration * delta_t

        if new_velocity < 0:
            new_velocity = 0
            if acceleration < 0:
                acceleration = 0  # If speed is zero, acceleration cannot be negative

        # Convert units back for display
        self.current_speed = new_velocity * 2.23694  # m/s to mph
        self.current_acceleration = acceleration * 3.28084  # m/s² to ft/s²

        self.data_changed.emit()

        # Stop the timer if the train has stopped and no power is commanded
        if self.current_speed == 0 and (effective_power_command == 0 or self.current_acceleration == 0):
            self.stop_timer()
