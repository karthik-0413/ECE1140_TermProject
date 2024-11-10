def calculate_train_speed(train_data, index, brake_deceleration=0.0):
    """
    Calculate the train's speed based on the commanded power and other factors.
    Updates the train's current speed and acceleration.
    
    Parameters:
    train_data (TrainData): The train data object containing information on power, speed, weight, etc.
    index (int): The index of the train data to use for calculation.
    brake_deceleration (float): The braking deceleration value (default is 0.0).
    """
    # Extract necessary variables from the train data
    power_command_kw = train_data.commanded_power[index]  # in kW
    power_command = power_command_kw * 1000  # Convert kW to Watts
    current_velocity = train_data.current_speed[index]  # in m/s
    mass = train_data.current_train_weight[index] * 1000  # Convert tonnes to kg
    delta_t = 1.0  # Time step in seconds

    # Calculate force from power (F = P / v), with protection against low speeds
    if current_velocity <= 0.1:  # Prevent division by zero and handle very low speeds
        force = power_command / 1.0  # Assume initial force at very low speed
    else:
        force = power_command / current_velocity  # F = P / v

    # Calculate frictional force (simplified model)
    frictional_force = 0.002 * mass * 9.81  # F_friction = coefficient * mass * gravity

    # Calculate braking force (F_brake = a_brake * m)
    brake_force = brake_deceleration * mass

    # Net force: power-based force minus friction and braking force
    net_force = force - frictional_force - brake_force

    # Calculate acceleration (a = F / m)
    acceleration = net_force / mass

    # Limit acceleration to realistic values (max acceleration and deceleration)
    max_acceleration = 0.5  # m/s²
    max_deceleration = -3.0  # m/s² (e.g., emergency braking)

    if acceleration > max_acceleration:
        acceleration = max_acceleration
    elif acceleration < max_deceleration:
        acceleration = max_deceleration

    # Update the train data with the calculated acceleration
    train_data.current_acceleration[index] = acceleration

    # Update velocity (new_velocity = current_velocity + acceleration * delta_t)
    new_velocity = current_velocity + acceleration * delta_t

    # Ensure velocity doesn't go negative
    if new_velocity < 0:
        new_velocity = 0.0

    # Update the train data with the new velocity
    train_data.current_speed[index] = new_velocity  # in m/s

    # Update position (new_position = current_position + velocity * delta_t)
    new_position = train_data.current_position[index] + new_velocity * delta_t
    train_data.current_position[index] = new_position
