# power.py

def calculate_train_speed(train_data, index):
    """
    Calculate the train's speed based on the commanded power and other factors.
    Updates the train's current speed and acceleration.
    """
    # Extract necessary variables
    power_command = train_data.commanded_power[index]  # in Watts
    current_velocity = train_data.current_speed[index]  # in m/s
    mass = train_data.current_train_weight[index] * 1000  # Convert tonnes to kg
    max_power = 120000.0  # Max power in Watts (120 kW)
    delta_t = 5.0  # Time step in seconds (assuming update every 5 seconds)

    # Start power calculation
    if current_velocity == 0:
        force = max_power / 19.44
        print(f"Train {index+1} is stationary. Force: {force:.2f} N")
    else:
        force = power_command / current_velocity
        print(f"Train {index+1} - Force: {force:.2f} N")

        frictional_force = 0.002 * mass * 9.8  # Adjust coefficient as needed

        if force < frictional_force:
            print(f"Train {index+1} has stopped moving due to insufficient force.")
            force = 0
        else:
            force -= frictional_force
            print(f"Train {index+1} - Frictional Force: {frictional_force:.2f} N")

    # Calculate acceleration
    acceleration = force / mass
    print(f"Train {index+1} - Acceleration: {acceleration:.2f} m/s^2")

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

    # Update the train's position
    new_position = train_data.current_position[index] + new_velocity * delta_t
    train_data.current_position[index] = new_position