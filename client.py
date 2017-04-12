import socket
import sys
import base64
import ssl
args = sys.argv
print args
PORT = int(args[2])
HOST = args[1]
GET = '/'+str(args[3])
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock = ssl.wrap_socket(sock,
                             server_side=False,
                             certfile="cert.pem",
                             keyfile="cert.pem",
                             ssl_version=ssl.PROTOCOL_SSLv23) 
sock.connect((HOST, PORT))
username = ''
password = ''
status_code = ''
def authInput():
	username = raw_input('Username : ')
	password = raw_input('Password : ')
	authStr = username + ":" + password
	sendRequest(authStr)
# params = "/username="+username+"&"+"password="+password
# print ("POST %s HTTP/1.1\r\nHost: %s\r\n" % (params, HOST))
# sock.send("GET %s HTTP/1.0\r\nHost: %s\r\n" % (GET, HOST))
def sendRequest(authStr):
	s = "GET %s HTTP/1.1\r\nHost: %s\r\n" % (GET, HOST)
	x = "Authorization: Basic %s\r\n" % (base64.b64encode(authStr))
	print "no x " + authStr
	s = s + x
	print s
	sock.send(s)
	data1 = sock.recv(1024)
	print data1
	status_code = data1.split(' ')[1]
	# print status_code
	if status_code == str(401):
		# print "Asd"
		authInput()

authInput()

def sendFile(authStr):
	GET = 'qwe.html'
	s = "PUT %s HTTP/1.1\r\nHost: %s\r\n" % (GET, HOST)
	x = "Authorization: Basic %s\r\n" % (base64.b64encode(authStr))
	f = open(GET, 'r')
    f.read(request_message)
	print "no x " + authStr
	s = s + x
	print s
	sock.send(s)
	data1 = sock.recv(1024)
	print data1
	status_code = data1.split(' ')[1]
	if status_code == str(401):
		authInput()
# request_head, request_body = data1.split('\r\n', 1)
# request_head = request_head.splitlines()
# request_headline = request_head[0]
# fileName = request_headline.split(' ')[1]
# print fileName

# print data1
# sock.send("GET %s HTTP/1.0\r\nHost: %s\r\n" % (GET, HOST))
 
# data2 = sock.recv(1024*1024)
# print data
# string = ""
# while len(data):
#     string = string + data
#     print "babu"
#     data = sock.recv(1024)
#     print "babu2"
# print data
# print data2
sock.close()
 
 
sys.exit(0)