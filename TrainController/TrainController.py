from TrainControllerEngineer import TrainEngineer
from PyQt6.QtCore import QTimer, QElapsedTimer
import time

class TrainController:
    def __init__(self):
        
        # Everything Displayed to the User
        self.velocity_commanded = 0.0
        self.current_speed = 40.0
        self.initial_speed = 40.0
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
        self.train_id = 1
        self.operation_mode = "Manual"
        
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
        self._kp = 0.0
        self._ki = 0.0
        
        # Input from Train Model for Emergency Brake to be Applied
        self.passenger_brake_command = False
        
        # Values for the Braking System
        self.service_deceleration = -1.2  # m/s^2
        self.emergency_deceleration = -2.73  # m/s^2
        
        # For Timer
        self.elapsed_timer = QElapsedTimer()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_speed)
      
    def update_Kp_and_Ki(self):
        self._kp = TrainEngineer.get_kp(self)
        self._ki = TrainEngineer.get_ki(self)
        print(f'Train {self.train_id} Kp: {self._kp}, Ki: {self._ki}')
        
    # Setting Velocity Commanded for the block diagram
    def set_velocity_command(self):
        if self.setpoint_speed > self.commanded_speed:
            self.velocity_commanded = self.commanded_speed
        else: 
            self.velocity_commanded = self.setpoint_speed
            
        print(f"Velocity Command set to {self.velocity_commanded} km/h")
    
    # Setting Commanded Speed
    def set_commanded_speed(self, speed):
        self.commanded_speed = speed
        print(f"Commanded Speed set to {self.commanded_speed} km/h")

    # Setting Commanded Authority
    def set_commanded_authority(self, authority):
        self.commanded_authority = authority
        print(f"Commanded Authority set to {self.commanded_authority}")
        
    # Updating Train Authority
    def update_authority(self, authority, distance_traveled):
        self.commanded_authority = authority - distance_traveled
        print(f"Commanded Authority updated to {self.commanded_authority}")
        
    # Setting Setpoint Speed
    def set_setpoint_speed(self, speed):
        self.setpoint_speed = speed
        print(f"Setpoint Speed set to {self.setpoint_speed} km/h")
        
    # Setting Current Temperature
    def set_current_temperature(self, temperature):
        self.current_train_temperature = temperature
        print(f"Current Train Temperature set to {self.current_train_temperature}°F")
        
    # Setting Power Command
    def set_power_command(self, power):
        self.power_command = power
        print(f"Power Command set to {self.power_command} kW")
        
    # Updating Current Velocity
    def update_current_velocity(self, velocity):
        self.current_velocity = velocity
        print(f"Current Velocity updated to {self.current_velocity} km/h")
        
    def update_current_speed(self, speed):
        self.current_speed = speed
        print(f"Current Speed updated to {self.current_speed} km/h")
        
    def get_current_speed(self):    
        return self.current_speed
        
    # Updating the speed as the brakes are pressed
    def calculate_speed(self, u, a, t):
        """
        Calculate the speed of the train after time t with deceleration a.

        Parameters:
        u (float): Initial speed (m/s).
        a (float): Deceleration (m/s^2).
        t (float): Time (s).

        Returns:
        float: Speed after time t.
        """
        return u + (a * t)
    
    def start_braking(self):
        self.elapsed_timer.start()
        print("Braking Started")
        self.timer.start(1000)  # Update every 100 ms

    def stop_braking(self):
        self.timer.stop()
        # Update initial speed to the current speed for the next braking session
        self.initial_speed = self.current_speed

    def update_speed(self):
        elapsed_time = self.elapsed_timer.elapsed() / 1000  # Convert ms to seconds
        if self.driver_emergency_brake_command:
            print("Emergency Brake Applied Here")
            new_speed = self.calculate_speed(self.initial_speed * 0.44704, self.emergency_deceleration, elapsed_time) / 0.44704
        else:
            new_speed = self.calculate_speed(self.initial_speed * 0.44704, self.service_deceleration, elapsed_time) / 0.44704
        
        # Prevent the speed from going negative
        if new_speed < 0:
            new_speed = 0.0
        
        self.update_current_speed(new_speed)
        self.current_speed = round(new_speed, 2)
        print(f"Current Time: {elapsed_time} s")
        print(f"Current Speed: {self.current_speed} km/h")
        
        if new_speed == 0.0:
            print("Train Stopped")
            self.timer.stop()
            
    def reach_temperature(initial_temp, desired_temp, k=0.1, time_step=1):
        """
        Gradually increase temperature from initial_temp to desired_temp using a first-order equation.
        
        Parameters:
        - initial_temp (float): The starting temperature.
        - desired_temp (float): The desired temperature to reach.
        - k (float): The rate constant controlling the speed of change.
        - time_step (float): Time interval between updates in seconds.

        Returns:
        - None
        """
        # Ensure inputs are of float type
        if not isinstance(initial_temp, (int, float)):
            raise TypeError(f"Initial temperature should be a number, but got: {type(initial_temp)}")

        if not isinstance(desired_temp, (int, float)):
            raise TypeError(f"Desired temperature should be a number, but got: {type(desired_temp)}")

        current_temp = initial_temp
        while abs(current_temp - desired_temp) > 0.01:  # Tolerance for stopping
            # Calculate the change in temperature using a first-order equation
            dT = k * (desired_temp - current_temp)
            
            # Update the current temperature
            current_temp += dT
            
            # Print the current temperature
            print(f"Current Temperature: {current_temp:.2f}°C")
            
            # Wait for the specified time step
            time.sleep(time_step)

        print(f"Reached Desired Temperature: {current_temp:.2f}°C")

        
    # Triggering Failure Modes (Input in the actual Failure Name)
    def trigger_failure_mode(self, failure_type):
        if failure_type in self.failure_modes:
            self.failure_modes[failure_type] = True
            self.apply_emergency_brake()
            print(f"Failure Mode Triggered: {failure_type}")
            # if failure_type == 'signal_pickup_failure':
                # STOP UPDATING THE SPEED AND AUTHORITY
                # Commanded Speed will remain the same, since it always stays the same
                # But, commanded authority will not be updated anymore until it is fixed
        else:
            print(f"Unknown failure type: {failure_type}")
        
    
    # Passenger Brake has been activated
    def passenger_brake(self):
        self.passenger_brake_command = True
        self.apply_emergency_brake()
        print("Passenger Brake Command Activated")
        
    
    # Graudally updating the train temperature
    def update_train_temperature(self, temperature):
        self.current_train_temperature = temperature
        print(f"Train Temperature updated to {self.current_train_temperature}°F")

    def get_engine_failure_status(self):
        return self.failure_modes['engine_failure']



    # Output Actions
    
    # When pressed by the driver (different deceleartion rate)
    def apply_emergency_brake(self):
        self.driver_emergency_brake_command = True
        print("Emergency Brake Activated!")
        # Additional logic for stopping the train
        # Add logic for stopping train using Physics equations - Done in update_speed()

    # When pressed by the driver (different deceleration rate)
    def apply_service_brake(self):
        self.driver_service_brake_command = True
        print("Service Brake Applied.")
        # Logic to gradually slow down the train
         # Add logic for stopping train using Physics equations - Done in update_speed()
         
         
    # When the driver wants to open the right door
    def control_right_doors(self, open_doors):
        if open_doors:
            print("Right Doors Opening")
        else:
            print("Right Doors Closing")
            
     # When the driver wants to open the left door
    def control_left_doors(self, open_doors):
        if open_doors:
            print("Left Doors Opening")
        else:
            print("Left Doors Closing")

    # When the driver wants to turn on the exterior lights
    def control_exterior_lights(self, lights_on):
        if lights_on:
            print("Exterior Lights ON")
        else:
            print("Exterior Lights OFF")
            
    # When the driver wants to turn on the interior lights
    def control_interior_lights(self, lights_on):
        if lights_on:
            print("Interior Lights ON")
        else:
            print("Interior Lights OFF")

    # Write the message that has to be announced
    def make_announcement(self, message):
        print(f"Announcement: {message}")

                
                
if __name__ == "__main__":
    train_controller = TrainController()
    # Create a QTimer to call update_Kp_and_Ki at regular intervals
    update_timer = QTimer()
    update_timer.timeout.connect(train_controller.update_Kp_and_Ki)
    update_timer.start(1000)  # Update every 1000 ms (1 second)
    train_controller.set_commanded_speed(80)
    train_controller.update_current_velocity(75)
    train_controller.apply_emergency_brake()
    train_controller.make_announcement("Arriving at next station.")
