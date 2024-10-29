# power.py

import math

def calculate_train_speed(train_data, delta_t=1.0):
    # current_velocity = pyqtsignal(float) - Karthik Raja
    """Calculate and update the train's speed, acceleration, and position."""
    mass = train_data.current_train_weight * 1000  # Convert to kg

    # Convert current speed from mph to m/s
    current_speed_mps = train_data.current_speed * 0.44704  # mph to m/s

    power_command_w = train_data.commanded_power * 1000  # Convert kW to W
    max_power_w = 120000  # 120 kW in watts

    # If emergency brake is engaged, turn off service brake
    if train_data.emergency_brake or train_data.passenger_emergency_brake:
        train_data.service_brake = False
        train_data.auto_service_brake = False

    # Check for brakes
    if train_data.emergency_brake or train_data.passenger_emergency_brake:
        acceleration = -2.73  # m/s²
        power_command_w = 0
    elif train_data.service_brake or train_data.auto_service_brake:
        acceleration = -1.2  # m/s²
        power_command_w = 0
    else:
        # Normal operation
        if current_speed_mps == 0:
            force = max_power_w / 19.44  # Use 19.44 m/s when speed is zero
        else:
            force = power_command_w / current_speed_mps

        # Frictional force
        frictional_force = 0.002 * mass * 9.8

        # Grade calculations
        slope_angle = math.atan(train_data.grade / 100)  # Convert grade percentage to angle in radians
        grade_force = mass * 9.8 * math.sin(slope_angle)
        print(f"Grade Force: {grade_force:.2f} N")

        # Adjust force with friction and grade
        net_force = force - frictional_force - grade_force
        print(f"Net Force: {net_force:.2f} N")

        acceleration = net_force / mass
        print(f"Acceleration: {acceleration:.2f} m/s^2")

        # Cap positive acceleration to +0.5 m/s²
        if acceleration > 0.5:
            acceleration = 0.5

    # Update speed
    new_speed_mps = current_speed_mps + acceleration * delta_t
    # self.current_velocity_signal.emit(new_speed_mps * 2.23694)  # Convert m/s to mph
    # Do the connect function in train_model.py, which calls a function that updates the speed in the UI

    if new_speed_mps < 0:
        new_speed_mps = 0
        acceleration = 0  # If speed is zero, acceleration cannot be negative

    # Update position
    new_position = train_data.current_position + (delta_t * new_speed_mps)
    train_data.current_position = new_position

    # Update train_data
    train_data.current_acceleration = acceleration * 3.28084  # Convert m/s² to ft/s²
    train_data.current_speed = new_speed_mps * 2.23694  # Convert m/s back to mph

    return train_data.current_speed
