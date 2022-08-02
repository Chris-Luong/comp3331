import errno
import os, sys

"""
    Implements message receiving for non-blocking TCP connection
    Parameter is the socket
    Return type is string
"""
def recv_msg(sock):
    try:
        msgList = sock.recv(1024).decode().split('\0')
        return msgList
    except IOError as e:
        # EAGAIN and EWOULDBLOCK are errors for no incoming data
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print(e)
            exit(1)
