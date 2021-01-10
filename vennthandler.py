from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from collections import defaultdict
import hashlib, json, sys, time, uuid
import venntdb, rate_limiter

MAX_REQUEST_SIZE = 10000

PATHS = {
	"GET_ATTR" : '/get_attr',
	"SET_ATTR" : '/set_attr',
	"CREATE_CHARACTER" : "/create_character",
	"CREATE_CAMPAIGN" : "/create_campaign",
	"SET_ROLE" : "/set_role",
	"GET_ROLE" : "/get_role",
	"LOGOUT" : "/logout",
	"GET_CAMPAIGNS" : "/get_campaigns",
	"GET_CHARACTERS" : "/get_characters",
	"GET_CHARACTER" : "/get_character"
}


KEY_AUTH = "auth_token"
KEY_ATTR = "attr"
KEY_VAL = "val"
KEY_NAME = "name"
KEY_ID = "id"

MSG_BAD_AUTH = "Authentication invalid"
MSG_TOO_MANY_REQ = "Too many requests"
MSG_REQ_LARGE = "Request too large"



class VenntHandler(BaseHTTPRequestHandler):

	def log_message(self, format, *args):
		sys.stdout.write("%s - - [%s] %s\n" %
						 (hashlib.md5(('venntserver' + self.client_address[0]).encode('utf-8')).hexdigest(),
						  self.log_date_time_string(),
						  format % args))

	def respond(self, data):
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.send_header('Access-Control-Allow-Origin','*')
		self.end_headers()
		self.wfile.write(json.dumps(data).encode('utf-8'))


	def check_keys(self, args, keys_req, keys_opt=[]):
		for key in keys_req:
			if key not in args:
				return 'Missing required key ' + key + '.'
		for key in args.keys():
			if key not in keys_req and key not in keys_opt:
				return 'Unknown key ' + key + '.'
		return None

	def do_HEAD(self):
		if rate_limiter.is_rate_limited(self.client_address[0]):
			return self.respond({"success":False, "info":MSG_TOO_MANY_REQ})
	
		parse = urlparse(self.path)
		path = parse.path
		if len(path) > MAX_REQUEST_SIZE:
			return self.respond({"success":False, "info":MSG_REQ_LARGE})

		if path in [val for key, val in PATHS.items()]:
			return self.respond({"success":True})
		else:
			return self.respond({"success":False})
			
	def do_POST(self):
		print("do_POST received")
		#self.do_GET()
		if rate_limiter.is_rate_limited(self.client_address[0]):
			return self.respond({"success":False, "info":MSG_TOO_MANY_REQ})
		
		content_length = int(self.headers['Content-Length'])
		if content_length > MAX_REQUEST_SIZE:
			return self.respond({"success":False, "info":MSG_REQ_LARGE})
			
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
			self.respond(result)
			return
		
		if result == {}:
			if "register" in json_data:
				username = json_data["register"]
				if self.server.db.account_exists(username):
					result["success"] = False
					result["info"] = "Username already exists"
					self.respond(result)
					return
				if "password" in json_data:
					password = json_data["password"]
				else:
					result["success"] = False
					result["info"] = "No password key"
					self.respond(result)
					return
				self.server.db.create_account(username, hashlib.md5(password.encode('utf-8')).hexdigest())
				result["success"] = True
				result["info"] = "Account created"
				auth_token = hashlib.md5((username + str(time.time())).encode('utf-8')).hexdigest()
				self.server.db.authenticate(username, auth_token)
				result["auth_token"] = auth_token
				self.respond(result)
				return
			elif "login" in json_data:
				username = json_data["login"]
				if not self.server.db.account_exists(username):
					result["success"] = False
					result["info"] = "No such user"
					self.respond(result)
					return
				else:
					if "password" in json_data:
						password = json_data["password"]
					else:
						result["success"] = False
						result["info"] = "No password key"
						self.respond(result)
						return
					pass_hash = hashlib.md5(password.encode('utf-8')).hexdigest()
					if not self.server.db.does_password_match(username, pass_hash):
						result["success"] = False
						result["info"] = "Incorrect password"
						self.respond(result)
						return
					else:
						result["success"] = True
						result["info"] = "Successful login"
						auth_token = hashlib.md5((username + str(time.time())).encode('utf-8')).hexdigest()
						self.server.db.authenticate(username, auth_token)
						result["auth_token"] = auth_token
						self.respond(result)
						return
			else:
				result["success"] = False
				result["info"] = "POST must contain register or login key"
				self.respond(result)
				return
		

	def do_GET(self):
		if rate_limiter.is_rate_limited(self.client_address[0]):
			return self.respond({"success":False, "info":MSG_TOO_MANY_REQ})
	
		parse = urlparse(self.path)
		path = parse.path
		if len(path) > MAX_REQUEST_SIZE:
			return self.respond({"success":False, "info":MSG_REQ_LARGE})

		# get the JSON arguments
		query = parse_qs(parse.query)

		if 'q' not in query:
			return self.respond('Missing query q.')

		if len(query['q']) != 1:
			return self.respond('Multiple query q.')

		try:
			args = json.loads(query['q'][0])
		except ValueError:
			return self.respond('Error parsing JSON.')


		# handle different path requests
		if path == PATHS["CREATE_CHARACTER"]:
			# check args
			key_error = self.check_keys(args, [KEY_AUTH, KEY_NAME], keys_opt=venntdb.ATTRIBUTES)
			if key_error:
				return self.respond(key_error)
				
			if not self.server.db.is_authenticated(args[KEY_AUTH]):
				return self.respond({"success":False, "info":MSG_BAD_AUTH})
			
			name = args[KEY_NAME]		
			id = str(uuid.uuid4())
			character = {"name":name, "id":id}
			for key in args:
				if key in ATTRIBUTES:
					character[key] = args[key]
			username = self.server.db.get_authenticated_user(args[KEY_AUTH])
			self.server.db.create_character(username, character)
			
			ret = {"success":True, "id":id}
			return self.respond(ret)
			
		elif path == PATHS["CREATE_CAMPAIGN"]:
			# check args
			key_error = self.check_keys(args, [KEY_AUTH, KEY_NAME])
			if key_error:
				return self.respond(key_error)
				
			if not self.server.db.is_authenticated(args[KEY_AUTH]):
				return self.respond({"success":False, "info":MSG_BAD_AUTH})
			
			name = args[KEY_NAME]		
			id = str(uuid.uuid4())
			campaign = {"name":name, "id":id}
			username = self.server.db.get_authenticated_user(args[KEY_AUTH])
			self.server.db.create_campaign(username, campaign)
			
			ret = {"success":True, "id":id}
			return self.respond(ret)
			
		elif path == PATHS["SET_ATTR"]:
			key_error = self.check_keys(args, [KEY_AUTH, KEY_ID, KEY_ATTR, KEY_VAL])
			if key_error:
				return self.respond(key_error)
				
			if not self.server.db.is_authenticated(args[KEY_AUTH]):
				return self.respond({"success":False, "info":MSG_BAD_AUTH})
			
			char_id = args[KEY_ID]
			attr = args[KEY_ATTR]
			val = args[KEY_VAL]
			
			if attr not in venntdb.ATTRIBUTES:
				return self.respond({"success":False,"info":"Unknown attribute"})
				
			username = self.server.db.get_authenticated_user(args[KEY_AUTH])
				
			if not self.server.db.character_exists(username, char_id):
				return self.respond({"success":False,"info":"No such character"})
			
			self.server.db.set_attr(username, char_id, attr, val)
			return self.respond({"success":True})
			
		elif path == PATHS["GET_ATTR"]:
			key_error = self.check_keys(args, [KEY_AUTH, KEY_ID, KEY_ATTR])
			if key_error:
				return self.respond(key_error)
				
			if not self.server.db.is_authenticated(args[KEY_AUTH]):
				return self.respond({"success":False, "info":MSG_BAD_AUTH})
			
			char_id = args[KEY_ID]
			attr = args[KEY_ATTR]
			
			if attr not in venntdb.ATTRIBUTES:
				return self.respond({"success":False,"info":"Unknown attribute"})
				
			username = self.server.db.get_authenticated_user(args[KEY_AUTH])
				
			if not self.server.db.character_exists(username, char_id):
				return self.respond({"success":False,"info":"No such character"})
			
			val = self.server.db.get_attr(username, char_id, attr)
			return self.respond({"success":True, "value":str(val)})
			
		elif path == PATHS["LOGOUT"]:
			key_error = self.check_keys(args, [KEY_AUTH])
			if key_error:
				return self.respond(key_error)
			
			success = self.server.db.deauthenticate(args[KEY_AUTH])
			return self.respond({"success":success})
			
		elif path == PATHS["GET_CAMPAIGNS"]:
			key_error = self.check_keys(args, [KEY_AUTH])
			if key_error:
				return self.respond(key_error)
				
			if not self.server.db.is_authenticated(args[KEY_AUTH]):
				return self.respond({"success":False, "info":MSG_BAD_AUTH})
				
			username = self.server.db.get_authenticated_user(args[KEY_AUTH])
				
			return self.respond({"success":True, "value":str(self.server.db.get_campaigns(username))})
			
		elif path == PATHS["GET_CHARACTERS"]:
			key_error = self.check_keys(args, [KEY_AUTH])
			if key_error:
				return self.respond(key_error)
				
			if not self.server.db.is_authenticated(args[KEY_AUTH]):
				return self.respond({"success":False, "info":MSG_BAD_AUTH})
				
			username = self.server.db.get_authenticated_user(args[KEY_AUTH])
				
			return self.respond({"success":True, "value":str(self.server.db.get_characters(username))})
			
		elif path == PATHS["GET_CHARACTER"]:
			key_error = self.check_keys(args, [KEY_AUTH, KEY_ID])
			if key_error:
				return self.respond(key_error)
				
			if not self.server.db.is_authenticated(args[KEY_AUTH]):
				return self.respond({"success":False, "info":MSG_BAD_AUTH})
				
			username = self.server.db.get_authenticated_user(args[KEY_AUTH])
			id = args[KEY_ID]
				
			return self.respond({"success":True, "value":str(self.server.db.get_character(username, id))})
				
			
			
	# "SET_ROLE" : "/set_role",
	# "GET_ROLE" : "/get_role"
			
		elif path in PATHS:
			self.respond({"success":False, "info":"Not yet implemented"})
			
		else:
			# return error for unrecognized request
			return self.respond('Bad request path.')
