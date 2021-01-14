# Josh Aaron Miller 2021
# VenntDB methods for Inventory

import venntdb
from constants import *

# VenntDB Methods

def get_standard_weapon(self, weapon_name):
	for weapon in self.db["weapons"]:
		if weapon["name"] == weapon_name:
			return weapon
	return None
	
def get_custom_weapon(self, username, weapon_name):
	if not "weapons" in self.db["accounts"][username]:
		return None
	for weapon in self.db["accounts"][username]["weapons"]:
		if weapon["name"] == weapon_name:
			return weapon
	return None
	
def get_weapon(self, username, weapon_name):
	weapon = self.get_standard_weapon(weapon_name)
	if weapon is None:
		weapon = self.get_custom_weapon(username, weapon_name)
	return weapon
	
def remove_weapon(self, username, weapon_name):
	if not "weapons" in self.db["accounts"][username]:
		return False
	for weapon in self.db["accounts"][username]["weapons"]:
		if weapon["name"] == weapon_name:
			self.db["accounts"][username]["weapons"].remove(weapon)
			return True
			self.save_db()
	return False
	
def add_weapon(self, username, weapon):
	if not "weapons" in self.db["accounts"][username]:
		self.db["accounts"][username]["weapons"] = []
	self.db["accounts"][username]["weapons"].append(weapon)
	self.save_db()
	
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
		return False
	for item in self.db["accounts"][username]["items"]:
		if item["id"] == item_id:
			self.db["accounts"][username]["items"].remove(item)
			return True
			self.save_db()
	return False
	