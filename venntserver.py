from http.server import BaseHTTPRequestHandler, HTTPServer
import sys
import venntdb, vennthandler



HOST_NAME = ''
PORT_NUMBER = 3004



if __name__ == '__main__':
	if len(sys.argv) < 2 or len(sys.argv) > 3:
		print('usage: %s [db] [optional: port number, default 3004]' % sys.argv[0])
		sys.exit(-1)

	db = sys.argv[1]
	if len(sys.argv) == 3:
		PORT_NUMBER = int(sys.argv[2])
	
	httpd = HTTPServer((HOST_NAME, PORT_NUMBER), vennthandler.VenntHandler)
	httpd._db = venntdb.VenntDB(db)

	try:
		print("Ready")
		httpd.serve_forever()
	except KeyboardInterrupt:
		pass

	httpd.server_close()
