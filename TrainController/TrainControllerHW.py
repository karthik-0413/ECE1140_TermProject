import socket
import time

def send_data_to_pi(parameters, host='10.4.90.148', port=12345):
    """
    Sends data to the Raspberry Pi server and handles responses.
    """
    try:
        # Create a socket object
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            # Set socket options for buffer sizes and no Nagle's algorithm
            client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 4096)  # Increased buffer size to 16 KB
            client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 4096)  # Increased buffer size to 16 KB
            client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)  # Disable Nagle's algorithm
            
            print(f"Connecting to {host}:{port}...")
            client_socket.connect((host, port))
            print("Connection established.")

            # Convert parameters to a comma-separated string
            message = ','.join(map(str, parameters))
            print(f"Sending parameters: {message}")
            
            # Measure the time before sending data
            start_time = time.time()
            client_socket.sendall(message.encode('utf-8'))

            # Receive the response
            response = client_socket.recv(16384).decode('utf-8')  # Use larger buffer to receive bigger messages
            print(f"Received: {response}")
            
            # Measure the time after receiving data
            end_time = time.time()

            # Calculate the number of bits sent
            bytes_sent = len(message.encode('utf-8'))
            bytes_received = len(response.encode('utf-8'))

            # Calculate the elapsed time in seconds
            elapsed_time = end_time - start_time

            # Calculate the bit rate (bits per second)
            bits_sent = bytes_sent * 8
            bits_received = bytes_received * 8

            # Print out the bit rate
            print(f"Bit Rate: Sent = {bits_sent / elapsed_time} bps, Received = {bits_received / elapsed_time} bps")

            return response

    except ConnectionError as e:
        print(f"Connection error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        print("Client program has ended.")

# Example usage
# if __name__ == "__main__":
#     parameters = [
#         1.0, 0.0, 0.0, 120000.0, 0.0, 0.0, 0.0, 7173.0, 15.0, 
#         False, False, False, False, False, False, False
#     ]
#     send_data_to_pi(parameters, host='10.4.90.148', port=12345)