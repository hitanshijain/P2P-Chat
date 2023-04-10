import socket

# Define the server address and port
SERVER_ADDRESS = ('localhost', 12000)

# Create a UDP socket and bind it to the server address
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(SERVER_ADDRESS)

# Store registered users in a dictionary
registered_users = {}

# Store messages in a list of tuples: (sender, recipient, message)
messages = []

while True:
    # Wait for incoming messages
    message, client_address = server_socket.recvfrom(1024)
    
    # Parse the message and determine its type
    message_parts = message.decode().split('|')
    message_type = message_parts[0]
    
    if message_type == 'login':
        # Check if the username and password are correct
        username = message_parts[1]
        password = message_parts[2]
        
        if username in registered_users and registered_users[username] == password:
            # Send a success message back to the client
            server_socket.sendto('login|success'.encode(), client_address)
        else:
            # Send a failure message back to the client
            server_socket.sendto('login|failure'.encode(), client_address)
    
    elif message_type == 'register':
        # Add the user to the list of registered users
        username = message_parts[1]
        password = message_parts[2]
        registered_users[username] = client_address
        
        # Send a success message back to the client
        server_socket.sendto('register|success'.encode(), client_address)
    
    elif message_type == 'send':
        # Forward the message to the appropriate peer
        recipient = message_parts[1]
        message_text = message_parts[2]
        sender = message_parts[3]
        
        # Find the recipient's address in the registered_users dictionary
        if recipient in registered_users:
            recipient_address = registered_users[recipient]
            messages.append((sender, recipient, message_text))
            server_socket.sendto(f'send|{sender}|{message_text}'.encode(), recipient_address)
        else:
            # Send a failure message back to the client
            server_socket.sendto(f'send|failure|{recipient}'.encode(), client_address)
    
    elif message_type == 'view':
        # Send a list of messages to the requesting user
        username = message_parts[1]
        user_messages = [m for m in messages if m[0] == username or m[1] == username]
        message_list = '\n'.join([f'{m[0]} -> {m[1]}: {m[2]}' for m in user_messages])
        server_socket.sendto(f'view|{message_list}'.encode(), client_address)
