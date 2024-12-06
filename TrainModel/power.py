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

    # # prints the current positions of the trains
    # # print(train_data.current_position)