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

while data != '': # this should be while connected
    # send loggin_in var to the server


    # receive response from the server
    # 1024 is a suggested packet size, you can specify it as 2048 or others
    if not firstConnection:
        data = clientSocket.recv(1024)
    else:
        firstConnection = False
    receivedMessage = data.decode()       
    # print(receivedMessage)
    if receivedMessage == BLOCKED_USER_MESSAGE:
        # close the socket
        print(receivedMessage)
        clientSocket.close()
        break
    # Input username
    # print("requesting username")
    username = input(receivedMessage)
    clientSocket.send(str.encode(username))
    # will need to receive from server to see if success or fail from message

    # Input password
    # print("requesting password")
    password = input(clientSocket.recv(1024).decode())
    clientSocket.send(str.encode(password))

# close the socket
# print("closing connection")
# clientSocket.close()
