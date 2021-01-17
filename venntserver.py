# Josh Aaron Miller 2021
# Vennt Server Main

from http.server import BaseHTTPRequestHandler, HTTPServer
import sys
import ssl
import venntdb, vennthandler



HOST_NAME = ''
PORT_NUMBER = 3004
	

if __name__ == '__main__':
	if len(sys.argv) < 3 or len(sys.argv) > 4:
		print('usage: %s [db] [certfile path] [optional: port number, default 3004]' % sys.argv[0])
		sys.exit(-1)

	db = sys.argv[1]
	cert = sys.argv[2]
	if len(sys.argv) == 4:
		PORT_NUMBER = int(sys.argv[3])
	
	httpd = HTTPServer((HOST_NAME, PORT_NUMBER), vennthandler.VenntHandler)
	httpd.socket = ssl.wrap_socket(httpd.socket, certfile=cert, server_side=True)
	httpd.db = venntdb.VenntDB(db)

	try:
		print("Ready")
		httpd.serve_forever()
	except KeyboardInterrupt:
		pass

	httpd.server_close()
