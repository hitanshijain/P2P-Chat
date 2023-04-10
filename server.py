import socket

def run_server():
    # Set up the server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8000))
    server_socket.listen()

    # Create a dictionary to store the client sockets and their associated usernames
    clients = {}

    # Receive connections and messages from clients
    while True:
        # Wait for a client to connect
        print('Waiting for a client to connect...')
        client_socket, client_address = server_socket.accept()
        print(f'Client connected: {client_address}')

        # Receive the client's username and store it in the clients dictionary
        username = client_socket.recv(1024).decode()
        clients[username] = client_socket
        print(username)

        # Receive messages from the client
        while True:
            message = client_socket.recv(1024).decode()
            if message == 'exit':
                break
            print(f'Received message from {username}: {message}')

            # Send the message to the intended recipient
            if ':' in message:
                recipient_username, message_body = message.split(':', 1)
                if recipient_username in clients:
                    recipient_socket = clients[recipient_username]
                    recipient_socket.send(f'{username}: {message_body}'.encode())
                else:
                    print(f'Error: {recipient_username} not found.')
            else:
                print(f'Error: Invalid message format.')

        # Remove the client from the clients dictionary
        del clients[username]

        # Close the client socket
        client_socket.close()

    # Close the server socket
    server_socket.close()

if __name__ == '__main__':
    run_server()
