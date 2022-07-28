# Exercise 1

## Question 1

The throughput achieved by flow tcp2 is higher than tcp1 between 6 sec - 8 sec because the bandwidth from n3 to n2 is larger than that of n0-n1-n2 (10 Mbps vs 2.5 Mbps). Tcp2 has more packages in the span of 6 - 8 sec.

## Question 2

The throughput of tcp 1 is fluctuating in the time span 0.5 - 2 sec due to congestion control i.e. the congestion window is being adjusted and the slow start phase is being initiated.

## Question 3

The maximum throughput achieved by any one flow is capped at around 1.5 Mbps because incoming packets from n0 and n3 going to n2 are dropped, causing a decrease in window size which initiates the slow start phase. When tcp2 enters after tcp1, there is an increase in the package loss/delay in tcp1 so tcp1 cannot achieve a higher throughput.

# Exercise 2

## Question 1

Th data sizes that caused fragmentation are 2000 and 3500 as the default maximum segment size is 1500 bytes. The host that fragmented the original datagram is 192.168.1.103. When the data size is specfied as 2000, 2 fragments are created.

## Question 2

The reply from destintion 8.8.8.8 for 3500-byte data size also got fragmented because it is larger than the max segment size of 1500 bytes.

## Question 3

The ID, length, flag and offset values for all the fragments of the first packet sent by 192.168.1.103 with data size 3500 bytes are:
[7a7b | 1514 | 0x2000, more fragments | 0 -> 0]
[7a7b | 1514 | 0x20b9, more fragments | 1480 -> 185]
[7a7b | 582 | 0x0172 | 260 -> 370]
