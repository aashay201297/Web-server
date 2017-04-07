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
	#print "abcd\n" + request
	if len(request) == 0:
		continue
	request_head, request_body = request.split('\r\n', 1)

	# first line is request headline, and others are headers
	request_head = request_head.splitlines()
	request_headline = request_head[0]
	fileName = '.' + request_headline.split(' ')[1]
	if os.path.isfile(fileName) :
		http_response1 = """HTTP/1.1 200 OK\n"""

		#print request_headline
		# headers have their name up to first ': '. In real world uses, they
		# could duplicate, and dict drops duplicates by default, so
		# be aware of this.
		request_headers = dict(x.split(': ', 1) for x in request_head[1:])

		f = open(fileName,'rb')
		l = f.read(1024)
		#print l
		http_response2 = ''
		http_response2 = http_response2 + l
		#print http_response

		f.close()
		
		# request = normalize_line_endings(recv_all(client_sock)) # hack again
		# headline has form of "POST /can/i/haz/requests HTTP/1.0"
		request_method, request_uri, request_proto = request_headline.split(' ', 3)
		response_headers = {
	            'Content-Type': 'text/html; encoding=utf8',
	            'Content-Length': len(http_response2),
	            'Connection': 'close',
			}

		response_headers_raw = ''.join('%s: %s\n' % (k, v) for k, v in response_headers.iteritems())

	    


		client_connection.sendall(http_response1)
		client_connection.send(response_headers_raw)
		client_connection.sendall(http_response2)
	else:
		http_response1 = """HTTP/1.1 404 Not Found\n"""

		#print request_headline
		# headers have their name up to first ': '. In real world uses, they
		# could duplicate, and dict drops duplicates by default, so
		# be aware of this.
		request_headers = dict(x.split(': ', 1) for x in request_head[1:])

		http_response2 = '\n'
		#http_response2 = http_response2 + l
		#print http_response

		
		# request = normalize_line_endings(recv_all(client_sock)) # hack again
		# headline has form of "POST /can/i/haz/requests HTTP/1.0"
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