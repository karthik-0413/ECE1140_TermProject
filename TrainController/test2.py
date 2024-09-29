import time

def reach_temperature(initial_temp, desired_temp, k=0.1, time_step=1):
    """
    Gradually increase temperature from initial_temp to desired_temp using a first-order equation.
    
    Parameters:
    - initial_temp (float): The starting temperature.
    - desired_temp (float): The desired temperature to reach.
    - k (float): The rate constant controlling the speed of change.
    - time_step (float): Time interval between updates in seconds.

    Returns:
    - None
    """
    current_temp = initial_temp
    while abs(current_temp - desired_temp) > 0.01:  # Tolerance for stopping
        # Calculate the change in temperature using a first-order equation
        dT = k * (desired_temp - current_temp)
        
        # Update the current temperature
        current_temp += dT
        
        # Print the current temperature
        print(f"Current Temperature: {current_temp:.2f}°C")
        
        # Wait for the specified time step
        time.sleep(time_step)

    print(f"Reached Desired Temperature: {current_temp:.2f}°C")

# Input from the user
initial_temperature = float(input("Enter the initial temperature (°C): "))
desired_temperature = float(input("Enter the desired temperature (°C): "))

# Simulate temperature change
reach_temperature(initial_temperature, desired_temperature)
