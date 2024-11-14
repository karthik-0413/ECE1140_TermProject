import paramiko
import re

def send_numbers_to_pi(hostname, port, username, password, numbers):
    # Create the command to execute on the Raspberry Pi with numbers as arguments
    numbers = [0.00, 5.00, 7173.0, 15.0, 0.00, 0.00, 120000]
    command = f"python3 /home/maj214/Desktop/ECE1140/find_power_command.py {numbers[0]} {numbers[1]} {numbers[2]} {numbers[3]} {numbers[4]} {numbers[5]} {numbers[6]} {numbers
                                                                                                                                                                       [7]} {numbers[8]}"

    # Create SSH client
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Connect to the Raspberry Pi
        client.connect(hostname, port=port, username=username, password=password)
        # Execute the command
        stdin, stdout, stderr = client.exec_command(command)
        
        # Print any output or errors
        output = stdout.read().decode()
        error = stderr.read().decode()
        if error:
            print("Error:", error)
        else:
            print("Raw output from Raspberry Pi:", output)
            
            # Adjust regex to be more flexible and match the output line
            match = re.search(r"The sum of the numbers is:\s*(\d+)", output)
            if match:
                sum_result = int(match.group(1))
                print(f"Sum stored in variable: {sum_result}")
                return sum_result
            else:
                print("Could not find the sum in the output.")
                return None
    finally:
        client.close()

if __name__ == "__main__":
    # Replace with your Raspberry Pi details
    raspberry_pi_hostname = '192.168.0.204'  # e.g., '192.168.1.100'
    raspberry_pi_port = 22  # Default SSH port
    raspberry_pi_username = 'maj214'  # e.g., 'pi'
    raspberry_pi_password = 'password'  # e.g., 'raspberry'
    numbers = [
        19.0,   # Desired Velocity
        0.0,    # Current Velcity
        0.0,    # ek_current
        0.0,    # ek_previous
        0.0,    # uk_current
        0.0,    # uk_previous
        120000.0,   # max_power
        7313.0,   # kp
        15.0    # ki
    ]
    
    send_numbers_to_pi(raspberry_pi_hostname, raspberry_pi_port, raspberry_pi_username, raspberry_pi_password, numbers)