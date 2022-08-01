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
from time import strftime

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

with open('credentials.txt', 'r') as file:
    for credential in file.readlines():
        details = {}
        details['password'] = credential.split()[1]
        details['status'] = INACTIVE_USER
        details['blocked_until'] = datetime.now()
        userInfo[credential.split()[0]] = details

activeUserCnt = 0

# session dict for userlog.txt? See if required or if userInfo is enough
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
        # print(f"{clientAddress[0]} {clientAddress[1]}") gives IP addr and port no.
        self.clientAlive = True

    def run(self):
        global attemptCnt, userInfo, numAttempts, activeUserCnt
        attemptCnt = 0
        username = ''
        while self.clientAlive:
            # Authentication
            res = authenticate(self, userInfo, attemptCnt, numAttempts, activeUserCnt)
            if len(res) == 3:
                message, userInfo, attemptCnt = res
            elif len(res) == 5:
                message, userInfo, attemptCnt, username, activeUserCnt = res
            print(f"MESSAGE IS {message}") # check if message is correct

            self.clientSocket.send(message.encode())
            if message == S_USERNAME_ERROR_MESSAGE or message == S_PASSWORD_ERROR_MESSAGE:
                continue # do smthn?
            elif message == S_FIRST_BLOCKED_USER_MESSAGE or message == S_BLOCKED_USER_MESSAGE:
                # self.clientSocket.close()
                self.clientAlive = False
                break

            while userInfo[username]['status'] == ACTIVE_USER:
                print("[send] command request")
                self.clientSocket.send(str.encode(S_COMMAND_INSTRUCTIONS))
                received = self.clientSocket.recv(1024).decode()
                print("[recv] command response")
                print(received)

                # KeyboardInterrupt
                if received == '':
                    print(f"{username} forced logout")
                    activeUserCnt = logUserOut(username, userInfo)
                    if activeUserCnt is None:
                        activeUserCnt = 0
                    else:
                        activeUserCnt -= 1
                    self.clientSocket.close()
                    self.clientAlive = False
                    break
                receivedList = received.split()
                command = receivedList[0]

                if command == 'OUT':
                    activeUserCnt = logUserOut(username, userInfo)
                    if activeUserCnt is None:
                        activeUserCnt = 0
                    else:
                        activeUserCnt -= 1
                    print(f"{username} logout")
                    print("[send] goodbye message")
                    self.clientSocket.send(str.encode(f"Bye, {username}!\0"))
                    # client close connection after this
                    self.clientAlive = False
                    break
                elif command == 'BCM':
                    message = receivedList[1]
                    print(message)
                    continue


"""
    parameters are self, userInfo dict, attempt count and number of attempts allowed
    returns tuple (constant string, userInfo dict and attempt count)
"""
def authenticate(self, userInfo, attemptCnt, numAttempts, activeUserCnt):
    print("[send] username request")
    self.clientSocket.send(str.encode(S_USERNAME_REQUEST))
    username = self.clientSocket.recv(1024).decode()
    print("[recv] username response")
    if username not in userInfo.keys() or username == "":
        print("[send] username error")
        return S_USERNAME_ERROR_MESSAGE, userInfo, attemptCnt

    if attemptCnt == 0:
        blockedDelay = datetime.now() # initialise var

    print("[send] password request")
    self.clientSocket.send(str.encode(S_PASSWORD_REQUEST))
    password = self.clientSocket.recv(1024).decode()
    print("[recv] password response")

    # unblock user after 10s
    if (userInfo[username]['status'] == BLOCKED_USER and 
        datetime.now() > userInfo[username]['blocked_until']):
        userInfo[username]['status'] = INACTIVE_USER
        attemptCnt = 0

    # check password and number of attempts, then send correct message
    if (password != userInfo[username]['password'] and
        userInfo[username]['status'] != BLOCKED_USER) or password == '':
        attemptCnt += 1
        if attemptCnt >= numAttempts:
            userInfo[username]['status'] = BLOCKED_USER
            print("[send] user blocked. Closing connection")
            blockedDelay = datetime.now() + timedelta(seconds=10)
            userInfo[username]['blocked_until'] = blockedDelay
            return S_FIRST_BLOCKED_USER_MESSAGE, userInfo, attemptCnt
        else:
            print("[send] password error")
            return S_PASSWORD_ERROR_MESSAGE, userInfo, attemptCnt
    elif userInfo[username]['status'] is BLOCKED_USER:
        print("[send] user still blocked. Closing connection")
        return S_BLOCKED_USER_MESSAGE, userInfo, attemptCnt
    
    # user is active if username and password are valid, add them to active user list
    userInfo[username]['status'] = ACTIVE_USER
    activeUserCnt += 1
    
    timestamp = datetime.now().strftime("%d %b %Y %H:%M:%S") # e.g. 31 Jul 2022 14:14:!4
    with open("userlog.txt", 'a') as file:
        file.write(f"{activeUserCnt}; {timestamp}; {username}\n")
    print(LOGGED_IN_USER_MESSAGE)
    return S_WELCOME_MESSAGE, userInfo, attemptCnt, username, activeUserCnt

def logUserOut(username, userInfo):
    userInfo[username]['status'] = INACTIVE_USER
    with open("userlog.txt", "r") as f:
        lines = f.readlines()
    with open("userlog.txt", "w") as f:
        i = 1
        for line in lines:
            if line.split()[5] != username:
                newLine = line.replace(line.split()[0], str(i) + ";")
                i +=1
                f.write(newLine)
                return i

print("\n===== Server is running =====")
print("===== Waiting for connection request from clients...=====")

try:
    while True:
        serverSocket.listen()
        clientSockt, clientAddress = serverSocket.accept()
        clientThread = ClientThread(clientAddress, clientSockt)
        clientThread.start()
finally:
    # delete userlog for clean start on next server run
    os.remove("userlog.txt")