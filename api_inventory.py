# Josh Aaron Miller 2021
# API calls for Inventory

import venntdb, uuid
from constants import *

# VenntHandler methods

def view_items(self, args, username):
	character_id = args[KEY_ID]
	if self.server.db.permissions(username, character_id) < Permission.PRIVATE_VIEW:
		return self.respond({"success":False, "info":MSG_NO_PERMISSION})
	items = self.server.db.view_items(username, args[KEY_ID])
	return self.respond({"success":True, "value":items})
	
def remove_item(self, args, username):
	character_id = args[KEY_ID]
	if self.server.db.permissions(username, character_id) < Permission.EDIT:
		return self.respond({"success":False, "info":MSG_NO_PERMISSION})
	return self.respond({"success":self.server.db.remove_item(username, args[KEY_ID], args[KEY_ID2])})


def add_item(self, args, username):
	character_id = args[KEY_ID]
	if self.server.db.permissions(username, character_id) < Permission.ADD:
		return self.respond({"success":False, "info":MSG_NO_PERMISSION})
	
	name = args[KEY_NAME]
	
	if len(name) > MAX_NAME_LENGTH:
		return self.respond({"success":False, "info":MSG_NAME_LONG})
		
	desc = args[KEY_DESC]
	if len(desc) > MAX_DESC_LENGTH:
		return self.respond({"success":False, "info":MSG_DESC_LONG})
		
	try:
		bulk = int(args[KEY_BULK])
	except:
		return self.respond({"success":False, "info":MSG_NOT_INT.format(KEY_BULK)})
	
	id = IDType.ITEM + str(uuid.uuid4())
	item = { ITEM_ID: id, ITEM_NAME: name, ITEM_DESC: desc, ITEM_BULK: bulk, ITEM_TYPE: "custom" }
	if ITEM_TYPE in args and len(args[ITEM_TYPE]) <= MAX_NAME_LENGTH:
		item[ITEM_TYPE] = args[ITEM_TYPE]
	if ITEM_COURSES in args and len(args[ITEM_COURSES]) <= MAX_NAME_LENGTH:
		item[ITEM_COURSES] = args[ITEM_COURSES]

	success = self.server.db.add_item(username, args[KEY_ID], item)
	
	if not success:
		return self.respond({"success":False, "info":"Max items exceeded"})
	
	ret = {"success":True, "id":id}
	return self.respond(ret)
	
def get_weapon(self, args, username):
	weapon = self.server.db.get_weapon(username, args[KEY_NAME])
	if weapon is None:
		return self.respond({"success":False, "info":"No such weapon"})
		
	return self.respond({"success":True, "value":weapon})
	
def add_weapon(self, args, username):
	weapon_name = args[KEY_NAME]
	if len(weapon_name) > MAX_NAME_LENGTH:
		return self.respond({"success":False, "info":MSG_NAME_LONG})
		
	if self.server.db.get_weapon(username, weapon_name) is not None:
		return self.respond({"success":False, "info":"Weapon already exists"})
		
	attr = args[KEY_ATTR]
	if attr not in ATTRIBUTES:
		return self.respond({"success":False,"info":MSG_NO_ATTR})
		
	dmg = args[KEY_DMG]
	# TODO verify dmg is well-ordered
	
	if KEY_MODS in args:
		mods = args[KEY_MODS]
		# TODO verify mods are well-ordered
		
	weapon = {"name":weapon_name, "attr":attr, "dmg":dmg, "mods":mods}
	self.server.db.add_weapon(username, weapon)
	
	return self.respond({"success":True})
	
def remove_weapon(self, args, username):
	return self.respond({"success":self.server.db.remove_weapon(username, args[KEY_NAME])})