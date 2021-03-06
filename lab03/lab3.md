# Exercise 3

## Q1

- IP address: 13.185.0.1

- It is a recursive query

- Command: dig www.eecs.berkeley.edu A

- Output:

; <<>> DiG 9.16.27-Debian <<>> www.eecs.berkeley.edu A
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 29444
;; flags: qr rd ra; QUERY: 1, ANSWER: 3, AUTHORITY: 4, ADDITIONAL: 6

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;www.eecs.berkeley.edu.		IN	A

;; ANSWER SECTION:
www.eecs.berkeley.edu.	72431	IN	CNAME	live-eecs.pantheonsite.io.
live-eecs.pantheonsite.io. 600	IN	CNAME	fe1.edge.pantheon.io.
fe1.edge.pantheon.io.	300	IN	A	23.185.0.1

;; AUTHORITY SECTION:
edge.pantheon.io.	127	IN	NS	ns-644.awsdns-16.net.
edge.pantheon.io.	127	IN	NS	ns-2013.awsdns-59.co.uk.
edge.pantheon.io.	127	IN	NS	ns-1213.awsdns-23.org.
edge.pantheon.io.	127	IN	NS	ns-233.awsdns-29.com.

;; ADDITIONAL SECTION:
ns-233.awsdns-29.com.	144643	IN	A	205.251.192.233
ns-644.awsdns-16.net.	82154	IN	A	205.251.194.132
ns-1213.awsdns-23.org.	78985	IN	A	205.251.196.189
ns-1213.awsdns-23.org.	67006	IN	AAAA	2600:9000:5304:bd00::1
ns-2013.awsdns-59.co.uk. 77471	IN	A	205.251.199.221

;; Query time: 20 msec
;; SERVER: 129.94.208.3#53(129.94.208.3)
;; WHEN: Thu Jun 23 16:04:22 AEST 2022
;; MSG SIZE  rcvd: 369

## Q2

The canonical name (CNAME) is fel.edge.pantheon.io

- Having an alias for the server means multiple hostnames will point to the same subdomain, where each hostname could serve a different purpose.

## Q3

The details in the Authority section tells us that there are multiple aws dns name servers that have the authority to respond to the query.

The Additional section provides resource records (RRs) which relate to the query but are not strictly answers for the query, like information about the IP addresses of the authoritative DNS servers shown in the Authority section.

## Q4

nameserver 129.94.242.2

cat /etc/resolv.conf

domain orchestra.cse.unsw.EDU.AU.
nameserver 129.94.242.2
nameserver 129.94.242.45
nameserver 129.94.242.33
options rotate
search orchestra.cse.unsw.EDU.AU. cse.unsw.EDU.AU. unsw.EDU.AU.


## Q5

DNS nameservers are:

- 169.229.60.61
- 169.229.60.153
- 128.32.136.3
- 128.32.136.14
- 192.107.102.142

dig eecs.berkeley.edu A

; <<>> DiG 9.9.5-9+deb8u19-Debian <<>> eecs.berkeley.edu A
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 34576
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 5, ADDITIONAL: 10

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;eecs.berkeley.edu.		IN	A

;; ANSWER SECTION:
eecs.berkeley.edu.	72919	IN	A	23.185.0.1

;; AUTHORITY SECTION:
eecs.berkeley.edu.	47630	IN	NS	adns3.berkeley.edu.
eecs.berkeley.edu.	47630	IN	NS	adns1.berkeley.edu.
eecs.berkeley.edu.	47630	IN	NS	adns2.berkeley.edu.
eecs.berkeley.edu.	47630	IN	NS	ns.CS.berkeley.edu.
eecs.berkeley.edu.	47630	IN	NS	ns.eecs.berkeley.edu.

;; ADDITIONAL SECTION:
ns.CS.berkeley.edu.	75466	IN	A	169.229.60.61
ns.eecs.berkeley.edu.	52520	IN	A	169.229.60.153
ns.eecs.berkeley.edu.	32340	IN	AAAA	2607:f140:8:2160::30
adns1.berkeley.edu.	405	IN	A	128.32.136.3
adns1.berkeley.edu.	405	IN	AAAA	2607:f140:ffff:fffe::3
adns2.berkeley.edu.	405	IN	A	128.32.136.14
adns2.berkeley.edu.	405	IN	AAAA	2607:f140:ffff:fffe::e
adns3.berkeley.edu.	405	IN	A	192.107.102.142
adns3.berkeley.edu.	405	IN	AAAA	2607:f140:a000:d::abc

