
# TODO
- test for whitespace and newline in user credentials and other stuff (invalid stuff) ask tutor help
- implement accepting commands in client side
- Need to add following info into userlog.txt
    - Active user sequence number; timestamp; username; client IP address;
    client UDP server port number
    - e.g. 1; 1 Jun 2022 21:30:04; Yoda; 129.64.1.11; 6666
- active users and log off functionality
    - (need to write to a **userlog.txt** file)
- report.pdf: attribute multithreading to WebCMS sample code
- single user login
- blocking for unsuccessful attempts (based on number and time)
- multiple clients logged in
- broadcast, read and room functionality
    - (write to **messagelog.txt**, use sys and os to create file if it doesn't exist)


# Testing
    Add some newlines to the bottom of credentials.txt to see if it crashes

# Thoughts
- userInfo is list of dicts, or dict with username as key and dict of things as value

- userInfo.status options: [active, inactive, blocked] with active = logged in;

- maybe use json.dumps for making a json file with user info.

- with any future options, might have to group with 'active' in conditional as logged in

# Assumptions

- users all have different usernames

# Notes

## Authentication

- Once blocked, terminal is shutdown. If user tries again within 10s, only shutdown terminal with message after password entered.

## Timestamps

Check 3.2 (authentication) and 3rd para of 3.3 for format. Could have error message with the proper format

## SRB

- check if usename exists
- User cannot create a room with themselves
    - error message if usernames are the same, check spec

## UPD

- Client must be using UDP connection, not TCP.

- Copy while loop from server to use, but will need to do the UDP stuff on your own.

- Will need to create a sub-thread for this, similar to server main thread. This is because the client will act as a server too in the p2p network. (**HARDEST PART**)

- Will need to implement some sortof checksum function in the client (e.g. check the size of file sent with received).

- If the client cannot see the video, the thing is not considered working and you will not get marks.

## Miscellaneous