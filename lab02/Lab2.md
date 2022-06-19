# Exercise 3

## Q1

Return from server to client browser:

- Status code - 200
- Phrase - OK

## Q2

- Last modified: Tue, 23 Sep 2003 05:29:00 GMT
- Date: Tue, 23 Sep 2003 05:29:50 GMT

Last modified is when the resource was last modified while date is when the HTTP response message was sent.

## Q3

- The connection is persistent as the 'Connection' field says Keep-Alive

## Q4

73 bytes are being returned to the server

## Q5

The data contained inside the HTTP response packet is text/html. It provides details on the request e.g. if it was successful, when it was made, etc.

# Exercise 4

## Q1

I do not see an "IF-MODIFIED-SINCE" line in the HTTP GET.

## Q2

The response indicates the last time the file was modified was Tue, 23 Sep 2003 05:35:00 GMT.

## Q3

Yes I can see the 2 fileds in the HTTP GET request:

- IF-MODIFIED-SINCE - Tue, 23 Sep 2003 05:35:00 GMT
- IF-NONE-MATCH - "qbfef-173-8f4ae900"

## Q4

The HTTP status code is 304 and the phrase is Not Modified. The server did not explicitly return the contents of the file since the status code was a 3xx which indicates some form of redirect. This response does not contain a body. This can be determined by no bytes of File Data being returned.

## Q5

The value of the Etag is "1bfef-173-8f4ae900". It is used as an identifier for a specific version of a resource, letting caches be more efficient and saving bandwidth (returning the requested resource with a 200 status only if it doesn't match other given/stored Etags).

It has not changed since the first response message was received.
