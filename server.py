import socket
import os.path

HOST, PORT = '', 8888

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(1)
print 'Serving HTTP on port %s ...' % PORT
while True:
	client_connection, client_address = listen_socket.accept()
	request = client_connection.recv(1024)

	# Checking the condition for empty requests (which we were getting while testing)
	if len(request) == 0:
		continue

	request_head, request_body = request.split('\r\n', 1)
	request_head = request_head.splitlines()
	request_headline = request_head[0]
	fileName = '.' + request_headline.split(' ')[1]

	# Checking if file is in the current directory
	if os.path.isfile(fileName) :
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
	            'Content-Type': 'text/html; encoding=utf8',
	            'Content-Length': len(http_responseFile),
	            'Connection': 'close',
			}

		response_headers_raw = ''.join('%s: %s\n' % (k, v) for k, v in response_headers.iteritems())

		client_connection.sendall(http_response1)
		client_connection.send(response_headers_raw)
		client_connection.sendall(http_responseFile)
	else:
		http_response1 = """HTTP/1.1 404 Not Found\n"""

		request_headers = dict(x.split(': ', 1) for x in request_head[1:])

		http_response2 = '\n'
		request_method, request_uri, request_proto = request_headline.split(' ', 3)
		response_headers = {
	            'Content-Type': 'text/html; encoding=utf8',
	            'Content-Length': len(http_response2),
	            'Connection': 'close',
			}

		response_headers_raw = ''.join('%s: %s\n' % (k, v) for k, v in response_headers.iteritems())

		client_connection.sendall(http_response1)
		#client_connection.send(response_headers_raw)
		client_connection.sendall(http_response2)

	client_connection.close()