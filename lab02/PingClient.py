# Python3
# Written by Christopher Luong (z5309196) June 2022
import sys
#coding: utf-8
import socket, datetime, time

def ping(rttSum, rttArray, pingNum, host, port):
    address = (host, port)
    # inint the socket for the TCP connection
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # to calculate the RTT
    t1 = datetime.datetime.now()

    # we want totsend this messsage to serverside
    # "PING sequence number time CRLF"
    msg = f"PING test {t1}\r\n"

    # send the message to the address
    sock.sendto(msg.encode(), address)

    # set timeout = 600ms
    sock.settimeout(0.6)

    try:
        # recv the response from serverside
        data = sock.recv(1024)

        # calculate RTT
        t2 = datetime.datetime.now()
        rtt = (t2-t1).total_seconds() * 1000
        rttSum += rtt
        rttArray.append(rtt)

        print(f"PING to {host}, seq = {pingNum+3331}, rtt = {rtt} ms\r\n")
        return rttSum
    except Exception as e:
        return -1
        # Should put exception code here

if __name__ == "__main__":

    rttSum = 0
    rttArray = []
    newSum = 0
    # These need to be argv for user input
    host = '127.0.0.1'
    port = 7777

    for i in range(15):
        newSum = ping(rttSum, rttArray, i, host, port)
        if newSum == -1:
            break
        else:
            rttSum = newSum
    if i == 0 or (rttSum != newSum and i != 14):
        print(f"PING to {host}, seq = {i+3331}, rtt = time out\r\n")
    else:
        print(f"PING to {host}, seq = {i+3331}, rtt = time out\r\n")

    if i != 0:    
        rttArray.sort()
        min = rttArray[0]
        max = rttArray[-1]
        average = rttSum / i
        print(f"min_RTT = {min} ms, max_RTT = {max} ms, average_RTT = {average} ms")

    '''
    TODO:
        1. user for loop to send 15 packets
        2. Calc avg RTT
        3. Accept userinput "argv", so we can specify the recv IP and port number
    '''