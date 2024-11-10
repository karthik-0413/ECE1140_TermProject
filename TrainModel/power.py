# power.py

import math

def calculate_train_speed(train_data, index):
    """
    Calculate the train's speed based on the commanded power, brake inputs, grade, and other factors.
    Updates the train's current speed and acceleration.
    """

    delta_t = 1.0  # Time step in seconds

    # Get brake states
    emergency_brake_active = train_data.emergency_brake[index]
    service_brake_active = train_data.service_brake[index]

    # Determine acceleration based on brake states
    if emergency_brake_active:
        # Emergency brake: highest priority
        acceleration = -2.73  # m/s²
        train_data.commanded_power[index] = 0
    elif service_brake_active:
        # Service brake
        acceleration = -1.2  # m/s²
        train_data.commanded_power[index] = 0
    else:
        # No brakes active, proceed with force calculations
        # Extract necessary variables
        power_command_kw = train_data.commanded_power[index]  # in kW
        power_command = power_command_kw * 1000  # Convert kW to Watts
        current_velocity = train_data.current_speed[index]  # in m/s
        mass = train_data.current_train_weight[index] * 1000  # Convert tons to kg

        # Calculate force from power
        if current_velocity == 0.00:  # Prevent division by zero and handle very low speeds
            force = power_command / 19.44  # Assume initial force at very low speed
        else:
            force = power_command / current_velocity  # F = P / v

        # Calculate frictional force (simplified model)
        frictional_force = 0.002 * mass * 9.81  # F_friction = coefficient * mass * gravity

        # Calculate grade force
        if len(train_data.grade) > index:
            grade = train_data.grade[index]  # in percent
        else:
            grade = 0.0

        # Convert grade percentage to angle in radians
        slope_angle = math.atan(grade / 100)
        # Calculate grade force
        grade_force = mass * 9.81 * math.sin(slope_angle)
        # Optionally, print grade force for debugging
        # print(f"Grade Force: {grade_force:.2f} N")

        # Net force: power-based force minus friction minus grade force
        net_force = force - frictional_force - grade_force

        # Calculate acceleration
        acceleration = net_force / mass  # a = F / m

        # Limit acceleration to realistic values
        max_acceleration = 0.5  # m/s²
        # max_deceleration = -2.73  # m/s² (e.g., emergency braking)

        if acceleration > max_acceleration:
            acceleration = max_acceleration
        # elif acceleration < max_deceleration:
        #     acceleration = max_deceleration

    # Update acceleration
    train_data.current_acceleration[index] = acceleration

    # Update velocity
    current_velocity = train_data.current_speed[index]
    new_velocity = current_velocity + acceleration * delta_t

    # Ensure velocity doesn't go negative
    if new_velocity < 0:
        new_velocity = 0.0

    # Update the train data
    train_data.current_speed[index] = new_velocity  # in m/s

    # Update position
    new_position = train_data.current_position[index] + new_velocity * delta_t
    train_data.current_position[index] = new_position
