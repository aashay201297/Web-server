#!/usr/bin/python

"""
Code Zone 0

Consists of all the modules required in the following code.
The followign modules have been imported, their functionality can now be used in
the code.
For more info on any of these, google the module name and open the docs.python.org page
"""

import socket
import os.path
from threading import Thread 
import base64
import ssl

"""
End Code Zone 0
"""

HOST, PORT = '', 8888

"""
Code Zone 3
This is divided into Sub Code Zones. Go in order for easier understanding.
Mostly hard-coded, tatti code.
"""

"""
We define a class named server in this code zone.
It inherits from class Thread - see https://docs.python.org/2/library/threading.html
Look up inheritance if not clear

start()
    Start the thread's activity.
    It must be called at most once per thread object. It arranges for the object's
    run() method to be invoked in a separate thread of control.
    This method will raise RuntimeError if called more than once on the same object.

run()
    Method representing the thread's activity.
    You may override this method in a subclass. The standard run() method invokes
    the callable object passed to the object's constructor as the target argument,
    if any, with a sequential and keyword arguments taken from the args and kwargs arguments, respectively.
"""

class server(Thread) :
    """
    Code Zone 3.1
    Constructor object - Initializes client_connection and client_address variables of
    object with the values passed as parameters
    """
    def __init__(self, client_connection, client_address) : 
        Thread.__init__(self) 
        self.client_connection = client_connection
        self.client_address = client_address

    def parseRequest(self, request) :
        request_head, request_body = request.split('\r\n', 1)
        request_head = request_head.splitlines()
        request_headline = request_head[0]
        fileName = '.' + request_headline.split(' ')[1]
        return request_head, request_body, request_headline, fileName


    def auth(self, request_body) :
        request_body = request_body.split('\r\n')
        flag = 0
        s = ''
        for request in request_body :
            if request.split(':')[0] == "Authorization" :
                s = base64.b64decode(request.split(':')[1].split(' ')[2])
                flag = 1
                break
        
        if flag == 1 and s.split(':')[0] == "aashay" and  s.split(':')[1] == "password" :
            return True
        return False    


    def putResponse(self, request) :
        request_head, request_body, request_headline, fileName = self.parseRequest(request)
        if self.auth(request_body) == False :
            http_response1 = """HTTP/1.1 401 Unauthorized\n"""
            response_headers = {
                'WWW-Authenticate': 'Basic',
                'Content-Type': 'text/html; encoding=utf8',
                'Content-Length': 0,
                'Connection': 'close',
            }
            response_headers_raw = ''.join('%s: %s\r\n' % (k, v) for k, v in response_headers.iteritems())
            sendData = http_response1+response_headers_raw+'\n'
            self.client_connection.sendall(sendData)

        else :
            request_message = request.split('\r\n\r\n')[1]
            f = open(fileName, 'w')
            f.write(request_message)
            http_response1 = """HTTP/1.1 200 OK\n"""
            request_method, request_uri, request_proto = request_headline.split(' ', 3)
            f = open('uploadDone.html','rb')
            l = f.read(1024)
            response_headers = {
                    'Content-Type': 'text/html; encoding=utf8',
                    'Content-Length': len(l),
                    'Connection': 'close',
                }
            response_headers_raw = ''.join('%s: %s\r\n' % (k, v) for k, v in response_headers.iteritems())

            sendData = http_response1+response_headers_raw+'\n'+l
            self.client_connection.sendall(sendData)


    def postResponse(self, request) :
        request_head, request_body, request_headline, fileName = self.parseRequest(request)
        params = request_headline.split(' ')
        params = params[1]
        params = params.split('/')
        params = params[1]
        if params == '':
            return
        http_response1 = """HTTP/1.1 200 OK\n"""
        request_method, request_uri, request_proto = request_headline.split(' ', 3)
        response_headers = {
                'Content-Type': 'text/html; encoding=utf8',
                'Content-Length': 0,
                'Connection': 'close',
            }

        response_headers_raw = ''.join('%s: %s\r\n' % (k, v) for k, v in response_headers.iteritems())
        sendData = http_response1 + '\n'
        self.client_connection.sendall(sendData)


    def getResponse(self, request) :
        request_head, request_body, request_headline, fileName = self.parseRequest(request)
        
        if self.auth(request_body) == False :
            http_response1 = """HTTP/1.1 401 Unauthorized\n"""
            response_headers = {
                'WWW-Authenticate': 'Basic',
                'Content-Type': 'text/html; encoding=utf8',
                'Content-Length': 0,
                'Connection': 'close',
            }
            response_headers_raw = ''.join('%s: %s\r\n' % (k, v) for k, v in response_headers.iteritems())
            sendData = http_response1+response_headers_raw+'\n'
            self.client_connection.sendall(sendData)

        # Checking if file is in the current directory
        elif os.path.isfile(fileName)  :
            http_response1 = """HTTP/1.1 200 OK\n"""
            # Making a dict with headers and their values
            request_headers = dict(x.split(': ', 1) for x in request_head[1:])

            f = open(fileName,'rb')
            l = f.read(1024)
            http_responseFile = ''
            http_responseFile = http_responseFile + l
            f.close()
            request_method, request_uri, request_proto = request_headline.split(' ', 3)
            response_headers = {
                    'WWW-Authenticate': 'Basic',
                    'Content-Type': 'text/html; encoding=utf8',
                    'Content-Length': len(http_responseFile),
                    'Connection': 'close',
                }

            response_headers_raw = ''.join('%s: %s\r\n' % (k, v) for k, v in response_headers.iteritems())
            sendData = http_response1+response_headers_raw+'\n'+http_responseFile
            self.client_connection.sendall(sendData)
        else:
            http_response1 = """HTTP/1.1 404 Not Found\n"""
            http_response2 = '\n'
            response_headers = {
                    'Content-Type': 'text/html; encoding=utf8',
                    'Content-Length': len(http_response2),
                    'Connection': 'close',
                }
            response_headers_raw = ''.join('%s: %s\r\n' % (k, v) for k, v in response_headers.iteritems())

            sendData = http_response1 + response_headers_raw + '\n' + http_response2
            self.client_connection.sendall(sendData)

    """
    Code Zone 3.3
    This method parses the request by first splitting it into 2 pieces on basis of
    \r\n characters (see https://www.tutorialspoint.com/python/string_split.htm)
    It then calls the appropriate handling method on the basis of whether the request is a get request,
    a post request or a put request
    Why we have split the way we split is basically done by studying format of HTTP requests
    and then hardcoding the procedure to get exactly what we want.
    You can try and verify this manually.
    """
    def respond(self, request):
        request_head, request_body = request.split('\r\n', 1)
        request_head = request_head.splitlines()

        requestType = request_head[0].split(' ')[0]

        # All three functions are pretty much hard-coded, with fixed repsonse messages.
        # If you've been able to follow this far, then you should have no trouble understanding them
        # on your own - witha bit of google, obviously.
        # In case of any problems, gimme a call.
        if requestType == "GET" :
            self.getResponse(request)
        elif requestType == "POST" :
            self.postResponse(request)
        elif requestType == "PUT" :
            self.putResponse(request)

    """
    Code Zone 3.2
    This is the run method described above. This function would be called as soon as
    start is called - which was done in Zone 2 (remember?)
    """
    def run(self):
        while True:
            # See https://stackoverflow.com/questions/7174927/when-does-socket-recvrecv-size-return
            request = self.client_connection.recv(102400)
            # Checking the condition for empty requests (which we were getting while testing)
            if len(request) == 0:
                continue
            print "request = " ,request
            # Call respond method of class to respond to incoming request (Zone 3.3)
            self.respond(request)
        
        # Once done with everything, close connection
        self.client_connection.close()

