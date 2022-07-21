# Exercise 1

## Question 1

The maximum size of the congestion window that the TCP flw reaches is 100. When the congestion window reaches this value, there is a triple dup ACK/timeout and the congestion window size drops to 1. The slow start threshold (ssthresh) is set to half of 100 which is 50. This is done to avoid congestion. The slow start phase will start again after this with the window size being 1.

## Question 2

From the WindowTPut graph, the average throughput is around 188 packets/sec which is confirmed in WindowMon.tr where the last data point (line 59) shows the average is 188.97610921501706 packets/second. The average throughput in bytes/second is:
[500 (packet payload) + 20 (IP header) + 20] (TCP header) * 188.97610921501706 (avg tput)
= 102047.098976 bps.

## Question 3

As the window size decreases, the amount of oscillation in TCP decreases. 50 is the value of the maximum congestion window at which TCP stops oscillating. The average throughput at this point is 227.73037542662115 packets/sec which is 122974.40273 bps. Average throughput compare to link capacity of 1Mbps (125000 bytes):
122974.40273 / 125000 * 100 = 98.38%

Q3 - increase the number before 100ms until there is no congestion (65 has none, 70 has congestion). 70 shows Tahoe because of the slow start to AIMD

## Question 4



# Exercise 3

TCP has congestion control while UDP doesn't so UDP will have more throughput.