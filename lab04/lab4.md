# Exercise 1
- go to bottom of file for link
## Question 1

Server (gaia.cs.umass.edu): 128.119.245.12, port 1161 
Client: 192.18.1.102, port 80

## Question 2

Sequence number of TCP segment containing HTTP POST command: 232129013

0000   00 06 25 da af 73 00 20 e0 8a 70 1a 08 00 45 00   ..%..s. ..p...E.
0010   02 5d 1e 21 40 00 80 06 a2 e7 c0 a8 01 66 80 77   .].!@........f.w
0020   f5 0c 04 89 00 50 0d d6 01 f5 34 a2 74 1a 50 18   .....P....4.t.P.
0030   44 70 1f bd 00 00 50 4f 53 54 20 2f 65 74 68 65   Dp....POST /ethe
0040   72 65 61 6c 2d 6c 61 62 73 2f 6c 61 62 33 2d 31   real-labs/lab3-1
0050   2d 72 65 70 6c 79 2e 68 74 6d 20 48 54 54 50 2f   -reply.htm HTTP/
0060   31 2e 31 0d 0a 48 6f 73 74 3a 20 67 61 69 61 2e   1.1..Host: gaia.
0070   63 73 2e 75 6d 61 73 73 2e 65 64 75 0d 0a 55 73   cs.umass.edu..Us
0080   65 72 2d 41 67 65 6e 74 3a 20 4d 6f 7a 69 6c 6c   er-Agent: Mozill
0090   61 2f 35 2e 30 20 28 57 69 6e 64 6f 77 73 3b 20   a/5.0 (Windows; 
00a0   55 3b 20 57 69 6e 64 6f 77 73 20 4e 54 20 35 2e   U; Windows NT 5.
00b0   31 3b 20 65 6e 2d 55 53 3b 20 72 76 3a 31 2e 30   1; en-US; rv:1.0
00c0   2e 32 29 20 47 65 63 6b 6f 2f 32 30 30 33 30 32   .2) Gecko/200302
00d0   30 38 20 4e 65 74 73 63 61 70 65 2f 37 2e 30 32   08 Netscape/7.02
00e0   0d 0a 41 63 63 65 70 74 3a 20 74 65 78 74 2f 78   ..Accept: text/x
00f0   6d 6c 2c 61 70 70 6c 69 63 61 74 69 6f 6e 2f 78   ml,application/x
0100   6d 6c 2c 61 70 70 6c 69 63 61 74 69 6f 6e 2f 78   ml,application/x
0110   68 74 6d 6c 2b 78 6d 6c 2c 74 65 78 74 2f 68 74   html+xml,text/ht
0120   6d 6c 3b 71 3d 30 2e 39 2c 74 65 78 74 2f 70 6c   ml;q=0.9,text/pl
0130   61 69 6e 3b 71 3d 30 2e 38 2c 76 69 64 65 6f 2f   ain;q=0.8,video/
0140   78 2d 6d 6e 67 2c 69 6d 61 67 65 2f 70 6e 67 2c   x-mng,image/png,
0150   69 6d 61 67 65 2f 6a 70 65 67 2c 69 6d 61 67 65   image/jpeg,image
0160   2f 67 69 66 3b 71 3d 30 2e 32 2c 74 65 78 74 2f   /gif;q=0.2,text/
0170   63 73 73 2c 2a 2f 2a 3b 71 3d 30 2e 31 0d 0a 41   css,*/*;q=0.1..A
0180   63 63 65 70 74 2d 4c 61 6e 67 75 61 67 65 3a 20   ccept-Language: 
0190   65 6e 2d 75 73 2c 20 65 6e 3b 71 3d 30 2e 35 30   en-us, en;q=0.50
01a0   0d 0a 41 63 63 65 70 74 2d 45 6e 63 6f 64 69 6e   ..Accept-Encodin
01b0   67 3a 20 67 7a 69 70 2c 20 64 65 66 6c 61 74 65   g: gzip, deflate
01c0   2c 20 63 6f 6d 70 72 65 73 73 3b 71 3d 30 2e 39   , compress;q=0.9
01d0   0d 0a 41 63 63 65 70 74 2d 43 68 61 72 73 65 74   ..Accept-Charset
01e0   3a 20 49 53 4f 2d 38 38 35 39 2d 31 2c 20 75 74   : ISO-8859-1, ut
01f0   66 2d 38 3b 71 3d 30 2e 36 36 2c 20 2a 3b 71 3d   f-8;q=0.66, *;q=
0200   30 2e 36 36 0d 0a 4b 65 65 70 2d 41 6c 69 76 65   0.66..Keep-Alive
0210   3a 20 33 30 30 0d 0a 43 6f 6e 6e 65 63 74 69 6f   : 300..Connectio
0220   6e 3a 20 6b 65 65 70 2d 61 6c 69 76 65 0d 0a 52   n: keep-alive..R
0230   65 66 65 72 65 72 3a 20 68 74 74 70 3a 2f 2f 67   eferer: http://g
0240   61 69 61 2e 63 73 2e 75 6d 61 73 73 2e 65 64 75   aia.cs.umass.edu
0250   2f 65 74 68 65 72 65 61 6c 2d 6c 61 62 73 2f 6c   /ethereal-labs/l
0260   61 62 33 2d 31 2e 68 74 6d 0d 0a                  ab3-1.htm..

## Question 3

First 6 segments in TCP connnection (POST command as the first)

|Segment number |Sequence numbers |Time (sec) |ACK receieved |RTT (sec) | Estimated RTT|
|--- | --- | --- | --- | --- | ---|
|1|232129013|0.02647700||||
|2|232129578|||||
|3|232131038|||||
|4|232132498|||||
|5|232133958|||||
|6|232135418|||||

## Question 4

|Segment number | Segment length|
|--- | ---|
|1|565|
|2|1460|
|3|1460|
|4|1460|
|5|1460|
|6|1460|
































https://github.com/wickwickthedog/comp3331