;; Query time: 0 msec
;; SERVER: 129.94.242.2#53(129.94.242.2)
;; WHEN: Mon Jun 27 22:44:32 AEST 2022
;; MSG SIZE  rcvd: 351


## Q6

DNS name: webserver.seecs.nust.edu.pk

nslookup 111.68.101.54

Server:		129.94.242.2
Address:	129.94.242.2#53

Non-authoritative answer:
54.101.68.111.in-addr.arpa	name = webserver.seecs.nust.edu.pk.

Authoritative answers can be found from:
101.68.111.in-addr.arpa	nameserver = ns1.hec.gov.pk.
101.68.111.in-addr.arpa	nameserver = ns2.hec.gov.pk.
ns1.hec.gov.pk	internet address = 103.4.93.5
ns2.hec.gov.pk	internet address = 103.4.93.6

## Q7

Did not get an authoritative answer because the IP address we used in the query is not in the Authority section meaning it does have the authority to respond to the query.

dig 129.94.242.33 yahoo.com 

; <<>> DiG 9.9.5-9+deb8u19-Debian <<>> 129.94.242.33 yahoo.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NXDOMAIN, id: 26458
;; flags: qr rd ra; QUERY: 1, ANSWER: 0, AUTHORITY: 1, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;129.94.242.33.			IN	A

;; AUTHORITY SECTION:
.			10800	IN	SOA	a.root-servers.net. nstld.verisign-grs.com. 2022062700 1800 900 604800 86400

;; Query time: 6 msec
;; SERVER: 129.94.242.2#53(129.94.242.2)
;; WHEN: Mon Jun 27 23:02:12 AEST 2022
;; MSG SIZE  rcvd: 117

;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 40330
;; flags: qr rd ra; QUERY: 1, ANSWER: 6, AUTHORITY: 5, ADDITIONAL: 10

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;yahoo.com.			IN	A

;; ANSWER SECTION:
yahoo.com.		640	IN	A	98.137.11.164
yahoo.com.		640	IN	A	98.137.11.163
yahoo.com.		640	IN	A	74.6.231.20
yahoo.com.		640	IN	A	74.6.231.21
yahoo.com.		640	IN	A	74.6.143.26
yahoo.com.		640	IN	A	74.6.143.25

;; AUTHORITY SECTION:
yahoo.com.		39538	IN	NS	ns4.yahoo.com.
yahoo.com.		39538	IN	NS	ns2.yahoo.com.
yahoo.com.		39538	IN	NS	ns1.yahoo.com.
yahoo.com.		39538	IN	NS	ns3.yahoo.com.
yahoo.com.		39538	IN	NS	ns5.yahoo.com.

;; ADDITIONAL SECTION:
ns1.yahoo.com.		150342	IN	A	68.180.131.16
ns1.yahoo.com.		48262	IN	AAAA	2001:4998:1b0::7961:686f:6f21
ns2.yahoo.com.		132928	IN	A	68.142.255.16
ns2.yahoo.com.		46456	IN	AAAA	2001:4998:1c0::7961:686f:6f21
ns3.yahoo.com.		1558	IN	A	27.123.42.42
ns3.yahoo.com.		1558	IN	AAAA	2406:8600:f03f:1f8::1003
ns4.yahoo.com.		562192	IN	A	98.138.11.157
ns5.yahoo.com.		21764	IN	A	202.165.97.53
ns5.yahoo.com.		21764	IN	AAAA	2406:2000:1d0::7961:686f:6f21

;; Query time: 4 msec
;; SERVER: 129.94.242.2#53(129.94.242.2)
;; WHEN: Mon Jun 27 23:02:12 AEST 2022
;; MSG SIZE  rcvd: 416


## Q8

Similar response to Q7.

dig 169.229.60.61 yahoo.com A

; <<>> DiG 9.9.5-9+deb8u19-Debian <<>> 169.229.60.61 yahoo.com A
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NXDOMAIN, id: 52992
;; flags: qr rd ra; QUERY: 1, ANSWER: 0, AUTHORITY: 1, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;169.229.60.61.			IN	A

;; AUTHORITY SECTION:
.			10800	IN	SOA	a.root-servers.net. nstld.verisign-grs.com. 2022062700 1800 900 604800 86400

;; Query time: 51 msec
;; SERVER: 129.94.242.2#53(129.94.242.2)
;; WHEN: Mon Jun 27 23:15:26 AEST 2022
;; MSG SIZE  rcvd: 117

;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 24790
;; flags: qr rd ra; QUERY: 1, ANSWER: 6, AUTHORITY: 5, ADDITIONAL: 10

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;yahoo.com.			IN	A

