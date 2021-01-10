import _pickle as cPickle
import json, os

ATTRIBUTES = [
"AGI", "CHA", "DEX", "INT", "PER", "SPI",
"STR", "TEK", "WIS", "HP", "MAX_HP", "MP",
"MAX_MP", "VIM", "MAX_VIM", "ARMOR", "HERO",
"INIT", "SPEED"
]

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
		
	def character_exists(self, username, char_id):
		return self.get_character(username, char_id) is not None
		
	def get_character(self, username, char_id):
		for character in self.db["accounts"][username]["characters"]:
			if char_id == character["id"]:
				return character
		return None
			
	def create_account(self, username, pass_hash):
		self.db["accounts"][username] = {}
		self.db["accounts"][username]["password"] = pass_hash
		self.save_db()
		
	def create_character(self, username, character):
		if not "characters" in self.db["accounts"][username]:
			self.db["accounts"][username]["characters"] = []
		for attr in ATTRIBUTES:
			character[attr] = 0 # init
		self.db["accounts"][username]["characters"].append(character)
		self.save_db()
		
	def create_campaign(self, username, campaign):
		if not "campaigns" in self.db["accounts"][username]:
			self.db["accounts"][username]["campaigns"] = []
		self.db["accounts"][username]["campaigns"].append(campaign)
		self.save_db()
		
	def get_attr(self, username, char_id, attr):
		if not self.account_exists(username):
			raise ValueError("Tried to access non-existent user")
		if not self.character_exists(username, char_id):
			raise ValueError("Tried to access non-existent character")
		return self.get_character(username, char_id)[attr]
		
	def set_attr(self, username, char_id, attr, val):
		if not self.account_exists(username):
			raise ValueError("Tried to access non-existent user")
		if not self.character_exists(username, char_id):
			raise ValueError("Tried to access non-existent character")
		self.get_character(username, char_id)[attr] = val
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