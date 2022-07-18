import os
from socket import *
from threading import Thread
import sys, select

# acquire server host and port from command line parameter
if len(sys.argv) != 3:
    print("\n===== Error usage, python3 TCPServer3.py SERVER_PORT number_of_consecutive_failed_attempts ======\n")
    exit(0)
serverHost = "127.0.0.1"
serverPort = int(sys.argv[1])
serverAddress = (serverHost, serverPort)
attemps = int(sys.argv[2])

# define socket for the server side and bind address
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(serverAddress)

# read credentials file and turn it into a dictionary
credentials_dict = {}
f = open('credentials.txt', 'r')
for pairs in f.readlines():
    credentials_dict[pairs.split()[0]] = pairs.split()[1]


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
        message = ''

        while self.clientAlive:
            # use recv() to receive message from the client
            # data = self.clientSocket.recv(1024)
            # message = data.decode()
            # print(message)
            self.process_login()

            # if the message from client is empty, the client would be off-line then set the client as offline (alive=Flase)
            # if message == '':
            #     self.clientAlive = False
            #     print("===== the user disconnected - ", clientAddress)
            #     break

            # # handle message from the client
            # if message == 'login':
            #     print("[recv] New login request")
            #     self.process_login()
            # elif message == 'download':
            #     print("[recv] Download request")
            #     message = 'download filename'
            #     print("[send] " + message)
            #     self.clientSocket.send(message.encode())
            # else:
            #     print("[recv] " + message)
            #     print("[send] Cannot understand this message")
            #     message = 'Cannot understand this message'
            # self.clientSocket.send(message.encode())

    def process_login(self):
        message = 'user credentials request'
        print('[send] ' + message)
        self.clientSocket.send(message.encode())
        username = self.clientSocket.recv(1024)
        username = username.decode()
        if username not in credentials_dict.keys():
            print(f"Invalid username :" + {username})
        message = 'password request'
        print('[send] ' + message)
        self.clientSocket.send(message.encode())
        password = self.clientSocket.recv(1024)
        password = password.decode()
        if password != credentials_dict[username]:
            print("you're done")
        else:
            print("OK")


print("\n===== Server is running =====")
print("===== Waiting for connection request from clients...=====")


while True:
    serverSocket.listen()
    clientSockt, clientAddress = serverSocket.accept()
    clientThread = ClientThread(clientAddress, clientSockt)
    clientThread.start()