import paramiko
import re

def send_numbers_to_pi(hostname, port, username, password, numbers):
    command = f"python3 /home/maj214/Desktop/ECE1140/find_power_command.py {numbers[0]} {numbers[1]} {numbers[2]} {numbers[3]} {numbers[4]} {numbers[5]} {numbers[6]} {numbers[7]} {numbers[8]}"

    # Create SSH client
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Connect to the Raspberry Pi
        client.connect(hostname, port=port, username=username, password=password)
    
        # Execute the command
        stdin, stdout, stderr = client.exec_command(command)
    
        
        #Print any output or errors
        output = stdout.read().decode()
        error = stderr.read().decode()
        if error:
            print("Error:", error)
        else:
            print("Command output received:")
            print(output)
            
            # Parse the output to retrieve power_command, ek_previous, uk_previous, uk_current, ek_current
            output_values = output.split(',')
            if len(output_values) == 5:
                power_command, ek_previous, uk_previous, uk_current, ek_current = map(float, output_values)
                return power_command, ek_previous, uk_previous, uk_current, ek_current
            else:
                print("Unexpected output format.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
       client.close()

# if __name__ == "__main__":
#     # Replace with your Raspberry Pi details
#     raspberry_pi_hostname = '192.168.0.204'  # e.g., '192.168.1.100'
#     raspberry_pi_port = 22  # Default SSH port
#     raspberry_pi_username = 'maj214'  # e.g., 'pi'
#     raspberry_pi_password = 'password'  # e.g., 'raspberry'
#     numbers = [
#         16.0,   # Desired Velocity
#         0.0,    # Current Velcity
#         0.0,    # ek_current
#         0.0,    # ek_previous
#         0.0,    # uk_current
#         0.0,    # uk_previous
#         120000.0,   # max_power
#         7173.0,   # kp
#         15.0    # ki
#     ]
    
#     result = send_numbers_to_pi(raspberry_pi_hostname, raspberry_pi_port, raspberry_pi_username, raspberry_pi_password, numbers)
    
#     # Check if result is not None, then print the values
#     if result:
#         power_command, ek_previous, uk_previous, uk_current, ek_current = result
#         print(f"Returned values:\n"
#               f"Power Command: {power_command}\n"
#               f"ek_previous: {ek_previous}\n"
#               f"uk_previous: {uk_previous}\n"
#               f"uk_current: {uk_current}\n"
#               f"ek_current: {ek_current}")