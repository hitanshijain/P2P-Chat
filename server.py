import socket
import sqlite3
import datetime

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
        
        # Connect to the database and execute a query to retrieve the user's password
        with sqlite3.connect('messenger.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
            result = cursor.fetchone()
            
            if result is not None and result[0] == password:
                # Send a success message back to the client
                server_socket.sendto('login|success'.encode(), client_address)
            else:
                # Send a failure message back to the client
                server_socket.sendto('login|failure'.encode(), client_address)

    elif message_type == 'register':
        # Add the user to the database
        username = message_parts[1]
        password = message_parts[2]
        
        # Connect to the database and execute a query to check if the username is already in use
        with sqlite3.connect('messenger.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
            result = cursor.fetchone()
            if result is not None:
                # Send a failure message back to the client if the username is already in use
                server_socket.sendto('register|failure|Username already in use'.encode(), client_address)
            else:
                # Execute a query to insert the new user if the username is available
                cursor.execute('INSERT INTO users VALUES (?, ?)', (username, password))
                conn.commit()
            
                # Send a success message back to the client
                server_socket.sendto('register|success'.encode(), client_address)

    elif message_type == 'send':
        # Forward the message to the appropriate peer
        recipient = message_parts[1]
        message_text = message_parts[2]
        sender = message_parts[3]
        
        # Connect to the database and execute a query to insert the new message
        with sqlite3.connect('messenger.db') as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO messages (sender, recipient, message, sent_at) VALUES (?, ?, ?, ?)',
                (sender, recipient, str(message_text), str(datetime.datetime.now())))

            conn.commit()
        # Find the recipient's address in the registered_users dictionary
        cursor.execute('SELECT * FROM users WHERE username = ?', (recipient,))
        result = cursor.fetchone()
        if result is not None:
            server_socket.sendto(f'send|{sender}|{message_text}'.encode(), client_address)
        else:
            # Send a failure message back to the client
            server_socket.sendto(f'send|failure|{recipient}'.encode(), client_address)

    elif message_type == 'view':
        # Send a list of messages to the requesting user
        username = message_parts[1]
        
        # Connect to the database and execute a query to retrieve the user's messages
        with sqlite3.connect('messenger.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT sender, message FROM messages WHERE recipient = ?', (username,))
            result = cursor.fetchall()
        
        # Format the messages as a string
        user_messages = [f'{row[0]}: {row[1]}' for row in result]
        message_list = '\n'.join(user_messages)
        server_socket.sendto(f'view|{message_list}'.encode(), client_address)