"""
End Code Zone 3
"""


"""
Code Zone 1
"""

"""
1. listen_socket = socket.socket() => listen_socket is now a socket object that you
can use.
Look up - https://docs.python.org/2/library/socket.html [1]
and     - https://stackoverflow.com/questions/1593946/what-is-af-inet-and-why-do-i-need-it
socket.AF_INET and socket.SOCK_STREAM are parameters to be sent which decide the
type of socket object to be created.

(Assuming you're decently familiar with OOP concepts like class and object.
Gimme a call/Google otherwsie (StackOverflow FTW))

2. listen_socket.setsockopt() => Allows setting or knowing current options in socket object
Here, we're setting it to reuse addresses
Parameter order and meaning - search on [1]
Why do we do this - https://stackoverflow.com/questions/3229860/what-is-the-meaning-of-so-reuseaddr-setsockopt-option-linux

3. listen_socket.bind() => Bind socket to localhost or 127.0.0.1 with port 8888
These values have been defined globally right under Zone 0
"""

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))

"""
End Code Zone 1
(Simple enough so far)
"""

"""
Code Zone 2
"""

# Printing Port number to terminal for convenience. Can now access server from browser
# or clientside code. From browser, enter address as 127.0.0.1
print 'Serving HTTP on port %s ...' % PORT

threads = [] # Created an empty list named threads (Think similar to arrays in c/c++)
requesting_clients = dict() # Created an empty dictionary of name requesting_clients
list_client = [] # An empty list
blacklist = [] #Another empty list

while True:
    listen_socket.listen(4) # Listening for incoming connections - https://stackoverflow.com/questions/2444459/python-sock-listen

    # A TCP connection is identified by address of client and server
    # This accepts a connection and returns values accordingly
    # Think of client_connection as a manifestation of connection that you can manipulate (will see below)
    # client_address is simply the address of incoming client
    # For a bit more light, see https://stackoverflow.com/questions/12454675/whats-the-return-value-of-socket-accept-in-python
    client_connection, client_address = listen_socket.accept()

    # Check if client IP is in blacklist
    if client_address[0] in blacklist :
        # If in blacklist, close connection
        client_connection.close()
        continue

    # newthread is an object of the class named server that we have defined in this codefile
    # connection object and address sent as parameters
    # More on this in Code Zone 3
    newthread = server(client_connection, client_address) 

    # Maintain number of requesting clients from an IP
    if client_address[0] in list_client : 
        requesting_clients[client_address[0]] +=  1
    else:
        requesting_clients[client_address[0]] = 1
        list_client.append(client_address[0])

    # Iteraing over elements in list_client
    for value in list_client : 
        # If number of requesting clients from an IP is greater than 300, blacklist that IP
        if requesting_clients[value] > 300 : 
            blacklist.append(value)

    # Start execution of thread (Would become clearer in Zone 3)
    newthread.start()
    # Add thread to a list of thread objects (as newthread variable is reused in each iteration of while loop)
    threads.append(newthread)

# Ensure that you wait for all child threads to terminate before exiting
# Also see https://stackoverflow.com/questions/15085348/what-is-the-use-of-join-in-python-threading
for t in threads: 
    t.join()

"""
Keeping multiple threads (one for each connection) allows maintaining multiple connections
without explicitly coding each instance. An object of same class is created everytime a
new connection is made, with each having its own "identity", so to speak, as each handles a
different connection, which it is given as a parameter while construction.
"""

"""
End Code Zone 2
"""

"""
Also see - https://www.tutorialspoint.com/python/python_dictionary.htm
"""