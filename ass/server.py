"""
    Python 3
    Usage: python3 server.py [PORT NUMBER] [NUMBER OF CONSECUTIVE ATTEMPTS]
    coding: utf-8
    Christopher Luong (z5309196)
"""

import os
from datetime import datetime, timedelta
from socket import *
from threading import Thread
import sys, select
import json

from myconstants import *

# acquire server host and port from command line parameter
if len(sys.argv) != 3:
    print("\n===== Error usage, python3 server.py SERVER_PORT number_of_consecutive_failed_attempts ======\n")
    exit(0)
elif not sys.argv[2].isalnum() or int(sys.argv[2]) > 5 or int(sys.argv[2]) < 1: # error message from spec
    print(INVALID_ATTEMPT_NUMBER_MESSAGE + sys.argv[2] + ". The valid value of argument number is an integer between 1 and 5.")
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
for credential in f.readlines():
    details = {}
    details['password'] = credential.split()[1]
    details['status'] = INACTIVE_USER
    details['blocked_until'] = datetime.now()
    userInfo[credential.split()[0]] = details
    # userInfo[credential.split()[0]] = credential.split()[1]

# attempts dictionary, or put this as the status in userInfo
failed_attempt_IP = {} # or have a blockdUser dict

# session dict for userlog.txt? See if required or if userInfo is enough
session_dict = {}

"""if active user will need to send message of welcome to TOOM"""

"""
    parameters are self, userInfo dict, attempt count and number of attempts allowed
    returns tuple (constant string, userInfo dict and attempt count)
"""
def authenticate(self, userInfo, attemptCnt, numAttempts):
    print(f"[send] username request")
    self.clientSocket.send(str.encode('Username: '))
    # send_msg(self.clientSocket, 'Username: ')
    username = self.clientSocket.recv(1024).decode()
    print("[recv] username response")
    if username not in userInfo.keys() or username == "":
        print("[send] username error")
        return USERNAME_ERROR_MESSAGE, userInfo, attemptCnt

    if attemptCnt == 0:
        blockedDelay = datetime.now() # initialise var

    print("[send] password request")
    self.clientSocket.send(str.encode('Password: '))
    password = self.clientSocket.recv(1024).decode()
    print("[recv] password response")

    # unblock user after 10s
    if (userInfo[username]['status'] == BLOCKED_USER and 
        datetime.now() > userInfo[username]['blocked_until']):
        userInfo[username]['status'] = INACTIVE_USER
        attemptCnt = 0

    # check password and number of attempts, then send correct message
    if (password != userInfo[username]['password'] and
        userInfo[username]['status'] != BLOCKED_USER) or password == "":
        attemptCnt += 1
        if attemptCnt >= numAttempts:
            userInfo[username]['status'] = BLOCKED_USER
            print("[send] user blocked. Closing connection")
            blockedDelay = datetime.now() + timedelta(seconds=10)
            userInfo[username]['blocked_until'] = blockedDelay
            return FIRST_BLOCKED_USER_MESSAGE, userInfo, attemptCnt
        else:
            print("[send] password error")
            return PASSWORD_ERROR_MESSAGE, userInfo, attemptCnt
    elif userInfo[username]['status'] is BLOCKED_USER:
        print("[send] user still blocked. Closing connection")
        return BLOCKED_USER_MESSAGE, userInfo, attemptCnt
    
    userInfo[username]['status'] = ACTIVE_USER
    print(LOGGED_IN_USER_MESSAGE)
    return WELCOME_MESSAGE, userInfo, attemptCnt, username

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
        # print(f"{clientAddress[0]} {clientAddress[1]}") gives IP addr and port no.
        self.clientAlive = True

    def run(self):
        global attemptCnt
        attemptCnt = 0
        username = ''
        while self.clientAlive:
            global userInfo, numAttempts
            # Authentication
            res = authenticate(self, userInfo, attemptCnt, numAttempts)
            if len(res) == 3:
                message, userInfo, attemptCnt = res
            elif len(res) == 4:
                message, userInfo, attemptCnt, username = res
            print(f"MESSAGE IS {message}") # check if message is correct
            self.clientSocket.send(message.encode())
            if message == USERNAME_ERROR_MESSAGE or message == PASSWORD_ERROR_MESSAGE:
                continue # do smthn?
            elif message == FIRST_BLOCKED_USER_MESSAGE or message == BLOCKED_USER_MESSAGE:
                # self.clientSocket.close()
                self.clientAlive = False
                break
            else:
                print(f"[send] username: {username}")
                self.clientSocket.send(str.encode(username))

            while userInfo[username]['status'] == ACTIVE_USER:
                print("[send] comamnd request")
                self.clientSocket.send(str.encode(COMMAND_INSTRUCTIONS))
                command = self.clientSocket.recv(1024).decode()
                print("[recv] command response")

                if command == 'OUT':
                    userInfo[username]['status'] = INACTIVE_USER
                    # ------ update userlog.txt (remove line containing user, move subsequent lines up)
                    # ------ active user sequence numbers updated accordingly
                    print(f"{username} logout")
                    print("[send] goodbye message")
                    self.clientSocket.send(str.encode(f"Bye, {username}!"))
                    # client close connection after this
                    self.clientAlive = False
                    break

print("\n===== Server is running =====")
print("===== Waiting for connection request from clients...=====")


while True:
    serverSocket.listen()
    clientSockt, clientAddress = serverSocket.accept()
    clientThread = ClientThread(clientAddress, clientSockt)
    clientThread.start()