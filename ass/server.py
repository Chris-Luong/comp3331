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

# serverHost = gethostbyname(gethostname())
serverHost = 'localhost'
serverPort = int(sys.argv[1])
serverAddress = (serverHost, serverPort)
numAttempts = int(sys.argv[2])

# define socket for the server side and bind address
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(serverAddress)

userInfo = {}

"""
    Read credentials file to create a dicionary for user information. Example structure:
    {"hans": [
        'password': falcon*solo,
        'status': 1,
        'blocked_until': [insert datetime object]
        'room_IDs': [1, 2, 5]
    ]}
"""
with open('credentials.txt', 'r') as file:
    for credential in file.readlines():
        details = {}
        details['password'] = credential.split()[1]
        details['status'] = INACTIVE_USER # constant integer
        details['blocked_until'] = datetime.now()
        details['room_IDs'] = [] # list of ints corresponding to room IDs
        userInfo[credential.split()[0]] = details

activeUserCnt = 0
messageCnt = 1

# key is room id and value is dict similar to userInfo which will have more deets
# the inner dict contains messageNum (like messageCnt but for each room) and list containing members
messageRooms = {}
roomCnt = 1

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
        global messageRooms, roomCnt
        clientUDPport = self.clientSocket.recv(1024).decode()
        attemptCnt = 0
        username = ''
        while self.clientAlive:
            res = authenticate(self, userInfo, attemptCnt, numAttempts, activeUserCnt)
            if len(res) == 3:
                message, userInfo, attemptCnt = res
            elif len(res) == 5:
                message, userInfo, attemptCnt, username, activeUserCnt = res
            # print(f"MESSAGE IS {message}") #FIXME: REMOVE-------------------------------------------------

            # retry authentication until user is blocked
            self.clientSocket.send(str.encode(message + '\0'))
            if message == USERNAME_ERROR_MESSAGE or message == PASSWORD_ERROR_MESSAGE:
                continue
            elif message == FIRST_BLOCKED_USER_MESSAGE or message == BLOCKED_USER_MESSAGE:
                self.clientAlive = False
                break

            while userInfo[username]['status'] == ACTIVE_USER:
                # print("[send] command request") #FIXME: REMOVE---------------------------------------------
                self.clientSocket.send(str.encode(COMMAND_INSTRUCTIONS + '\0'))
                received = self.clientSocket.recv(1024).decode()
                # print("[recv] command response") #FIXME: REMOVE--------------------------------------------
                # print(received)

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
                    arguments = received.split()
                    command = arguments[0]
                    arguments.pop(0)

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
                elif command == 'BCM': # TODO: retest since receivedList changed to arguments
                    i = 0
                    message = ""
                    while i < len(arguments):
                        message += arguments[i] + " "
                        i += 1
                    message = message[:-1] # remove the last space
                    timestamp = datetime.now()
                    timestamp = timestamp.strftime("%-d %b %Y %H:%M:%S")

                    print(f"{username} broadcasted BCM #{messageCnt} \"{message}\" at {timestamp}.")

                    loggedMessage, messageCnt = logMessage(messageCnt, timestamp, username, message)
                    loggedMessage = loggedMessage.split(';')
                    confirmationMessage = \
                    f"Broadcast message, #{loggedMessage[0]} broadcast at {loggedMessage[1]}."

                    self.clientSocket.send(str.encode(confirmationMessage + '\0'))
                    continue
                elif command == 'ATU':
                    print(f"{username} issued ATU command")
                    activeUsersMessageList = retrieveActiveUsers(username)
                    print(f"Return messages:\n{activeUsersMessageList}")
                    self.clientSocket.send(str.encode(activeUsersMessageList + '\0'))
                    continue
                elif command == 'SRB': # create SR_ID_messagelog.txt for each room (SR_ID = room id)
                    print(f"{username} issued SRB command")
                    invalidUser, errorMessage = checkValidUsernames(username, arguments, userInfo)
                    if invalidUser == '':
                        roomExists, roomID = isExistingRoom(username, arguments, messageRooms, userInfo)
                        if roomExists:
                            message = f"a separate room (ID: {roomID}) already created for these users\0"
                            print(f"Return message:\n{message}")
                            self.clientSocket.send(str.encode(message))
                        else:
                            print("make room")
                            message = createRoom(username, arguments, messageRooms, userInfo, roomCnt)
                            self.clientSocket.send(str.encode(message))
                    else:
                        print(f"Return message:\n{errorMessage}")
                        self.clientSocket.send(str.encode(errorMessage + invalidUser + '\0'))
                    continue
                elif command == 'SRM':
                    print("broadcast message to separate room")
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
def authenticate(self, userInfo: dict, attemptCnt: int, numAttempts: int, activeUserCnt: int) -> tuple:
    # print("[send] username request") #FIXME: REMOVE-------------------------------------------------------
    self.clientSocket.send(str.encode(USERNAME_REQUEST + '\0'))
    username = self.clientSocket.recv(1024).decode()
    # print("[recv] username response") #FIXME: REMOVE------------------------------------------------------
    if username not in userInfo.keys() or username == "":
        print("[send] username error") #FIXME: REMOVE-----------------------------------------------------
        return USERNAME_ERROR_MESSAGE, userInfo, attemptCnt

    # print("[send] password request") #FIXME: REMOVE-----------------------------------------------------
    self.clientSocket.send(str.encode(PASSWORD_REQUEST + '\0'))
    password = self.clientSocket.recv(1024).decode()
    # print("[recv] password response") #FIXME: REMOVE-----------------------------------------------------

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
            return FIRST_BLOCKED_USER_MESSAGE, userInfo, attemptCnt
        else:
            print("[send] password error") #FIXME: REMOVE-------------------------------------------------
            return PASSWORD_ERROR_MESSAGE, userInfo, attemptCnt
    elif userInfo[username]['status'] is BLOCKED_USER:
        print("[send] user still blocked. Closing connection") #FIXME: REMOVE-----------------------------
        return BLOCKED_USER_MESSAGE, userInfo, attemptCnt
    
    # user is active if username and password are valid, add them to active user list (userlog.txt)
    userInfo[username]['status'] = ACTIVE_USER
    activeUserCnt += 1
    
    timestamp = datetime.now().strftime("%-d %b %Y %H:%M:%S") # e.g. 31 Jul 2022 14:14:!4
    with open("userlog.txt", 'a') as file:
        file.write(f"{activeUserCnt}; {timestamp}; {username}; {self.clientAddress[0]}; {clientUDPport}\n")
    print(LOGGED_IN_USER_MESSAGE)
    return WELCOME_MESSAGE, userInfo, attemptCnt, username, activeUserCnt


