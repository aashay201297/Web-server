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
sock.connect((HOST, PORT))
username = ''
password = ''
status_code = ''


def authInput():
	username = raw_input('Username : ')
	password = raw_input('Password : ')
	authStr = username + ":" + password
	sendRequest(authStr) # Send file for uploading file using PUT request

def sendRequest(authStr):
	s = "GET %s HTTP/1.1\r\nHost: %s\r\n" % (GET, HOST)
	x = "Authorization: Basic %s\r\n" % (base64.b64encode(authStr))
	s = s + x
	print s
	sock.send(s)
	data1 = sock.recv(1024)
	print data1
	status_code = data1.split(' ')[1]
	if status_code == str(401):
		authInput()

authInput()

sock.close()
sys.exit(0)
