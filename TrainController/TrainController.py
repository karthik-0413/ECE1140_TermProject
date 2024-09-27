import TrainControllerEngineer

class TrainController:
    def __init__(self):
        # Everything Displayed to the User
        self.train_number = 0  # Default train number, can be set dynamically

        # Initialize train-specific attributes
        self.train_data = {}

        # Method to initialize train data
        def initialize_train_data(train_number):
            return {
            'current_speed': 0.0,
            'commanded_speed': 0.0,
            'commanded_authority': 0.0,
            'current_train_temperature': 72.0,
            'power_command': 0.0,
            'next_station': "Shadyside",
            'failure_modes': {
                'engine_failure': False,
                'signal_pickup_failure': False,
                'brake_failure': False
            },
            'setpoint_speed': 0.0,
            'setpoint_speed_submit': False,
            'desired_train_temperature': 72.0,
            'train_id': {
                'train_id': train_number,
                'kp': TrainControllerEngineer.get_kp(self, train_number),  # Default Kp value
                'ki': TrainControllerEngineer.get_ki(self, train_number)   # Default Ki value
            },
            'operation_mode': "Manual",
            'driver_service_brake_command': False,
            'driver_emergency_brake_command': False,
            'status_modes': {
                'interior_lights': False,   # False = Off, True = On
                'exterior_lights': False,   # False = Off, True = On
                'brake_status': False,      # False = Off, True = On
                'right_door_status': False, # False = Closed, True = Open
                'left_door_status': False   # False = Closed, True = Open
            },
            'passenger_brake_command': False
            }

        # Initialize data for the default train number
        self.train_data[self.train_number] = initialize_train_data(self.train_number)
        
        # Syntax to access variables -> self.train_number['current_speed'] = 0.0

    def set_train_number(self, train_number):
        self.train_number = train_number
        if train_number not in self.train_data:
            self.train_data[train_number] = self.initialize_train_data(train_number)
        print(f"Train number set to {self.train_number}")
    
    # Input Handling Methods
    def set_commanded_speed(self, speed):
        self.commanded_speed = speed
        print(f"Commanded Speed set to {self.commanded_speed} km/h")

    def set_commanded_authority(self, authority):
        self.commanded_authority = authority
        print(f"Commanded Authority set to {self.commanded_authority}")

    def update_current_velocity(self, velocity):
        self.current_velocity = velocity
        print(f"Current Velocity updated to {self.current_velocity} km/h")

    def trigger_failure_mode(self, failure_type):
        if failure_type in self.failure_modes:
            self.failure_modes[failure_type] = True
            print(f"Failure Mode Triggered: {failure_type}")
        else:
            print(f"Unknown failure type: {failure_type}")

    def passenger_brake(self):
        self.passenger_brake_command = True
        print("Passenger Brake Command Activated")

    def set_train_temperature(self, actual_temp, desired_temp):
        self.actual_train_temperature = actual_temp
        self.desired_train_temperature = desired_temp
        print(f"Train temperature set to {self.actual_train_temperature}°C, Desired: {self.desired_train_temperature}°C")

    # Output Actions
    def apply_emergency_brake(self):
        print("Emergency Brake Activated!")
        # Additional logic for stopping the train

    def apply_service_brake(self):
        print("Service Brake Applied.")
        # Logic to gradually slow down the train

    def control_power(self, power_on):
        if power_on:
            print("Power Command: ON")
        else:
            print("Power Command: OFF")

    def control_doors(self, open_doors):
        if open_doors:
            print("Doors Opening")
        else:
            print("Doors Closing")

    def control_lights(self, lights_on):
        if lights_on:
            print("Lights ON")
        else:
            print("Lights OFF")

    def make_announcement(self, message):
        print(f"Announcement: {message}")

    # Failure handling based on inputs
    def handle_failures(self):
        for failure, triggered in self.failure_modes.items():
            if triggered:
                print(f"Handling {failure}...")
                # Implement the logic to handle failures (e.g., stop train, alert driver)

if __name__ == "__main__":
    train_controller = TrainController()
    train_controller.set_commanded_speed(80)
    train_controller.update_current_velocity(75)
    train_controller.set_train_temperature(20, 22)
    train_controller.apply_emergency_brake()
    train_controller.make_announcement("Arriving at next station.")
