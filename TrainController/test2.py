class TrainController:
    def __init__(self):
        self.kp = 10.0
        self.ki = 0.5
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
        self.uk_previous += self.uk_current
        
        # Power command bound
        if self.power_command > self.max_power:
            self.power_command = self.max_power
        else:
            self.power_command = self.power_command
        
        # Returning the power command
        return self.power_command

    def update_current_velocity(self, current_velocity, power_command, friction_coefficient=0.05, max_velocity=19.44, serviceBrake=False, emergencyBrake=False):
        mass = 40900
        
        # FORCE
        if current_velocity == 0:
            if serviceBrake or emergencyBrake:
                force = 0
            else:
                force = 1000
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
        

        self.previous_acceleration = acceleration

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
    controller.run_simulation(19.44)

if __name__ == "__main__":
    main()
