# Python3
import socket, threading, time, re, os, sys

def tcplink(sock, addr):
    print("Accept new conn from %s:%s" % addr)

    while True:
        data = sock.recv(1024) # receive request
        time.sleep(1)
        if data: # if any data recvd from the cient

            #TODO process data (i.e. if html do this, png do that)
            print(data.split())
            dataList = data.split()
            print(dataList[1]) # can only concatenate str (not "bytes") to str
            # send response (wlll need to change depending on data)
            sock.send("\HTTP/1.1 200 OK\n\n".encode())
            # send index (content)
            with open('index.html', 'rb') as f:
                content = f.read()
                sock.sendall(content)
                f.close()
            break
    sock.close() # close conn
    print("Conn from %s:%s closed." % addr)


if __name__ == '__main__':
    if (len(sys.argv) < 2):
        print("USAGE: python3 WebServer.py [PORT]")
        exit()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # init socket
    s.bind(('127.0.0.1', int(sys.argv[1]))) # IP address and Port number
    s.listen(5) # at most 5 clients

    print("wait for conn...")
    while True:
        sock, addr = s.accept()
        t = threading.Thread(target=tcplink, args=(sock, addr))
        t.start()

# TODO: look above AND accept argv