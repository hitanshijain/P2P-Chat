import socket
import sqlite3

# Define the server address and port
SERVER_ADDRESS = ('localhost', 12000)

# Connect to the SQLite database
conn = sqlite3.connect('messenger.db')
c = conn.cursor()

# Create the users table if it does not exist
c.execute('''CREATE TABLE IF NOT EXISTS users
             (username text primary key, password text)''')

# Create the messages table if it does not exist
c.execute('''CREATE TABLE IF NOT EXISTS messages
             (id integer primary key autoincrement, sender text, recipient text,
             message text, sent_at datetime default current_timestamp)''')


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
        
        # Check if the user exists in the database
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        user = c.fetchone()
        
        if user is None:
            # User does not exist, display an error message
            print('Error: User does not exist.')
        elif user[1] != password:
            # Password is incorrect, display an error message
            print('Error: Password is incorrect.')
        else:
            # Login successful, display the message screen
            print("User Logged in successfully!")
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
                    
                    # Check if the recipient exists in the database
                    c.execute("SELECT * FROM users WHERE username=?", (recipient,))
                    recipient_user = c.fetchone()
                    
                    if recipient_user is None:
                        # Recipient does not exist, display an error message
                        print(f"Error: User '{recipient}' not found.")
                    else:
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
                    # Retrieve messages from the database
                    c.execute("SELECT * FROM messages WHERE recipient=?", (username,))
                    messages = c.fetchall()
                    
                    # Display the messages
                    if len(messages) == 0:
                        print('No messages.')
                    else:
                        for message in messages:
                            print(f"{message[1]}: {message[3]} ({message[4]})")
                
                elif choice == '3':
                    # Logout and return to the login/register screen
                    break

                
                # Send a logout request to the server
            client_socket.sendto(f'logout|{username}'.encode(), SERVER_ADDRESS)
                
            
    elif choice == '2':
        # Get the username and password from the user
        username = input('Enter your username: ')
        password = input('Enter your password: ')
        
        # Check if the user already exists in the database
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        user = c.fetchone()
        
        if user:
            # User already exists, display an error message
            print('Error: User already exists.')
        else:
            
            # Send a register request to the server
            client_socket.sendto(f'register|{username}|{password}'.encode(), SERVER_ADDRESS)
            
            # Wait for a response from the server
            response, server_address = client_socket.recvfrom(1024)
            
            # Parse the response and determine if the registration was successful
            response_parts = response.decode().split('|')
            response_type = response_parts[0]
            
            if response_type == 'register':
                if response_parts[1] == 'success':
                    print("User Registered successfully!")
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

