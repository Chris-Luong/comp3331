# Assignment

- For login, could have a JSON format for storing actions and credentials e.g. dictionary with {ACTION: DATA} where data could be a list/dictionary with username and password. You can also extend this JSON format when you need more functionality, e.g. adding another field to start having response objects like login success, etc.
- Make sure you run through examples in assignment spec and see if you get the same output.
- With room chats: sender sends the message to server but server does not send it yet. Only sends it when receiver in message room requests for message through some command.
- UPD: need to ask server for receiver's IP address and port number (so every client needs to tell the server its address when it joins peer network to save time), then send file to this address. Third step is report if the whole file has been received e.g. using checksum, length of video or something else.
    - Needs multi threading so that it can receive at the same time

# TCP and UDP

- TCP is a protocol for the carrier (transport) of the message
- So is UDP, but TCP is MORE RELIABLE than UDP. UDP is good for low latency, faster and less resources

# DNS

- DNS use UDP, not TCP

# Miscellaneous

- in the dig command, if the flags has aa, it means authoritative answer which means it is definitely correct.
- 192.168.xxx.x and 10.0.0.x refer to local router
- ack no. is seq no. + data
- SYN is 1 so if you have seq no. of 0, then the ack in [SYN, ACK] for the 3 way handshake is 1.