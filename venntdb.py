# Josh Aaron Miller 2021
# Vennt DB

import _pickle as cPickle
import json, os

from authentication import Authenticator
from constants import *
	

class VenntDB:

	from db_campaigns import create_campaign, get_campaign_invites, send_campaign_invite, remove_campaign_invite, add_user_to_campaign, get_campaign, get_campaigns, get_joined_campaigns
	from db_characters import character_exists, get_character, create_character, get_characters, get_attr, set_attr
	from db_inventory import get_standard_weapon, get_custom_weapon, get_weapon, remove_weapon, add_weapon, add_item, view_items, remove_item
	from db_abilities import get_cached_ability, cache_ability, find_ability, get_abilities, get_ability, get_or_make_ability, add_ability
	from db_initiative import reset_turn_order, add_turn, next_turn, get_turn_order, get_current_turn


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
			self.db["abilities"] = {}
			if os.path.exists("abilities.json"):
				with open("abilities.json",encoding="utf8") as f: # encoding for smart quotes
					self.db["abilities"] = json.load(f)
			self.db["ability_cache"] = [None] * (MAX_ABILITY_CACHE +) 1 # list of Ability dicts
			self.db["ability_cache_index"] = 0
		
	def dump(self):
		print(json.dumps(self.db, indent=4, separators=(',', ': '), sort_keys=True))
			
	def account_exists(self, username):
		return username in self.db["accounts"]
			
	def create_account(self, username, pass_hash):
		self.db["accounts"][username] = {}
		self.db["accounts"][username]["password"] = pass_hash
		self.save_db()
		
	def create_enemy(self, username, enemy):
		if not "enemies" in self.db["accounts"][username]:
			self.db["accounts"][username]["enemies"] = []
		for attr in ATTRIBUTES:
			if attr not in enemy:
				enemy[attr] = 0
		self.db["accounts"][username]["enemies"].append(enemy)
		self.save_db()

	def does_password_match(self, username, pass_hash):
		if not self.account_exists(username):
			raise AssertionError("Tried to access non-existent user")
		return pass_hash == self.db["accounts"][username]["password"]

	def save_db(self):
		cPickle.dump((self.db), open(self.filename, 'wb'))