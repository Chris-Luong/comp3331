
# TODO
    Add some newlines to the bottom of credentials.txt to see if it crashes
    report.pdf: attribute multithreading to WebCMS sample code
    single user login
    blocking for unsuccessful attempts (based on number and time)
    multiple clients logged in
    broadcast, read and room functionality
        (write to messagelog.txt, use sys and os to create file if it doesn't exist)
    active users and log off functionality
        (need to write to a userlog.txt file)

# Thoughts
- userInfo is list of dicts, or dict with username as key and dict of things as value

- userInfo.status options: [active, inactive, blocked] with active = logged in;

- with any future options, might have to group with 'active' in conditional as logged in

# Notes

## Authentication

- Once blocked, terminal is shutdown. If user tries again within 10s, only shutdown terminal with message after password entered.

## Timestamps

Check the top of spec for format. Could have error message with the proper format

## SRB

- check if usename exists
- User cannot create a room with themselves
    - error message if usernames are the same, check spec

## OUT

Could use a try and except for the OUT to test the case where the user exits terminal without logging out first. Will server just crash normally? 

## UPD

- Client must be using UDP connection, not TCP.

- Copy while loop from server to use, but will need to do the UDP stuff on your own.

- Will need to create a sub-thread for this, similar to server main thread. This is because the client will act as a server too in the p2p network. (**HARDEST PART**)

- Will need to implement some sortof checksum function in the client (e.g. check the size of file sent with received).

- If the client cannot see the video, the thing is not considered working and you will not get marks.

## Miscellaneous