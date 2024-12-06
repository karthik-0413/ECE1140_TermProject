import socket

def send_data_to_pi(parameters, host='10.4.119.113', port=12345):
    """
    Sends data to the Raspberry Pi server and handles responses.
    """

    try:
        # Create a socket object
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 8192)  # 8 KB receive buffer
            client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 8192)  # 8 KB send buffer
            
            print(f"Connecting to {host}:{port}...")
            client_socket.connect((host, port))
            print("Connection established.")

            # Convert parameters to a comma-separated string
            message = ','.join(map(str, parameters))
            print(f"Sending parameters: {message}")
            client_socket.sendall(message.encode('utf-8'))

            # Receive and print the server's response
            response = client_socket.recv(1024).decode('utf-8')
            print(f"Received: {response}")

            # Terminate the session
            print("Sending CLOSE message to terminate session.")
            client_socket.sendall("CLOSE".encode('utf-8'))

    except ConnectionError as e:
        print(f"Connection error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        print("Client program has ended.")

if __name__ == "__main__":
    parameters = [
            17.0,   # Desired Velocity
            0.0,    # Current Velocity
            0.0,    # ek_current
            120000.0,  # Max Power
            0.0,    # uk_current
            0.0,    # uk_previous
            0.0,    # ek_previous
            7173.0,  # kp
            15.0,     # ki
        ]
    # Update host and port as needed
    send_data_to_pi(parameters, host='10.4.119.113', port=12345)
