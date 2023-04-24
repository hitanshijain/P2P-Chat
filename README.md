# P2P-Chat
Team Members: Hitanshi Jain, Ajay Krishna Anand

- This is a Peer to Peer chat application that uses the User Datagram Protocol (UDP) for communication. The server and client code are provided in two separate files. Please find the server.py and client.py code files for Peer to Peer Chat implementation using Python. 
- We have included login, registration, send messages, view messages functionalities in our application. 
- We have used SQLite database in our application, which has users and messages table in it. 

Explanation:

- Server File:

1. The script defines a server that listens for incoming messages from clients over the network using the User Datagram Protocol (UDP).
2. The server address and port number are defined in the script.
3. The server creates a UDP socket using the socket module and binds it to the server address.
4. The script stores registered users in a dictionary and messages in a list of tuples.
5. The server listens for incoming messages from clients in an infinite loop using the recvfrom() method.
6. The incoming message is parsed to determine its type.
7. If the message type is login, the server checks if the username and password are correct by looking up the username in the registered users dictionary.
8. If the message type is register, the server adds the user to the list of registered users.
9. If the message type is send, the server forwards the message to the appropriate peer by looking up the recipient's address in the registered users dictionary.
10. If the message type is view, the server sends a list of messages to the requesting user by filtering the messages list and joining the messages into a string.
11. The server sends a response back to the client over the network using the sendto() method.

- Client File:

1. The script defines a client that connects to the server using the server address and port number.
2. The client creates a UDP socket using the socket module.
3. The client displays a login/register screen to the user using the input() function.
4. If the user chooses to login, the client prompts the user to enter their username and password.
5. The client sends a login request to the server over the network using the sendto() method.
6. The client waits for a response from the server using the recvfrom() method.
7. The client parses the response and determines if the login was successful.
8. If the login was successful, the client displays a message screen to the user using the input() function.
9. If the user chooses to send a message, the client prompts the user to enter the recipient and message.
10. The client sends the message to the server over the network using the sendto() method.
11. The client waits for a response from the server using the recvfrom() method.
12. The client parses the response and determines if the message was sent successfully.
13. If the user chooses to view messages, the client sends a request for messages to the server over the network using the sendto() method.
14. The client waits for a response from the server using the recvfrom() method.
15. The client parses the response and displays the messages to the user using the print() function.
16. If the user chooses to logout, the client sends a logout request to the server over the network using the sendto() method and returns to the login/register screen.
