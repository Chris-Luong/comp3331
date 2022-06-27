# Python3
import socket, threading, time, re, os, sys

def tcplink(sock, addr):
    print("Accept new conn from %s:%s" % addr)

    while True:
        data = sock.recv(1024) # receive request
        time.sleep(1)
        if data: # if any data recvd from the cient

            #TODO process data (i.e. if html do this, png do that)
            dataList = data.split()
            # dataList.decode("utf-8")
            print(dataList)
            page = dataList[1].decode('utf-8')

            # page = ""
            if (page != "/index.html" and
                page != "/black-dog.png" and
                page != "/white-dog.png" and
                page != "/german-shepherd.png"):
                sock.send("\HTTP/1.1 404 Not Found\n\n".encode())
                break
            page = page.replace("/", "")
            # if (dataPage = "/index.html"):
            #     page = 'index.html'
            # send response (wlll need to change depending on data)
            sock.send("\HTTP/1.1 200 OK\n\n".encode())
            # send index (content)
            with open(page, 'rb') as f:
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
