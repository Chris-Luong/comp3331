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

# data = clientSocket.recv(1024)
# firstConnection = True
isActive = False
justTurnedActive = False
res = INACTIVE_USER
commands = ['BCM', 'ATU', 'SRB', 'SRM', 'RDM', 'OUT', 'UPD']
username = ''

"""
    Parameter is the message received from server
    Return type is constant integer
"""
def loginUser(receivedMessage):
    while receivedMessage == 'Username: ':
        username = input(receivedMessage)
        if username == '':
            continue
        clientSocket.send(str.encode(username))
        return INACTIVE_USER
    if receivedMessage == 'Password: ':
        password = input(receivedMessage)
        clientSocket.send(str.encode(password))
        return INACTIVE_USER
    elif receivedMessage == USERNAME_ERROR_MESSAGE or receivedMessage == PASSWORD_ERROR_MESSAGE:
        print(receivedMessage)
        return INACTIVE_USER
    elif receivedMessage == FIRST_BLOCKED_USER_MESSAGE or receivedMessage == BLOCKED_USER_MESSAGE:
        print(receivedMessage)
        return BLOCKED_USER
    elif receivedMessage == WELCOME_MESSAGE:
        print(receivedMessage)
        return ACTIVE_USER
    else:
        return ERROR

while True:
    """
        Only one receiver as TCP is a stream-based (not message-based) protocol.
        Some messages from server may be segmented across a few recv() calls so
        having one receiver causes less issues than multiple receivers treating
        send() calls as 1 message for 1 recv() call.
    """
    receivedMessage = clientSocket.recv(1024).decode()

    if not isActive:
        res = loginUser(receivedMessage)

        if res == INACTIVE_USER or res == ERROR:
            # invalid username/password message received so get next msg from server (username: or password:)
            continue
        elif res == BLOCKED_USER:
            clientSocket.close() # test this since server is not closing conn now
            break
        elif res == ACTIVE_USER:
            isActive = True
            justTurnedActive = True
            continue

    if justTurnedActive:
        username = receivedMessage # maybe get the username from userlog instead since serv's username msg seems to stuff things up
        print(username)
        justTurnedActive = False
        continue

    while receivedMessage == COMMAND_INSTRUCTIONS:
        userInput = input(receivedMessage)
        if userInput not in commands:
            print("Error. Invalid command!")
            continue
        clientSocket.send(str.encode(userInput))
        break
    if receivedMessage == (f"Bye, {username}!"): # OUT
        print(receivedMessage)
        clientSocket.close()
        break

# close the socket
# print("closing connection")
# clientSocket.close()
# print(f"USERNAME IS {username}")
# print(f"COMMMAND IS {receivedMessage}")
