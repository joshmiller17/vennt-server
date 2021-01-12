# Josh Aaron Miller 2021
# Vennt DB

import _pickle as cPickle
import json, os

from authentication import Authenticator
from constants import *



class VenntDB:

	def __init__(self, filename):
		self.filename = filename
		self.auth = Authenticator()

		if os.path.exists(self.filename):
			self.db = cPickle.load(open(self.filename, 'rb'))
		else:
			self.db = {}
			self.db["accounts"] = {}
			self.db["campaigns"] = {}
			self.db["weapons"] = {}
			if os.path.exists("weapons.json"):
				with open("weapons.json") as f:
					self.db["weapons"] = json.load(f)
			
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
		
	def get_weapon(self, weapon_name):
		for weapon in self.db["weapons"]:
			if weapon["name"] == weapon_name:
				return weapon
		return None
		
	def add_item(self, username, item):
		if not "items" in self.db["accounts"][username]:
			self.db["accounts"][username]["items"] = []
		if len(self.db["accounts"][username]["items"]) >= MAX_INVENTORY_SIZE:
			return False
		self.db["accounts"][username]["items"].append(item)
		self.save_db()
		return True
		
	def view_items(self, username):
		if not "items" in self.db["accounts"][username]:
			return []
		return self.db["accounts"][username]["items"]
		
	def remove_item(self, username, item_id):
		if not "items" in self.db["accounts"][username]:
			self.db["accounts"][username]["items"] = []
			return False
		for item in self.db["accounts"][username]["items"]:
			if item["id"] == item_id:
				self.db["accounts"][username]["items"].remove(item)
				return True
				self.save_db()
		return False
		
	def create_character(self, username, character):
		if not "characters" in self.db["accounts"][username]:
			self.db["accounts"][username]["characters"] = []
		for attr in ATTRIBUTES:
			if attr not in character:
				character[attr] = 0
		self.db["accounts"][username]["characters"].append(character)
		self.save_db()
		
	def create_enemy(self, username, enemy):
		if not "enemies" in self.db["accounts"][username]:
			self.db["accounts"][username]["enemies"] = []
		for attr in ATTRIBUTES:
			if attr not in enemy:
				enemy[attr] = 0
		self.db["accounts"][username]["enemies"].append(enemy)
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
		self.save_db()
		return True
		
	def delete_campaign_invite(self, username, campaign_id):
		if not "campaign_invites" in self.db["accounts"][username]:
			return []
			
		for inv in self.db["accounts"][username]["campaign_invites"]:
			if inv["id"] == campaign_id:
				self.db["accounts"][username]["campaign_invites"].remove(inv)
				self.save_db()
				return True
		return False			
		
	def add_user_to_campaign(self, username, campaign_id):
		if username in self.db["campaigns"][campaign_id]["members"]:
			raise AssertionError(username + " already in campaign.")
		self.db["campaigns"][campaign_id]["members"].append({"username":username,"role":None})
		if "joined_campaigns" not in self.db["accounts"][username]:
			self.db["accounts"][username]["joined_campaigns"] = []
		self.db["accounts"][username]["joined_campaigns"].append(campaign_id)
		self.save_db()
	
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

	def save_db(self):
		cPickle.dump((self.db), open(self.filename, 'wb'))