;; ANSWER SECTION:
yahoo.com.		1800	IN	A	74.6.231.20
yahoo.com.		1800	IN	A	74.6.143.26
yahoo.com.		1800	IN	A	98.137.11.163
yahoo.com.		1800	IN	A	74.6.231.21
yahoo.com.		1800	IN	A	98.137.11.164
yahoo.com.		1800	IN	A	74.6.143.25

;; AUTHORITY SECTION:
yahoo.com.		38744	IN	NS	ns5.yahoo.com.
yahoo.com.		38744	IN	NS	ns4.yahoo.com.
yahoo.com.		38744	IN	NS	ns2.yahoo.com.
yahoo.com.		38744	IN	NS	ns1.yahoo.com.
yahoo.com.		38744	IN	NS	ns3.yahoo.com.

;; ADDITIONAL SECTION:
ns1.yahoo.com.		149548	IN	A	68.180.131.16
ns1.yahoo.com.		47468	IN	AAAA	2001:4998:1b0::7961:686f:6f21
ns2.yahoo.com.		132134	IN	A	68.142.255.16
ns2.yahoo.com.		45662	IN	AAAA	2001:4998:1c0::7961:686f:6f21
ns3.yahoo.com.		764	IN	A	27.123.42.42
ns3.yahoo.com.		764	IN	AAAA	2406:8600:f03f:1f8::1003
ns4.yahoo.com.		561398	IN	A	98.138.11.157
ns5.yahoo.com.		20970	IN	A	202.165.97.53
ns5.yahoo.com.		20970	IN	AAAA	2406:2000:1d0::7961:686f:6f21

;; Query time: 100 msec
;; SERVER: 129.94.242.2#53(129.94.242.2)
;; WHEN: Mon Jun 27 23:15:26 AEST 2022
;; MSG SIZE  rcvd: 416

## Q9

dig @68.180.131.16 yahoo.com NS

; <<>> DiG 9.9.5-9+deb8u19-Debian <<>> @68.180.131.16 yahoo.com NS
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 54507
;; flags: qr aa rd; QUERY: 1, ANSWER: 5, AUTHORITY: 0, ADDITIONAL: 10
;; WARNING: recursion requested but not available

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1272
;; QUESTION SECTION:
;yahoo.com.			IN	NS

;; ANSWER SECTION:
yahoo.com.		172800	IN	NS	ns1.yahoo.com.
yahoo.com.		172800	IN	NS	ns2.yahoo.com.
yahoo.com.		172800	IN	NS	ns5.yahoo.com.
yahoo.com.		172800	IN	NS	ns4.yahoo.com.
yahoo.com.		172800	IN	NS	ns3.yahoo.com.

;; ADDITIONAL SECTION:
ns1.yahoo.com.		1209600	IN	A	68.180.131.16
ns2.yahoo.com.		1209600	IN	A	68.142.255.16
ns3.yahoo.com.		1800	IN	A	27.123.42.42
ns4.yahoo.com.		1209600	IN	A	98.138.11.157
ns5.yahoo.com.		86400	IN	A	202.165.97.53
ns1.yahoo.com.		86400	IN	AAAA	2001:4998:1b0::7961:686f:6f21
ns2.yahoo.com.		86400	IN	AAAA	2001:4998:1c0::7961:686f:6f21
ns3.yahoo.com.		1800	IN	AAAA	2406:8600:f03f:1f8::1003
ns5.yahoo.com.		86400	IN	AAAA	2406:2000:1d0::7961:686f:6f21

;; Query time: 141 msec
;; SERVER: 68.180.131.16#53(68.180.131.16)
;; WHEN: Mon Jun 27 23:27:50 AEST 2022
;; MSG SIZE  rcvd: 320

dig @68.180.131.16 yahoo.com MX

; <<>> DiG 9.9.5-9+deb8u19-Debian <<>> @68.180.131.16 yahoo.com MX
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 7989
;; flags: qr aa rd; QUERY: 1, ANSWER: 3, AUTHORITY: 0, ADDITIONAL: 1
;; WARNING: recursion requested but not available

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1272
;; QUESTION SECTION:
;yahoo.com.			IN	MX

;; ANSWER SECTION:
yahoo.com.		1800	IN	MX	1 mta7.am0.yahoodns.net.
yahoo.com.		1800	IN	MX	1 mta5.am0.yahoodns.net.
yahoo.com.		1800	IN	MX	1 mta6.am0.yahoodns.net.

;; Query time: 141 msec
;; SERVER: 68.180.131.16#53(68.180.131.16)
;; WHEN: Mon Jun 27 23:29:39 AEST 2022
;; MSG SIZE  rcvd: 117

## Q10

