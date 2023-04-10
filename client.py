import socket

# Define the server address and port
SERVER_ADDRESS = ('localhost', 12000)

# Create a UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    # Display the login/register screen
    print('1. Login')
    print('2. Register')
    choice = input('Enter your choice: ')
    
    if choice == '1':
        # Get the username and password from the user
        username = input('Enter your username: ')
        password = input('Enter your password: ')
        
        # Send a login request to the server
        client_socket.sendto(f'login|{username}|{password}'.encode(), SERVER_ADDRESS)
        
        # Wait for a response from the server
        response, server_address = client_socket.recvfrom(1024)
        
        # Parse the response and determine if the login was successful
        response_parts = response.decode().split('|')
        response_type = response_parts[0]
        
        if response_type == 'login':
            if response_parts[1] == 'success':
                # Login successful, display the message screen
                while True:
                    # Display the message screen
                    print('1. Send message')
                    print('2. View messages')
                    print('3. Logout')
                    choice = input('Enter your choice: ')
                    
                    if choice == '1':
                        # Get the recipient and message from the user
                        recipient = input('Enter the recipient username: ')
                        message_text = input('Enter the message: ')
                        
                        # Send the message to the server
                        client_socket.sendto(f'send|{recipient}|{message_text}|{username}'.encode(), SERVER_ADDRESS)
                        
                        # Wait for a response from the server
                        response, server_address = client_socket.recvfrom(1024)
                        
                        # Parse the response and determine if the message was sent successfully
                        response_parts = response.decode().split('|')
                        response_type = response_parts[0]
                        
                        if response_type == 'send':
                            if response_parts[1] == 'failure':
                                print(f"Error: User '{response_parts[2]}' not found.")
                            else:
                                print('Message sent successfully.')
                        
                    elif choice == '2':
                        # Send a request for messages to the server
                        client_socket.sendto(f'view|{username}'.encode(), SERVER_ADDRESS)
                        
                        # Wait for a response from the server
                        response, server_address = client_socket.recvfrom(1024)
                        
                        # Parse the response and display the messages
                        response_parts = response.decode().split('|')
                        response_type = response_parts[0]
                        
                        if response_type == 'view':
                            message_list = response_parts[1]
                            print(message_list)
                        
                    elif choice == '3':
                        # Logout and return to the login/register screen
                        break
                
                # Send a logout request to the server
                client_socket.sendto(f'logout|{username}'.encode(), SERVER_ADDRESS)
                
            else:
                # Login failed, display an error message
                print('Error: Login failed.')
        
    elif choice == '2':
        # Get the username and password from the user
        username = input('Enter your username: ')
        password = input('Enter your password: ')
        
        # Send a register request to the server
        client_socket.sendto(f'register|{username}|{password}'.encode(), SERVER_ADDRESS)
        
        # Wait for a response from the server
        response, server_address = client_socket.recvfrom(1024)
        
        # Parse the response and determine if the registration was successful
        response_parts = response.decode().split('|')
        response_type = response_parts[0]
        
        if response_type == 'register':
            if response_parts[1] == 'success':
                # Registration successful, display the message screen
                while True:
                    # Display the message screen
                    print('1. Send message')
                    print('2. View messages')
                    print('3. Logout')
                    choice = input('Enter your choice: ')
                    
                    if choice == '1':
                        # Get the recipient and message from the user
                        recipient = input('Enter the recipient username: ')
                        message_text = input('Enter the message: ')
                        
                        # Send the message to the server
                        client_socket.sendto(f'send|{recipient}|{message_text}|{username}'.encode(), SERVER_ADDRESS)
                        
                        # Wait for a response from the server
                        response, server_address = client_socket.recvfrom(1024)
                        
                        # Parse the response and determine if the message was sent successfully
                        response_parts = response.decode().split('|')
                        response_type = response_parts[0]
                        
                        if response_type == 'send':
                            if response_parts[1] == 'failure':
                                print(f"Error: User '{response_parts[2]}' not found.")
                            else:
                                print('Message sent successfully.')
                        
                    elif choice == '2':
                        # Send a request for messages to the server
                        client_socket.sendto(f'view|{username}'.encode(), SERVER_ADDRESS)
                        
                        # Wait for a response from the server
                        response, server_address = client_socket.recvfrom(1024)
                        
                        # Parse the response and display the messages
                        response_parts = response.decode().split('|')
                        response_type = response_parts[0]
                        
                        if response_type == 'view':
                            message_list = response_parts[1]
                            print(message_list)
                        
                    elif choice == '3':
                        # Logout and return to the login/register screen
                        break
                
                # Send a logout request to the server
                client_socket.sendto(f'logout|{username}'.encode(), SERVER_ADDRESS)
                
            else:
                # Registration failed, display an error message
                print('Error: Registration failed.')
