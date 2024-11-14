import paramiko
import re

def send_numbers_to_pi(hostname, port, username, password, numbers):
    # Ensure that numbers has exactly 9 elements
    if len(numbers) != 9:
        print(f"Error: The number of elements in the numbers list is incorrect. Found {len(numbers)} elements.")
        return None
    
    # Print the list of numbers for debugging
    #print(f"Numbers being passed: {numbers}")
    
    # Construct the command to run on the Raspberry Pi (the full path to your script)
    command = f"python3 -c 'import sys; sys.path.insert(0, \"/home/maj214/Desktop/ECE1140\"); from find_power_command import update_power_command; print(*update_power_command({', '.join(map(str, numbers))}), sep=\",\")'"
    
    # Print the command to verify
    #print(f"Running command: {command}")
    
    # Create SSH client
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        # Connect to the Raspberry Pi
        client.connect(hostname, port=port, username=username, password=password)
        
        # Execute the command
        stdin, stdout, stderr = client.exec_command(command)
        
        # Capture the output and remove any extra spaces or newlines
        output = stdout.read().decode().strip()
        error = stderr.read().decode().strip()

        # Check if there were any errors
        if error:
            print(f"Error occurred: {error}")
            return None
        else:
            # Debugging: print the output from Raspberry Pi
            #print("Command output received:")
            #print(output)
            
            # Now, we use a regex to extract only the five expected numbers
            # We expect five numbers separated by commas, so we'll extract the first line of output
            numeric_output = re.findall(r'[-+]?\d*\.\d+|\d+', output.splitlines()[0])
            
            #print(f"Filtered numeric output: {numeric_output}")
            
            if len(numeric_output) == 5:
                # Convert output values to float
                power_command, ek_previous, uk_previous, uk_current, ek_current = map(float, numeric_output)
                return power_command, ek_previous, uk_previous, uk_current, ek_current
            else:
                print("Unexpected output format.")
                return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        # Close the client connection
        client.close()


if __name__ == "__main__":
    # Replace with your Raspberry Pi details
    raspberry_pi_hostname = '192.168.0.204'  # e.g., '192.168.1.100'
    raspberry_pi_port = 22  # Default SSH port
    raspberry_pi_username = 'maj214'  # e.g., 'pi'
    raspberry_pi_password = 'password'  # e.g., 'raspberry'
    numbers = [
        16.0,   # Desired Velocity
        0.0,    # Current Velcity
        0.0,    # ek_current
        120000.0,   # max_power
        0.0,    # uk_current
        0.0,    # uk_previous
        0.0,    # ek_previous
        7173.0,   # kp
        15.0    # ki
    ]
    
    result = send_numbers_to_pi(raspberry_pi_hostname, raspberry_pi_port, raspberry_pi_username, raspberry_pi_password, numbers)
    
    
    # # Check if result is not None, then print the values
    if result:
        power_command, ek_previous, uk_previous, uk_current, ek_current = result
        print(f"Returned values:\n"
              f"Power Command: {power_command}\n"
              f"ek_previous: {ek_previous}\n"
              f"uk_previous: {uk_previous}\n"
              f"uk_current: {uk_current}\n"
              f"ek_current: {ek_current}")