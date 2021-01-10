from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import hashlib, json, sys, time
import venntdb

PATHS = {
	"REGISTER" : '/register',
	"GET" : '/get',
	"SET" : '/set'
}


KEY_USER = "username"
KEY_PASS = "password"



class VenntHandler(BaseHTTPRequestHandler):

	def log_message(self, format, *args):
		sys.stdout.write("%s - - [%s] %s\n" %
						 (hashlib.md5(('venntserver' + self.client_address[0]).encode('utf-8')).hexdigest(),
						  self.log_date_time_string(),
						  format % args))

	def _send_success(self, data):
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.send_header('Access-Control-Allow-Origin','*')
		self.end_headers()

		if data != None:
			result = { 'result': True, 'data': data }
			self.wfile.write(json.dumps(result))
		
	def _send_error(self, data):
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.send_header('Access-Control-Allow-Origin','*')
		self.end_headers()

		if data != None:
			result = { 'result': False, 'data': data }
			self.wfile.write(json.dumps(result))

	def _check_keys(self, args, keys_req, keys_opt=[]):
		for key in keys_req:
			if not args.has_key(key):
				return 'Missing required key ' + key + '.'
		for key in args.iterkeys():
			if key not in keys_req and key not in keys_opt:
				return 'Unknown key ' + key + '.'
		return None

	def do_HEAD(self):
		parse = urlparse.urlparse(self.path)
		path = parse.path

		if path in [val for key, val in PATHS.items()]:
			return self._send_success(None)
		else:
			return self._send_error(None)
			
	def do_POST(self):
		print("do_POST received")
		#self.do_GET()
		
		content_length = int(self.headers['Content-Length'])
		post_data = self.rfile.read(content_length)
		post_data = post_data.decode('utf-8')
		print("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n" %
				(str(self.path), str(self.headers), post_data))
		
		result = {}		
		try:
			json_data = json.loads(post_data)
		except:
			result["success"] = False
			result["info"] = "Bad JSON"
			self.return_post(result)
			return
		
		if result == {}:
			if "register" in json_data:
				username = json_data["register"]
				if self.server._db.account_exists(username):
					result["success"] = False
					result["info"] = "Username already exists"
					self.return_post(result)
					return
				if "password" in json_data:
					password = json_data["password"]
				else:
					result["success"] = False
					result["info"] = "No password key"
					self.return_post(result)
					return
				self.server._db.create_account(username, hashlib.md5(password.encode('utf-8')).hexdigest())
				result["success"] = True
				result["info"] = "Account created"
				auth_token = hashlib.md5((username + str(time.time())).encode('utf-8')).hexdigest()
				self.server._db.authenticate(username, auth_token)
				result["auth_token"] = auth_token
				self.return_post(result)
				return
			elif "login" in json_data:
				username = json_data["login"]
				if not self.server._db.account_exists(username):
					result["success"] = False
					result["info"] = "No such user"
					self.return_post(result)
					return
				else:
					if "password" in json_data:
						password = json_data["password"]
					else:
						result["success"] = False
						result["info"] = "No password key"
						self.return_post(result)
						return
					pass_hash = hashlib.md5(password.encode('utf-8')).hexdigest()
					if not self.server._db.does_password_match(username, pass_hash):
						result["success"] = False
						result["info"] = "Incorrect password"
						self.return_post(result)
						return
					else:
						result["success"] = True
						result["info"] = "Successful login"
						auth_token = hashlib.md5((username + str(time.time())).encode('utf-8')).hexdigest()
						self.server._db.authenticate(username, auth_token)
						result["auth_token"] = auth_token
						self.return_post(result)
						return
			else:
				result["success"] = False
				result["info"] = "POST must contain register or login key"
				self.return_post(result)
				return
			
		
	def return_post(self, result):
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.send_header('Access-Control-Allow-Origin','*')
		self.end_headers()
		self.wfile.write(json.dumps(result).encode('utf-8'))
		

	def do_GET(self):
		parse = urlparse.urlparse(self.path)
		path = parse.path

		# get the JSON arguments
		query = urlparse.parse_qs(parse.query)

		if not query.has_key('q'):
			return self._send_error('Missing query q.')

		if len(query['q']) != 1:
			return self._send_error('Multiple query q.')

		try:
			args = json.loads(query['q'][0])
		except ValueError:
			return self._send_error('Error parsing JSON.')

		# handle different path requests
		if path == PATHS["REGISTER"]:
			# check args
			key_error = self._check_keys(args, [KEY_USER, KEY_PASS])
			if key_error:
				return self._send_error(key_error)
				
			username = args[KEY_USER]
			password = args[KEY_PASS]
			
			
			
			return self._send_success(True)
			
		else:
			# return error for unrecognized request
			return self._send_error('Bad request path.')