129.94.210.20, queried 5 DNS

- Commands:

dig . NS

; <<>> DiG 9.16.27-Debian <<>> . NS
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 62545
;; flags: qr rd ra; QUERY: 1, ANSWER: 13, AUTHORITY: 0, ADDITIONAL: 27

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;.				IN	NS

;; ANSWER SECTION:
.			238055	IN	NS	h.root-servers.net.
.			238055	IN	NS	f.root-servers.net.
.			238055	IN	NS	d.root-servers.net.
.			238055	IN	NS	a.root-servers.net.
.			238055	IN	NS	l.root-servers.net.
.			238055	IN	NS	j.root-servers.net.
.			238055	IN	NS	e.root-servers.net.
.			238055	IN	NS	i.root-servers.net.
.			238055	IN	NS	m.root-servers.net.
.			238055	IN	NS	b.root-servers.net.
.			238055	IN	NS	c.root-servers.net.
.			238055	IN	NS	k.root-servers.net.
.			238055	IN	NS	g.root-servers.net.

;; ADDITIONAL SECTION:
a.root-servers.net.	148339	IN	A	198.41.0.4
a.root-servers.net.	104368	IN	AAAA	2001:503:ba3e::2:30
b.root-servers.net.	101068	IN	A	199.9.14.201
b.root-servers.net.	107409	IN	AAAA	2001:500:200::b
c.root-servers.net.	94507	IN	A	192.33.4.12
c.root-servers.net.	30663	IN	AAAA	2001:500:2::c
d.root-servers.net.	101068	IN	A	199.7.91.13
d.root-servers.net.	107409	IN	AAAA	2001:500:2d::d
e.root-servers.net.	462663	IN	A	192.203.230.10
e.root-servers.net.	30663	IN	AAAA	2001:500:a8::e
f.root-servers.net.	65939	IN	A	192.5.5.241
f.root-servers.net.	30663	IN	AAAA	2001:500:2f::f
g.root-servers.net.	504481	IN	A	192.112.36.4
g.root-servers.net.	82578	IN	AAAA	2001:500:12::d0d
h.root-servers.net.	506812	IN	A	198.97.190.53
h.root-servers.net.	30663	IN	AAAA	2001:500:1::53
i.root-servers.net.	101068	IN	A	192.36.148.17
i.root-servers.net.	30663	IN	AAAA	2001:7fe::53
j.root-servers.net.	504482	IN	A	192.58.128.30
j.root-servers.net.	107409	IN	AAAA	2001:503:c27::2:30
k.root-servers.net.	30663	IN	A	193.0.14.129
k.root-servers.net.	30663	IN	AAAA	2001:7fd::1
l.root-servers.net.	522744	IN	A	199.7.83.42
l.root-servers.net.	107409	IN	AAAA	2001:500:9f::42
m.root-servers.net.	94506	IN	A	202.12.27.33
m.root-servers.net.	107409	IN	AAAA	2001:dc3::35

;; Query time: 12 msec
;; SERVER: 129.94.208.3#53(129.94.208.3)
;; WHEN: Thu Jun 23 14:42:11 AEST 2022
;; MSG SIZE  rcvd: 811

dig @198.41.0.4 lyre00.cse.unsw.edu.au NS

; <<>> DiG 9.16.27-Debian <<>> @198.41.0.4 lyre00.cse.unsw.edu.au NS
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 13625
;; flags: qr rd; QUERY: 1, ANSWER: 0, AUTHORITY: 4, ADDITIONAL: 9
;; WARNING: recursion requested but not available

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;lyre00.cse.unsw.edu.au.		IN	NS

;; AUTHORITY SECTION:
au.			172800	IN	NS	q.au.
au.			172800	IN	NS	t.au.
au.			172800	IN	NS	s.au.
au.			172800	IN	NS	r.au.

;; ADDITIONAL SECTION:
q.au.			172800	IN	A	65.22.196.1
q.au.			172800	IN	AAAA	2a01:8840:be::1
t.au.			172800	IN	A	65.22.199.1
t.au.			172800	IN	AAAA	2a01:8840:c1::1
s.au.			172800	IN	A	65.22.198.1
s.au.			172800	IN	AAAA	2a01:8840:c0::1
r.au.			172800	IN	A	65.22.197.1
r.au.			172800	IN	AAAA	2a01:8840:bf::1

;; Query time: 152 msec
;; SERVER: 198.41.0.4#53(198.41.0.4)
;; WHEN: Thu Jun 23 14:44:39 AEST 2022
;; MSG SIZE  rcvd: 291

dig @65.22.196.1 lyre00.cse.unsw.edu.au NS

