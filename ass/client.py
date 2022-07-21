"""
    Python 3
    Usage: python3 client.py [SERVER IP] [SERVER PORT]
    coding: utf-8
    Christopher Luong
"""

"""
TODO:
    proper request calls
    peer to peer communication
"""

from socket import *
import sys

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

while True:
    # send loggin_in var to the server

    # Input username
    # username = input(clientSocket.recv(1024).decode())
    clientSocket.send(username.encode())

    # Input password
    password = input(clientSocket.recv(1024).decode())
    clientSocket.send(str.encode(password))

    # receive response from the server
    # 1024 is a suggested packet size, you can specify it as 2048 or others
    data = clientSocket.recv(1024)
    receivedMessage = data.decode()
    print(receivedMessage)


# close the socket
clientSocket.close()