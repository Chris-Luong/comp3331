"""
    Python 3
    Usage: python3 client.py [SERVER IP] [SERVER PORT]
    coding: utf-8
    Christopher Luong (z5309196)
"""

"""
TODO:
    proper request calls
    peer to peer communication
"""

from socket import *
import sys

from myconstants import *

# Server would be running on the same host as Client
if len(sys.argv) != 3:
    print("\n===== Error usage, python3 client.py SERVER_IP SERVER_PORT ======\n")
    exit(0)


serverHost = sys.argv[1]
serverPort = int(sys.argv[2])
serverAddress = (serverHost, serverPort)

# define a socket for the client side, it would be used to communicate with the server
clientSocket = socket(AF_INET, SOCK_STREAM)

# build connection with the server and send message to it
clientSocket.connect(serverAddress)

data = clientSocket.recv(1024)
firstConnection = True
isActive = False
result = INACTIVE_USER

"""
    Parameter is the message received from server
    Return type is constant integer
"""
def loginUser(receivedMessage):
    if receivedMessage == FIRST_BLOCKED_USER_MESSAGE or receivedMessage == BLOCKED_USER_MESSAGE:
        print(receivedMessage)
        return BLOCKED_USER
    elif receivedMessage == USERNAME_ERROR_MESSAGE or receivedMessage == PASSWORD_ERROR_MESSAGE:
        print(receivedMessage)
        return INACTIVE_USER
    elif receivedMessage == WELCOME_MESSAGE:
        return ACTIVE_USER
    else:
        userInput = input(receivedMessage)
        clientSocket.send(str.encode(userInput))
        return INACTIVE_USER

while data != '': # this should be while connected
    # send loggin_in var to the server


    # receive response from the server
    # 1024 is a suggested packet size, you can specify it as 2048 or others
    if not firstConnection:
        data = clientSocket.recv(1024)
    else:
        firstConnection = False
    receivedMessage = data.decode()

    if not isActive:
        result = loginUser(receivedMessage)
        if result == INACTIVE_USER: # invalid username/password message received so get next msg from server (username: or password:)
            continue    
        elif result == BLOCKED_USER:
            clientSocket.close()
            break
        elif result == ACTIVE_USER:
            isActive = True
            print('user is active')
    
    message = clientSocket.recv(1024).decode()
    if message == COMMAND_INSTRUCTIONS:
        print("do smthn")

# close the socket
# print("closing connection")
# clientSocket.close()
