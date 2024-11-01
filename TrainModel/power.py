# power.py

def calculate_train_speed(train_data, index):
    """
    Calculate the train's speed based on the commanded power, current speed, and other factors.

    Parameters:
    - train_data: TrainData instance containing all trains' data.
    - index: Integer index of the train to calculate speed for.
    """
    # Constants
    GRAVITY = 9.80665  # m/s^2
    TRAIN_MASS = train_data.current_train_weight[index] * 1000  # Convert tonnes to kg
    MAX_ACCELERATION = 0.5  # m/s^2, maximum allowed acceleration

    # Get the necessary data for the current train
    power = train_data.commanded_power[index] * 1000  # Convert kW to W
    current_speed_mps = train_data.current_speed[index] * 0.44704  # Convert mph to m/s
    grade = train_data.grade[index] / 100  # Convert percentage to decimal

    # Calculate the tractive effort
    if current_speed_mps > 0:
        tractive_effort = power / current_speed_mps
    else:
        tractive_effort = power / 0.1  # Avoid division by zero

    # Calculate the grade resistance
    grade_resistance = TRAIN_MASS * GRAVITY * grade

    # Calculate the net force
    net_force = tractive_effort - grade_resistance

    # Calculate acceleration
    acceleration = net_force / TRAIN_MASS

    # Limit acceleration to maximum allowed
    if acceleration > MAX_ACCELERATION:
        acceleration = MAX_ACCELERATION
    elif acceleration < -MAX_ACCELERATION:
        acceleration = -MAX_ACCELERATION

    # Update the train's acceleration
    train_data.current_acceleration[index] = acceleration * 3.28084  # Convert m/s^2 to ft/s^2

    # Update the speed
    delta_time = 1  # Assuming time step of 1 second
    new_speed_mps = current_speed_mps + acceleration * delta_time

    # Ensure speed doesn't go negative
    if new_speed_mps < 0:
        new_speed_mps = 0

    # Update the train's current speed
    train_data.current_speed[index] = new_speed_mps * 2.23694  # Convert m/s to mph

    # Update the train's position
    new_position = train_data.current_position[index] + new_speed_mps * delta_time
    train_data.current_position[index] = new_position
