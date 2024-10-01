import time
import random

# Function to simulate sensor readings
def read_voltage():
    # Simulate voltage reading
    return random.uniform(1.0, 5.0)  # Voltage between 1V and 5V

def read_current():
    # Simulate current reading
    return random.uniform(0.1, 2.0)  # Current between 0.1A and 2A

def calculate_power(voltage, current):
    return voltage * current

def main():
    while True:
        voltage = read_voltage()
        current = read_current()
        power = calculate_power(voltage, current)
        
        print(f"Voltage: {voltage:.2f} V, Current: {current:.2f} A, Power: {power:.2f} W")
        
        time.sleep(1)  # Update every 1 second

if __name__ == "__main__":
    main()