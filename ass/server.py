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
    {"hans": {
        'password': falcon*solo,
        'status': 1,
        'blocked_until': [insert datetime object]
        'room_IDs': [1, 2, 5]
        }
    }
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

"""
    Similar to userInfo dictionary with the room ID as the key, example:
    {"1": {
        "message_num": 2
        "members": [uno, dos]
        }
    }
"""
messageRooms = {}
roomCnt = 1

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
        global attemptCnt, userInfo, numAttempts, activeUserCnt, clientUDPport, messageCnt
        global messageRooms, roomCnt, SRmessageNumber
        clientUDPport = self.clientSocket.recv(1024).decode()
        attemptCnt = 0
        username = ''
        while self.clientAlive:
            res = authenticate(self, userInfo, attemptCnt, numAttempts, activeUserCnt)
            if len(res) == 3:
                message, userInfo, attemptCnt = res
            elif len(res) == 5:
                message, userInfo, attemptCnt, username, activeUserCnt = res

            # retry authentication until user is blocked
            self.clientSocket.send(str.encode(message + '\0'))
            if message == USERNAME_ERROR_MESSAGE or message == PASSWORD_ERROR_MESSAGE:
                continue
            elif message == FIRST_BLOCKED_USER_MESSAGE or message == BLOCKED_USER_MESSAGE:
                self.clientAlive = False
                break

            while userInfo[username]['status'] == ACTIVE_USER:
                self.clientSocket.send(str.encode(COMMAND_INSTRUCTIONS + '\0'))
                received = self.clientSocket.recv(1024).decode()

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
                    if invalidUser == None:
                        roomExists, roomID = isExistingRoom(username, arguments, messageRooms, userInfo)
                        if roomExists:
                            message = f"a separate room (ID: {roomID}) already created for these users\0"
                            print(f"Return message:\n{message}")
                            self.clientSocket.send(str.encode(message))
                        else:
                            message, roomCnt, messageRooms, userInfo = \
                                createRoom(username, arguments, messageRooms, userInfo, roomCnt)
                            print(message)
                            self.clientSocket.send(str.encode(message))
                    else:
                        print(f"Return message:\n{errorMessage}{invalidUser}")
                        self.clientSocket.send(str.encode(errorMessage + invalidUser + '\0'))
                    continue
                elif command == 'SRM':
                    i = 0
                    roomID = int(arguments[0])
                    errorMessage = checkValidRoom(roomID, username, messageRooms)
                    if errorMessage is not None:
                        print(f"Return message:\n{errorMessage}")
                        self.clientSocket.send(str.encode(errorMessage + '\0'))
                        continue
                    arguments.pop(0)
                    message = ""
                    while i < len(arguments):
                        message += arguments[i] + " "
                        i += 1
                    message = message[:-1] # remove the last space
                    timestamp = datetime.now()
                    timestamp = timestamp.strftime("%-d %b %Y %H:%M:%S")

                    SRmessageNumber = messageRooms[roomID]['message_num']
                    loggedMessage, SRmessageNumber = \
                        logSRMessage(roomID, SRmessageNumber, timestamp, username, message)
                    messageRooms[roomID]['message_num'] = SRmessageNumber
                    
                    print(f"{username} issued a message in separate room {roomID}: {loggedMessage}")
                    
                    loggedMessage = loggedMessage.split(';')
                    confirmationMessage = f"Issued separate room message to room ID: {roomID}, "\
                        + f"message #{loggedMessage[0]} issued at {loggedMessage[1]}."

                    self.clientSocket.send(str.encode(confirmationMessage + '\0'))
                    continue
                elif command == 'RDM':
                    print(f"RDM command issued by {username}")
                    messageType = arguments[0]
                    timestamp = f"{arguments[1]} {arguments[2]} {arguments[3]} {arguments[4]}"

                    if messageType == 'b':
                        print()
                        messageList = retrieveMessages(timestamp)
                    elif messageType == 's':
                        messageList = retrieveSRMessages(timestamp, userInfo, username)
                    else:
                        print(messageType)
                        print("wrong message type u nong")
                        continue

                    if messageList == '':
                        print(RDM_NO_MSG)
                        self.clientSocket.send(str.encode(RDM_NO_MSG + '\0'))
                        continue
                    print(f"Return messages:\n{messageList}")
                    self.clientSocket.send(str.encode(messageList + '\0'))
                    continue
                elif command == 'UPD':
                    print("nope")
                    self.clientSocket.send(str.encode("nope\0"))
                    continue


"""
    parameters are self, userInfo dict, attempt count and number of attempts allowed
    returns tuple (constant string, userInfo dict and attempt count) on unsuccessful attempts
    returns (constant string, userInfo dict, attempt count, username and active user count) 
    on successs.
"""
def authenticate(self, userInfo: dict, attemptCnt: int, numAttempts: int, activeUserCnt: int) -> tuple:
    
    self.clientSocket.send(str.encode(USERNAME_REQUEST + '\0'))
    username = self.clientSocket.recv(1024).decode()
    if username not in userInfo.keys() or username == "":
        return USERNAME_ERROR_MESSAGE, userInfo, attemptCnt
    self.clientSocket.send(str.encode(PASSWORD_REQUEST + '\0'))
    password = self.clientSocket.recv(1024).decode()

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
            print(f"Password error, number of attempts is: {attemptCnt}")
            return PASSWORD_ERROR_MESSAGE, userInfo, attemptCnt
    elif userInfo[username]['status'] is BLOCKED_USER:
        print("[send] user still blocked. Closing connection")
        return BLOCKED_USER_MESSAGE, userInfo, attemptCnt
    
    # user is active if username and password match, add them to active user list (userlog.txt)
    userInfo[username]['status'] = ACTIVE_USER
    activeUserCnt += 1
    
    timestamp = datetime.now().strftime("%-d %b %Y %H:%M:%S") # e.g. 31 Jul 2022 14:14:14
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
    Returns tuple containing string and message number
