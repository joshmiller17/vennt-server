# Josh Aaron Miller 2021
# Vennt authentication-related processing

import hashlib, time, threading

TIMEOUT = 3600 * 12

# VenntHandler methods
def handle_register(self, json_data):
	result = {}
	username = json_data["register"][0]
	if self.server.db.is_valid("accounts", username):
		result["success"] = False
		result["info"] = "Username already exists"
		self.respond(result)
		return
	if "password" in json_data:
		password = json_data["password"][0]
	else:
		result["success"] = False
		result["info"] = "No password key"
		self.respond(result)
		return
	self.server.db.create_account(username, hashlib.md5(password.encode('utf-8')).hexdigest())
	result["success"] = True
	result["info"] = "Account created"
	auth_token = hashlib.md5((username + str(time.time())).encode('utf-8')).hexdigest()
	self.server.db.auth.authenticate(self.client_address[0], username, auth_token)
	result["auth_token"] = auth_token
	self.respond(result)
	return


def handle_login(self, json_data):
	result = {}
	username = json_data["login"][0]
	if not self.server.db.is_valid("accounts", username):
		result["success"] = False
		result["info"] = "No such user"
		self.respond(result)
		return
	else:
		if "password" in json_data:
			password = json_data["password"][0]
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
			self.server.db.auth.authenticate(self.client_address[0], username, auth_token)
			result["auth_token"] = auth_token
			self.respond(result)
			return


class Client:
	
	def __init__(self, address, username):
		self.address = address
		self.username = username
		self.last_activity = time.time()

class Authenticator:

	def __init__(self):
		self.tokens = {} # token : Client
		self.timeout_auth_thread = threading.Thread(target=self.timeout_auth_tokens, daemon=True)
		self.timeout_auth_thread.start()
		
	def timeout_auth_tokens(self):
		while True:
			time.sleep(3600)
			current = time.time()
			inactive_tokens = []
			for token, client in self.tokens.items():
				if current - client.last_activity > TIMEOUT:
					inactive_tokens.append(token)
			for token in inactive_tokens:
				del self.tokens[token]

	def deauthenticate(self, token):
		success = token in self.tokens
		del self.tokens[token]
		return success
		
	def deauthenticate_user(self, username):
		invalid_tokens = []
		for token in self.tokens:
			client = self.tokens[token]
			if client.username == username:
				invalid_tokens.append(token)
		for token in invalid_tokens:
			self.deauthenticate(token)
		
	def authenticate(self, address, username, token):
		self.deauthenticate_user(username) # remove old tokens
		client = Client(address, username)
		self.tokens[token] = client
		
	def is_authenticated(self, address, token):
		if token in self.tokens:
			if address == self.tokens[token].address:
				self.tokens[token].last_activity = time.time() # refresh last activity
				return token
		
	def get_authenticated_user(self, address, token):
		if not self.is_authenticated(address, token):
			raise AssertionError("Tried to access non-authenticated user")
		return self.tokens[token].username
		
	def check_and_fetch(self, address, token):
		if not self.is_authenticated(address, token):
			return None
		return self.get_authenticated_user(address, token)