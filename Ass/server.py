"""
    Python 3
    Usage: python3 server.py [PORT NUMBER] [NUMBER OF CONSECUTIVE ATTEMPTS]
    coding: utf-8
    Christopher Luong
"""

"""
TODO:
report.pdf: attribute multithreading to WebCMS sample code
    single user login
    blocking for unsuccessful attempts (based on number and time)
    multiple clients logged in
    broadcast, read and room functionality
    active users and log off functionality
"""

"""
Thoughts:
    userInfo is list of dicts, or dict with username as key and dict of things as value
    userInfo.status options: [active, inactive, blocked] with active = logged in;
    with any future options, might have to group with 'active' in conditional as logged in
"""

import os
from time import time
from socket import *
from threading import Thread
import sys, select

# acquire server host and port from command line parameter
if len(sys.argv) != 3:
    print("\n===== Error usage, python3 TCPServer3.py SERVER_PORT number_of_consecutive_failed_attempts ======\n")
    exit(0)
elif not sys.argv[2].isalnum() or int(sys.argv[2]) > 5 or int(sys.argv[2]) < 1:
    print(f"Invalid number of allowed failed consecutive attempt: {sys.argv[2]}. The valid value of argument number is an integer between 1 and 5.")
    exit(0)
serverHost = "127.0.0.1"
serverPort = int(sys.argv[1])
serverAddress = (serverHost, serverPort)
numAttempts = int(sys.argv[2])

# define socket for the server side and bind address
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(serverAddress)

# read credentials file and turn it into a dictionary
userInfo = {}
f = open('credentials.txt', 'r')
for pairs in f.readlines():
    userInfo[pairs.split()[0]] = pairs.split()[1]

# attempts dictionary, or put this as the status in userInfo
failed_attempt_IP = {}

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
        is_logged = False

        while self.clientAlive:

            # Authentication
            if not is_logged:
                failed_count = 0
                while failed_count < numAttempts:
                    print('[send] username request')
                    self.clientSocket.send(str.encode('Username: '))  # Username
                    username = self.clientSocket.recv(1024)
                    username = username.decode()

                    # check if username exists
                    if username not in userInfo.keys():
                        message = 'Invalid username!'
                        self.clientSocket.send(str.encode(message))
                        failed_count += 1
                        continue

                    print('[send] password request')
                    self.clientSocket.send(str.encode('Password: '))  # Password
                    password = self.clientSocket.recv(1024)
                    password = password.decode()

                    # Check if password is valid
                    if password != userInfo[username]:
                        failed_count += 1
                        message = 'Invalid password!'
                        self.clientSocket.send(str.encode(message))
                        continue
                    else:
                        print("User logged in successfully!")
                        self.clientSocket.send(str.encode("Welcome to TOOM!\n"))

            self.clientSocket.close()


print("\n===== Server is running =====")
print("===== Waiting for connection request from clients...=====")


while True:
    serverSocket.listen()
    clientSockt, clientAddress = serverSocket.accept()
    clientThread = ClientThread(clientAddress, clientSockt)
    clientThread.start()