"""
def logMessage(messageNumber: int, timestamp, username: str, message: str) -> tuple:
    result = f"{messageNumber}; {timestamp}; {username}; {message}\n"

    with open("messagelog.txt", 'a') as file:
        file.write(result)
    messageNumber += 1
    return result, messageNumber


"""
    Creates a message log according to the specified format and appends to SR_ID_messagelog.txt
    Parameters: message number, timestamp, username, message
    Returns tuple
"""
def logSRMessage(roomID: int, messageNumber: int, timestamp, username: str, message: str) -> tuple:
    result = f"{messageNumber}; {timestamp}; {username}; {message}\n"

    with open(f"SR_{roomID}_messagelog.txt", 'a') as file:
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
def isExistingRoom(username: str, users: list, rooms: dict, userDict: dict) -> tuple:
    users.append(username)
    roomIDs = userDict[username]['room_IDs']
    if roomIDs == []:
        return False, None
    # check the rooms the user is part of and see if these rooms contain the other users already
    for roomID in roomIDs:
        # room exists if its size is equal to that of the user list + the user.
        if len(rooms[roomID]['members']) != (len(users)):
            continue
        isMember = False
        for user in users:
            if user in rooms[roomID]['members']:
                isMember = True
            else:
                isMember = False
                break
        if isMember:
            return True, roomID
    return False, None


"""
    Create a new separate room
    Parameters: username, list of users, message rooms dictionary, users dictionary
    Returns tuple containing message and updated room count
"""
def createRoom(username: str, userList: list, messageRooms: dict, userInfo: dict, roomNum: int) -> tuple:
    message = ""
    details = {}

    details['message_num'] = 1
    details['members'] = userList
    messageRooms[roomNum] = details
    # update userInfo dict with room IDs
    userInfo[username]['room_IDs'].append(roomNum)
    for user in userList:
        print(user)
        if user == username:
            continue
        userInfo[user]['room_IDs'].append(roomNum)

    users = ', '.join(str(user) for user in userList)
    message = f"Separate chat room has been created, room ID: {roomNum}, "\
        + f"users in this room: {users}\0"

    with open(f"SR_{roomNum}_messagelog.txt", 'w') as file:
        file.write("")

    roomNum += 1
    return message, roomNum, messageRooms, userInfo


"""
    Checks if room ID provided exists and if user is part of the room
    Parameters: room ID, username, message rooms dictionary
    Returns string as message
"""
def checkValidRoom(roomID: int, username: str, messageRooms: dict) -> str:
    if roomID not in messageRooms:
        return SRM_NON_EXISTENT_ROOM
    if username not in messageRooms[roomID]['members']:
        return SRM_INVALID_ROOM
    return None


"""
    Retrieves messages from broadcast/separate room service
    Parameters: string for timestamp
    Returns list of messages
"""
def retrieveMessages(timestamp: str) -> str:
    timestamp = formatTime(timestamp)
    fromTime = datetime.strptime(timestamp, "%d %b %Y %H:%M:%S")
    result = ''

    try:
        with open("messagelog.txt", 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.split(';')
                line[1] = line[1][1:]
                line[1] = formatTime(line[1])
                time = datetime.strptime(line[1], "%d %b %Y %H:%M:%S")
                if time < fromTime:
                    continue
                messageNum = line[0]
                user = line[2]
                message = line[3].strip('\n')
                timeSent = line[1] + '\n'

                line = f"#{messageNum};{user}:{message} at {timeSent}"
                result += line
    except:
        return RDM_NO_MSG
    return result

"""
    Retrieves messages from broadcast/separate room service
    Parameters: string for timestamp, user info dictionary, username
    Returns list of messages
"""
def retrieveSRMessages(timestamp: str, userInfo: dict, username: str) -> str:
    timestamp = formatTime(timestamp)
    fromTime = datetime.strptime(timestamp, "%d %b %Y %H:%M:%S")
    result = ''
    roomIDs = userInfo[username]['room_IDs']

    currentRoom = -1
    for room in roomIDs:
        if currentRoom != room:
            result += f"room-{room}:\n"
            currentRoom = room
        with open(f"SR_{room}_messagelog.txt", 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.split(';')
                line[1] = line[1][1:]
                line[1] = formatTime(line[1])
                time = datetime.strptime(line[1], "%d %b %Y %H:%M:%S")
                if time < fromTime:
                    continue
                messageNum = line[0]
                user = line[2]
                message = line[3].strip('\n')
                timeSent = line[1] + '\n'

                line = f"#{messageNum};{user}:{message} at {timeSent}"
                result += line
    return result


# format 0 to date in timestamp
def formatTime(timestamp: str) -> str:
    timeString = timestamp.split()

    date = int(timeString[0])

    if date < 10:
        newDate = '0' + str(date)
    timeString = timeString[1:]

    timeString.insert(0, newDate)
    newTime = ' '.join(timeString)
    return newTime





print(f"\n===== Server is running =====")# on {serverAddress[0]}:{serverAddress[1]}
print("===== Waiting for connection request from clients...=====")

try:
    while True:
        serverSocket.listen()
        clientSockt, clientAddress = serverSocket.accept()
        clientThread = ClientThread(clientAddress, clientSockt)
        clientThread.start()
finally:
    # delete created files for clean start on next server run
    files = os.listdir()
    for file in files:
        if file == "credentials.txt":
            continue
        elif file.endswith(".txt"):
            os.remove(file)

    serverSocket.close()