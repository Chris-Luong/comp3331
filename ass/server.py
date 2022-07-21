"""
    Python 3
    Usage: python3 server.py [PORT NUMBER] [NUMBER OF CONSECUTIVE ATTEMPTS]
    coding: utf-8
    Christopher Luong
"""

"""
TODO: CHECK ass_notes.md
"""


import os
from time import sleep, time
from socket import *
from threading import Thread
import sys, select

# acquire server host and port from command line parameter
if len(sys.argv) != 3:
    print("\n===== Error usage, python3 server.py SERVER_PORT number_of_consecutive_failed_attempts ======\n")
    exit(0)
elif not sys.argv[2].isalnum() or int(sys.argv[2]) > 5 or int(sys.argv[2]) < 1: # error message from spec
    print(f"Invalid number of allowed failed consecutive attempt: {sys.argv[2]}. The valid value of argument number is an integer between 1 and 5.")
    exit(0)
serverHost = "127.0.0.1"
serverPort = int(sys.argv[1])
serverAddress = (serverHost, serverPort)
numAttempts = int(sys.argv[2])

# define socket for the server side and bind address
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(serverAddress)

# read credentials file to create a dicionary for user information
userInfo = {} # make this a list of dicts instead
f = open('credentials.txt', 'r')
for pairs in f.readlines():
    userInfo[pairs.split()[0]] = pairs.split()[1]

# attempts dictionary, or put this as the status in userInfo
failed_attempt_IP = {} # or have a blockdUser dict

# session dict
session_dict = {}


"""
    Define multi-thread class for client
    This class would be used to define the instance for each connection from each client
    For example, client-1 makes a connection request to the server, the server will call
    class (ClientThread) to define a thread for client-1, and when client-2 make a connection
    request to the server, the server will call class (ClientThread) again and create a thread
    for client-2. Each client will be runing in a separate therad, which is the multi-threading
"""


class ClientThread(Thread):
    def __init__(self, clientAddress, clientSocket):
        Thread.__init__(self)
        self.clientAddress = clientAddress
        self.clientSocket = clientSocket
        self.clientAlive = False

        print("===== New connection created for: ", clientAddress)
        self.clientAlive = True

    def run(self):
        # When user is not logged in, check if the cookie for this
        # User is stored within the session dict
        isLogged = False

        while self.clientAlive:
            # Make it while not logged, if numAttempt reached, sleep
            # Authentication
            if not isLogged:
                attemptCnt = 0
                while attemptCnt < numAttempts:
                    print('[send] username request')
                    self.clientSocket.send(str.encode('Username: '))  # Username
                    username = self.clientSocket.recv(1024)
                    username = username.decode()

                    # check if username exists TODO: if user logged in already
                    if username not in userInfo.keys():
                        message = 'Invalid username!'
                        self.clientSocket.send(str.encode(message))
                        attemptCnt += 1 # remove if user can do unlimited tims
                        continue

                    print('[send] password request')
                    self.clientSocket.send(str.encode('Password: '))  # Password
                    password = self.clientSocket.recv(1024)
                    password = password.decode()

                    # Check if password is valid TODO: if user is blocked
                    if password != userInfo[username]:
                        message = 'Invalid password!'
                        self.clientSocket.send(str.encode(message))
                        attemptCnt += 1
                        continue
                    isLogged = True
                    print("User logged in successfully!")
                    self.clientSocket.send(str.encode("Welcome to TOOM!\n"))

            self.clientSocket.send(str.encode("Invalid password. Account blocked 10s\n"))
            print("[send] user blocked. Closing connection")
            self.clientSocket.close()
            self.clientAlive = False

# if not isLogged:
#     # sleep pauses everything so use a time add instead.
#     # https://www.programiz.com/python-programming/time
#     # how to print one line but separated in code
#     print("Your account is blocked due to multiple login failures. Please try again later")
#     sleep(10)
print("\n===== Server is running =====")
print("===== Waiting for connection request from clients...=====")


while True:
    serverSocket.listen()
    clientSockt, clientAddress = serverSocket.accept()
    clientThread = ClientThread(clientAddress, clientSockt)
    clientThread.start()