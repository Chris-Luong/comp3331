"""
    Python 3
    Usage: python3 server.py [PORT NUMBER] [NUMBER OF CONSECUTIVE ATTEMPTS]
    coding: utf-8
    Christopher Luong (z5309196)
"""

"""
TODO:
"""

import os
from datetime import datetime, timedelta
from socket import *
from threading import Thread
import sys, select
import json
from time import sleep, strftime
from typing import final

from myconstants import *
from helper import *

# acquire server host and port from command line parameter
if len(sys.argv) != 3:
    print("\n===== Error usage, python3 server.py SERVER_PORT " +
        "number_of_consecutive_failed_attempts ======\n")
    exit(0)
elif not sys.argv[2].isalnum() or int(sys.argv[2]) > 5 or int(sys.argv[2]) < 1:
    print(INVALID_ATTEMPT_NUMBER_MESSAGE + sys.argv[2] + 
        ". The valid value of argument number is an integer between 1 and 5.")
    exit(0)

serverHost = gethostbyname(gethostname())
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
messageCnt = 1

# key is roomd id and value is dict similar to userInfo which will have more deets
# the inner dict contains messageNum (like messageCnt but for each room) and list containing members
messageRooms = {}

# TODO: implement parameters for UDP stuff (client IP addr and port no.)
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
        # print(f"{clientAddress[0]} {clientAddress[1]}") gives IP addr and port no. for UPD
        self.clientAlive = True

    def run(self):
        global attemptCnt, userInfo, numAttempts, activeUserCnt, clientUDPport, messageCnt
        clientUDPport = self.clientSocket.recv(1024).decode()
        attemptCnt = 0
        username = ''
        while self.clientAlive:
            res = authenticate(self, userInfo, attemptCnt, numAttempts, activeUserCnt)
            if len(res) == 3:
                message, userInfo, attemptCnt = res
            elif len(res) == 5:
                message, userInfo, attemptCnt, username, activeUserCnt = res
            print(f"MESSAGE IS {message}") #FIXME: REMOVE-------------------------------------------------

            # retry authentication until user is blocked
            self.clientSocket.send(message.encode())
            if message == S_USERNAME_ERROR_MESSAGE or message == S_PASSWORD_ERROR_MESSAGE:
                continue
            elif message == S_FIRST_BLOCKED_USER_MESSAGE or message == S_BLOCKED_USER_MESSAGE:
                self.clientAlive = False
                break

            while userInfo[username]['status'] == ACTIVE_USER:
                print("[send] command request") #FIXME: REMOVE---------------------------------------------
                self.clientSocket.send(str.encode(S_COMMAND_INSTRUCTIONS))
                received = self.clientSocket.recv(1024).decode()
                print("[recv] command response") #FIXME: REMOVE--------------------------------------------
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
                if len(received) == 1:
                    command = received
                else:
                    receivedList = received.split()
                    command = receivedList[0]

                if command == 'OUT':
                    activeUserCnt = logUserOut(username, userInfo)
                    if activeUserCnt is None:
                        activeUserCnt = 0
                    else:
                        activeUserCnt -= 1
                    print(f"{username} logout")
                    self.clientSocket.send(str.encode(f"Bye, {username}!\0"))
                    sleep(0.5) # pause program so client can receive msg before socket is closed
                    self.clientAlive = False
                    break
                elif command == 'BCM':
                    i = 1
                    message = ""
                    while i < len(receivedList):
                        message += receivedList[i] + " "
                        i += 1
                    message = message[:-1]
                    timestamp = datetime.now()

                    print(f"{username} broadcasted BCM #{messageCnt} \"{message}\" at {timestamp}.")

                    loggedMessage, messageCnt = logMessage(messageCnt, timestamp, username, message)
                    loggedMessage = loggedMessage.split(';')
                    confirmationMessage = \
                    f"Broadcast message, #{loggedMessage[0]} broadcast at {loggedMessage[1]}."

                    self.clientSocket.send(str.encode(confirmationMessage + "\0"))
                    continue
                elif command == 'ATU':
                    print("print active users")
                    users = retrieveActiveUsers(username)
                    continue
                elif command == 'SRB': # create SR_ID_messagelog.txt for each room (SR_ID = room id)
                    print("broadcast message to separate room")
                elif command == 'SRM':
                    print("make separate room")
                elif command == 'RDM':
                    print("read message")
                elif command == 'UPD':
                    print("do UDP thread stuff with client and all")


