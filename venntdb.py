import _pickle as cPickle
import json, os



class VenntDB:

	def __init__(self, filename):
		self.filename = filename

		if os.path.exists(self.filename):
			self.db = cPickle.load(open(self.filename, 'rb'))
			self.db["auth_tokens"] = {}
		else:
			self.db = {}
			self.db["accounts"] = {}
			self.db["auth_tokens"] = {}
			
	def account_exists(self, username):
		return username in self.db["accounts"]
			
	def create_account(self, username, pass_hash):
		self.db["accounts"][username] = {}
		self.db["accounts"][username]["password"] = pass_hash
		self.save_db()
		
	def does_password_match(self, username, pass_hash):
		if not self.account_exists(username):
			raise ValueError("Tried to access non-existent user")
		return pass_hash == self.db["accounts"][username]["password"]
		
	def authenticate(self, username, token):
		self.db["auth_tokens"][token] = username
		
	def is_authenticated(self, token):
		return token in self.db["auth_tokens"]
		
	def get_authenticated_user(self, token):
		if not self.is_authenticated(token):
			raise ValueError("Tried to access non-authenticated user")
		return self.db["auth_tokens"][token]

	def save_db(self):
		cPickle.dump((self.db), open(self.filename, 'wb'))