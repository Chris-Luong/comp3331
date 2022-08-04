"""
    Python 3
    Usage: python3 client.py [SERVER IP] [SERVER PORT]
    coding: utf-8
    Christopher Luong (z5309196)
"""

"""
TODO:
    receive IP addr and port number as parameters: wherever needed
"""
import os
from socket import *
import sys
import difflib

from myconstants import *
from helper import *

# Server would be running on the same host as Client
if len(sys.argv) != 4:
    print("\n===== Error usage, python3 client.py SERVER_IP SERVER_PORT CLIENT_UDP_PORT ======\n")
    exit(0)


serverHost = sys.argv[1]
serverPort = int(sys.argv[2])
serverAddress = (serverHost, serverPort)

ipAddress = gethostbyname(gethostname())
UDPport = int(sys.argv[3])

# define a socket for the client side, it would be used to communicate with the server
clientSocket = socket(AF_INET, SOCK_STREAM)

# build connection with the server and send message to it
clientSocket.connect(serverAddress)
# .recv() call will not prevent other functions from running if it receives nothing
# this allows server-client communication to be stream-based
clientSocket.setblocking(False)

isActive = False
justTurnedActive = False
justConnected = True
res = INACTIVE_USER
COMMANDS = ['BCM', 'ATU', 'SRB', 'SRM', 'RDM', 'OUT', 'UPD']
username = ''
msgQueue = []


"""
    Function for logging the user in
    Parameter is the string message received from server
    Return type is constant integer
"""
def loginUser(recvMsg: str) -> int:
    while recvMsg == 'Username: ':
        username = input(recvMsg)
        if username == '':
            continue
        clientSocket.send(str.encode(username))
        return INACTIVE_USER
    if recvMsg == 'Password: ':
        password = input(recvMsg)
        clientSocket.send(str.encode(password))
        return INACTIVE_USER
    elif recvMsg == USERNAME_ERROR_MESSAGE or recvMsg == PASSWORD_ERROR_MESSAGE:
        print(recvMsg)
        return INACTIVE_USER
    elif recvMsg == FIRST_BLOCKED_USER_MESSAGE or recvMsg == BLOCKED_USER_MESSAGE:
        print(recvMsg)
        return BLOCKED_USER
    elif recvMsg == WELCOME_MESSAGE:
        print(recvMsg)
        return ACTIVE_USER
    else:
        # received doesn't match expected formats for login process
        print(f"\'{recvMsg}\' => \'{USERNAME_ERROR_MESSAGE}\'")
        for i,s in enumerate(difflib.ndiff(recvMsg, USERNAME_ERROR_MESSAGE)):
            if s[0]==' ': continue
            elif s[0]=='-':
                print(u'Delete "{}" from position {}'.format(s[-1],i))
            elif s[0]=='+':
                print(u'Add "{}" to position {}'.format(s[-1],i))
        exit(1)

"""
    Assumes format of userlog.txt is the one specified in the specifcation i.e.
    Ativer user sequence number; timestamp; username
    e.g. 1; 31 Jul 2022 17:52:15; hans
    Returns string (username)
"""
def getUsername() -> str:
    with open("userlog.txt", "rb") as file:
        try: # go to last line
            file.seek(-2, os.SEEK_END)
            while file.read(1) != b'\n':
                file.seek(-2, os.SEEK_CUR)
        except OSError:
            file.seek(0)
        last_line = file.readline().decode()
        # go to 6th string for username
        return last_line.split()[5].strip(';')

"""
    See if response is expected from server and return True/False
    Parameter: message
    Returns boolean
"""
def processResponse(message: str) -> bool:
    if message.find("Broadcast message,") != -1 or message.find("active since") != -1\
        or message.find(ATU_STATUS_ALONE) != -1 or message.find(SRB_INACTIVE_USER_MESSAGE) != -1 or\
        message.find(SRB_NOT_EXISTENT_USER_MESSAGE) != -1 or message.find(SRB_YOURSELF_USER_MESSAGE) != -1\
        or message.find("Separate chat room has been created") != -1 or message.find("already created") != -1\
        or message.find(SRM_INVALID_ROOM) != -1 or message.find(SRM_NON_EXISTENT_ROOM) != -1 \
        or message.find("Issued separate room message") != -1 or message.find("Messages in") != -1\
        or message.find(RDM_NO_MSG) != -1 or message.find("#") != -1 or message.find("room-") != -1:
        print(message)
        return True
    return False

# TODO: implement parameters for UDP stuff (client IP addr and port no.)
while True:
    """
        Only one receiver as TCP is a stream-based (not message-based) protocol.
        Some messages from server may be segmented/bundled across a few recv() calls so
        having one receiver causes less issues than multiple receivers treating
        send() calls as 1 message for 1 recv() call.
    """
    if justConnected:
        clientSocket.send(str(UDPport).encode())        
        justConnected = False
    # Listen to server socket and put messages into a queue (buffer)
    received = recv_msg(clientSocket)
    if received is None and len(msgQueue) == 0:
        continue
    if received is not None:
        for r in received:
            if r != '':
                msgQueue.append(r)
    try:
        recvMsg = msgQueue[0]
    except Exception as e:
        print(e)
        print("exiting due to exception")
        exit(1)

    if not isActive:
        # print("isActive is ", isActive)
        res = loginUser(recvMsg)
        if res == INACTIVE_USER:
            msgQueue.pop(0) # remove most recent message from queue
            continue
        elif res == BLOCKED_USER:
            clientSocket.close()
            break
        elif res == ACTIVE_USER:
            isActive = True
            justTurnedActive = True
            msgQueue.pop(0)
            continue
    if justTurnedActive:
        username = getUsername()
        justTurnedActive = False

    # Check for and print responses from server after input for commands
    # print("recvMsg is ", recvMsg)
    if processResponse(recvMsg):
        msgQueue.pop(0)
        continue

    while recvMsg == COMMAND_INSTRUCTIONS:
        userInput = input(recvMsg)
        inputList = userInput.split()
        command = inputList[0]

        if command not in COMMANDS:
            print("Error. Invalid command!")
            continue
        elif command == 'BCM':
            if len(inputList) < 2:
                print("Usage: BCM [message]")
                continue
        elif command == 'SRB':
            if len(inputList) < 2:
                print("Usage: SRB [username1] [username2] ... A minimum of 1 username is required")
                continue
        elif command == 'SRM':
            if len(inputList) < 3:
                print("Usage: SRM [roomID] [message]")
                continue
        elif command == 'RDM':
            if len(inputList) < 3:
                print("Usage: RDM [messageType] [timestamp]")
                continue
        elif command == 'ATU' or command == 'OUT':
            # don't care if user adds arguments after these commands, just issue the command itself
            clientSocket.send(str.encode(command))
            break

        clientSocket.send(str.encode(userInput))
        
        # retrieve message from server before receiving next command
        break
    if recvMsg == (f"Bye, {username}!"): # OUT
        print(recvMsg)
        clientSocket.close()
        exit(0)
    # print("before final queue pop, recvMsg is ", recvMsg)
    msgQueue.pop(0)

# close the socket
# print("closing connection")
# clientSocket.close()
# print(f"USERNAME IS {username}")
# print(f"COMMMAND IS {recvMsg}")
