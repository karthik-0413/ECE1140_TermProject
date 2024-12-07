import matplotlib.pyplot as plt

class TrainController:
    def __init__(self):
        self.kp = 7173.0 # up if too much oscillation
        self.ki = 15.0  # up if the max is reached to fast
        self.dt = 3.0  # Increased time step for faster simulation
        self.max_power = 120000
        self.speed_limit = 70
        self.integral_error = 0.0
        self.previous_acceleration = 0.0
        self.previous_velocity = 0.0
        self.power_command = 0.0
        self.uk_current = 0.0
        self.ek_current = 0.0
        self.uk_previous = 0.0
        self.ek_previous = 0.0
        self.current_position = 0.0
        self.current_velocity = 0.0
        self.time_steps = []
        self.velocities = []

    def update_power_command(self, desired_velocity):
        
        # # # print desired and current speed in mph (if needed)
        # # print(f"Desired Speed: {desired_velocity:.2f} m/s, Current Speed: {self.current_velocity:.2f} m/s")
        
        # Finding the velocity error
        self.ek_current = desired_velocity - self.current_velocity
        
        # Using the different cases from lecture slides
        if self.power_command < self.max_power:
            self.uk_current = self.uk_previous + (1.0 / 2) * (self.ek_current + self.ek_previous)
        else:
            self.uk_current = self.uk_previous
        
        # Finding the power command
        self.power_command = self.kp * self.ek_current + self.ki * self.uk_current

        # Updating the previous variables for the next iteration
        self.ek_previous = self.ek_current
        self.uk_previous = self.uk_current
        
        # Power command bound
        if self.power_command > self.max_power:
            self.power_command = self.max_power
        # elif self.power_command < 0:
        #     self.power_command = 0
        #     # # print("Service Brake Applied")
        else:
            self.power_command = self.power_command

        # Returning the power command
        return self.power_command

    def update_current_velocity(self, power_command):
        mass = 56700
        # mass = 40700
        
        if self.current_velocity == 0:
            force = self.max_power / 19.44
        else:
            force = power_command / self.current_velocity
            # # print(f"Force: {force:.2f} N")
            
            frictional_force = 0.002 * mass * 9.8
            
            if force < frictional_force:
                pass
                # # print("Train has stopped moving")
                
            force -= frictional_force
            
            # # print(f"Frictional Force: {frictional_force:.2f} N")
            
        acceleration = force / mass
        # # print(f"Acceleration: {acceleration:.2f} m/s^2")
        
        if acceleration > 0.5:
            acceleration = 0.5
        
        new_velocity = self.current_velocity + acceleration * 5.0

        self.current_velocity = new_velocity

        return new_velocity

    def run_simulation(self, desired_velocity):

        for i in range(400):
            power_command = self.update_power_command(desired_velocity)
            self.current_velocity = self.update_current_velocity(power_command)
            
            self.time_steps.append(i * self.dt)
            self.velocities.append(self.current_velocity)

            # # print(f"Current Velocity: {self.current_velocity:.2f} m/s, Power Command: {power_command:.2f} Watts")

    def plot_velocity(self):
        plt.plot(self.time_steps, self.velocities)
        plt.xlabel('Time (s)')
        plt.ylabel('Current Velocity (m/s)')
        plt.title('Current Velocity vs Time')
        plt.grid(True)
        plt.show()

def main():
    controller = TrainController()
    # controller.run_simulation(19)
    # controller.plot_velocity()
    power = controller.update_power_command(16)
    # print(power)


if __name__ == "__main__":
    main()