from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from collections import defaultdict
import hashlib, json, sys, time, uuid, asyncio
import venntdb

MAX_REQUESTS_PER_MINUTE = 60
MAX_REQUEST_SIZE = 10000

PATHS = {
	"GET_ATTR" : '/get_attr',
	"SET_ATTR" : '/set_attr',
	"CREATE_CHARACTER" : "/create_character",
	"CREATE_CAMPAIGN" : "/create_campaign",
	"SET_ROLE" : "/set_role",
	"GET_ROLE" : "/get_role"
}


KEY_AUTH = "auth_token"
KEY_ATTR = "attr"
KEY_VAL = "val"
KEY_NAME = "name"


class VenntHandler(BaseHTTPRequestHandler):

	def __init__(self, *args):
		super().__init__(*args)
		self.requests = {}
		self.scheduler = asyncio.create_task(self.clear_rate_limiits())
		
	async def clear_rate_limiits(self):
		self.requests = {}
		await asyncio.sleep(60)
		
	def is_rate_limited(self):
		client = self.client_address[0]
		if not client in self.requests:
			self.requests[client] = defaultdict(int)
		self.requests[client] += 1
		return self.requests[client] < MAX_REQUESTS_PER_MINUTE

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
			result = { 'success': True, 'data': data }
			self.wfile.write(json.dumps(result).encode('utf-8'))
		
	def _send_error(self, data):
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.send_header('Access-Control-Allow-Origin','*')
		self.end_headers()

		if data != None:
			result = { 'success': False, 'data': data }
			self.wfile.write(json.dumps(result).encode('utf-8'))

	def _check_keys(self, args, keys_req, keys_opt=[]):
		for key in keys_req:
			if key not in args:
				return 'Missing required key ' + key + '.'
		for key in args.keys():
			if key not in keys_req and key not in keys_opt:
				return 'Unknown key ' + key + '.'
		return None

	def do_HEAD(self):
		if self.is_rate_limited():
			return self._send_error("Too many requests")
	
		parse = urlparse(self.path)
		path = parse.path
		if len(path) > MAX_REQUEST_SIZE:
			return self._send_error("Request too large")

		if path in [val for key, val in PATHS.items()]:
			return self._send_success(None)
		else:
			return self._send_error(None)
			
	def do_POST(self):
		print("do_POST received")
		#self.do_GET()
		if self.is_rate_limited():
			return self._send_error("Too many requests.")
		
		content_length = int(self.headers['Content-Length'])
		if content_length > MAX_REQUEST_SIZE:
			return self._send_error("Request too large")
			
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
		if self.is_rate_limited():
			return self._send_error("Too many requests")
	
		parse = urlparse(self.path)
		path = parse.path
		if len(path) > MAX_REQUEST_SIZE:
			return self._send_error("Request too large")

		# get the JSON arguments
		query = parse_qs(parse.query)

		if 'q' not in query:
			return self._send_error('Missing query q.')

		if len(query['q']) != 1:
			return self._send_error('Multiple query q.')

		try:
			args = json.loads(query['q'][0])
		except ValueError:
			return self._send_error('Error parsing JSON.')


		# handle different path requests
		if path == PATHS["CREATE_CHARACTER"]:
			# check args
			key_error = self._check_keys(args, [KEY_AUTH, KEY_NAME])
			if key_error:
				return self._send_error(key_error)
			
			name = args[KEY_NAME]		
			id = str(uuid.uuid4())
			character = {"name":name, "id":id}
			username = self.server._db.get_authenticated_user(args[KEY_AUTH])
			self.server._db.create_character(username, character)
			
			ret = {"success":True, "id":id}
			return self._send_success(ret)
			
		elif path in PATHS:
			self._send_success({"success":False, "info":"Not yet implemented"})
			
		else:
			# return error for unrecognized request
			return self._send_error('Bad request path.')
