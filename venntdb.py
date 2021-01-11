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
			self.db["campaigns"] = {}
			self.db["auth_tokens"] = {}
			
	def dump(self):
		print(json.dumps(self.db, indent=4, separators=(',', ': '), sort_keys=True))
			
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
			if attr not in character:
				character[attr] = 0
		self.db["accounts"][username]["characters"].append(character)
		self.save_db()
		
	def get_campaign_invites(self, username):
		if not "campaign_invites" in self.db["accounts"][username]:
			return []
		return self.db["accounts"][username]["campaign_invites"]
		
	def send_campaign_invite(self, user_from, user_to, campaign_id):
		invite = {"from":user_from, "id":campaign_id}
		if not "campaign_invites" in self.db["accounts"][user_to]:
			self.db["accounts"][user_to]["campaign_invites"] = []
		for invites in self.db["accounts"][user_to]["campaign_invites"]:
			if invites["id"] == campaign_id:
				return False
		self.db["accounts"][user_to]["campaign_invites"].append(invite)
		return True
		
	def delete_campaign_invite(self, username, campaign_id):
		del self.db["accounts"][username]["campaign_invites"][campaign_id]
		
	def add_user_to_campaign(self, username, campaign_id):
		if username in self.db["campaigns"][campaign_id]["members"]:
			raise AssertionError(username + " already in campaign.")
		self.db["campaigns"][campaign_id]["members"].append({"username":username,"role":None})
		if "joined_campaigns" not in self.db["accounts"][username]:
			self.db["accounts"][username]["joined_campaigns"] = []
		self.db["accounts"][username]["joined_campaigns"].append(campaign_id)
	
	def get_campaign(self, campaign_id):
		if campaign_id in self.db["campaigns"]:
			return self.db["campaigns"][campaign_id]
		else:
			return None
	
	def get_campaigns(self, username):
		if not "campaigns" in self.db["accounts"][username]:
			return []
		return self.db["accounts"][username]["campaigns"]
		
	def get_joined_campaigns(self, username):
		if not "joined_campaigns" in self.db["accounts"][username]:
			return []
		return self.db["accounts"][username]["joined_campaigns"]
		
	def get_characters(self, username):
		if not "characters" in self.db["accounts"][username]:
			return []
		return self.db["accounts"][username]["characters"]
		
	def create_campaign(self, username, campaign):
		if not "campaigns" in self.db["accounts"][username]:
			self.db["accounts"][username]["campaigns"] = []
		self.db["accounts"][username]["campaigns"].append(campaign)
		self.db["campaigns"][campaign["id"]] = {}
		self.db["campaigns"][campaign["id"]]["owner"] = username
		self.db["campaigns"][campaign["id"]]["members"] = []
		self.db["campaigns"][campaign["id"]]["members"].append({"username":username,"role":None})
		self.save_db()
		
	def get_attr(self, username, char_id, attr):
		if not self.account_exists(username):
			raise AssertionError("Tried to access non-existent user")
		if not self.character_exists(username, char_id):
			raise AssertionError("Tried to access non-existent character")
		return self.get_character(username, char_id)[attr]
		
	def set_attr(self, username, char_id, attr, val):
		if not self.account_exists(username):
			raise AssertionError("Tried to access non-existent user")
		if not self.character_exists(username, char_id):
			raise AssertionError("Tried to access non-existent character")
		self.get_character(username, char_id)[attr] = val
		self.save_db()
		
	def does_password_match(self, username, pass_hash):
		if not self.account_exists(username):
			raise AssertionError("Tried to access non-existent user")
		return pass_hash == self.db["accounts"][username]["password"]
		
	def deauthenticate(self, token):
		success = token in self.db["auth_tokens"]
		del self.db["auth_tokens"][token]
		return success
		
	def authenticate(self, username, token):
		self.db["auth_tokens"][token] = username
		
	def is_authenticated(self, token):
		return token in self.db["auth_tokens"]
		
	def get_authenticated_user(self, token):
		if not self.is_authenticated(token):
			raise AssertionError("Tried to access non-authenticated user")
		return self.db["auth_tokens"][token]

	def save_db(self):
		cPickle.dump((self.db), open(self.filename, 'wb'))