"""
    parameters are self, userInfo dict, attempt count and number of attempts allowed
    returns tuple (constant string, userInfo dict and attempt count) on unsuccessful attempts
    returns (constant string, userInfo dict, attempt count, username and active user count) 
    on successs.
"""
def authenticate(self, userInfo, attemptCnt, numAttempts, activeUserCnt):
    print("[send] username request") #FIXME: REMOVE-------------------------------------------------------
    self.clientSocket.send(str.encode(S_USERNAME_REQUEST))
    username = self.clientSocket.recv(1024).decode()
    print("[recv] username response") #FIXME: REMOVE------------------------------------------------------
    if username not in userInfo.keys() or username == "":
        print("[send] username error") #FIXME: REMOVE-----------------------------------------------------
        return S_USERNAME_ERROR_MESSAGE, userInfo, attemptCnt

    print("[send] password request") #FIXME: REMOVE-----------------------------------------------------
    self.clientSocket.send(str.encode(S_PASSWORD_REQUEST))
    password = self.clientSocket.recv(1024).decode()
    print("[recv] password response") #FIXME: REMOVE-----------------------------------------------------

    # unblock user after 10s
    if (userInfo[username]['status'] == BLOCKED_USER and 
        datetime.now() > userInfo[username]['blocked_until']):
        userInfo[username]['status'] = INACTIVE_USER
        attemptCnt = 0

    # check password and number of attempts, then send correct message
    if (password != userInfo[username]['password'] and
        userInfo[username]['status'] != BLOCKED_USER) or password == '':
        attemptCnt += 1
        if attemptCnt >= numAttempts: # Block user for 10s after too many attempts
            userInfo[username]['status'] = BLOCKED_USER
            print("[send] user blocked. Closing connection")
            userInfo[username]['blocked_until'] = datetime.now() + timedelta(seconds=10)
            return S_FIRST_BLOCKED_USER_MESSAGE, userInfo, attemptCnt
        else:
            print("[send] password error") #FIXME: REMOVE-------------------------------------------------
            return S_PASSWORD_ERROR_MESSAGE, userInfo, attemptCnt
    elif userInfo[username]['status'] is BLOCKED_USER:
        print("[send] user still blocked. Closing connection") #FIXME: REMOVE-----------------------------
        return S_BLOCKED_USER_MESSAGE, userInfo, attemptCnt
    
    # user is active if username and password are valid, add them to active user list (userlog.txt)
    userInfo[username]['status'] = ACTIVE_USER
    activeUserCnt += 1
    
    timestamp = datetime.now().strftime("%d %b %Y %H:%M:%S") # e.g. 31 Jul 2022 14:14:!4
    with open("userlog.txt", 'a') as file:
        file.write(f"{activeUserCnt}; {timestamp}; {username}; {self.clientAddress[0]}; {clientUDPport}\n")
    print(LOGGED_IN_USER_MESSAGE)
    return S_WELCOME_MESSAGE, userInfo, attemptCnt, username, activeUserCnt


"""
    Logs out user and removes them from userlog.txt
    Parameters: username and userInfo dict
    Returns integer (number of active users)
"""
def logUserOut(username, userInfo):
    userInfo[username]['status'] = INACTIVE_USER
    with open("userlog.txt", "r") as f:
        lines = f.readlines()
    with open("userlog.txt", "w") as f:
        if len(lines) == 1:
            f.close()
            return None
        i = 1
        for line in lines:
            if line.split()[5].strip(';') != username:
                newLine = line.replace(line.split()[0], str(i) + ";")
                i +=1
                f.write(newLine)
        return i


"""
    Creates a message log according to the specified format and appends to messagelog.txt
    Parameters: message number, timestamp, username, message
    Returns the string that is appended
"""
def logMessage(messageNumber, timestamp, username, message):
    timestamp = timestamp.strftime("%d %b %Y %H:%M:%S")
    result = f"{messageNumber}; {timestamp}; {username}; {message}\n"
    with open("messagelog.txt", 'a') as file:
        file.write(result)
    messageNumber += 1
    return result, messageNumber


"""
    Retrieves all active users from userlog.txt excluding the user that requested
    Parameters: username
    Returns string of users
"""
def retrieveActiveUsers(username):
    result = ""
    with open("messagelog.txt", 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.split()[5].strip(';') != username:
                result += line
    return result


print(f"\n===== Server is running on {serverAddress[0]}:{serverAddress[1]} =====")
print("===== Waiting for connection request from clients...=====")

try:
    while True:
        serverSocket.listen()
        clientSockt, clientAddress = serverSocket.accept()
        clientThread = ClientThread(clientAddress, clientSockt)
        clientThread.start()
finally:
    # delete created files for clean start on next server run
    if os.path.exists("userlog.txt"):
        os.remove("userlog.txt")
    if os.path.exists("messagelog.txt"):
        os.remove("messagelog.txt")
    # for id in SR_ID list or whatever:
    # remove f"{id}_messagelog.txt"
    serverSocket.close()