"""
    Logs out user and removes them from userlog.txt
    Parameters: username and userInfo dict
    Returns integer (number of active users)
"""
def logUserOut(username: str, userInfo: dict) -> int:
    userInfo[username]['status'] = INACTIVE_USER
    with open("userlog.txt", "r") as f:
        lines = f.readlines()
    with open("userlog.txt", "w") as f:
        if len(lines) == 1:
            f.close()
            return None
        i = 1
        for line in lines:
            if line.split()[5].strip(';') == username:
                continue
            newLine = line.replace(line.split()[0], str(i) + ";")
            i +=1
            f.write(newLine)
        return i


"""
    Creates a message log according to the specified format and appends to messagelog.txt
    Parameters: message number, timestamp, username, message
    Returns the string that is appended
"""
def logMessage(messageNumber: int, timestamp, username: str, message: str) -> tuple:
    result = f"{messageNumber}; {timestamp}; {username}; {message}\n"
    with open("messagelog.txt", 'a') as file:
        file.write(result)
    messageNumber += 1
    return result, messageNumber


"""
    Retrieves all active users from userlog.txt, excluding the user that requested
    Parameters: username
    Returns string of users, or the message "no other active user"
"""
def retrieveActiveUsers(username: str) -> str:
    result = ""
    with open("userlog.txt", 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.split()[5].strip(';') == username:
                continue
            newLine = line.replace(';', '')
            lineElements = newLine.split()
            
            ATUmessage = f"{lineElements[5]}, active since {lineElements[1]} {lineElements[2]} " \
            + f"{lineElements[3]} {lineElements[4]} on {lineElements[6]}:{lineElements[7]}.\n"
            result += ATUmessage
    
    if result == "":
        return ATU_STATUS_ALONE
    result = result[:-1] # remove the last '\n'
    return result


"""
    Checks if list of users exist, are active, and are not the user that created the group
    Parameters: username of user and list of usernames to be added
    Returns tuple of the invalid username and error message or None if no issues are detected
"""
def checkValidUsernames(username: str, userList: list, userDict: dict) -> tuple:
    for user in userList:
        if user not in userDict:
            return user, SRB_NOT_EXISTENT_USER_MESSAGE
        elif username == user:
            return user, SRB_YOURSELF_USER_MESSAGE
        elif userDict[user]['status'] != ACTIVE_USER:
            return user, SRB_INACTIVE_USER_MESSAGE
    return None, None


"""
    Check if user is already in a room with the list of usernames provided
    Parameters: username, list of users, room dictionary, user dictionary
    Returns boolean: true if room exists, false if not
"""
def isExistingRoom(username: str, users: list, rooms: dict, userDict: dict) -> bool:
    roomIDs = userDict[username]['room_IDs']
    if roomIDs == []:
        return False
    # check the rooms the user is part of and see if these rooms contain the other users already
    for roomID in roomIDs:
        # room exists if its size is equal to that of the user list + the user.
        if len(rooms[roomID]) != (len(users) + 1):
            continue
        isMember = False

        for user in users:
            if user in rooms[roomID]:
                print("user in this room")
                isMember = True
            else:
                isMember = False
                break
        if isMember:
            return True, roomID
    return False


"""
    Create a new separate room
    Parameters: username, list of users, message rooms dictionary, users dictionary
    Returns tuple containing message and updated room count
"""
# key is room id and value is dict similar to userInfo which will have more deets
# the inner dict contains messageNum (like messageCnt but for each room) and list containing members
def createRoom(username: str, userList: list, messageRooms: dict, userInfo: dict, roomNum: int) -> tuple:
    message = ""
    # if not messageRooms: # there are no existing rooms
    details = {}
    details['message_num'] = 1
    details['members'] = userList.append(username)
    messageRooms[roomNum] = details
    roomNum += 1
    print('first room ever')
    userInfo[username]['room_IDs'] = roomNum

    return message, roomNum

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