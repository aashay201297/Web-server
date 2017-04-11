import socket
import sys
 
args = sys.argv
print args
PORT = int(args[2])
HOST = args[1]
GET = '/'+str(args[3])
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
sock.connect((HOST, PORT))
username = raw_input('Username : ')
password = raw_input('Password : ')
params = "/username="+username+"&"+"password="+password
# print ("POST %s HTTP/1.1\r\nHost: %s\r\n" % (params, HOST))
# sock.send("GET %s HTTP/1.0\r\nHost: %s\r\n" % (GET, HOST))
sock.send("POST %s HTTP/1.1\r\nHost: %s\r\n" % (params, HOST))
data1 = sock.recv(1024)

sock.send("GET %s HTTP/1.0\r\nHost: %s\r\n" % (GET, HOST))
 
data2 = sock.recv(1024*1024)
# print data
# string = ""
# while len(data):
#     string = string + data
#     print "babu"
#     data = sock.recv(1024)
#     print "babu2"
# print data
print data2
sock.close()
 
 
sys.exit(0)