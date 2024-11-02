# power.py

def calculate_train_speed(train_data, index):
    """
    Calculate the train's speed based on the commanded power and other factors.
    Updates the train's current speed and acceleration.
    """
    # Extract necessary variables
    power_command = train_data.commanded_power[index]  # in Watts
    current_velocity = train_data.current_speed[index]  # in m/s
    mass = train_data.current_train_weight[index] * 1000  # Convert ton to kg
    max_power = 120000.0  # Max power in Watts (120 kW)
    delta_t = 5.0  # Time step in seconds (assuming update every 5 seconds)

    # Start power calculation
    if current_velocity == 0:
        # Use the exact logic you provided
        force = max_power / 19.44
    else:
        # Calculate force using power command and current velocity
        force = power_command / current_velocity

        # Frictional force (assuming coefficient of friction is negligible as per your logic)
        frictional_force = 0.00 * mass * 9.8

        if force < frictional_force:
            # If the force is less than friction, the train stops moving
            force = 0
            print(f"Train {index+1} has stopped moving due to insufficient force.")
        else:
            # Subtract frictional force from the applied force
            force -= frictional_force

    # Calculate acceleration
    acceleration = force / mass

    # Limit acceleration to a maximum value (e.g., 0.5 m/s^2)
    if acceleration > 0.5:
        acceleration = 0.5

    # Update velocity
    new_velocity = current_velocity + acceleration * delta_t

    # Ensure velocity doesn't go negative
    if new_velocity < 0:
        new_velocity = 0

    # Update the train data
    train_data.current_speed[index] = new_velocity  # in m/s
    train_data.current_acceleration[index] = acceleration  # in m/s^2

    # Update position
    new_position = train_data.current_position[index] + current_velocity * delta_t + 0.5 * acceleration * delta_t ** 2
    train_data.current_position[index] = new_position  # in meters
