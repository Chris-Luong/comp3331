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
import os
from socket import *
import sys
import difflib

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

msgQueue = []

"""
    Parameter is the message received from server
    Return type is constant integer
"""
def loginUser(recvMsg):
    print("entering username while loop")
    while recvMsg == 'Username: ':
        print("requesting username in while loop")
        username = input(recvMsg)
        if username == '':
            print("username is empty string")
            continue
        print("sending username to server")
        clientSocket.send(str.encode(username))
        return INACTIVE_USER
    print("entering if else statement block")
    if recvMsg == 'Password: ':
        print("requesting password")
        password = input(recvMsg)
        print("sending password")
        clientSocket.send(str.encode(password))
        return INACTIVE_USER
    elif recvMsg == USERNAME_ERROR_MESSAGE or recvMsg == PASSWORD_ERROR_MESSAGE:
        print("printing recvMsg")
        print(recvMsg)
        return INACTIVE_USER
    elif recvMsg == FIRST_BLOCKED_USER_MESSAGE or recvMsg == BLOCKED_USER_MESSAGE:
        print(recvMsg)
        return BLOCKED_USER
    elif recvMsg == WELCOME_MESSAGE:
        print(recvMsg)
        return ACTIVE_USER
    else:
        print(f"\'{recvMsg}\' => \'{USERNAME_ERROR_MESSAGE}\'")
        for i,s in enumerate(difflib.ndiff(recvMsg, USERNAME_ERROR_MESSAGE)):
            if s[0]==' ': continue
            elif s[0]=='-':
                print(u'Delete "{}" from position {}'.format(s[-1],i))
            elif s[0]=='+':
                print(u'Add "{}" to position {}'.format(s[-1],i))
        print(recvMsg)
        return ERROR

while True:
    """
        Only one receiver as TCP is a stream-based (not message-based) protocol.
        Some messages from server may be segmented/bundled across a few recv() calls so
        having one receiver causes less issues than multiple receivers treating
        send() calls as 1 message for 1 recv() call.
    """
    received = clientSocket.recv(1024).decode().split('\0')
    for r in received:
        print("r is "+r)
        if r != '':
           msgQueue.append(r)
    recvMsg = msgQueue[0]
    print("recvMsg is "+recvMsg)
    for thing in msgQueue:
        print("msgQueue is "+thing)

    if not isActive:
        # print("isActive is ", isActive)
        res = loginUser(recvMsg)
        print("after loginUser function, result is ", res)
        if res == INACTIVE_USER or res == ERROR:
            # invalid username/password message received so get next msg from server (username: or password:)
            print("message to be popped "+msgQueue[0])
            msgQueue.pop(0) # remove most recent message from queue
            continue
        elif res == BLOCKED_USER:
            clientSocket.close() # test this since server is not closing conn now
            break
        elif res == ACTIVE_USER:
            isActive = True
            justTurnedActive = True
            msgQueue.pop(0)
            continue

    if justTurnedActive:
        """
            Code below is for reading the last line of a file, taken from
            https://www.codingem.com/how-to-read-the-last-line-of-a-file-in-python/
            Assumes format of userlog.txt is the one specified in the specifcation i.e.
            Ativer user sequence number; timestamp; username
            e.g. 1; 31 Jul 2022 17:52:15; hans
        """
        with open("userlog.txt", "rb") as file:
            try:
                file.seek(-2, os.SEEK_END)
                while file.read(1) != b'\n':
                    file.seek(-2, os.SEEK_CUR)
            except OSError:
                file.seek(0)
            last_line = file.readline().decode()
            username = last_line.split()[5]
        justTurnedActive = False

    while recvMsg == COMMAND_INSTRUCTIONS:
        userInput = input(recvMsg)
        if userInput not in commands:
            print("Error. Invalid command!")
            continue
        clientSocket.send(str.encode(userInput))
        break
    if recvMsg == (f"Bye, {username}!"): # OUT
        print(recvMsg)
        clientSocket.close()
        break

    msgQueue.pop(0)

# close the socket
# print("closing connection")
# clientSocket.close()
# print(f"USERNAME IS {username}")
# print(f"COMMMAND IS {recvMsg}")