; <<>> DiG 9.16.27-Debian <<>> @65.22.196.1 lyre00.cse.unsw.edu.au NS
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 35442
;; flags: qr rd; QUERY: 1, ANSWER: 0, AUTHORITY: 3, ADDITIONAL: 6
;; WARNING: recursion requested but not available

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1232
;; QUESTION SECTION:
;lyre00.cse.unsw.edu.au.		IN	NS

;; AUTHORITY SECTION:
unsw.edu.au.		900	IN	NS	ns3.unsw.edu.au.
unsw.edu.au.		900	IN	NS	ns1.unsw.edu.au.
unsw.edu.au.		900	IN	NS	ns2.unsw.edu.au.

;; ADDITIONAL SECTION:
ns1.unsw.edu.au.	900	IN	A	129.94.0.192
ns2.unsw.edu.au.	900	IN	A	129.94.0.193
ns3.unsw.edu.au.	900	IN	A	192.155.82.178
ns1.unsw.edu.au.	900	IN	AAAA	2001:388:c:35::1
ns2.unsw.edu.au.	900	IN	AAAA	2001:388:c:35::2

;; Query time: 24 msec
;; SERVER: 65.22.196.1#53(65.22.196.1)
;; WHEN: Thu Jun 23 14:47:00 AEST 2022
;; MSG SIZE  rcvd: 209

dig @129.94.0.192 lyre00.cse.unsw.edu.au NS

; <<>> DiG 9.16.27-Debian <<>> @129.94.0.192 lyre00.cse.unsw.edu.au NS
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 30165
;; flags: qr rd; QUERY: 1, ANSWER: 0, AUTHORITY: 2, ADDITIONAL: 5
;; WARNING: recursion requested but not available

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;lyre00.cse.unsw.edu.au.		IN	NS

;; AUTHORITY SECTION:
cse.unsw.edu.au.	300	IN	NS	maestro.orchestra.cse.unsw.edu.au.
cse.unsw.edu.au.	300	IN	NS	beethoven.orchestra.cse.unsw.edu.au.

;; ADDITIONAL SECTION:
beethoven.orchestra.cse.unsw.edu.au. 300 IN A	129.94.242.2
beethoven.orchestra.cse.unsw.edu.au. 300 IN A	129.94.172.11
beethoven.orchestra.cse.unsw.edu.au. 300 IN A	129.94.208.3
maestro.orchestra.cse.unsw.edu.au. 300 IN A	129.94.242.33

;; Query time: 4 msec
;; SERVER: 129.94.0.192#53(129.94.0.192)
;; WHEN: Thu Jun 23 14:50:24 AEST 2022
;; MSG SIZE  rcvd: 171

dig @129.94.242.2 lyre00.cse.unsw.edu.au NS

; <<>> DiG 9.16.27-Debian <<>> @129.94.242.2 lyre00.cse.unsw.edu.au NS
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 4237
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 0, AUTHORITY: 1, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;lyre00.cse.unsw.edu.au.		IN	NS

;; AUTHORITY SECTION:
cse.unsw.EDU.AU.	900	IN	SOA	maestro.orchestra.cse.unsw.EDU.AU. hostmaster.cse.unsw.edu.au. 2022062200 2000 300 1209600 900

;; Query time: 12 msec
;; SERVER: 129.94.242.2#53(129.94.242.2)
;; WHEN: Thu Jun 23 14:50:52 AEST 2022
;; MSG SIZE  rcvd: 131

dig @129.94.242.2 lyre00.cse.unsw.edu.au A

; <<>> DiG 9.16.27-Debian <<>> @129.94.242.2 lyre00.cse.unsw.edu.au A
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 51828
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 2, ADDITIONAL: 3

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;lyre00.cse.unsw.edu.au.		IN	A

;; ANSWER SECTION:
lyre00.cse.unsw.EDU.AU.	3600	IN	A	129.94.210.20

;; AUTHORITY SECTION:
cse.unsw.EDU.AU.	3600	IN	NS	beethoven.orchestra.cse.unsw.EDU.AU.
cse.unsw.EDU.AU.	3600	IN	NS	maestro.orchestra.cse.unsw.EDU.AU.

;; ADDITIONAL SECTION:
maestro.orchestra.cse.unsw.EDU.AU. 3600	IN A	129.94.242.33
beethoven.orchestra.cse.unsw.EDU.AU. 3600 IN A	129.94.208.3

;; Query time: 0 msec
;; SERVER: 129.94.242.2#53(129.94.242.2)
;; WHEN: Thu Jun 23 14:50:58 AEST 2022
;; MSG SIZE  rcvd: 177
