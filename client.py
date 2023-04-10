import socket

def run_client(token):
    # Set up the client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 8000))

    # Send the token to the server to authenticate the client
    client_socket.send(token.encode())

    # Send messages to the server
    while True:
        # Prompt the user to enter a recipient username and a message
        recipient_username = input('Enter recipient username: ')
        message = input('Enter a message (type "exit" to quit): ')
        if message == 'exit':
            client_socket.send(message.encode())
            break
        # Send the message in the correct format
        formatted_message = f"{recipient_username}:{message}:{token}"
        client_socket.send(formatted_message.encode())

    # Close the connection
    client_socket.close()

# if __name__ == '__main__':
#     run_client()