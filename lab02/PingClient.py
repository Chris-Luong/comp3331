# Python3
import sys
#coding: utf-8
import socket, datetime, time

def ping(rttSum, pingNum, host = '127.0.0.1', port = 7777):
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

    # set timeout = 1s
    sock.settimeout(1)

    try:
        # recv the response from serverside
        data = sock.recv(1024)

        # calculate RTT
        t2 = datetime.datetime.now()
        rtt = (t2-t1).total_seconds() * 1000
        rttSum += rtt

        print(f"ping to {host}. rtt = {rtt} ms. rttSum = {rttSum}")
        # return rtt
    except socket.timeout():
        print(f"ping to {host}. rtt = time out. rttSum = {rttSum}")


if __name__ == "__main__":

    rttSum = 0
    for i in range(15):
        ping(rttSum, i)
    
    average = rttSum / i
    print(average)

    '''
    TODO:
        1. user for loop to send 15 packets
        2. Calc avg RTT
        3. Accept userinput "argv", so we can specify the recv IP and port number
    '''