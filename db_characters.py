# Josh Aaron Miller 2021
# VenntDB methods for Characters

import venntdb
from constants import *

# VenntDB Methods

def character_exists(self, username, char_id):
	return self.get_character(username, char_id) is not None
	
def get_character(self, username, char_id):
	if not "characters" in self.db["accounts"][username]:
		return None
	for character in self.db["accounts"][username]["characters"]:
		if char_id == character["id"]:
			return character
	return None
	
def create_character(self, username, character):
	if not "characters" in self.db["accounts"][username]:
		self.db["accounts"][username]["characters"] = []
	for attr in ATTRIBUTES:
		if attr not in character:
			character[attr] = 0
	self.db["accounts"][username]["characters"].append(character)
	self.save_db()
	
def get_characters(self, username):
	if not "characters" in self.db["accounts"][username]:
		return []
	return self.db["accounts"][username]["characters"]
		
def get_attr(self, username, char_id, attr):
	if not self.is_valid(account,username):
		raise AssertionError("Tried to access non-existent user")
	if not self.character_exists(username, char_id):
		raise AssertionError("Tried to access non-existent character")
	return self.get_character(username, char_id)[attr]
	
def set_attr(self, username, char_id, attr, val):
	if not self.is_valid(account,username):
		raise AssertionError("Tried to access non-existent user")
	if not self.character_exists(username, char_id):
		raise AssertionError("Tried to access non-existent character")
	self.get_character(username, char_id)[attr] = val
	self.save_db()