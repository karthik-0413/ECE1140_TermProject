# class TrainController:
#     def __init__(self):
#         self.kp = 25.0
#         self.ki = 0.2
#         self.dt = 3.0  # Increased time step for faster simulation
#         self.max_power = 120000
#         self.speed_limit = 70
#         self.P_MAX = 120000
#         self.integral_error = 0.0
#         self.previous_acceleration = 0.0
#         self.previous_velocity = 0.0
#         self.power_command = 0.0
#         self.uk_current = 0.0
#         self.ek_current = 0.0
#         self.uk_previous = 0.0
#         self.ek_previous = 0.0

#     def update_power_command(self, desired_speed, current_speed):
        
#         # Determining speed bound
#         if desired_speed > self.speed_limit:
#             desired_speed = self.speed_limit
#         else:
#             desired_speed = desired_speed
            
#         # Print desired and current speed
#         print(f"Desired Speed: {desired_speed:.2f} m/s, Current Speed: {current_speed:.2f} m/s")
        
#         # Finding the velocity error
#         self.ek_current = desired_speed - current_speed
        
#         # Finding the power command
#         self.power_command = self.kp * self.ek_current + self.ki * self.uk_current

#         # Using the different cases from lecture slides
#         if self.power_command < self.max_power:
#             self.uk_current = self.uk_previous + (self.dt / 2) * (self.ek_current + self.ek_previous)
#         else:
#             self.uk_current = self.uk_previous

#         # Updating the previous variables for next iteration
#         self.ek_previous = self.ek_current
#         self.uk_previous = self.uk_current
        
#         # Power command bound
#         if self.power_command > self.max_power:
#             self.power_command = self.max_power
#         else:
#             self.power_command = self.power_command
        
#         # Returning the power command
#         return self.power_command

#     def update_current_velocity(self, current_velocity, power_command, friction_coefficient, max_velocity=19.44, serviceBrake=False, emergencyBrake=False):
#         mass = 500
        
#         # FORCE
#         if current_velocity == 0:
#             if serviceBrake or emergencyBrake:
#                 force = 0
#             else:
#                 force = 1000
#         else:
#             force = power_command / current_velocity
#             frictional_force = 0.05 * mass * 9.8
#             force -= frictional_force
            
#         # ACCERLATION - Max acceleration is 0.5 m/s^2
#         acceleration = force / mass
#         if (acceleration > 0.5 and not serviceBrake and not emergencyBrake):
#             acceleration = 0.5
        
        
        
        
        
            
#         # ACCERLATION
#         acceleration = (force/mass)
#         if (acceleration > 0.5 and not serviceBrake and not emergencyBrake):
#             # If all brakes are OFF and accelerationCalc is above the limit
#             acceleration = 0.5
#         elif (serviceBrake and not emergencyBrake): # accelerationCalc < self.DECELERATION_LIMIT_SERVICE and
#             # If the service brake is ON and accelerationCalc is below the limit
#             acceleration = -1.2
#         elif (not serviceBrake and emergencyBrake): # accelerationCalc < self.DECELERATION_LIMIT_EMERGENCY and
#             # If the emergency brake is ON and accelerationCalc is below the limit
#             acceleration = -2.73
#         elif (serviceBrake and emergencyBrake): # Edge case if both emergency brake and service brake are turned on
#             acceleration = -2.73 # Emergency brake takes priority
            
#         # VELOCITY
#         new_velocity = current_velocity + (self.dt / 2) * (acceleration + self.previous_acceleration)
#         if(new_velocity >= max_velocity):
#             # If the velocity is GREATER than max train speed
#             new_velocity = max_velocity # m/s
#         if(new_velocity <= 0):
#             # If the velocity is LESS than 0
#             new_velocity = 0
        
#         self.previous_acceleration = acceleration

#         return new_velocity

#     def run_simulation(self, desired_velocity):
#         max_velocity = desired_velocity
#         current_velocity = 0.0

#         while current_velocity < desired_velocity:
#             power_command = self.update_power_command(desired_velocity, current_velocity)
#             current_velocity = self.update_current_velocity(current_velocity, power_command, 0.05, max_velocity)

#             # Reduced frequency of print statements
#             if int(current_velocity) % 1 == 0:
#                 print(f"Current Velocity: {current_velocity:.2f} m/s, Power Command: {power_command:.2f} Watts")
                
#             if current_velocity == desired_velocity:
#                 break

# def main():
#     controller = TrainController()
#     controller.run_simulation(19.44)

# if __name__ == "__main__":
#     main()




setpoint_speed = 10
current_velocity = 10
speed_limit = 30
commanded_speed = 25

# ONLY WHEN CHANGING FROM MANUAL TO AUTOMATIC MODE
if setpoint_speed < speed_limit and setpoint_speed < commanded_speed and commanded_speed < speed_limit:
    # If the setpoint speed is less than the speed limit and the commanded speed
    current_velocity = commanded_speed
elif setpoint_speed < speed_limit and setpoint_speed < commanded_speed and commanded_speed > speed_limit:
    # If the setpoint speed is less than the speed limit and the commanded speed is greater than the speed limit
    current_velocity = speed_limit