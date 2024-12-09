# power.py
import math
import time
from PyQt6.QtCore import QCoreApplication
def calculate_train_speed(train_data, index):
    """
    Calculate the train's speed based on the commanded power, brake inputs, grade, and other factors.
    Updates the train's current speed and acceleration.
    """

    delta_t = 1.0  # Time step in seconds

    # Get brake states
    emergency_brake_active = train_data.emergency_brake[index]
    service_brake_active = train_data.service_brake[index]

    if emergency_brake_active:
        # Emergency brake: highest priority
        acceleration = -2.73  # m/s²
        train_data.commanded_power[index] = 0
    elif service_brake_active:
        # Service brake
        acceleration = -1.2  # m/s²
        train_data.commanded_power[index] = 0
    else:
        power_command_w = train_data.commanded_power[index]  # in W

        if power_command_w > 0:
            # No brakes active and power is commanded
            current_velocity = train_data.current_speed[index]  # in m/s
            mass = train_data.current_train_weight[index] * 1000  # Convert tons to kg

            # Calculate force from power
            if current_velocity == 0.00:
                force = 120000 / 19.44
            else:
                force = power_command_w / current_velocity  # F = P / v

            # Calculate grade force
            grade = train_data.grade[index] if index < len(train_data.grade) else 0.0
            slope_angle = math.atan(grade / 100)
            grade_force = mass * 9.81 * math.sin(slope_angle)

            # Net force
            net_force = force - grade_force

            # Calculate acceleration
            acceleration = net_force / mass  # a = F / m

            # Limit acceleration
            max_acceleration = 0.5  # m/s²
            acceleration = min(acceleration, max_acceleration)
        else:
            # No power commanded, no acceleration
            acceleration = 0.0

    # Update acceleration
    train_data.current_acceleration[index] = acceleration

    # Update velocity
    new_velocity = train_data.current_speed[index] + acceleration * delta_t

    # Ensure velocity doesn't go negative
    train_data.current_speed[index] = max(new_velocity, 0.0)
    train_data.current_speed_UI[index] = train_data.current_speed[index] * 2.23  # in mph

    # Update position
    train_data.current_position[index] += train_data.current_speed[index] * delta_t
    
    if train_data.cabin_temperature[index] < train_data.desired_temperature[index]:
        train_data.desired_temperature[index] += 0.01
    else:
        train_data.desired_temperature[index] -= 0.01
    
    ### Temperature Calculation Starts Here ###
    initial_temp = train_data.cabin_temperature[index]
    desired_temp = train_data.desired_temperature[index]
    current_temp = initial_temp
    k = 0.3
    time_step = 0.5
    
    if abs(current_temp - desired_temp) > 0.01:  # Tolerance for stopping
        dT = k * (desired_temp - current_temp)
        current_temp += dT
        train_data.cabin_temperature[index] = current_temp
        QCoreApplication.processEvents()  # Process events to update the UI
        time.sleep(time_step)

    # print(f"Updated Temperature: {train_data.cabin_temperature[index]:.2f}°F")
    
    ### Temperature Calculation Starts Here ###
    
# def update_desired_temperature(train_data, index, temp):
#         train_data.desired_temperature[index] = temp
#         # # print(f"Desired temperature set to: {train_data.desired_temperature[index]}°F")
#         if train_data.cabin_temperature[index] < train_data.desired_temperature[index]:
#             train_data.desired_temperature[index] += 0.01
#         else:
#             train_data.desired_temperature[index] -= 0.01
#         reach_temperature(train_data, index)
#     # else:
        
#         # # print("Temperature out of range. Please enter a value between 60°F and 75.")

# def reach_temperature(train_data, index, k=0.3, time_step=0.5):
#         initial_temp = train_data.cabin_temperature[index]
#         desired_temp = train_data.desired_temperature[index]
#         print(f"Initial Temperature: {initial_temp:.2f}°F")
#         print(f"Desired Temperature: {desired_temp:.2f}°F")

#         current_temp = initial_temp
#         while abs(current_temp - desired_temp) > 0.01:  # Tolerance for stopping
#             dT = k * (desired_temp - current_temp)
            
#             current_temp += dT
            
#             train_data.cabin_temperature[index] = current_temp
#             QCoreApplication.processEvents()  # Process events to update the UI
#             # # print(f"Current Temperature: {current_temp:.2f}°F")
#             time.sleep(time_step)

#         # # print(f"Reached Desired Temperature: {current_temp:.2f}°F")
