from TrainControllerEngineer import TrainEngineer

class TrainController:
    def __init__(self):
        # Everything Displayed to the User
        self.current_speed = 0.0
        self.commanded_speed = 0.0
        self.commanded_authority = 0.0
        self.current_train_temperature = 72.0
        self.power_command = 0.0
        self.next_station = "Shadyside"
        self.failure_modes = {
            'engine_failure': False,
            'signal_pickup_failure': False,
            'brake_failure': False
        }
        
        # Everything Inputted by the User
        self.setpoint_speed = 0.0
        self.setpoint_speed_submit = False
        self.desired_train_temperature = 72.0
        self.train_id = {
            'train_id': 0.0,
            'kp': 0.0,
            'ki': 0.0
        }
        self.operation_mode = "Manual"
        # MAKE SEPARATE CLASS FOR ENGINEER IN SEPARATE FILE
        
        # Everything Interactable for the User
        self.driver_service_brake_command = False
        self.driver_emergency_brake_command = False
        self.status_modes = {
            'interior_lights': False,   # False = Off, True = On
            'exterior_lights': False,   # False = Off, True = On
            'brake_status': False,      # False = Off, True = On
            'right_door_status': False, # False = Closed, True = Open
            'left_door_status': False   # False = Closed, True = Open
        }
        
        # Engineering Kp and Ki Values from other file
        self.kp = TrainEngineer.get_kp(self, self.train_id)
        self.ki = TrainEngineer.get_ki(self, self.train_id)
        
        # Input from Train Model for Emergency Brake to be Applied
        self.passenger_brake_command = False
      
    def print_Kp_Ki(self):
        print(f'Train {self.train_id} Kp: {self.kp}, Ki: {self.ki}')
    
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
                
    # def PID(Kp, Ki, Kd, setpoint, measurement):
    #     global time, integral, time_prev, e_prev  # Value of offset - when the error is equal zero
    #     offset = 320 
    #     # PID calculations
    #     e = setpoint - measurement 
    #     P = Kp*e
    #     integral = integral + Ki*e*(time - time_prev)
    #     D = Kd*(e - e_prev)/(time - time_prev)  # calculate manipulated variable - MV 
    #     MV = offset + P + integral + D 
    #     # update stored data for next iteration
    #     e_prev = e
    #     time_prev = time
    #     return MV

if __name__ == "__main__":
    train_controller = TrainController()
    train_controller.print_Kp_Ki()
    train_controller.set_commanded_speed(80)
    train_controller.update_current_velocity(75)
    train_controller.set_train_temperature(20, 22)
    train_controller.apply_emergency_brake()
    train_controller.make_announcement("Arriving at next station.")
