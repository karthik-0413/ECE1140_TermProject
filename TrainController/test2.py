class TrainController:
    def __init__(self):
        self.kp = 25.0  # up if too much oscillation
        self.ki = 0.5  # up if the max is reached to fast
        self.dt = 1.0  # Increased time step for faster simulation
        self.max_power = 120000
        self.speed_limit = 70
        self.P_MAX = 120000
        self.integral_error = 0.0
        self.previous_acceleration = 0.0
        self.previous_velocity = 0.0
        self.power_command = 0.0
        self.uk_current = 0.0
        self.ek_current = 0.0
        self.uk_previous = 0.0
        self.ek_previous = 0.0
        self.current_position = 0.0
       
    def update_power_command(self, desired_speed, current_speed):
        
        # Determining speed bound
        if desired_speed > self.speed_limit:
            desired_speed = self.speed_limit
        else:
            desired_speed = desired_speed
            
        # Print desired and current speed
        print(f"Desired Speed: {desired_speed:.2f} m/s, Current Speed: {current_speed:.2f} m/s")
        
        # Finding the velocity error
        self.ek_current = desired_speed - current_speed
        
        # Finding the power command
        self.power_command = self.kp * self.ek_current + self.ki * self.uk_current

        # Using the different cases from lecture slides
        if self.power_command < self.max_power:
            self.uk_current = self.uk_previous + (self.dt / 2) * (self.ek_current + self.ek_previous)
        else:
            self.uk_current = self.uk_previous

        # Updating the previous variables for next iteration
        self.ek_previous = self.ek_current
        self.uk_previous = self.uk_current
        
        # Power command bound
        if self.power_command > self.max_power:
            self.power_command = self.max_power
        elif self.power_command < 0:
            self.power_command = 0
            print("Service Brake Applied")
        else:
            self.power_command = self.power_command
        
        # Returning the power command
        return self.power_command

    def update_current_velocity(self, current_velocity, power_command, friction_coefficient, max_velocity, serviceBrake=False, emergencyBrake=False):
        # Mass of full train
        mass = 56700
        
        # FORCE
        if current_velocity == 0:
            force = self.max_power / 19.44
        else:
            force = power_command / current_velocity
            print(f"Force: {force:.2f} N")
            
            frictional_force = friction_coefficient * mass * 9.8
            
            if force < frictional_force:
                print("Train has stopped moving")
                
            force -= frictional_force
            
            print(f"Frictional Force: {frictional_force:.2f} N")
            
        # ACCERLATION - Max acceleration is 0.5 m/s^2
        acceleration = force / mass
        
        if (acceleration > 0.5 and not serviceBrake and not emergencyBrake):
            acceleration = 0.5
        
        # VELOCITY - Max velocity is 19.44 m/s
        new_velocity = current_velocity + (self.dt / 2) * (acceleration + self.previous_acceleration)
        
        if (new_velocity >= max_velocity):
            new_velocity = max_velocity # m/s
            
        if (new_velocity <= 0):
            new_velocity = 0
        
        new_position = self.current_position + (self.dt / 2) * (new_velocity + current_velocity)
        print(f"New Velocity: {new_velocity:.2f} m/s, New Position: {new_position:.2f} m")

        self.previous_acceleration = acceleration
        self.current_position = new_position

        return new_velocity

    def run_simulation(self, desired_velocity):
        max_velocity = desired_velocity
        current_velocity = 10.0

        tolerance = 0.01  # Define a small tolerance value
        while abs(current_velocity - desired_velocity) > tolerance:
            power_command = self.update_power_command(desired_velocity, current_velocity)
            current_velocity = self.update_current_velocity(current_velocity, power_command, 0.05, max_velocity)

            # Reduced frequency of print statements
            if int(current_velocity) % 1 == 0:
                print(f"Current Velocity: {current_velocity:.2f} m/s, Power Command: {power_command:.2f} Watts")
                

def main():
    controller = TrainController()
    controller.run_simulation(15)
    # power = controller.update_power_command(19, 1)
    # print(f"Previous Velocity Error (ek_previous): {controller.ek_previous:.2f}")
    # power2 = controller.update_power_command(19, 8)
    # print(power)
    
    # print(power)
    # print(power2)
    # print(f"Previous Velocity Error (ek_previous): {controller.ek_previous:.2f}")
    # print(power2)
    
    # MANUAL = 1 
    # AUTOMATIC = 0
    
    # NOTES:
    # In manual mode, the train should initially go at commanded speed, then the driver should be able to change the speed via the setpoint speed input
        # The setpoint speed should be lower than the speed limit, if not then the speed is set to the speed limit
        # If no setpoint speed is given, then the commanded speed should be my desired speed
        # If setpoint speed is given, then the setpoint speed should be my desired speed
    
    # In automatic mode, the current speed would always be bounded by the commanded speed
        # The command speed would be my desired speed
    
    # In either mode, the current speed would be an input from the test bench
    
    
    # DESCRIPTION SENT TO ANUJ:
    # My current speed would be an input from the test bench and my desired speed would either be setpoint speed or commanded speed depending on the speed limit


if __name__ == "__main__":
    main()
